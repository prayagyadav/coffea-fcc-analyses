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
class Fourleptons(processor.ProcessorABC):
    '''
    Processor: Define actual calculations here
    '''
    def __init__(self, *args, **kwargs):
        pass

    def process(self,events):

        #Create a Packed Selection object to get a cutflow later
        cut = PackedSelection()

        # Main calculations
        E = events.ReconstructedParticles.E

        # Define individual cuts
        cut.add('No cut', ak.all(E > 0, axis=1))
        cut.add('cut1', ak.all(E < 100, axis=1))
        cut.add('cut2', ak.all(E < 90, axis=1))
        cut.add('cut3', ak.all(E < 80, axis=1))
        cut.add('cut4', ak.all(E < 70, axis=1))
        cut.add('cut5', ak.all(E < 60, axis=1))
        cut.add('cut6', ak.all(E < 50, axis=1))
        

        # Selections: A collection of cuts
        sel = {}
        sel[0] = ['No cut']
        sel[1] = ['No cut','cut1']
        sel[2] = ['No cut','cut1','cut2']
        sel[3] = ['No cut','cut1','cut2','cut3']
        sel[4] = ['No cut','cut1','cut2','cut3','cut4']
        sel[5] = ['No cut','cut1','cut2','cut3','cut4','cut5']
        sel[6] = ['No cut','cut1','cut2','cut3','cut4','cut5','cut6']

        # Get cutflow hists
        sel_ocl = {key:cut.cutflow(*val).yieldhist() for key,val in sel.items()}
        
        # Apply the selection to the relevant variables
        vars_sel = {}
        for key,selections in sel.items():
            vars_sel[key] = {
                'selectedmuons_p':E[cut.all(*selections)],
                'fourmuons_mass':E[cut.all(*selections)],
                'fourmuons_pmin':E[cut.all(*selections)],
                'Z_res_mass':E[cut.all(*selections)],
                'Z_non_res_mass':E[cut.all(*selections)],
                'vis_e_woMuons':E[cut.all(*selections)],
                'iso_least_isolated_muon':E[cut.all(*selections)],
                'missing_p':E[cut.all(*selections)],
                'cos_theta_miss':E[cut.all(*selections)],
            }
        

        #Prepare output
        Output = {
            'histograms': {
                'sel0':{name:get_1Dhist(name,var,flatten=True) for name,var in vars_sel[0].items()},
                'sel1':{name:get_1Dhist(name,var,flatten=True) for name,var in vars_sel[1].items()},
                'sel2':{name:get_1Dhist(name,var,flatten=True) for name,var in vars_sel[2].items()},
                'sel3':{name:get_1Dhist(name,var,flatten=True) for name,var in vars_sel[3].items()},
                'sel4':{name:get_1Dhist(name,var,flatten=True) for name,var in vars_sel[4].items()},
                'sel5':{name:get_1Dhist(name,var,flatten=True) for name,var in vars_sel[5].items()},
                'sel6':{name:get_1Dhist(name,var,flatten=True) for name,var in vars_sel[6].items()},
            },
            'cutflow': {
                'sel0': {'Onecut':sel_ocl[0][0],'Cutflow':sel_ocl[0][1],'Labels':sel_ocl[0][2]},
                'sel1': {'Onecut':sel_ocl[1][0],'Cutflow':sel_ocl[1][1],'Labels':sel_ocl[1][2]},
                'sel2': {'Onecut':sel_ocl[2][0],'Cutflow':sel_ocl[2][1],'Labels':sel_ocl[2][2]},
                'sel3': {'Onecut':sel_ocl[3][0],'Cutflow':sel_ocl[3][1],'Labels':sel_ocl[3][2]},
                'sel4': {'Onecut':sel_ocl[4][0],'Cutflow':sel_ocl[4][1],'Labels':sel_ocl[4][2]},
                'sel5': {'Onecut':sel_ocl[5][0],'Cutflow':sel_ocl[5][1],'Labels':sel_ocl[5][2]},
                'sel6': {'Onecut':sel_ocl[6][0],'Cutflow':sel_ocl[6][1],'Labels':sel_ocl[6][2]},
            }
        }
        return Output

    def postprocess(self, accumulator):
        pass
