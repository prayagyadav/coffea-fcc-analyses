import numpy as np

# Custom Recombiners
class E0_scheme:
    '''
    E0 Scheme Recombiner
    Find the C++ equivalent at https://github.com/HEP-FCC/FCCAnalyses/blob/master/addons/FastJet/src/ExternalRecombiner.cc
    '''
    def preprocess(p):
        pass
    def recombine(pa, pb):
        psum = pa+pb
        pmag = np.sqrt(psum.px()**2 + psum.py()**2 + psum.pz()**2)
        E0scale = psum.E() / pmag

        psum.px = psum.px()*E0scale
        psum.py = psum.py()*E0scale
        psum.pz = psum.pz()*E0scale

        return psum*E0scale
