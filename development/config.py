# Configuration to run the analysis

#################
# Run Variables #
#################

# process = {
#     'collider':'FCCee',
#     'campaign':'spring2021',
#     'detector':'IDEA',
#     'samples':['p8_ee_ZZ_ecm240','p8_ee_WW_ecm240','p8_ee_ZH_ecm240']
# }
process = {
    'collider':'FCCee',
    'campaign':'spring2021',
    'detector':'IDEA',
    'samples':['p8_ee_ZZ_ecm240']
}
# fraction = {
#     'p8_ee_ZZ_ecm240':0.005,
#     'p8_ee_WW_ecm240':0.5,
#     'p8_ee_ZH_ecm240':0.2
# }
fraction = {
    # test
    'p8_ee_ZZ_ecm240':0.001,
}
ecm = 240.0 # #\sqrt(s) in GeV


###################
# Plot properties #
###################

plots = {
    'Zm':{'name':'Zm','title':'Z Candidate mass','xlabel':'$Z_{mass}$ [GeV]','ylabel':'Events','bins':100,'xmin':0,'xmax':250},
    'Zm_zoom':{'name':'Zm_zoom','title':'Z Candidate mass','xlabel':'$Z_{mass}$ [GeV]','ylabel':'Events','bins':40,'xmin':80,'xmax':100},
    'Recoilm':{'name':'Recoilm','title':'Leptonic Recoil mass','xlabel':'$Recoil_{mass}$ [GeV]','ylabel':'Events','bins':100,'xmin':0,'xmax':200},
    'Recoilm_zoom':{'name':'Recoilm_zoom','title':'Leptonic Recoil mass','xlabel':'$Recoil_{mass}$ [GeV]','ylabel':'Events','bins':200,'xmin':80,'xmax':160},
    'Recoilm_zoom1':{'name':'Recoilm_zoom1','title':'Leptonic Recoil mass','xlabel':'$Recoil_{mass}$ [GeV]','ylabel':'Events','bins':100,'xmin':120,'xmax':140},
    'Recoilm_zoom2':{'name':'Recoilm_zoom2','title':'Leptonic Recoil mass','xlabel':'$Recoil_{mass}$ [GeV]','ylabel':'Events','bins':200,'xmin':120,'xmax':140},
    'Recoilm_zoom3':{'name':'Recoilm_zoom3','title':'Leptonic Recoil mass','xlabel':'$Recoil_{mass}$ [GeV]','ylabel':'Events','bins':400,'xmin':120,'xmax':140},
    'Recoilm_zoom4':{'name':'Recoilm_zoom4','title':'Leptonic Recoil mass','xlabel':'$Recoil_{mass}$ [GeV]','ylabel':'Events','bins':800,'xmin':120,'xmax':140},
    'Recoilm_zoom5':{'name':'Recoilm_zoom5','title':'Leptonic Recoil mass','xlabel':'$Recoil_{mass}$ [GeV]','ylabel':'Events','bins':2000,'xmin':120,'xmax':140},
    'Recoilm_zoom6':{'name':'Recoilm_zoom6','title':'Leptonic Recoil mass','xlabel':'$Recoil_{mass}$ [GeV]','ylabel':'Events','bins':100,'xmin':130.3,'xmax':140}
}

#############
# Processor #
#############

from processor_mHrecoil import mHrecoil
processor_path = "processor_mHrecoil"
processor_name = "mHrecoil"
processor_args = []
processor_kwargs = {"ecm":ecm}
processor = mHrecoil(*processor_args, **processor_kwargs)

######################
# Plotting Variables #
######################

selections = ['sel0','sel1']
stack = [True, False]
log = [True, False]
formats = ['png','pdf']
req_plots = ['Zm', 'Zm_zoom', 'Recoilm', 'Recoilm_zoom', 'Recoilm_zoom1']
# req_hists = {
#     "ZH":{"type":'Signal',"datasets":['p8_ee_ZH_ecm240'],"color":'r'},
#     "ZZ":{"type":'Background',"datasets":['p8_ee_ZZ_ecm240'],"color":'g'},
#     "WW":{"type":'Background',"datasets":['p8_ee_WW_ecm240'],"color":'b'}
# }
req_hists = {
    "ZZ":{"type":'Background',"datasets":['p8_ee_ZZ_ecm240'],"color":'g'},
    "ZH":{"type":'Signal',"datasets":['p8_ee_ZZ_ecm240'],"color":'b'},
}
cross_sections = {#in pb-1 # Taken as is from FCC events catalogue at https://fcc-physics-events.web.cern.ch/FCCee/spring2021/Delphesevents_IDEA.php
    'p8_ee_WW_ecm240': 16.4385,
    'p8_ee_ZZ_ecm240': 1.35899,
    'p8_ee_ZH_ecm240': 0.201868
}
plot_path      = 'outputs/FCCee/higgs/mH-recoil/mumu/plots/'
intLumi        = 5.0e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} \\rightarrow ZH \\rightarrow \\mu^{+}\\mu^{-} + X'
delphesVersion = '3.4.2'
energy         = ecm #in GeV
collider       = 'FCC-ee'
