# Helper functions
import awkward as ak
import numpy as np
import vector
vector.register_awkward()
# 1. To replace: FCCAnalyses::ZHfunctions::resonanceBuilder_mass(91.2,false)(selected_muons, MCRecoAssociations0, MCRecoAssociations1, ReconstructedParticles, Particle, Particle0, Particle1)
def resonanceBuilder_mass(resonance_mass=None, use_MC_Kinematics=False, leptons=None, MCRecoAssociations=None, ReconstructedParticles=None, MCParticles=None):
    '''
    Build the Z resonance based on the available leptons. Returns the best lepton pair compatible with the Z mass and recoil at 125 GeV
    technically, it returns a ReconstructedParticleData object with index 0 the di-lepton system, index and 2 the leptons of the pair
    '''
    if leptons is None:
        raise AttributeError("No leptons passed")
    #Create all the combinations
    combs = ak.combinations(leptons,2)
    # Get dileptons
    lep1 , lep2 = ak.unzip(combs)
    di_lep = lep1 + lep2 # This process drops any other field except 4 momentum fields

    di_lep["charge"] =  lep1.charge + lep2.charge
    di_lep["l1_index"] = lep1.index
    di_lep["l2_index"] = lep2.index

    # Choose oppositely charged leptons
    di_lep = di_lep[di_lep.charge == 0]

    # Sort by closest mass to the resonance value
    sort_mask = ak.argsort(abs(resonance_mass-di_lep.mass), axis=1)
    Reso = di_lep[sort_mask]

    return Reso
    return Reso, used_lep1, used_lep2

# 2. To replace: FCCAnalyses::ZHfunctions::getTwoHighestPMuons(rest_of_muons)") # Find the higest p muon pair from the remaining muons (off-shell Z)
def getTwoHighestPMuons(muons):
    '''
    Sort by decending P and return the pair of particles with highest P and opposite charges
    '''
    # if not ak.all(ak.num(muons, axis=1) > 1 ):
    #     raise IndexError("Need at least two particles!")
    sorted_muons_p = ak.argsort(muons.p, ascending=False)
    sorted_muons = muons[sorted_muons_p]

    # First particle is always selected, if the second one has the opposite charge, then its accepted otherwise we move on to the third and so on
    # Interestingly, this type of operation is non trivial in an array format
    first_muon, other_muons = sorted_muons[:, 0:1], sorted_muons[:, 1:]

    # prepare before cartesian : replace none with []
    first_muon = ak.fill_none(first_muon, [], axis=0)
    other_muons = ak.fill_none(other_muons, [], axis=0)
    # All combinations
    all_comb = ak.cartesian([first_muon, other_muons])
    l1, l2 = ak.unzip(all_comb)
    charge_mask = l1.charge!= l2.charge
    l1 = l1[charge_mask]
    l2 = l2[charge_mask]

    at_least_one_opp_charged = ak.sum(charge_mask, axis=1) > 0 # is an event selection
    
    return ak.firsts(l1), ak.firsts(l2), at_least_one_opp_charged
# 3. To sum all the lorentz vectors in a an array of lorentzvectors
def sum_all(array_of_lv):
    #array_of_lv = ak.drop_none(array_of_lv)

    out = ak.zip(
        {
            "px":ak.sum(array_of_lv.px , axis=1),
            "py":ak.sum(array_of_lv.py , axis=1),
            "pz":ak.sum(array_of_lv.pz , axis=1),
            "E":ak.sum(array_of_lv.E , axis=1)
        },
        with_name="Momemtum4D"
    )

    return out
# 4. To replace : FCCAnalyses::ZHfunctions::coneIsolation(0.0,0.523599)(fourMuons,rest_of_particles)
def coneIsolation(particle, rest_of_the_particles, min_dr=0.0 , max_dr=0.4):
    ''' Refer: https://github.com/delphes/delphes/blob/master/modules/Isolation.cc#L154
    '''
    neutral_particles = ak.mask(rest_of_the_particles, rest_of_the_particles.charge == 0)
    charged_particles = ak.mask(rest_of_the_particles, rest_of_the_particles.charge != 0)

    n_combs = ak.cartesian((particle,neutral_particles[:,np.newaxis]), axis=1)
    n1,n2 = ak.unzip(n_combs)
    c_combs = ak.cartesian((particle,charged_particles[:,np.newaxis]), axis=1)
    c1,c2 = ak.unzip(c_combs)

    n_angle = n1.deltaangle(n2)
    c_angle = c1.deltaangle(c2)

    n_angle_mask = (n_angle < max_dr) & (n_angle >= min_dr)
    c_angle_mask = (c_angle < max_dr) & (c_angle >= min_dr)

    filtered_neutral = n2[n_angle_mask]
    filtered_charged = c2[c_angle_mask]

    sumNeutral = ak.sum(filtered_neutral.p, axis=2)
    sumCharged = ak.sum(filtered_charged.p, axis=2)

    total_sum = sumNeutral + sumCharged

    ratio = total_sum / particle.p

    return ratio
