import mplhep as hep, pandas as pd, numpy as np, matplotlib.pyplot as plt
import  collections, argparse, hist, copy, glob, os, re
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from coffea.util import load
from pandas.core.indexes.base import Level
import config

##################################
# Definition of useful functions #
##################################

plot_props = pd.DataFrame(config.plots)

from collections import defaultdict
from numbers import Number

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

def get_xsec_scale(dataset, raw_events, Luminosity):
    '''
    Get final scale factor from cross section
    '''
    xsec = config.cross_sections[dataset] #in per picobarn
    if raw_events > 0:
        sf = (xsec*Luminosity)/raw_events
    else :
        raise ValueError('Raw events less than of equal to zero!')
    #return round(float(sf),3)
    return float(sf)


def hist_sorter(preferred_order, unsorted_hists, unsorted_labels, unsorted_colors):
    '''Custom histogram sorter to plot in histplot'''
    sorted_hists, sorted_labels, sorted_colors = [], [], []
    for l in preferred_order[::-1]:
        pos = unsorted_labels.index(l)
        sorted_hists.append(unsorted_hists[pos])
        sorted_labels.append(unsorted_labels[pos])
        sorted_colors.append(unsorted_colors[pos])

    return sorted_hists, sorted_labels, sorted_colors


def yield_plot(name, title, keys, scaled, unscaled, formats, path, plot_width=8, plot_height=8):
    '''
    Create yield plots
    '''

    fig, ax = plt.subplots(figsize=(plot_width,plot_height))
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.text(0.25, 1.02, 'FCC Analyses: FCC-ee Simulation (Delphes)', fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    ax.text(0.92, 1.02, '$\\sqrt{s} = '+str(config.energy)+' GeV$', fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    ax.text(0.10, 0.95, config.collider, fontsize=14, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
    ax.text(0.10, 0.88,'Delphes Version: '+ config.delphesVersion, fontsize=14, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
    ax.text(0.10, 0.81, 'Signal : $'+config.ana_tex+'$', fontsize=14, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
    ax.text(0.10, 0.74, '$L = '+str(config.intLumi/1e6)+' ab^{-1}$', fontsize=14, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)


    table_scale = getattr(config, "yield_table_scale", 1)
    print("table_scale", table_scale)
    level, linespacing = 0.72, 0.05
    for scale,obs in zip(['UNSCALED','SCALED'],[unscaled,scaled]):
        ax.text(0.02, level, scale, weight='bold', fontsize=int(13*table_scale), horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        level -= linespacing*table_scale
        ax.text(0.02, level, 'Sample', weight='bold', fontsize=int(12*table_scale), horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        ax.text(0.30, level, 'Type', weight='bold', fontsize=int(12*table_scale), horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        ax.text(0.49, level, 'Raw', weight='bold', fontsize=int(12*table_scale), horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        ax.text(0.68, level, 'Yield', weight='bold', fontsize=int(12*table_scale), horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        ax.text(0.87, level, 'Yield %', weight='bold', fontsize=int(12*table_scale), horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        for i in range(len(keys)):
            datasets = config.req_hists[list(keys)[i]]['datasets']
            Type = config.req_hists[list(keys)[i]]['type']
            color = config.req_hists[list(keys)[i]]['color']
            yield_text = str(round(obs[i]['Cutflow'].values()[-1],2))
            raw_text = str(round(obs[i]['Cutflow'].values()[0],2))
            percentage = str(round(obs[i]['Cutflow'].values()[-1]*100/obs[i]['Cutflow'].values()[0],2))
            level -= linespacing*table_scale
            ax.text(0.02, level, list(keys)[i], fontsize=int(10*table_scale), color=color,horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
            ax.text(0.30, level, Type, color=color, fontsize=int(12*table_scale), horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
            ax.text(0.49, level, raw_text, color=color, fontsize=int(12*table_scale), horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
            ax.text(0.68, level, yield_text, color=color, fontsize=int(12*table_scale), horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
            ax.text(0.87, level, percentage, color=color, fontsize=int(12*table_scale), horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        level -= 2*linespacing*table_scale

    ax.set_title(title,pad=25,  fontsize= "15", color="#192655")
    for format in formats :
        filename = name+'.'+format
        full_name = path+filename
        fig.savefig(full_name,dpi=240);
        print(filename, " saved at ", path)
    plt.close()

def cuts_table(name, title, labels, formats, path):
    '''
    Create cut table and save as png
    '''

    fig, ax = plt.subplots(figsize=(8,8))
    ax.text(0.25, 1.02, 'FCC Analyses: FCC-ee Simulation (Delphes)', fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    ax.text(0.92, 1.02, '$\\sqrt{s} = '+str(config.energy)+' GeV$', fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

    level, linespacing = 0.90, 0.05
    ax.text(0.02, level, 'Cut Order', weight='bold', fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
    ax.text(0.30, level, 'Label', weight='bold', fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)

    for i in range(len(labels)):
        level -= linespacing
        ax.text(0.02, level, str(i), fontsize=10,horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        ax.text(0.30, level, labels[i],fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
    level -= 2*linespacing

    ax.set_title(title,pad=25,  fontsize= "15", color="#192655")
    for format in formats :
        filename = name+'.'+format
        full_name = path+filename
        fig.savefig(full_name,dpi=240);
        print(filename, " saved at ", path)
    plt.close()

def generate_plots(input_dict, req_hists, req_plots, selections, stack, log, formats, path, plotprops):
    '''
    Batch plot processor: Creates Yield, Cutflow and Kinematic plots
    '''
    for sel in selections:
        print('_________________________________________________________________')
        print('---------------------','Selection:', sel ,'---------------------')
        plot_path_selection = path+sel+'/'
        if not os.path.exists(plot_path_selection):
            os.makedirs(plot_path_selection)

        #Get hist array for different backgrounds
        label_list, label_list_signal = [], []
        dataset_list, dataset_list_signal = [], []
        color_list, color_list_signal = [], []
        hist_list, hist_list_signal = [], []
        unscaled_hist_list, unscaled_hist_list_signal = [], []
        for key in req_hists :
            print('-------------------------------------------------------------------')
            print(f"Key: {key}            Sample:{req_hists[key]['datasets']} ")
            print('-------------------------------------------------------------------')
            if req_hists[key]['type'] == 'Signal':
                print('-->Type: Signal')
                label_signal = key
                datasets_signal = req_hists[key]['datasets']
                color_signal = req_hists[key]['color']
                hists_signal = []
                unscaled_hists_signal = []
                for i in datasets_signal:
                    cutflow_hist = input_dict[i]['cutflow'][sel]['Cutflow']
                    cut_labels = input_dict[i]['cutflow'][sel]['Labels']
                    cutflow_values = cutflow_hist.values()
                    Raw_Events_signal = cutflow_values[0]
                    print(f'-->RawEvents for {i}: {Raw_Events_signal}')
                    xsec_scale_factor = get_xsec_scale(i, Raw_Events_signal, config.intLumi)
                    print(f'-->xsec_scale for {i} = {xsec_scale_factor}')
                    Hist_signal = input_dict[i]['histograms'][sel]
                    scaled_hist_signal = { name: xsec_scale_factor*hist for name, hist in Hist_signal.items()}
                    scaled_hist_signal['Cutflow'] = xsec_scale_factor*cutflow_hist
                    hists_signal.append(scaled_hist_signal)
                    unscaled_hist = copy.deepcopy(Hist_signal)
                    unscaled_hist['Cutflow'] = cutflow_hist
                    unscaled_hists_signal.append(unscaled_hist)
                label_list_signal.append(label_signal)
                dataset_list_signal.append(datasets_signal)
                color_list_signal.append(color_signal)
                hist_list_signal.append(accumulate(hists_signal))
                unscaled_hist_list_signal.append(accumulate(unscaled_hists_signal))

            elif req_hists[key]['type'] == 'Background':
                print('-->Type: Background')
                label = key
                datasets = req_hists[key]['datasets']
                color = req_hists[key]['color']
                hists = []
                unscaled_hists = []
                for i in datasets:
                    cutflow_hist = input_dict[i]['cutflow'][sel]['Cutflow']
                    cut_labels = input_dict[i]['cutflow'][sel]['Labels']
                    cutflow_values = cutflow_hist.values()
                    Raw_Events = cutflow_values[0]
                    print(f'-->RawEvents for {i}: {Raw_Events}')
                    xsec_scale_factor = get_xsec_scale(i, Raw_Events, config.intLumi)
                    print(f'-->xsec_scale for {i} = {xsec_scale_factor}')
                    Hist = input_dict[i]['histograms'][sel]
                    scaled_hist = { name: xsec_scale_factor*hist for name, hist in Hist.items()}
                    scaled_hist['Cutflow'] = xsec_scale_factor*cutflow_hist
                    hists.append(scaled_hist)
                    unscaled_hist = copy.deepcopy(Hist)
                    unscaled_hist['Cutflow'] = cutflow_hist
                    unscaled_hists.append(unscaled_hist)
                label_list.append(label)
                dataset_list.append(datasets)
                color_list.append(color)
                hist_list.append(accumulate(hists))
                unscaled_hist_list.append(accumulate(unscaled_hists))
            else:
                raise TypeError('Unrecognised type in req_hists')


        # Make Cut table
        print('---------------------------------------------------------------')
        print('Cuts Table : Info about the cuts')
        print('---------------------------------------------------------------')
        cuts_table(
            name='Cuts_table',
            title=f'{sel} cuts',
            labels=cut_labels,
            formats=formats,
            path=plot_path_selection
        )
        print('---------------------------------------------------------------')


        #Make Yield Plots
        print('---------------------------------------------------------------')
        print('Yield : Unscaled  and Scaled')
        print('---------------------------------------------------------------')
        yield_plot(
            name='Yield',
            title=f'{sel} Yield',
            keys=req_hists.keys(),
            scaled=hist_list_signal+hist_list,
            unscaled=unscaled_hist_list_signal+unscaled_hist_list,
            formats=formats,
            path=plot_path_selection,
            plot_width=12
        )
        print('---------------------------------------------------------------')

        # Add cutflow to plot_props
        xticks = np.arange(len(cutflow_values))
        plotprops = plotprops.assign(Cutflow = ['Cutflow',sel+' Cutflow','Cut Order','Events',len(xticks)+1,xticks[0],xticks[-1]])

        # Start plotting
        for hist_name in req_plots+['Cutflow']:
            hist = [hists[hist_name] for hists in hist_list]
            n_bkgs = len(hist)
            hist_signal = [hists[hist_name] for hists in hist_list_signal]
            n_sig = len(hist_signal)
            cutflow_mode=False
            if hist_name =='Cutflow':
                cutflow_mode=True

            print(hist_name, ' : ', plotprops[hist_name].title)
            print('---------------------------------------------------------------')
            for log_mode in log :
                for stack_mode in stack:
                    fig, ax = plt.subplots(figsize=(8,8))

                    order = getattr(config, "custom_mc_order", None)
                    if not order is None:
                        ordered_hist, ordered_label_list, ordered_color_list = hist_sorter(order, hist, label_list, color_list)
                    else:
                        ordered_hist, ordered_label_list, ordered_color_list = hist, label_list, color_list

                    #Backgrounds
                    makeplot(
                        fig=fig,
                        ax=ax,
                        hist=ordered_hist,
                        name=plotprops[hist_name].name,
                        title=plotprops[hist_name].title,
                        label=ordered_label_list,
                        xlabel=plotprops[hist_name].xlabel,
                        ylabel=plotprops[hist_name].ylabel,
                        bins=plotprops[hist_name].bins,
                        xmin=plotprops[hist_name].xmin,
                        xmax=plotprops[hist_name].xmax,
                        log=log_mode,
                        stack=True, #Always stack backgrounds
                        color=ordered_color_list,
                        histtype='fill',
                        cutflow_mode=cutflow_mode,
                        xticks=8
                    )
                    #Signal
                    stop_plotting_signal = False
                    if stack_mode and n_bkgs != 0 and n_sig != 0:
                        sigl_hist = [h+sum(hist) for h in hist_signal] #Manual stacking because independent stacking is not supported in mplhep
                    elif n_sig != 0 :
                        sigl_hist = hist_signal
                    else:
                        stop_plotting_signal = True

                    if not stop_plotting_signal:

                        hep.histplot(
                            sigl_hist,
                            color=color_list_signal,
                            label=label_list_signal,
                            histtype='step',
                            stack=False, #overridden by stack_mode bool
                            linewidth=1,
                            ax=ax
                        )
                    fig.legend(prop={"size":10},loc= getattr(config, "legend_location", (0.74,0.74)), reverse=getattr(config, "Reverse_legend_labels", False) )

                    if log_mode :
                        log_mode_text = 'log'
                    else :
                        log_mode_text = 'linear'

                    if stack_mode :
                        stack_mode_text = 'stacked'
                    else :
                        stack_mode_text = 'unstacked'
                    for format in formats :
                        filename = plotprops[hist_name].name+'_'+log_mode_text+'_'+stack_mode_text+'.'+format
                        full_name = plot_path_selection+filename
                        fig.savefig(full_name,dpi=240);
                        print(filename, " saved at ", plot_path_selection)
                    plt.close()
            print('-------------------------------------------------------------------')
        print('_____________________________________________________________________\n')

def makeplot(fig, ax, hist, name, title, label, xlabel, ylabel, bins, xmin, xmax, log, stack, color, histtype, xticks=10, cutflow_mode=False):
    '''
    Makes a single kinematic plot on an ax object
    '''
    # plt.ylim(1,1000000)
    if len(hist) != 0 :
        hep.histplot(
            hist,
            yerr=0,
            histtype=histtype,
            label=label,
            color=color,
            alpha=0.8,
            stack=stack,
            edgecolor='black',
            linewidth=1,
            # sort='label',
            ax=ax
        )

    ax.text(*getattr(config, "FCC_text_location", (0.27, 1.02,)), 'FCC Analyses: FCC-ee Simulation (Delphes)', fontsize=9, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    ax.text(*getattr(config, "sqrt_s_text_location", (0.92, 1.02)), f'$\\sqrt{{s}} = {config.energy} GeV$', fontsize=9, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

    if  cutflow_mode:
        ax.set_ylabel(ylabel)
    else:
        per_bin = '/'+str((xmax-xmin)/bins)
        ax.set_ylabel(ylabel+per_bin+' [GeV]')
        plt.xlim([xmin,xmax])
        plt.xticks(np.linspace(xmin,xmax,xticks+1))
        ax.xaxis.set_minor_locator(AutoMinorLocator(5))
    ax.set_xlabel(xlabel)

    if log :
        ax.set_yscale('log')
        plt.tick_params(axis='y', which='minor')
    else:
        ax.yaxis.set_minor_locator(AutoMinorLocator(5))

    ax.set_title(title,pad=25,  fontsize= "15", color="#192655")


###################
# Input arguments #
###################
parser = argparse.ArgumentParser()
parser.add_argument(
    "-i",
    "--input",
    help="Enter the input directory where the coffea files are saved",
    default=config.input_path,
    type=str
)
inputs = parser.parse_args()


#########################
# Load the coffea files #
#########################
#Input configuration
input_path = inputs.input+"/"
base_filename = config.output_filename+".coffea"
print(f'Current configuration:\n\tinput_path:\t{input_path}\n\tbase_filename:\t{base_filename}\n')
print("Loading coffea files...")

#Find coffea files
coffea_files = glob.glob(input_path+'*.coffea')
print('Detected coffea files:')
for file in coffea_files : print('\t'+file)
print(f'Choosing:\n\t{base_filename}')

#Find chunked coffea files and combine them
chunked_coffea_files = glob.glob(input_path+base_filename.strip('.coffea')+'-chunk*.coffea')
if len(chunked_coffea_files) != 0 :
    print('Joining chunks:')
    chunk_index_list = []
    chunk_list = []
    for file in chunked_coffea_files:
        print('\t'+file)
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
    input = accumulate(input_list)

#If there is only one chunk no need to join chunks
else :
    input = load(input_path+base_filename)


#######################
# Plot the histograms #
#######################
print("Plotting...")
if not os.path.exists(config.plot_path):
    os.makedirs(config.plot_path)

generate_plots(input, config.req_hists, config.req_plots, config.selections, config.stack, config.log, config.formats, config.plot_path, plot_props)
