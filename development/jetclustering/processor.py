from coffea import processor
from coffea.analysis_tools import PackedSelection, Cutflow
import awkward as ak
import pandas as pd
import dask_awkward as dak
import hist.dask as hda
from collections import namedtuple
import hist
import fastjet
import vector
vector.register_awkward()
from config import plots
import sys
ROOT_DIR="/home/prayag/coffeafcc/coffea-fcc-analyses/"
sys.path.append(ROOT_DIR+"analyzers")
import ReconstructedParticle

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
class jetclustering(processor.ProcessorABC):
    '''
    Processor: Define actual calculations here
    '''
    def __init__(self, *args, **kwargs):
        pass

    def process(self,events):

        Muons = events.ReconstructedParticles.match_collection(events.Muonidx0)
        Z = ReconstructedParticle.resonanceBuilder(Muons, 91.0)
        Recoil = ReconstructedParticle.recoilBuilder(Z, 240.0)
        z_cuts = PackedSelection()
        jet_cuts = PackedSelection()

        #Define Selections
        sel_p_gt_25_Muons = Muons.p > 25.0
        
        sel_n_e_0_Muons = ak.num(Muons, axis=1) == 0
        sel_n_gte_2_Muons = ak.num(Muons, axis=1) >= 2

        sel_q_e_0_Z = Z.charge == 0
        sel_m_gt_70_Z = Z.m > 70.0
        sel_m_lt_100_Z = Z.m < 100.0
        
        sel_p_gt_20_Z = Z.p > 20.0
        sel_p_lt_70_Z = Z.p < 70.0
        
        sel_m_gt_120_Recoil = Recoil.m > 120.0
        sel_m_lt_140_Recoil = Recoil.m < 140.0
        
        # Add the selections to the cuts Packed Selection
        z_cuts.add("p_gt_25_Muons", ak.any(sel_p_gt_25_Muons, axis=1))
        z_cuts.add("n_gte_2_Muons", sel_n_gte_2_Muons)
        z_cuts.add("q_e_0_Z", sel_q_e_0_Z)
        z_cuts.add("m_gt_70_Z", sel_m_gt_70_Z)
        z_cuts.add("m_lt_100_Z", sel_m_lt_100_Z)
        z_cuts.add("p_gt_20_Z", sel_p_gt_20_Z)
        z_cuts.add("p_lt_70_Z", sel_p_lt_70_Z)
        z_cuts.add("m_gt_120_Recoil", sel_m_gt_120_Recoil)
        z_cuts.add("m_lt_140_Recoil", sel_m_lt_140_Recoil)
        jet_cuts.add("n_e_0_Muons", sel_n_e_0_Muons)

        # Calculate the final variables
        Good_Z = Z[z_cuts.all()]
        Good_Recoil = Recoil[z_cuts.all()]

        rps_no_mu = events.ReconstructedParticles[sel_n_e_0_Muons]
        pseudo_jets = ak.zip(
            {
            'px':rps_no_mu.px,
            'py':rps_no_mu.py,
            'pz':rps_no_mu.pz,
            'E':rps_no_mu.E
            },
            with_name="Momentum4D"
        )
        jetdef = fastjet.JetDefinition0Param(fastjet.ee_kt_algorithm)
        # Requirements: 
        # [Done] arg_exclusive = 2
        # [Not Sure] arg_cut = 2 i.e., N jets for m_exclusive
        # [Not Sure] arg_sorted = 0 i.e., p_T ordering
        # [Not Sure] arg_recombination = 10 i.e., E0_scheme : Special for FCCAnalyses
        jetdef.set_recombination_scheme(0) # E scheme
        #jetdef.description()
        cluster = fastjet.ClusterSequence(pseudo_jets, jetdef)
        jet_constituents = cluster.constituents()
        jets = cluster.exclusive_jets(2)
        dijets = ak.sum(jets, axis=1)

        #Prepare output
        #Choose the required histograms and their assigned variables to fill
        names = plot_props.columns.to_list()
        vars_z_sel = [dijets.m, Good_Recoil.m, Good_Z.p, Good_Z.m]
        vars_jet_sel = vars_z_sel
        z_sel_ocl = z_cuts.cutflow(*z_cuts.names).yieldhist()
        jet_sel_ocl = jet_cuts.cutflow(*jet_cuts.names).yieldhist()
        

        Output = {
            'histograms': {
                'z_sel':{name:get_1Dhist(name,var,flatten=False) for name,var in zip(names,vars_z_sel)},
                'jet_sel':{name:get_1Dhist(name,var,flatten=False) for name,var in zip(names,vars_jet_sel)}
            },
            'cutflow': {
                'z_sel': {'Onecut':z_sel_ocl[0],'Cutflow':z_sel_ocl[1],'Labels':z_sel_ocl[2]},
                'jet_sel': {'Onecut':jet_sel_ocl[0],'Cutflow':jet_sel_ocl[1],'Labels':jet_sel_ocl[2]}
            }
        }
        return Output

    def postprocess(self, accumulator):
        pass
