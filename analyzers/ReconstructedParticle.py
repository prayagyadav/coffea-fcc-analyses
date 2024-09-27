import dask_awkward as dak
import awkward as ak
import numpy as np


def resonanceBuilder(lepton, resonance):
    '''
    Builds Resonance candidates
    Input:    lepton(var*[var*LorentzVector]),
              resonance(float)
    Output: Reso([var*LorentzVecctor]) best resonance candidate in each event (maximum one per event)
    '''
    #Create all the combinations
    combs = ak.combinations(lepton,2)
    # Get dileptons
    lep1 , lep2 = ak.unzip(combs)
    di_lep = lep1 + lep2 # This process drops any other field except 4 momentum fields

    di_lep = ak.zip({"px":di_lep.px,"py":di_lep.py,"pz":di_lep.pz,"E":di_lep.E,"charge":lep1.charge + lep2.charge}, with_name="Momentum4D")

    # Sort by closest mass to the resonance value
    sort_mask = ak.argsort(abs(resonance-di_lep.mass), axis=1)
    Reso = di_lep[sort_mask]

    #Choose the best candidate
    Reso = ak.fill_none(Reso,[],axis=0) #Transform the None values at axis 0 to [], so that they survive the next operation
    Reso = ak.firsts(Reso) #Chooses the first elements and flattens out, [] gets converted to None

    return Reso

def recoilBuilder(vec, ecm):
    '''
    Builds Recoil from a given LorentzVector and Center of Mass Energy
    Input:    vec(var*[var*LorentzVector]),
              ecm(float)
    Output: Recoil([var*LorentzVecctor])
    '''
    Recoil = ak.zip({"px":0.0-vec.px,"py":0.0-vec.py,"pz":0.0-vec.pz,"E":ecm-vec.E},with_name="Momentum4D")
    return Recoil


def remove(array, idx):
    '''
    Returns all the particles except the indices defined in idx.index.
    Eg. remove(events.ReconstructedParticle, events.Muonidx0) returns the events.ReconstructedParticle array with all the muons removed
    '''
    index = idx.index
    all_index = ak.local_index(array,axis=1)

    i,a = ak.unzip(ak.cartesian([index[:,np.newaxis] ,all_index], nested=True))
    c = a == i
    d = ak.firsts(c)
    s = ak.sum(d, axis=2)
    kl = s == 1
    
    return array[~kl]
