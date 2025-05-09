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
    'campaign':'winter2023',
    'detector':'IDEA',
    'samples':[
        # Signal
        'wzp6_ee_qqH_HZZ_llll_ecm240',
        'wzp6_ee_nunuH_HZZ_ecm240',
        # Backgrounds
        'p8_ee_Zqq_ecm240',
        'p8_ee_ZZ_ecm240',
        'p8_ee_WW_ecm240',
        'wzp6_ee_tautauH_HWW_ecm240',
        'wzp6_ee_ccH_HWW_ecm240',
        'wzp6_ee_bbH_HWW_ecm240',
        'wzp6_ee_mumuH_HWW_ecm240',
        'wzp6_ee_mumuH_Hcc_ecm240',
        'wzp6_ee_mumuH_Hbb_ecm240',
        'wzp6_ee_mumuH_Hgg_ecm240',
        'wzp6_ee_mumuH_HZa_ecm240',
        ]
}
fraction = {
        # Signal
        'wzp6_ee_qqH_HZZ_llll_ecm240':0.01,
        'wzp6_ee_nunuH_HZZ_ecm240':0.01,
        # Backgrounds
        'p8_ee_Zqq_ecm240':0.01,
        'p8_ee_ZZ_ecm240':0.01,
        'p8_ee_WW_ecm240':0.01,
        'wzp6_ee_tautauH_HWW_ecm240':0.01,
        'wzp6_ee_ccH_HWW_ecm240':0.01,
        'wzp6_ee_bbH_HWW_ecm240':0.01,
        'wzp6_ee_mumuH_HWW_ecm240':0.01,
        'wzp6_ee_mumuH_Hcc_ecm240':0.01,
        'wzp6_ee_mumuH_Hbb_ecm240':0.01,
        'wzp6_ee_mumuH_Hgg_ecm240':0.01,
        'wzp6_ee_mumuH_HZa_ecm240':0.01,
}
ecm = 240.0 # #\sqrt(s) in GeV
local_yaml_dict = "../../filesets/"
output_path = "outputs"
output_filename = "4leptons"
executor = "dask" # 'dask' is local and 'condor' is batch

use_schema = "FCC"
schema_version = "latest"

###################
# Plot properties #
###################
plots = {
    'selectedmuons_p':{'name':'selected_muons_p','title':'$\\mu_p$ [GeV]','xlabel':'$p_T$ [GeV]','ylabel':'Events','bins':250,'xmin':0,'xmax':250},

    'fourmuons_mass':{'name':'fourMuons_mass','title':'$M_{4\\mu}$ [GeV]','xlabel':'$Mass$ [GeV]','ylabel':'Events','bins':50,'xmin':0,'xmax':250},
    'fourmuons_pmin':{'name':'fourMuons_pmin','title':'$(P_{4\\mu})_{min}$ [GeV]','xlabel':'$p_T$ [GeV]','ylabel':'Events','bins':20,'xmin':0,'xmax':100},

    'Z_res_mass':{'name':'zll_mass','title':'On-shell $M_{\\mu\\mu}$ [GeV]','xlabel':'$Mass$ [GeV]','ylabel':'Events','bins':50,'xmin':0,'xmax':250},
    'Z_non_res_mass':{'name':'non_res_Z_m','title':'Off-shell $M_{\\mu\\mu}$ [GeV]','xlabel':'$Mass$ [GeV]','ylabel':'Events','bins':50,'xmin':0,'xmax':250},

    'vis_e_woMuons':{'name':'vis_e_other_particles','title':'Visible Energy excluding muons [GeV]','xlabel':'$E$ [GeV]','ylabel':'Events','bins':50,'xmin':0,'xmax':250},
    'iso_least_isolated_muon':{'name':'fourMuons_min_iso','title':'iso(least isolated muon)','xlabel':'iso','ylabel':'Events','bins':50,'xmin':0,'xmax':20},
    'missing_p':{'name':'pmiss','title':'missing p [GeV]','xlabel':'$p^{miss}_T$ [GeV]','ylabel':'Events','bins':50,'xmin':0,'xmax':250},
    'cos_theta_miss':{'name':'cosTheta_miss','title':'Cos(Theta_miss)','xlabel':'$cos^{miss}\\theta$','ylabel':'Events','bins':100,'xmin':0,'xmax':1},

}


#############
# Processor #
#############
processor_path = "processor"
processor_name = "Fourleptons"
processor_args = []
processor_kwargs = {}


######################
# Plotting Variables #
######################
selections = ['sel0','sel1','sel2','sel3','sel4','sel5','sel6']
stack = [True, False]
log = [True, False]
formats = ['png']
req_plots = ['selectedmuons_p','fourmuons_mass','fourmuons_pmin','Z_res_mass','Z_non_res_mass','vis_e_woMuons','iso_least_isolated_muon','missing_p','cos_theta_miss']
req_hists = {
        #Signal
        "qqH_HZZ":{"type":'Signal',"datasets":['wzp6_ee_qqH_HZZ_llll_ecm240'],"color":'red'},
#        "nunuH_HZZ":{"type":'Signal',"datasets":['wzp6_ee_nunuH_HZZ_ecm240'],"color":'orange'},
        #Background
        "ZZ":{"type":'Background',"datasets":['p8_ee_ZZ_ecm240'],"color":'blue'},
        "Zqq":{"type":'Background',"datasets":['p8_ee_Zqq_ecm240'],"color":'yellow'},
        "mumuH_Hjj":{"type":'Background',"datasets":['wzp6_ee_mumuH_Hbb_ecm240','wzp6_ee_mumuH_Hcc_ecm240','wzp6_ee_mumuH_Hgg_ecm240',],"color":'cyan'},
        "WW":{"type":'Background',"datasets":['p8_ee_WW_ecm240'],"color":'gray'},
        "HWW":{"type":'Background',"datasets":['wzp6_ee_mumuH_HWW_ecm240','wzp6_ee_bbH_HWW_ecm240','wzp6_ee_tautauH_HWW_ecm240','wzp6_ee_ccH_HWW_ecm240'],"color":'teal'},
        "mumuH_HZa":{"type":'Background',"datasets":['wzp6_ee_mumuH_HZa_ecm240'],"color":'green'},
        
}
cross_sections = {#in pb # Taken as is from FCC events catalogue at https://fcc-physics-events.web.cern.ch/FCCee/winter2023/Delphesevents_IDEA.php
                  # Signal
                  'wzp6_ee_qqH_HZZ_llll_ecm240':3.777e-5,
                  'wzp6_ee_nunuH_HZZ_ecm240':0.00122,
                  # Backgrounds
                  'p8_ee_Zqq_ecm240':52.6539,
                  'p8_ee_ZZ_ecm240':1.35899,
                  'p8_ee_WW_ecm240':16.4385,
                  'wzp6_ee_tautauH_HWW_ecm240':0.001453,
                  'wzp6_ee_ccH_HWW_ecm240':0.005023,
                  'wzp6_ee_bbH_HWW_ecm240':0.00645,
                  'wzp6_ee_mumuH_HWW_ecm240':0.001456,
                  'wzp6_ee_mumuH_Hcc_ecm240':0.0001956,
                  'wzp6_ee_mumuH_Hbb_ecm240':0.00394,
                  'wzp6_ee_mumuH_Hgg_ecm240':0.0005538,
                  'wzp6_ee_mumuH_HZa_ecm240':1.037e-5,
                  }
input_path     = output_path
plot_path      = 'outputs/plots/'
intLumi        = 10.80e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} \\rightarrow ZH \\rightarrow 4\\mu+ X'
delphesVersion = '3.4.2'
energy         = ecm #in GeV
collider       = 'FCC-ee'
