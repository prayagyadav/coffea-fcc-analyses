# =========================================================================================================================
# Configuration to run the analysis
# =========================================================================================================================
# Here the fields are filled with a simple example
# Fill them with your desired values and delete this line if needed.

#################
# Run Variables #
#################
process = {
    'collider':'FCCee',
    'campaign':'spring2021',
    'detector':'IDEA',
    'samples':['p8_ee_ZH_ecm240','p8_ee_ZZ_ecm240','p8_ee_WW_ecm240']
}
fraction = {
    'p8_ee_ZH_ecm240':0.001,
    'p8_ee_ZZ_ecm240':0.0002,
    'p8_ee_WW_ecm240':0.0002
}
ecm = 240.0 # #\sqrt(s) in GeV
local_yaml_dict = "../filesets/"
output_path = "./"
output_filename = "out"
executor = "dask" # 'dask' is local and 'condor' is batch


###################
# Plot properties #
###################

plots = {
    'dijet_m':{'name':'dijet_higgs_m','title':'Dijet Higgs Mass','xlabel':'Dijet mass [GeV]','ylabel':'Events','bins':80,'xmin':70,'xmax':150},
    'pdgid':{'name':'jets_truth','title':'Jets Truth','xlabel':'Jet truth label PDGID','ylabel':'Events','bins':16,'xmin':-8,'xmax':8},
    'recoil':{'name':'zmumu_recoil_m','title':'Recoil from Z (mass)','xlabel':'Recoil [GeV]','ylabel':'Events','bins':200,'xmin':120,'xmax':140},
    'p_ll':{'name':'zmumu_p','title':'$Z\\rightarrow \\mu^{\\plus} \\mu^{\\minus}$ Momentum','xlabel':'$p\\left( \\mu^{\\plus} \\mu^{\\minus}\\right) \\ [GeV]$','ylabel':'Events','bins':50,'xmin':20,'xmax':70},
    'm_ll':{'name':'zmumu_m','title':'$Z\\rightarrow \\mu^{\\plus} \\mu^{\\minus}$ Mass','xlabel':'$m\\left( \\mu^{\\plus} \\mu^{\\minus}\\right) \\ [GeV]$','ylabel':'Events','bins':40,'xmin':70,'xmax':110},
}



#############
# Processor #
#############
from processor import jetclustering
processor_path = "processor"
processor_name = "jetclustering"
processor_args = []
processor_kwargs = {}
processor = jetclustering(*processor_args, **processor_kwargs)


######################
# Plotting Variables #
######################
selections = ['sel']
stack = [True, False]
log = [True, False]
formats = ['png','pdf']
req_plots = ['dijet_m', 'pdgid', 'recoil', 'p_ll', 'm_ll']
req_hists = {
    "ZZ":{"type":'Background',"datasets":['p8_ee_ZZ_ecm240'],"color":'g'},
    "ZH":{"type":'Signal',"datasets":['p8_ee_ZH_ecm240'],"color":'r'},
    "WW":{"type":'Background', "datasets":['p8_ee_WW_ecm240'], "color":'b'}
}
cross_sections = {#in pb-1 # Taken as is from FCC events catalogue at https://fcc-physics-events.web.cern.ch/FCCee/spring2021/Delphesevents_IDEA.php
    'p8_ee_ZZ_ecm240': 1.35899,
    'p8_ee_ZH_ecm240': 0.201868,
    'p8_ee_WW_ecm240': 16.4385
}
input_path     = output_path
plot_path      = '.'
intLumi        = 5.0e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} \\rightarrow Example \\rightarrow Process'
delphesVersion = '3.4.2'
energy         = ecm #in GeV
collider       = 'FCC-ee'
