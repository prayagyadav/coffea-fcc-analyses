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
import sys
import os
local_dir = os.environ['LOCAL_DIR']
sys.path.append(local_dir)

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

#################################
#Begin the processor definition #
#################################
class 4leptons(processor.ProcessorABC):
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
                'sel1':{name:get_1Dhist(name,var,flatten=True) for name,var in zip(names,vars_sel1)},
                'sel2':{name:get_1Dhist(name,var,flatten=True) for name,var in zip(names,vars_sel2)},
                'sel3':{name:get_1Dhist(name,var,flatten=True) for name,var in zip(names,vars_sel3)},
                'sel4':{name:get_1Dhist(name,var,flatten=True) for name,var in zip(names,vars_sel4)},
                'sel5':{name:get_1Dhist(name,var,flatten=True) for name,var in zip(names,vars_sel5)},
                'sel6':{name:get_1Dhist(name,var,flatten=True) for name,var in zip(names,vars_sel6)},
            },
            'cutflow': {
                'sel0': {'Onecut':sel0_ocl[0],'Cutflow':sel0_ocl[1],'Labels':sel0_ocl[2]},
                'sel1': {'Onecut':sel1_ocl[0],'Cutflow':sel1_ocl[1],'Labels':sel1_ocl[2]}
                'sel2': {'Onecut':sel1_ocl[0],'Cutflow':sel1_ocl[1],'Labels':sel2_ocl[2]}
                'sel3': {'Onecut':sel1_ocl[0],'Cutflow':sel1_ocl[1],'Labels':sel3_ocl[2]}
                'sel4': {'Onecut':sel1_ocl[0],'Cutflow':sel1_ocl[1],'Labels':sel4_ocl[2]}
                'sel5': {'Onecut':sel1_ocl[0],'Cutflow':sel1_ocl[1],'Labels':sel5_ocl[2]}
                'sel6': {'Onecut':sel1_ocl[0],'Cutflow':sel1_ocl[1],'Labels':sel6_ocl[2]}
            }
        }
        return Output

    def postprocess(self, accumulator):
        pass
