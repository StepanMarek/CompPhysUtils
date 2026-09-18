import matplotlib.pyplot as plt
from .. import __user_conf_dir
from ..parser import parseDatasetConfig
from ..parser import save, writeFile
from ..util import dynmod, ColorIterator, CyclicIterator, LinestyleIterator, MarkerstyleIterator
import configparser
from ..parser.combine import runGroupData
from ..fitting.fitter import from_config as fit_from_config 
from .transformer import transforms,transformModules
from .decorator import decorations,decorationModules
import importlib
import os

# Search for backend types
backendModules = dynmod([os.path.dirname(__file__)+"/backends"], [".py"])
backends = {}

# Names of the backends preferred for given extension
# TODO : Allow user to overwrite this or not?
preferred_backends = {
    ".png" : "matplotlib",
    ".pdf" : "matplotlib",
    ".svg" : "matplotlib",
    ".pgf" : "pgfplots",
    ".tex" : "pgfplots"
}

# Search for default plot types
plotModules = dynmod([os.path.dirname(__file__)+"/plot_types", __user_conf_dir+"/plot_types"], [".py"])
plotTypes = {}

def plot(datasets, plotType="scatter", axes=False, figure=False, **plotOptions):
    if not figure:
        figure = backends[plotOptions["backend"]].Figure()
    if not axes:
        axes = backends[plotOptions["backend"]].Axes(figure)
    if plotType in plotTypes:
        axes = plotTypes[plotType](datasets, axes, figure=figure, **plotOptions)
    elif plotType in plotModules:
        # Module is present but probably not loaded
        plotModules[plotType]["spec"].loader.exec_module(plotModules[plotType]["module"])
        plotModules[plotType]["loaded"] = True
        plotTypes[plotType] = plotModules[plotType]["module"].plot
        axes = plotTypes[plotType](datasets, axes, figure=figure, **plotOptions)
    else:
        # Defaults to scatter
        axes = plotTypes["scatter"](datasets, axes, **plotOptions)
    # Axes specific options
    axes.labels[0] = plotOptions["xlabel"]
    axes.labels[1] = plotOptions["ylabel"]
    if plotOptions["xlim"]:
        axes.xlim = plotOptions["xlim"]
    if plotOptions["ylim"]:
        axes.ylim = plotOptions["ylim"]
    # Insert tick labels
    if plotOptions["xticks"]:
        axes.xticks = plotOptions["xticks"][0]
        axes.xtick_labels = plotOptions["xticks"][1]
    if plotOptions["yticks"]:
        axes.yticks = plotOptions["yticks"][0]
        axes.ytick_labels = plotOptions["yticks"][1]
    # If requested, move ticks to top
    axes.xticks_swap = plotOptions["xticks-swap"]
    axes.yticks_swap = plotOptions["yticks-swap"]
    if plotOptions["xticks-rotate"]:
        axes.xticks_rotate = plotOptions["xticks-rotate"]
    if plotOptions["yticks-rotate"]:
        axes.yticks_rotate = plotOptions["yticks-rotate"]
    # TODO : Is it worth allowing for differing axes and figure dimensions?
    if plotOptions["fig-width"]:
        figure.width = plotOptions["fig-width"]
    if plotOptions["fig-width"]:
        figure.height = plotOptions["fig-height"]
    if plotOptions["axes-width"]:
        axes.width = plotOptions["axes-width"]
    if plotOptions["axes-width"]:
        axes.height = plotOptions["axes-height"]
    if plotOptions["axes-linewidth"]:
        axes.axes_linewidth = plotOptions["axes-linewidth"]
    # Legend
    if "legend" in plotOptions:
        axes.legend = plotOptions["legend"]
    return axes, figure

def fromConfig(configFileName, axes=False, figure=False, backend=False, datasets={}):
    axesGiven = False
    if axes:
        axesGiven = True
    cfg = configparser.ConfigParser()
    cfg.read(configFileName)
    # Run processing up to combine_commands
    datasets.update(runGroupData(cfg, datasets, configFileName))
    # Now, run any transform commands
    if "transform" in cfg["plot"]:
        transformCommands = cfg["plot"].get("transform").split("\n")
        for commandLine in transformCommands:
            commandSplitLine = commandLine.split()
            commandName = commandSplitLine[0]
            if not commandName in transformModules:
                raise ModuleNotFoundError("Transform module "+commandName+" not found in the search tree!")
            if not commandName in transforms:
                # Load
                transformModules[commandName]["spec"].loader.exec_module(transformModules[commandName]["module"])
                transforms[commandName] = transformModules[commandName]["module"].command
                transformModules[commandName]["loaded"] = True
            datasets = transforms[commandName](datasets, commandSplitLine[1:])
    if "savepoint" in cfg["plot"]:
        save(cfg["plot"].get("savepoint"), "transform", datasets)
    # Now, datasets are complete, and we can read the plot group
    # Start by processing all options/settings, which do not require us to have a specific backend setup
    # Also include options that are set directly via type - should be reserved for options that are not usable for many plot types
    graphTypeSplit = cfg["plot"].get("type", "scatter").split()
    graphType = graphTypeSplit[0]
    colCoords = cfg["plot"].get("cols", False)
    if colCoords:
        colCoords = colCoords.split("\n")
    else:
        colCoords = []
    for i in range(len(colCoords)):
        colCoords[i] = colCoords[i].split()
    chosenDatasets = []
    for i in range(len(colCoords)):
        chosenDatasets.append([])
        for j in range(0,len(colCoords[i]),2):
            try:
                chosenDatasets[i].append(datasets[colCoords[i][j]][int(colCoords[i][j+1])])
            except IndexError:
                raise IndexError("Cannot create plot for coordinates "+colCoords[i][j]+" "+colCoords[i][j+1])
    plotOptions = {}
    plotOptions["plotArgString"] = graphTypeSplit[1:]
    plotOptions["legend"] = cfg["plot"].getboolean("legend", True)
    plotOptions["legend-pos"] = cfg["plot"].get("legend-pos", "upper right")
    plotOptions["legend-cols"] = cfg["plot"].getint("legend-cols", 1)
    if "xlim" in cfg["plot"]:
        plotOptions["xlim"] = list(map(float, cfg["plot"].get("xlim").split()))
    else:
        plotOptions["xlim"] = False
    if "ylim" in cfg["plot"]:
        plotOptions["ylim"] = list(map(float, cfg["plot"].get("ylim").split()))
    else:
        plotOptions["ylim"] = False
    # TODO : This is somewhat backend dependent - allow to be set in figure?
    # if "font" in cfg["plot"]:
    #     plt.rcParams["font.family"] = cfg["plot"].get("font", "sans")
    # if "font-size" in cfg["plot"]:
    #     plt.rcParams["font.size"] = int(cfg["plot"].get("font-size", 12))
    # if "mathfont" in cfg["plot"]:
    #     plt.rcParams["mathtext.fontset"] = cfg["plot"].get("mathfont", "cm")
    # Figure width - for pgfplots set via axis width
    # Units are cm
    # Default aspect ratio is 4/3
    plotOptions["fig-width"] = cfg["plot"].getfloat("fig-width", 16)
    plotOptions["fig-height"] = cfg["plot"].getfloat("fig-height", 12)
    if not axesGiven:
        # TODO : Should the axis settings be available on a per-axis basis? And exposed to user?
        plotOptions["axes-width"] = plotOptions["fig-width"]
        plotOptions["axes-height"] = plotOptions["fig-height"]
    else:
        plotOptions["axes-width"] = False
        plotOptions["axes-height"] = False
    plotOptions["colorCycle"] = cfg["plot"].get("colorCycle", "red green blue cyan magenta yellow black")
    plotOptions["colorCycle"] = ColorIterator(plotOptions["colorCycle"])
    plotOptions["linestyleCycle"] = cfg["plot"].get("linestyleCycle", "solid")
    plotOptions["linestyleCycle"] = LinestyleIterator(plotOptions["linestyleCycle"])
    plotOptions["markerstyleCycle"] = cfg["plot"].get("markerstyleCycle", "x")
    plotOptions["markerstyleCycle"] = LinestyleIterator(plotOptions["markerstyleCycle"])
    plotOptions["xlabel"] = cfg["plot"].get("xlabel", None)
    plotOptions["ylabel"] = cfg["plot"].get("ylabel", None)
    plotOptions["axes-linewidth"] = cfg["plot"].get("axes-linewidth", 1);
    plotOptions["figfile"] = cfg["plot"].get("figfile", False)
    # Dataset labels
    plotOptions["datasetLabels"] = cfg["plot"].get("labels", False)
    if plotOptions["datasetLabels"]:
        plotOptions["datasetLabels"] = plotOptions["datasetLabels"].split("\n")
        if len(plotOptions["datasetLabels"]) < len(colCoords):
            toAdd = len(colCoords) - len(plotOptions["datasetLabels"])
            for i in range(toAdd):
                plotOptions["datasetLabels"].append(None)
    # Arguments supplied are the dataset name, convert it to a dataset that is then plotted
    for ticksName in ["xticks", "yticks"]:
        plotOptions[ticksName] = cfg["plot"].get(ticksName, False)
        if plotOptions[ticksName] and (not cfg["plot"].getboolean("hide-"+ticksName, False)):
            plotOptions[ticksName] = datasets[plotOptions[ticksName]]
        elif cfg["plot"].getboolean("hide-"+ticksName, False):
            plotOptions[ticksName] = [[],[]]
        plotOptions[ticksName+"-rotate"] = cfg["plot"].getfloat(ticksName+"-rotate", 0.0)
        # TODO : Implement for pgfplots
        # Line width and length
        plotOptions[ticksName+"-length"] = cfg["plot"].getfloat(ticksName+"-length", 5.0)
        plotOptions[ticksName+"-width"] = cfg["plot"].getfloat(ticksName+"-width", 1.0)
        plotOptions[ticksName+"-direction"] = cfg["plot"].get(ticksName+"-direction", "out")
        plotOptions[ticksName+"-ratio"] = cfg["plot"].getfloat(ticksName+"-ratio", 0.5)
        # ticks on top/right if requested
        plotOptions[ticksName+"-swap"] = cfg["plot"].getboolean(ticksName+"-swap", False)
    # Fitting : Is this a good place for fitting?
    fit_results = fit_from_config(configFileName, datasets)
    # Prepare decoration commands, but do not execute them yet
    decorationCommands = []
    if cfg["plot"].get("decorate", False):
        decorationCommands = cfg["plot"].get("decorate").split("\n")
        for decorationArgs in decorationCommands:
            decorationSplit = decorationArgs.split()
            if not decorationSplit[0] in decorationModules:
                raise ModuleNotFoundError("Decoration module "+decorationSplit[0]+" not found!")
            if not decorationModules[decorationSplit[0]]["loaded"]:
                decorationModules[decorationSplit[0]]["spec"].loader.exec_module(decorationModules[decorationSplit[0]]["module"])
                decorations[decorationSplit[0]] = decorationModules[decorationSplit[0]]["module"].command
                decorationModules[decorationSplit[0]]["loaded"] = True
    # Check for backend options, with default TODO : matplotlib
    plotOptions["backend"] = cfg["plot"].get("backend", False)
    config_filebase, _ = os.path.splitext(configFileName)
    # If figfile is not specified, choose default filename
    # Since default backend is pgfplots, default filename is *.pgf file
    if not axesGiven:
        fig_filenames = cfg["plot"].get("figfile", f"{config_filebase}.pgf").split()
        if not plotOptions["backend"]:
            # Try to guess the correct backend for each figfile based on preferred extension
            backend_types, backend_figfiles = guess_backends(fig_filenames)
        else:
            # Explicit backend specification means all figfiles with one backend
            # TODO : Alternatively, also allow for per-figure backend specification?
            backend_types = [plotOptions["backend"]]
            backend_figfiles = [fig_filenames]
    else:
        # One given from upper figure
        backend_types = [backend]
        backend_figfiles = []
    for backend_index in range(len(backend_types)):
        if not axesGiven:
            # Top level figure -- reset for every backend
            axes=False
            figure=False
            plotOptions["colorCycle"].reset()
            plotOptions["linestyleCycle"].reset()
            plotOptions["markerstyleCycle"].reset()
        plotOptions["backend"] = backend_types[backend_index]
        if not plotOptions["backend"] in backends:
            if plotOptions["backend"] in backendModules:
                # Try to dynload
                backendModules[plotOptions["backend"]]["spec"].loader.exec_module(backendModules[plotOptions["backend"]]["module"])
                backendModules[plotOptions["backend"]]["loaded"] = True
                backends[plotOptions["backend"]] = backendModules[plotOptions["backend"]]["module"]
            else:
                raise ModuleNotFoundError("Backend module "+str(plotOptions["backend"])+" not found!")
        axes, figure = plot(chosenDatasets, graphType, axes=axes, figure=figure, **plotOptions)
        # If the axes are hidden, hide them
        if cfg["plot"].get("hide-axes", False):
            axes.hide_axes = "both"

        for i in range(len(fit_results)):
            # TODO : Styles
            # TODO : Fit param position
            # TODO : Direct link to axes might not be the best way -- should or should not go through plot()?
            axes.plot(fit_results[i]["interpolation"][0], fit_results[i]["interpolation"][1],
                      label=fit_results[i]["label"], color=fit_results[i]["color"], linestyle="dotted")
            fit_offset = i * 0.04 * len(fit_results[i]["text"].split("\n"))
            axes.text((0.05, 0.8 - fit_offset), fit_results[i]["text"])

        # Handle decorations for axes
        for decorationArgs in decorationCommands:
            decorationSplit = decorationArgs.split()
            # All commands should be loaded
            axes, datasets = decorations[decorationSplit[0]](axes, datasets, decorationSplit[1:])
        # Legend options -- TODO : check whether here is good
        axes.legend_pos = plotOptions["legend-pos"]
        axes.legend_cols = plotOptions["legend-cols"]

        # If an inset directive is present, add an inset to the current axes
        if cfg["plot"].get("inset", False):
            insetLines = cfg["plot"].get("inset").split("\n")
            for i in range(len(insetLines)):
                # Arguments are xpos, ypos, xwidth, ywidth
                insetArgs = insetLines[i].split()
                insetAxes = axes.inset_axes(*map(float, insetArgs[1:]))
                # TODO : May not be needed in matplotlib, but needed in pgfplots
                figure.axes.append(insetAxes)
                fromConfig(insetArgs[0], axes=insetAxes, figure=figure, datasets=datasets, backend=plotOptions["backend"])
        if cfg["plot"].get("overlay", False):
            # Split by any whitespace
            overlayLines = cfg["plot"].get("overlay").split()
            for i in range(len(overlayLines)):
                # Apply a second graph on top of this one
                # TODO : Do not overwrite the options set up in the first (parent) config
                fromConfig(overlayLines[i], axes=axes, figure=figure, datasets=datasets, backend=plotOptions["backend"])
        if cfg["plot"].get("twinx", False):
            # Plot another dataset sharing the same x axis but different y axis
            # Always, only a single twinx makes sense - provide no arguments
            twinxAxes = axes.twinx()
            figure.axes.append(twinxAxes)
            fromConfig(cfg["plot"].get("twinx"), axes=twinxAxes, figure=figure, datasets=datasets, backend=plotOptions["backend"])
        if cfg["plot"].get("twiny", False):
            # same as twinx, but for shared y-axis
            twinyAxes = axes.twiny()
            figure.axes.append(twinyAxes)
            fromConfig(cfg["plot"].get("twiny"), axes=twinyAxes, figure=figure, datasets=datasets, backend=plotOptions["backend"])
        for figFileName in backend_figfiles[backend_index]:
            # TODO : Backend settings in backend implementation?
            # plt.savefig(figFileName, bbox_inches="tight", dpi=int(cfg["plot"].get("dpi", "300")))
            figure.save(figFileName)
    return figure

def guess_backends(filenames):
    needed_backends = []
    figfiles_for_backends = []
    for filename in filenames:
        basename, ext = os.path.splitext(filename)
        if ext in preferred_backends:
            if not preferred_backends[ext] in needed_backends:
                needed_backends.append(preferred_backends[ext])
                figfiles_for_backends.append([filename])
            else:
                # Backend already required, find its index
                figfiles_for_backends[needed_backends.index(preferred_backends[ext])].append(filename)
        else:
            raise ValueError("Chosen extension in the figfile {filename} does not have a preferred backend! Please specify.")
    return needed_backends, figfiles_for_backends
