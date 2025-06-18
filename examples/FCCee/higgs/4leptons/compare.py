# Script to compare the results from FCCAnalyses and coffeafccanalyses


# Load FCCAnalyses output : stage_1 sel_0

fcc_base_directory = "with_filter"
coffeafccanalyses_input_directory = "Batch"
output_filename = "4leptons" #for coffea

# Load coffeafccanalyses output
from coffea.util import load

from collections import defaultdict
from numbers import Number
import glob, re
import hist, uproot
import awkward as ak

# Info about plots
plots = {
    'selectedmuons_p':{'name':'selected_muons_p','title':'$\\mu_p$ [GeV]','xlabel':'$p_T$ [GeV]','ylabel':'Events','bins':250,'xmin':0,'xmax':250},

    'fourmuons_mass':{'name':'fourMuons_mass','title':'$M_{4\\mu}$ [GeV]','xlabel':'$Mass$ [GeV]','ylabel':'Events','bins':50,'xmin':0,'xmax':250},
    'fourmuons_pmin':{'name':'fourMuons_pmin','title':'$(P_{4\\mu})_{min}$ [GeV]','xlabel':'$p_{min}$ [GeV]','ylabel':'Events','bins':20,'xmin':0,'xmax':100},

    'Z_res_mass':{'name':'zll_mass','title':'On-shell $M_{\\mu\\mu}$ [GeV]','xlabel':'$Mass$ [GeV]','ylabel':'Events','bins':50,'xmin':0,'xmax':250},
    'Z_non_res_mass':{'name':'non_res_Z_m','title':'Off-shell $M_{\\mu\\mu}$ [GeV]','xlabel':'$Mass$ [GeV]','ylabel':'Events','bins':50,'xmin':0,'xmax':250},

    'vis_e_woMuons':{'name':'vis_e_other_particles','title':'Visible Energy excluding muons [GeV]','xlabel':'$E$ [GeV]','ylabel':'Events','bins':50,'xmin':0,'xmax':250},
    'iso_least_isolated_muon':{'name':'fourMuons_min_iso','title':'iso(least isolated muon)','xlabel':'iso','ylabel':'Events','bins':50,'xmin':0,'xmax':20},
    'missing_p':{'name':'pmiss','title':'missing p [GeV]','xlabel':'$p^{miss}$ [GeV]','ylabel':'Events','bins':50,'xmin':0,'xmax':250},
    'cos_theta_miss':{'name':'cosTheta_miss','title':'Cos(Theta_miss)','xlabel':'$cos_{miss}\\theta$','ylabel':'Events','bins':100,'xmin':0,'xmax':1},

}

histoList = {
    "selectedmuons_p":"selected_muons_p",
    "fourmuons_mass":"fourMuons_mass",
    "fourmuons_pmin":"fourMuons_pmin",
    "Z_res_mass":"zll_mass",
    "Z_non_res_mass":"non_res_Z_m",
    "vis_e_woMuons":"vis_e_other_particles",
    "iso_least_isolated_muon":"fourMuons_min_iso",
    "missing_p":"pmiss",
    "cos_theta_miss":"cosTheta_miss",
}

# Prepare coffea plots
def accumulate(dicts):
    """
    Recursively merges a list of dictionaries, supporting:
    - Numeric summation
    - List concatenation
    - Set union
    - Histogram addition (from `hist`)
    - Nested dictionaries
    - Key exceptions (preserve first)
    """
    try:
        from hist import Hist
    except ImportError:
        Hist = None  # Skip if hist is not available

    exception_list = {'Labels'}
    grouped = defaultdict(list)

    for d in dicts:
        for k, v in d.items():
            grouped[k].append(v)

    outdict = {}

    for key, values in grouped.items():
        first = values[0]

        if key in exception_list:
            outdict[key] = first
        elif all(isinstance(v, dict) for v in values):
            outdict[key] = accumulate(values)
        elif all(isinstance(v, list) for v in values):
            outdict[key] = sum(values, [])  # concatenate
        elif all(isinstance(v, set) for v in values):
            result = set()
            for v in values:
                result |= v
            outdict[key] = result
        elif Hist and all(isinstance(v, Hist) for v in values):
            total = values[0]
            for v in values[1:]:
                total += v
            outdict[key] = total
        elif all(isinstance(v, Number) for v in values):
            outdict[key] = sum(values)
        else:
            # Mixed types or strings — keep the first
            outdict[key] = first

    return outdict


input_path = coffeafccanalyses_input_directory+"/"
base_filename = output_filename+".coffea"
# print(f'Current configuration:\n\tinput_path:\t{input_path}\n\tbase_filename:\t{base_filename}\n')
# print("Loading coffea files...")

#Find coffea files
coffea_files = glob.glob(input_path+'*.coffea')
# print('Detected coffea files:')
# for file in coffea_files : print('\t'+file)
# print(f'Choosing:\n\t{base_filename}')

#Find chunked coffea files and combine them
chunked_coffea_files = glob.glob(input_path+base_filename.strip('.coffea')+'-chunk*.coffea')
if len(chunked_coffea_files) != 0 :
    # print('Joining chunks:')
    chunk_index_list = []
    chunk_list = []
    for file in chunked_coffea_files:
        # print('\t'+file)
        chunk_list.append(file)
        chunk_index_list.append(int(re.search('-chunk(.*).coffea',file).group(1)))
    chunk_index_list.sort()

    #Check if there are missing chunks
    full_set = set(range(len(chunk_index_list)))
    lst_set = set(chunk_index_list)
    missing = list(full_set - lst_set)
    if len(missing) != 0:
        raise FileNotFoundError(f'Missing chunk indexes : {missing}')

    #Load and accumulate all the chunks
    input_list = [load(file) for file in chunk_list]
    coffeafcc_input = accumulate(input_list)

#If there is only one chunk no need to join chunks
else :
    coffeafcc_input = load(input_path+base_filename)

coffea_hists = {}
for dataset in coffeafcc_input.keys():
    coffea_hists[dataset] = {}
    for r_plots in histoList.keys():
        coffea_hists[dataset][r_plots] = coffeafcc_input[dataset]['histograms']['sel0'][r_plots]


# prepare fcc plots
datasets = glob.glob(fcc_base_directory+"/*")
FCC_output = {}
for path in datasets:
    dataset_name = path.split('/')[-1]
    with uproot.open(path+"/chunk0.root") as f:
        FCC_output[dataset_name] = f['events'].arrays()

fcc_hists = {}
for dataset in FCC_output.keys():
    fcc_hists[dataset] = {}
    for name, var in histoList.items():
        to_plot = FCC_output[dataset][var]
        info = plots[name]
        fcc_hists[dataset][name] = hist.Hist.new.Reg( info['bins'], info['xmin'], info['xmax'] ).Double().fill(ak.ravel(to_plot))

# Now we can finally compare the histograms from fcc_hists and coffea_hists

for dataset in fcc_hists.keys():
    print(f"Checking {dataset} ...")
    for name in fcc_hists[dataset].keys():
        print(f"\t{name}")
        diff = coffea_hists[dataset][name] - fcc_hists[dataset][name]
        print(f"\t\tDifference is {diff.sum()}")


