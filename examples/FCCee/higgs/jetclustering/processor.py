from coffea import processor
from coffea.analysis_tools import PackedSelection, Cutflow
import awkward as ak
import pandas as pd
import dask_awkward as dak
import hist.dask as hda
from collections import namedtuple
import hist
import vector
vector.register_awkward()
from config import plots

plot_props = pd.DataFrame(plots)

def get_1Dhist(name, var, flatten=False):
    '''
    name: eg. Zm
    var: eg. variable containing array of mass of Z
    flatten: If to flatten var before fill; True by default
    Returns a histogram
    '''
    props = plot_props[name]
    if flatten : var = dak.ravel(var) # Removes None values and all the nesting
    var = var[~dak.is_none(var, axis=0)] # Remove None values only
    return hda.Hist.new.Reg(props.bins, props.xmin, props.xmax).Double().fill(var)

def get(events,collection,attribute,*cut):
    '''
    Get an attribute from a branch with or without a base cut.
    '''
    if len(cut) != 0:
        return events[collection+'/'+collection+'.'+attribute][cut[0]]
    return events[collection+'/'+collection+'.'+attribute]

def get_all(events,Collection,*basecut):
    '''
    Collect all the attributes of a collection into a namedtuple named particle, with or without a base cut
    '''
    prefix = '/'.join([Collection]*2)+'.'
    list_of_attr = [field.replace(prefix,'') for field in events.fields if field.startswith(prefix)]
    replace_list = ['.','[',']']
    valid_attr = list_of_attr
    for rep in replace_list:
        valid_attr = [field.replace(rep, '_') for field in valid_attr ]
    part = namedtuple('particle', valid_attr)
    return part(*[get(events,Collection,attr,*basecut) for attr in list_of_attr])

def get_reco(Reconstr_branch, needed_particle, events):
    '''
    Match the Reconstructed collection to the desired particle collection.
    '''
    part = namedtuple('particle', list(Reconstr_branch._fields))
    return part(*[getattr(Reconstr_branch,attr)[get(events,needed_particle,'index')] for attr in Reconstr_branch._fields])

def Reso_builder(lepton, resonance):
    '''
    Builds Resonance candidates
    Input:    lepton(var*[var*LorentzVector]),
              resonance(float)
    Output: Reso([var*LorentzVecctor]) best resonance candidate in each event (maximum one per event)
    '''
    #Create all the combinations
    combs = dak.combinations(lepton,2)
    # Get dileptons
    lep1 , lep2 = dak.unzip(combs)
    di_lep = lep1 + lep2 # This process drops any other field except 4 momentum fields

    di_lep = ak.zip({"px":di_lep.px,"py":di_lep.py,"pz":di_lep.pz,"E":di_lep.E,"q":lep1.q + lep2.q,}, with_name="Momentum4D")

    # Sort by closest mass to the resonance value
    sort_mask = dak.argsort(abs(resonance-di_lep.mass), axis=1)
    Reso = di_lep[sort_mask]

    #Choose the best candidate
    Reso = dak.fill_none(Reso,[],axis=0) #Transform the None values at axis 0 to [], so that they survive the next operation
    Reso = dak.firsts(Reso) #Chooses the first elements and flattens out, [] gets converted to None

    return Reso


#################################
#Begin the processor definition #
#################################
class jetclustering(processor.ProcessorABC):
    '''
    Processor: Define actual calculations here
    '''
    def __init__(self, *args, **kwargs):
        pass

    def process(self,events):

        #Create a Packed Selection object to get a cutflow later
        cut = PackedSelection()
        cut.add('No cut', dak.ones_like(dak.num(get(events,'ReconstructedParticles','energy'),axis=1),dtype=bool))

        # Selection 0 : No Cut (example)
        sel0_ocl = cut.cutflow(*cut.names).yieldhist()
        sel0_events = events

        # Filter out any event with no reconstructed particles and generate Reconstructed Particle Attributes
        #ak.mask preserves array length
        at_least_one_recon = dak.num(get(events,'ReconstructedParticles','energy'), axis=1) > 0
        good_events = dak.mask(events,at_least_one_recon)
        cut.add('At least one Reco Particle', at_least_one_recon)

        # Selection 1 : No Cut and At least one Reco Particle
        sel1_ocl = cut.cutflow(*cut.names).yieldhist()
        sel1_events = good_events

        #Prepare output
        #Choose the required histograms and their assigned variables to fill
        names = plot_props.columns.to_list()
        vars_sel0 = [get(sel0_events,'ReconstructedParticles','energy')]
        vars_sel1 = [get(sel1_events,'ReconstructedParticles','energy')]

        Output = {
            'histograms': {
                'sel0':{name:get_1Dhist(name,var,flatten=True) for name,var in zip(names,vars_sel0)},
                'sel1':{name:get_1Dhist(name,var,flatten=True) for name,var in zip(names,vars_sel1)}
            },
            'cutflow': {
                'sel0': {'Onecut':sel0_ocl[0],'Cutflow':sel0_ocl[1],'Labels':sel0_ocl[2]},
                'sel1': {'Onecut':sel1_ocl[0],'Cutflow':sel1_ocl[1],'Labels':sel1_ocl[2]}
            }
        }
        return Output

    def postprocess(self, accumulator):
        pass
