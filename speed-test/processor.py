from coffea import processor
from coffea.analysis_tools import PackedSelection, Cutflow
import awkward as ak
import pandas as pd
import dask_awkward as dak
import hist.dask as hda
import numpy as np
from collections import namedtuple
import hist
import fastjet
import vector
vector.register_awkward()
from config import plots
import sys
import os
local_dir = os.environ['LOCAL_DIR']
sys.path.append(local_dir)
import scripts
from scripts.analyzers import ReconstructedParticle as ReconstructedParticleUtil
from scripts.analyzers import Jet as JetUtil

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
class speed_test(processor.ProcessorABC):
    '''
    Processor: Define actual calculations here
    '''
    def __init__(self, *args, **kwargs):
        pass

    def process(self,events):

        # Object Selections
        Muons = events.ReconstructedParticles.match_collection(events.Muonidx0)
        sel_muon_p_gt_25 = Muons.p > 25.0
        Muons = Muons[sel_muon_p_gt_25]
        Z = ReconstructedParticleUtil.resonanceBuilder(Muons, 91.0)
        Recoil = ReconstructedParticleUtil.recoilBuilder(Z, 240.0)

        #Event Selections
        cuts = PackedSelection()
        cuts.add("n_gte_2_Muons", ak.num(Muons, axis=1) >= 2 )
        cuts.add("m_gt_70_Z", Z.m > 70.0 )
        cuts.add("m_lt_100_Z", Z.m < 100.0 )
        cuts.add("p_gt_20_Z", Z.p > 20.0 )
        cuts.add("p_lt_70_Z", Z.p < 70.0 )
        cuts.add("m_gt_120_Recoil", Recoil.m > 120.0 )
        cuts.add("m_lt_140_Recoil", Recoil.m < 140.0 )

        # Apply the event selections
        Good_Z = Z[cuts.all()]
        Good_Recoil = Recoil[cuts.all()]

        #Prepare output
        #Choose the required histograms and their assigned variables to fill
        names = plot_props.columns.to_list()
        vars_sel = [
            Good_Recoil.m,
            Good_Z.p,
            Good_Z.m,
        ]
        sel_ocl = cuts.cutflow(*cuts.names).yieldhist()

        Output = {
            'histograms': {
                'sel':{name:get_1Dhist(name,var,flatten=False) for name,var in zip(names,vars_sel)},
            },
            'cutflow': {
                'sel': {'Onecut':sel_ocl[0],'Cutflow':sel_ocl[1],'Labels':sel_ocl[2]},
            }
        }

        return Output

    def postprocess(self, accumulator):
        pass
