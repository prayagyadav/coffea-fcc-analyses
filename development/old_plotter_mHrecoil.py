import mplhep as hep, pandas as pd, numpy as np, matplotlib.pyplot as plt
import  collections, argparse, hist, copy, glob, os, re
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from coffea.analysis_tools import Cutflow
from coffea.util import load
from pandas.core.indexes.base import Level
from processor_mHrecoil import plot_props

##################################
# Definition of useful functions #
##################################

def lazy_summary(d,ntabs=1):
    '''
    Visualises a dictionary lazily:
        Gets integral of any hist.Hist object
        Gets initial value of any coffea.analysis_tools.Cutflow objects
        Gets type of of any other object
    Returns a print-ready string
    '''
    tab = '\t'*ntabs
    print_string ='{\n'
    for key,value in d.items():
        print_string += f"{tab}{key} : "
        if isinstance(value,dict):
            print_string += lazy_summary(value, ntabs=ntabs+1)
        elif isinstance(value, hist.hist.Hist):
            print_string += f"{type(value)}\tIntegral:{value.sum()}\n"
        elif isinstance(value, Cutflow):
            print_string += f"{type(value)}\tInitial events:{value.result().nevcutflow[0]}\n"
        else :
            print_string += f"{type(value)}\n"
    print_string += tab+'}\n'
    return print_string

def get_subdict(dicts, key):
    '''
    Get list of subdictionaries(if available) from a list of dictionaries
    '''
    out = []
    for d in dicts:
        for k in d.keys():
            if key == k:
                out.append(d[key])
    return out

def accumulate(dicts):
    """
    Merges an array of dictionaries and adds up the values of common keys.

    Parameters:
    dicts (list): A list of dictionaries to be merged.

    Returns:
    dict: A dictionary with combined keys and values summed for common keys.
    """

    outdict = {}

    for diction in dicts:
        dictionary = copy.deepcopy(diction)

        for key, value in dictionary.items():
            # print(f"{key} : {value}")
            # print(type(value))

            if isinstance(value,dict):
                value = accumulate(get_subdict(dicts,key))
                outdict[key] = value
            else:
                if key in outdict.keys():
                    outdict[key] += value  # Add values if the key is common
                else:
                    outdict[key] = value  # Otherwise, add the new key-value pair

    return outdict

def get_xsec_scale(dataset, raw_events, Luminosity):
    xsec = cross_sections[dataset] #in per picobarn
    if raw_events > 0:
        sf = (xsec*Luminosity)/raw_events
    else :
        raise ValueError('Raw events less than of equal to zero!')
    return sf

def add_cutflow(c1,c2):
    '''
    Add cutflow objects assuming they operate on non-overlaping sample regions
    '''
    r1 = c1.result()
    r2 = c2.result()


    if r1.labels == r2.labels :
        names = r1.labels
        names.remove('initial') # initial is added when Cutflow class is called, so removing it to preserve names list length
        names = names
        nevonecut = [a+b for a,b in zip(r1.nevonecut,r2.nevonecut)]
        nevcutflow = [a+b for a,b in zip(r1.nevcutflow,r2.nevcutflow)]
        masksonecut = [np.concatenate((a,b)) for a,b in zip(r1.masksonecut,r2.masksonecut)]
        maskscutflow = [np.concatenate((a,b)) for a,b in zip(r1.maskscutflow,r2.maskscutflow)]

    else:
        raise KeyError("The labels of the cutflow do not match!")
    return Cutflow(names, nevonecut, nevcutflow, masksonecut, maskscutflow, delayed_mode=False)

Cutflow.__add__ = add_cutflow #Monkey patch Cutflow class to enable the add method

def get_cutflow_props(object_list, **kwargs):
    '''
    Takes in a list of cutflow objects and returns the sum of their component arrays after scaling them
    '''
    if 'scale' in kwargs:
        scale = kwargs['scale'] #scale should be a list of scale factors corresponding to the objects
    else :
        scale =  np.ones(len(object_list))

    onecut_list = []
    cutflow_list = []
    labels_list = object_list[0].result().labels
    nevonecut_list = []
    nevcutflow_list = []
    for object, sf in zip(object_list, scale):
        res = object.result()
        if res.labels == labels_list :
            nevonecut_list.append(sf*np.array(res.nevonecut))
            nevcutflow_list.append(sf*np.array(res.nevcutflow))
            onecut_hist, cutflow_hist,l = object.yieldhist()
            onecut_list.append(sf*onecut_hist)
            cutflow_list.append(sf*cutflow_hist)
        else :
            raise ValueError("The labels of cutflow objects do not match.")
    nevonecut = sum(nevonecut_list)
    nevcutflow = sum(nevcutflow_list)
    onecut = sum(onecut_list)
    cutflow = sum(cutflow_list)
    c = collections.namedtuple('Cutflow',['labels','onecut','nevonecut','cutflow','nevcutflow'])
    return c(labels_list, onecut, nevonecut, cutflow, nevcutflow)

def yield_plot(name, title, keys, cutflow_obs, unscaled_cutflow_obs, formats, path):
    '''
    Create yield plots
    '''

    fig, ax = plt.subplots(figsize=(8,8))
    ax.text(0.25, 1.02, 'FCC Analyses: FCC Simulation Delphes', fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    ax.text(0.92, 1.02, '$\\sqrt{s} = '+str(energy)+' GeV$', fontsize=10, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    ax.text(0.10, 0.95, collider, fontsize=14, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
    ax.text(0.10, 0.88,'Delphes Version: '+delphesVersion, fontsize=14, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
    ax.text(0.10, 0.81, 'Signal : $'+ana_tex+'$', fontsize=14, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
    ax.text(0.10, 0.74, '$L = '+str(intLumi/1e6)+' ab^{-1}$', fontsize=14, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)

    level, linespacing = 0.60, 0.05
    for scale,obs in zip(['UNSCALED','SCALED'],[unscaled_cutflow_obs,cutflow_obs]):
        ax.text(0.02, level, scale, weight='bold', fontsize=13, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        level -= linespacing
        ax.text(0.02, level, 'Sample', weight='bold', fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        ax.text(0.30, level, 'Type', weight='bold', fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        ax.text(0.49, level, 'Raw', weight='bold', fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        ax.text(0.68, level, 'Yield', weight='bold', fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        ax.text(0.87, level, 'Yield %', weight='bold', fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        for i in range(len(keys)):
            datasets = req_hists[list(keys)[i]]['datasets']
            Type = req_hists[list(keys)[i]]['type']
            color = req_hists[list(keys)[i]]['color']
            yield_text = str(round(obs[i].nevcutflow[-1],2))
            raw_text = str(round(obs[i].nevcutflow[0],2))
            percentage = str(round(obs[i].nevcutflow[-1]*100/obs[i].nevcutflow[0],2))
            level -= linespacing
            ax.text(0.02, level, datasets, fontsize=10, color=color,horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
            ax.text(0.30, level, Type, color=color,fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
            ax.text(0.49, level, raw_text, color=color, fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
            ax.text(0.68, level, yield_text, color=color, fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
            ax.text(0.87, level, percentage, color=color, fontsize=12, horizontalalignment='left', verticalalignment='center', transform=ax.transAxes)
        level -= 2*linespacing

    ax.set_title(title,pad=25,  fontsize= "15", color="#192655")
    for format in formats :
        filename = name+'.'+format
        full_name = path+filename
        fig.savefig(full_name,dpi=240);
        print(filename, " saved at ", path)
    plt.close()

def cutflow(input_dict, req_hists, selections, stack, log, formats, path):
    '''
    Create cutflow and yield plots
    '''
    print('___________________________________________________________________')
    print('_____________________________Cutflows______________________________')
    for sel in selections:
        print('___________________________________________________________________')
        print('------------------------','Selection:', sel ,'--------------------------')

        cutflow_by_key = []
        # To create the yield summary
        for key in req_hists.keys():
            datasets = req_hists[key]['datasets']
            cutflow_object_list = []
            xsec_scale = []
            print('-------------------------------------------------------------------')
            print(f"Key: {key}            Sample:{datasets} ")
            print('-------------------------------------------------------------------')
            for i in datasets:
                object = input_dict[i]['cutflow'][sel]
                cutflow_object_list.append(object)
                object.print()
                Raw_Events = object.result().nevcutflow[0]
                xsec_scale.append(get_xsec_scale(i, Raw_Events, intLumi))
            unscaled_cutflow = get_cutflow_props(cutflow_object_list)
            cutflow = get_cutflow_props(cutflow_object_list, scale=xsec_scale)
            cutflow_by_key.append(cutflow)
            print('xsec_scale = ',xsec_scale)

        hists = [cutflow_object.cutflow for cutflow_object in cutflow_by_key]
        ncuts = len(cutflow_by_key[0].labels)
        xticks = np.arange(ncuts)
        color_list = [req_hists[key]['color'] for key in req_hists.keys()]
        plot_path_selection = path+sel+'/'
        if not os.path.exists(plot_path_selection):
            os.makedirs(plot_path_selection)

        #To create the cutflow plots
        print('-------------------------------------------------------------------')
        for log_mode in log:
            for stack_mode in stack:
                name = 'Cutflow'
                fig, ax = plt.subplots(figsize=(8,8))
                makeplot(
                    fig=fig,
                    ax=ax,
                    hist=hists,
                    name=name,
                    title=sel+' Cutflow',
                    label=req_hists.keys(),
                    xlabel='Cut Order',
                    ylabel='Events',
                    bins=len(xticks)+1,
                    xmin=xticks[0],
                    xmax=xticks[-1],
                    log=log_mode,
                    stack=stack_mode,
                    color=color_list,
                    histtype='fill',
                    cutflow_mode=True
                )
                if log_mode :
                    log_mode_text = 'log'
                else :
                    log_mode_text = 'linear'

                if stack_mode :
                    stack_mode_text = 'stacked'
                else :
                    stack_mode_text = 'unstacked'
                for format in formats :
                    filename = name+'_'+log_mode_text+'_'+stack_mode_text+'.'+format
                    full_name = plot_path_selection+filename
                    fig.savefig(full_name,dpi=240);
                    print(filename, " saved at ", plot_path_selection)
                plt.close()

        yield_plot(
            name='Yield',
            title=f'{sel} Yield',
            keys=req_hists.keys(),
            cutflow_obs=cutflow_by_key,
            # rawstats= raw_nev,
            formats=formats,
            path=plot_path_selection
        )
        print('-------------------------------------------------------------------')
        print('_____________________________________________________________________\n')

def plots(input_dict, req_hists, req_plots, selections, stack, log, formats, path):
    '''
    Batch plot processor
    '''
    for sel in selections:
        print('_________________________________________________________________')
        print('---------------------','Selection:', sel ,'---------------------')

        #Get hist array for different backgrounds
        label_list, label_list_signal = [], []
        dataset_list, dataset_list_signal = [], []
        color_list,color_list_signal = [], []
        hist_list, hist_list_signal = [], []
        for key in req_hists :
            if req_hists[key]['type'] == 'Signal':
                label_signal = key
                datasets_signal = req_hists[key]['datasets']
                color_signal = req_hists[key]['color']
                hists_signal = []
                for i in datasets_signal:
                    object_signal = input_dict[i]['cutflow'][sel]
                    Raw_Events_signal = object_signal.result().nevcutflow[0]
                    xsec_scale_signal = get_xsec_scale(i, Raw_Events_signal, intLumi)
                    hist_signal = input_dict[i]['histograms'][sel]
                    scaled_hist_signal = { name: xsec_scale_signal*hist for name, hist in hist_signal.items()}
                    hists_signal.append(scaled_hist_signal)
                label_list_signal.append(label_signal)
                dataset_list_signal.append(datasets_signal)
                color_list_signal.append(color_signal)
                hist_list_signal.append(accumulate(hists_signal))
            elif req_hists[key]['type'] == 'Background':
                label = key
                datasets = req_hists[key]['datasets']
                color = req_hists[key]['color']
                hists = []
                for i in datasets:
                    object = input_dict[i]['cutflow'][sel]
                    Raw_Events = object.result().nevcutflow[0]
                    xsec_scale = get_xsec_scale(i, Raw_Events, intLumi)
                    hist = input_dict[i]['histograms'][sel]
                    scaled_hist = { name: xsec_scale*hist for name, hist in hist.items()}
                    hists.append(scaled_hist)
                label_list.append(label)
                dataset_list.append(datasets)
                color_list.append(color)
                hist_list.append(accumulate(hists))
            else:
                raise TypeError('Unrecognised type in req_hists')

        plot_path_selection = path+sel+'/'
        if not os.path.exists(plot_path_selection):
            os.makedirs(plot_path_selection)

        for hist_name in req_plots:
            hist = [hists[hist_name] for hists in hist_list]
            hist_signal = [hists[hist_name] for hists in hist_list_signal]

            print(hist_name, ' : ', plot_props[hist_name].title)
            print('---------------------------------------------------------------')
            for log_mode in log :
                for stack_mode in stack:
                    fig, ax = plt.subplots(figsize=(8,8))
                    #Backgrounds
                    makeplot(
                        fig=fig,
                        ax=ax,
                        hist=hist,
                        name=plot_props[hist_name].name,
                        title=plot_props[hist_name].title,
                        label=label_list,
                        xlabel=plot_props[hist_name].xlabel,
                        ylabel=plot_props[hist_name].ylabel,
                        bins=plot_props[hist_name].bins,
                        xmin=plot_props[hist_name].xmin,
                        xmax=plot_props[hist_name].xmax,
                        log=log_mode,
                        stack=True, #Always stack backgrounds
                        color=color_list,
                        histtype='fill',
                    )
                    #Signal
                    if stack_mode :
                        sigl_hist = sum(hist_signal)+sum(hist) #Manual stacking because independent stacking is not supported in mplhep
                    else :
                        sigl_hist = hist_signal

                    hep.histplot(
                        sigl_hist,
                        color=color_list_signal,
                        label=label_list_signal,
                        histtype='step',
                        stack=False, #overridden by stack_mode bool
                        linewidth=1,
                        ax=ax
                    )
                    fig.legend(prop={"size":10},loc= (0.74,0.74) )
                    if log_mode :
                        log_mode_text = 'log'
                    else :
                        log_mode_text = 'linear'

                    if stack_mode :
                        stack_mode_text = 'stacked'
                    else :
                        stack_mode_text = 'unstacked'
                    for format in formats :
                        filename = plot_props[hist_name].name+'_'+log_mode_text+'_'+stack_mode_text+'.'+format
                        full_name = plot_path_selection+filename
                        fig.savefig(full_name,dpi=240);
                        print(filename, " saved at ", plot_path_selection)
                    plt.close()
            print('-------------------------------------------------------------------')
        print('_____________________________________________________________________\n')

def plots2(input_dict, req_hists, req_plots, selections, stack, log, formats, path, plotprops):
    '''
    Batch plot processor
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
        cutflow_by_key, cutflow_by_key_signal = [], []
        unscaled_cutflow_by_key, unscaled_cutflow_by_key_signal = [], []
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
                cutflow_object_list_signal = []
                xsec_scale_signal = []
                for i in datasets_signal:
                    object_signal = input_dict[i]['cutflow'][sel]
                    cutflow_object_list_signal.append(object_signal)
                    object_signal.print()
                    onecut_hist, cutflow_hist,l = object_signal.yieldhist()
                    Raw_Events_signal = object_signal.result().nevcutflow[0]
                    xsec_scale_factor = get_xsec_scale(i, Raw_Events_signal, intLumi)
                    xsec_scale_signal.append(xsec_scale_factor)
                    Hist_signal = input_dict[i]['histograms'][sel]
                    scaled_hist_signal = { name: xsec_scale_factor*hist for name, hist in Hist_signal.items()}
                    scaled_hist_signal['Cutflow'] = xsec_scale_factor*cutflow_hist
                    hists_signal.append(scaled_hist_signal)
                unscaled_cutflow_by_key_signal.append(get_cutflow_props(cutflow_object_list_signal))
                cutflow_by_key_signal.append(get_cutflow_props(cutflow_object_list_signal, scale=xsec_scale_signal))
                print('-->xsec_scale = ',xsec_scale_signal)
                label_list_signal.append(label_signal)
                dataset_list_signal.append(datasets_signal)
                color_list_signal.append(color_signal)
                hist_list_signal.append(accumulate(hists_signal))

            elif req_hists[key]['type'] == 'Background':
                print('-->Type: Background')
                label = key
                datasets = req_hists[key]['datasets']
                color = req_hists[key]['color']
                hists = []
                cutflow_object_list = []
                xsec_scale = []
                for i in datasets:
                    object = input_dict[i]['cutflow'][sel]
                    cutflow_object_list.append(object)
                    object.print()
                    onecut_hist, cutflow_hist,l = object.yieldhist()
                    Raw_Events = object.result().nevcutflow[0]
                    xsec_scale_factor = get_xsec_scale(i, Raw_Events, intLumi)
                    xsec_scale.append(xsec_scale_factor)
                    Hist = input_dict[i]['histograms'][sel]
                    scaled_hist = { name: xsec_scale_factor*hist for name, hist in Hist.items()}
                    scaled_hist['Cutflow'] = xsec_scale_factor*cutflow_hist
                    hists.append(scaled_hist)
                unscaled_cutflow_by_key.append(get_cutflow_props(cutflow_object_list))
                cutflow_by_key.append(get_cutflow_props(cutflow_object_list, scale=xsec_scale))
                print('-->xsec_scale = ',xsec_scale)
                label_list.append(label)
                dataset_list.append(datasets)
                color_list.append(color)
                hist_list.append(accumulate(hists))
            else:
                raise TypeError('Unrecognised type in req_hists')

        #Make Yield Plots
        print('---------------------------------------------------------------')
        print('Yield : Unscaled  and Scaled')
        print('---------------------------------------------------------------')
        yield_plot(
            name='Yield',
            title=f'{sel} Yield',
            keys=req_hists.keys(),
            cutflow_obs=cutflow_by_key_signal+cutflow_by_key,
            unscaled_cutflow_obs=unscaled_cutflow_by_key_signal+unscaled_cutflow_by_key,
            formats=formats,
            path=plot_path_selection
        )
        print('---------------------------------------------------------------')

        # Add cutflow to plot_props
        xticks = np.arange(len(l))
        plotprops = plotprops.assign(Cutflow = ['Cutflow',sel+' Cutflow','Cut Order','Events',len(xticks)+1,xticks[0],xticks[-1]])

        # Start plotting
        for hist_name in req_plots+['Cutflow']:
            hist = [hists[hist_name] for hists in hist_list]
            hist_signal = [hists[hist_name] for hists in hist_list_signal]
            cutflow_mode=False
            if hist_name =='Cutflow':
                cutflow_mode=True

            print(hist_name, ' : ', plotprops[hist_name].title)
            print('---------------------------------------------------------------')
            for log_mode in log :
                for stack_mode in stack:
                    fig, ax = plt.subplots(figsize=(8,8))
                    #Backgrounds
                    makeplot(
                        fig=fig,
                        ax=ax,
                        hist=hist,
                        name=plotprops[hist_name].name,
                        title=plotprops[hist_name].title,
                        label=label_list,
                        xlabel=plotprops[hist_name].xlabel,
                        ylabel=plotprops[hist_name].ylabel,
                        bins=plotprops[hist_name].bins,
                        xmin=plotprops[hist_name].xmin,
                        xmax=plotprops[hist_name].xmax,
                        log=log_mode,
                        stack=True, #Always stack backgrounds
                        color=color_list,
                        histtype='fill',
                        cutflow_mode=cutflow_mode
                    )
                    #Signal
                    if stack_mode :
                        sigl_hist = sum(hist_signal)+sum(hist) #Manual stacking because independent stacking is not supported in mplhep
                    else :
                        sigl_hist = hist_signal

                    hep.histplot(
                        sigl_hist,
                        color=color_list_signal,
                        label=label_list_signal,
                        histtype='step',
                        stack=False, #overridden by stack_mode bool
                        linewidth=1,
                        ax=ax
                    )
                    fig.legend(prop={"size":10},loc= (0.74,0.74) )
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
        sort='yield',
        ax=ax
    )

    ax.text(0.27, 1.02, 'FCC Analyses: FCC-ee Simulation (Delphes)', fontsize=9, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    ax.text(0.92, 1.02, '$\\sqrt{s} = 240GeV$', fontsize=9, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)

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
    default="outputs/FCCee/higgs/mH-recoil/mumu",
    type=str
)
inputs = parser.parse_args()


##################################
# Choose the required plots here #
##################################
selections = ['sel0','sel1']
stack = [True, False]
log = [True, False]
formats = ['png','pdf']
req_plots = ['Zm', 'Zm_zoom', 'Recoilm', 'Recoilm_zoom', 'Recoilm_zoom1']
req_hists = {
    "ZH":{"type":'Signal',"datasets":['p8_ee_ZH_ecm240'],"color":'r'},
    "ZZ":{"type":'Background',"datasets":['p8_ee_ZZ_ecm240'],"color":'g'},
    "WW":{"type":'Background',"datasets":['p8_ee_WW_ecm240'],"color":'b'}
}
cross_sections = {#in pb-1 # Taken as is from FCC events catalogue at https://fcc-physics-events.web.cern.ch/FCCee/spring2021/Delphesevents_IDEA.php
    'p8_ee_WW_ecm240': 16.4385,
    'p8_ee_ZZ_ecm240': 1.35899,
    'p8_ee_ZH_ecm240': 0.201868
}
plot_path = 'outputs/FCCee/higgs/mH-recoil/mumu/plots/'
intLumi        = 5.0e+06 #in pb-1
ana_tex        = 'e^{+}e^{-} \\rightarrow ZH \\rightarrow \\mu^{+}\\mu^{-} + X'
delphesVersion = '3.4.2'
energy         = 240.0 #in GeV
collider       = 'FCC-ee'


#########################
# Load the coffea files #
#########################
#Input configuration
input_path = inputs.input+"/"
base_filename = "mHrecoil_mumu.coffea"
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
if not os.path.exists(plot_path):
    os.makedirs(plot_path)
#cutflow(input, req_hists, selections, stack, log, formats, plot_path)
plots2(input, req_hists, req_plots, selections, stack, log, formats, plot_path,plot_props)