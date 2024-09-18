# =========================================================================================================================
# Configuration to run the analysis
# =========================================================================================================================


#################
# Run Variables #
#################
process = {
    'collider':'FCCee',
    'campaign':'spring2021',
    'detector':'IDEA',
    'samples':['p8_ee_ZH_ecm240','p8_ee_ZZ_ecm240']
}
fraction = {
    'p8_ee_ZH_ecm240':0.001,
    'p8_ee_ZZ_ecm240':0.001,
}
ecm = 240.0 # #\sqrt(s) in GeV
local_yaml_dict = "../../filesets/"
output_path = "outputs/FCCee/Example/"


###################
# Plot properties #
###################
plots = {
    'Recon_E':{'name':'Rec_E','title':'Reconstructed Particles Energy','xlabel':'$E$ [GeV]','ylabel':'Events','bins':100,'xmin':0,'xmax':250},
}


#############
# Processor #
#############
from processor import example_processor
processor_path = "processor_mHrecoil"
processor_name = "mHrecoil"
processor_args = []
processor_kwargs = {}
processor = example_processor(*processor_args, **processor_kwargs)


######################
# Plotting Variables #
######################
selections = ['sel0','sel1']
stack = [True, False]
log = [True, False]
formats = ['png','pdf']
req_plots = ['Recon_E',]
req_hists = {
    "ZZ":{"type":'Background',"datasets":['p8_ee_ZZ_ecm240'],"color":'g'},
    "ZH":{"type":'Signal',"datasets":['p8_ee_ZH_ecm240'],"color":'r'},
}
cross_sections = {#in pb-1 # Taken as is from FCC events catalogue at https://fcc-physics-events.web.cern.ch/FCCee/spring2021/Delphesevents_IDEA.php
    'p8_ee_ZZ_ecm240': 1.35899,
    'p8_ee_ZH_ecm240': 0.201868
}
input_path     = output_path
plot_path      = 'outputs/FCCee/Example/'
intLumi        = 5.0e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} \\rightarrow Example \\rightarrow Process'
delphesVersion = '3.4.2'
energy         = ecm #in GeV
collider       = 'FCC-ee'
