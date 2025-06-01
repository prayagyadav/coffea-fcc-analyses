from coffea import processor
from coffea.analysis_tools import PackedSelection, Cutflow
import awkward as ak
import numpy as np
import pandas as pd
import dask_awkward as dak
import hist.dask as hda
from collections import namedtuple
import hist
import vector
vector.register_awkward()
import config
import functions
import sys
import os
local_dir = os.environ['LOCAL_DIR']
sys.path.append(local_dir)

from scripts.analyzers.ReconstructedParticle import remove, recoilBuilder
from functions import *

plot_props = pd.DataFrame(config.plots)

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

def create_mask(a, b, c):
    mask1 = a != c
    mask2 = b != c
    mask = mask1 & mask2
    return mask

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
        Muons = events.ReconstructedParticles[events.Muonidx0.index]
        Muons["index"] = events.Muonidx0.index # Attach the local index for easier calculations later
        sel_muon = Muons.p > 2.0
        selected_muons_p = Muons[sel_muon]

        # Select events with at least 4 muons
        at_least_4_muons = ak.num(selected_muons_p, axis=1) > 3
        selected_muons = selected_muons_p[at_least_4_muons]

        # Build Z resonances
        Z = resonanceBuilder_mass(resonance_mass=91.2, use_MC_Kinematics=False, leptons=selected_muons)

        # On Shell Z
        zll = ak.firsts(Z)

        # Remove the used up muons from the muon list
        mask = create_mask(zll.l1_index, zll.l2_index, selected_muons.index)
        rest_of_muons = selected_muons[mask]

        m1, m2, c_mask = getTwoHighestPMuons(rest_of_muons)

        non_res_Z = m1 + m2
        # Angle between the two
        non_res_Z_angle = m1.deltaangle(m2)

        # Collect all the four Muons
        fourMuons_collected = ak.concatenate(
            (
                ak.drop_none(l1[c_mask])[:, np.newaxis],
                ak.drop_none(l2[c_mask])[:, np.newaxis],
                ak.drop_none(m1)[:, np.newaxis],
                ak.drop_none(m2)[:, np.newaxis]
            ),
            axis=1
        )
        fourMuons_collected = ak.mask(fourMuons_collected, ak.num(fourMuons_collected, axis=1) > 3)
        fourMuons = ak.mask(zll, c_mask) + non_res_Z

        fourMuons_pmin = ak.min(fourMuons_collected.p, axis=1)

        # rest_of_particles = remove(events_with_at_least_4_muons, fourMuons_collected)
        rest_of_particles = remove(events.ReconstructedParticles, fourMuons_collected)
        all_others = functions.sum_all(rest_of_particles)

        Emiss = recoilBuilder(functions.sum_all(events.ReconstructedParticles), ecm=config.ecm)
        pmiss = Emiss.E

        # Cone Isolation
        fourMuons_iso = functions.coneIsolation(fourMuons_collected, rest_of_particles, min_dr=0.0, max_dr=0.523599)
        fourMuons_min_iso = ak.max(fourMuons_iso, axis=1)

        #Placeholder
        E = events.ReconstructedParticles.E

        # Define individual cuts
        cut.add('No cut', ak.all(E > 0, axis=1))
        cut.add('cut1', ak.all(E > 0, axis=1))
        cut.add('cut2', ak.all(E > 0, axis=1))
        cut.add('cut3', ak.all(E > 0, axis=1))
        cut.add('cut4', ak.all(E > 0, axis=1))
        cut.add('cut5', ak.all(E > 0, axis=1))
        cut.add('cut6', ak.all(E > 0, axis=1))
        cut.add('at_least_4_muons', at_least_4_muons)


        # Selections: A collection of cuts (event selections)
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
                'selectedmuons_p':selected_muons.p[cut.all(*selections)],
                'fourmuons_mass':fourMuons.m[cut.all(*selections)],
                'fourmuons_pmin':fourMuons_pmin[cut.all(*selections)],
                'Z_res_mass':zll.m[cut.all(*selections)],
                'Z_non_res_mass':non_res_Z.m[cut.all(*selections)],
                'vis_e_woMuons':all_others.E[cut.all(*selections)],
                'iso_least_isolated_muon':fourMuons_min_iso[cut.all(*selections)],
                'missing_p':pmiss[cut.all(*selections)],
                'cos_theta_miss':Emiss.theta[cut.all(*selections)],
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
