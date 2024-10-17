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
        # print("pa : ", pa)
        # print("pb : ", pb)
        psum = pa+pb
        # print("Psum before : ", psum)
        pmag = np.sqrt(psum.px()**2 + psum.py()**2 + psum.pz()**2)
        # print("pmag : ", pmag)
        E0scale = psum.E() / pmag
        # print("E0scale : ", E0scale)

        # print("Available methods for psum : ", psum.__dir__())
        psum.reset(
                psum.px()*E0scale,
                psum.py()*E0scale,
                psum.pz()*E0scale,
                psum.E()
        )
        # print("psum after : ", psum)
        
        return psum
