# =========================================================================================================================
# Configuration to run the analysis
# =========================================================================================================================

#################
# Run Variables #
#################
process = {
    'collider':'FCCee',
    'campaign':'winter2023',
    'detector':'IDEA',
    'samples':['wzp6_ee_mumuH_Hbb_ecm240']
}
fraction = {
    'wzp6_ee_mumuH_Hbb_ecm240':1
}
ecm = 240.0 # #\sqrt(s) in GeV
local_yaml_dict = "../../filesets/"
output_path = "outputs/"
output_filename = "jetclustering"
executor = "dask"
#executor = "condor" # 'dask' is local and 'condor' is batch
use_schema = "FCC"
schema_version = "pre-edm4hep1"

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
processor_path = "processor"
processor_name = "jetclustering"
processor_args = []
processor_kwargs = {}


######################
# Plotting Variables #
######################
selections = ['sel']
stack = [False]
log = [True, False]
formats = ['png','pdf']
req_plots = ['dijet_m', 'pdgid', 'recoil', 'p_ll', 'm_ll']
req_hists = {
    "ZH":{"type":'Signal',"datasets":['wzp6_ee_mumuH_Hbb_ecm240'],"color":'r'},
}
cross_sections = {#in pb-1 # Taken as is from FCC events catalogue at https://fcc-physics-events.web.cern.ch/FCCee/winter2023/Delphesevents_IDEA.php
    'wzp6_ee_mumuH_Hbb_ecm240': 0.00394,
}
input_path     = output_path
plot_path      = 'outputs/FCCee/jetclustering/plots/'
intLumi        = 7.2e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} \\rightarrow Z(\\mu^{+}\\mu^{-})H(b\\bar{b})'
delphesVersion = '3.4.2'
energy         = ecm #in GeV
collider       = 'FCC-ee'
