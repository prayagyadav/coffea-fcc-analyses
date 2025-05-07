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
from scripts.plugins.fastjet import Recombiner

E0_Scheme = Recombiner.E0_Scheme.instance()

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

def JetTruthFinder(jet_constituents, mc, findGluons = False):
    """
    Make sure that jet_constituents and mc, all have
    the same number of events.

    We have to return the PDGID of the
    best matched genParton to the jets (by inspecting its dr with the jet constituents)

    """
    if not findGluons: #only quarks
        parton_cut = (abs(mc.PDG) <= 6)
    else: #only quarks and gluons
        parton_cut = (abs(mc.PDG) <= 6) | (abs(mc.PDG) == 21)

    genPartons = mc[parton_cut]

    jetcon_b, genParton_b = ak.unzip(ak.cartesian((jet_constituents[:,:,np.newaxis], genPartons[:,np.newaxis])))
    all_dr = jetcon_b.deltaR(genParton_b)
    sum_dr = ak.sum(all_dr, axis=3)
    min_idx = ak.argmin(sum_dr, axis=2)

    return genPartons[min_idx]

def easier_JetTruthFinder(jets, mc, findGluons = False):
    """
    Make sure that jets and mc, all have
    the same number of events.

    We have to return the PDGID of the
    best matched genParton to the jets (by inspecting its dr with the jet constituents)

    But maybe there is a better way? What if we just find
    the dr between the resultant jets and the partons?
    """
    if not findGluons: #only quarks
        parton_cut = (abs(mc.PDG) <= 6)
    else: #only quarks and gluons
        parton_cut = (abs(mc.PDG) <= 6) | (abs(mc.PDG) == 21)

    genPartons = mc[parton_cut]

    jet_b, genParton_b = ak.unzip(ak.cartesian((jets, genPartons[:,np.newaxis])))
    all_dr = jet_b.deltaR(genParton_b)
    index = ak.argmin(all_dr, axis=2)

    return genPartons[index]


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

        # The remove function removes those matched indices provided as argument 2
        # To remove muons with p greater than 25, we have to use that cut on indices
        # before passing on to the remove function
        high_p_muon_indices = events.Muonidx0[sel_muon_p_gt_25]
        rps_no_mu = ReconstructedParticleUtil.remove(events.ReconstructedParticles, high_p_muon_indices)
        rps_no_mu = rps_no_mu[cuts.all()] #Apply all the event selections
        pseudo_jets = ak.zip(
            {
            'px':rps_no_mu.px,
            'py':rps_no_mu.py,
            'pz':rps_no_mu.pz,
            'E':rps_no_mu.E
            },
            with_name="Momentum4D"
        )
        arg_sort_pt = ak.argsort(pseudo_jets.pt)
        jetdef = fastjet.JetDefinition0Param(fastjet.ee_kt_algorithm)
        jetdef.set_recombiner(E0_Scheme)
        cluster = fastjet.ClusterSequence(pseudo_jets[arg_sort_pt], jetdef)
        jets = cluster.exclusive_jets(2)
        jet_constituents = cluster.exclusive_jets_constituents(2)
        dijets = ak.sum(jets, axis=1)
        quarks_matched_to_jets = JetTruthFinder(jet_constituents, events.Particle[cuts.all()])
        pdgid = quarks_matched_to_jets.PDG

        #Prepare output
        #Choose the required histograms and their assigned variables to fill
        names = plot_props.columns.to_list()
        vars_sel = [
            dijets.m,
            ak.ravel(pdgid),
            Good_Recoil.m,
            Good_Z.p,
            Good_Z.m,
            dijets.m
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
