import matplotlib.pyplot as plt
from .. import __user_conf_dir
from ..parser import parseDatasetConfig
from ..parser import save, writeFile
import configparser
from ..parser.combine import runGroupData
from .fitter import plotFit 
from .transformer import transforms,transformModules
from .decorator import decorations,decorationModules
import importlib
import os

# Search for default plot types
roots = []
modFilenames = []
root, _, filenames = next(os.walk(os.path.dirname(__file__)+"/plot_types"))
roots.append(root)
modFilenames.append(filenames)
# Search for custom plot types
if os.path.isdir(os.path.expanduser(__user_conf_dir+"/plot_types")):
    root, _, filenames = next(os.walk(os.path.expanduser(__user_conf_dir+"/plot_types")))
    roots.append(root)
    modFilenames.append(filenames)
# Import all plot types
plotTypes = {}
plotModules = {}
for i in range(len(roots)):
    for filename in modFilenames[i]:
        plotTypeName = filename.split(".")[0]
        if plotTypeName[0:2] == "__":
            # Skip __init__.py and similar commands
            continue
        spec = importlib.util.spec_from_file_location("compphysutils.graphics.plot_types."+plotTypeName, roots[i]+"/"+filename)
        mod = importlib.util.module_from_spec(spec)
        plotModules[plotTypeName] = {"spec" : spec, "module" : mod, "loaded" : False}

class CyclicIterator:
    def __init__(self, cycle=[]):
        self.singleCycle = cycle
        self.cycleLen = len(cycle)
        self.currentIndex = 0

    def __iter__(self):
        return self

    def __next__(self):
        returnVal = self.singleCycle[self.currentIndex % self.cycleLen]
        self.currentIndex += 1
        return returnVal

class ColorIterator(CyclicIterator):
    def __init__(self, singleCycle="b"):
        # Change the format if necessary
        listOfColors = singleCycle.split()
        for i in range(len(listOfColors)):
            if listOfColors[i].find(",") >= 0:
                listOfColors[i] = tuple(map(float, listOfColors[i].split(",")))
        super().__init__(listOfColors)

class LinestyleIterator(CyclicIterator):
    def __init__(self, singleCycle="-"):
        super().__init__(singleCycle.split())

class MarkerstyleIterator(CyclicIterator):
    def __init__(self, singleCycle="o"):
        super().__init__(singleCycle.split())

def plot(datasets, plotType="scatter", axes=False, figure=False, **plotOptions):
    if not figure:
        figure = plt.gcf()
    if not axes:
        axes = figure.gca()
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
    axes.set_xlabel(plotOptions["xlabel"])
    axes.set_ylabel(plotOptions["ylabel"])
    if plotOptions["xlim"]:
        axes.set_xlim(*plotOptions["xlim"])
    if plotOptions["ylim"]:
        axes.set_ylim(*plotOptions["ylim"])
    # Insert tick labels
    if plotOptions["xticks"]:
        #axes.set_xticks(plotOptions["xticks"][0], labels=plotOptions["xticks"][1])
        axes.set_xticks(plotOptions["xticks"][0])
        axes.set_xticklabels(plotOptions["xticks"][1])
    if plotOptions["xticks-rotate"]:
        axes.tick_params(axis="x", labelrotation=90)
    # If requested, move ticks to top
    axes.tick_params(axis="x",
                     top=plotOptions["xticks-swap"],
                     labeltop=plotOptions["xticks-swap"],
                     bottom=not plotOptions["xticks-swap"],
                     labelbottom=not plotOptions["xticks-swap"]
                     )
    if plotOptions["yticks"]:
        axes.set_yticks(plotOptions["yticks"][0])
        axes.set_yticklabels(plotOptions["yticks"][1])
    return axes

def fromConfig(configFileName, axes=False, figure=False, datasets={}):
    axesGiven = False
    if not figure:
        figure = plt.gcf()
    if axes:
        axesGiven = True
    cfg = configparser.ConfigParser()
    cfg.read(configFileName)
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
    plotOptions["legend-pos"] = cfg["plot"].get("legend-pos", "best").split("\n")
    plotOptions["legend-cols"] = list(map(int, cfg["plot"].get("legend-cols", "1").split("\n")))
    if "xlim" in cfg["plot"]:
        plotOptions["xlim"] = list(map(float, cfg["plot"].get("xlim").split()))
    else:
        plotOptions["xlim"] = False
    if "ylim" in cfg["plot"]:
        plotOptions["ylim"] = list(map(float, cfg["plot"].get("ylim").split()))
    else:
        plotOptions["ylim"] = False
    if "font" in cfg["plot"]:
        plt.rcParams["font.family"] = cfg["plot"].get("font", "sans")
    if "font-size" in cfg["plot"]:
        plt.rcParams["font.size"] = int(cfg["plot"].get("font-size", 12))
    if "mathfont" in cfg["plot"]:
        plt.rcParams["mathtext.fontset"] = cfg["plot"].get("mathfont", "cm")
    figure.set_size_inches(
            float(cfg["plot"].get("fig-width-inches", 6.4)),
            float(cfg["plot"].get("fig-height-inches", 4.8))
    )
    plotOptions["colorCycle"] = cfg["plot"].get("colorCycle", "r g b c m y k")
    plotOptions["colorCycle"] = ColorIterator(plotOptions["colorCycle"])
    plotOptions["linestyleCycle"] = cfg["plot"].get("linestyleCycle", "solid")
    plotOptions["linestyleCycle"] = LinestyleIterator(plotOptions["linestyleCycle"])
    plotOptions["markerstyleCycle"] = cfg["plot"].get("markerstyleCycle", "o")
    plotOptions["markerstyleCycle"] = LinestyleIterator(plotOptions["markerstyleCycle"])
    plotOptions["xlabel"] = cfg["plot"].get("xlabel", None)
    plotOptions["ylabel"] = cfg["plot"].get("ylabel", None)
    plotOptions["axis-width"] = cfg["plot"].get("axis-width", 1);
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
        if plotOptions[ticksName] and (not cfg["plot"].get("hide-"+ticksName, False)):
            plotOptions[ticksName] = datasets[plotOptions[ticksName]]
        elif cfg["plot"].get("hide-"+ticksName, False):
            plotOptions[ticksName] = [[],[]]
        plotOptions[ticksName+"-rotate"] = cfg["plot"].get(ticksName+"-rotate", False)
    # xticks on top if requested
    plotOptions["xticks-swap"] = cfg["plot"].get("xticks-swap", False)
    axes = plot(chosenDatasets, graphType, axes=axes, figure=figure, **plotOptions)
    # If the axes are hidden, hide them
    if cfg["plot"].get("hide-axes", False):
        axes.set_axis_off()
    # Change width of all axes
    for place in ["top", "bottom", "left", "right"]:
        axes.spines[place].set_linewidth(plotOptions["axis-width"]);
    # If fit is present, handle it
    fitIndex = 0
    if cfg["plot"].get("fit", False):
        fitLabels = cfg["plot"].get("fit-labels", False)
        numFits = len(cfg["plot"].get("fit").split("\n"))
        if not fitLabels:
            fitLabels = [False] * numFits
        else:
            fitLabels = fitLabels.split("\n")
        if len(fitLabels) < numFits:
            fitLabels += [False] * (numFits - len(fitLabels))
        prevFitParams = []
        prevFitErrors = []
        fitParamLengths = []
        currFitParams = []
        currFitErrors = []
        fitColorIterator = ColorIterator(cfg["plot"].get("fit-colorCycle", "tab:blue tab:orange tab:green tab:cyan"))
        fitLinestyleIterator = LinestyleIterator(cfg["plot"].get("fit-linestyleCycle", ":"))
        # Ready the ranges for fits - each fit requires a separate range
        fitXMins = [False]*numFits
        fitXMaxs = [False]*numFits
        providedXMins = cfg["plot"].get("fit-xmin", False)
        providedXMaxs = cfg["plot"].get("fit-xmax", False)
        if providedXMins:
            providedXMins = providedXMins.split("\n")
            for i in range(len(providedXMins)):
                fitXMins[i] = float(providedXMins[i])
        if providedXMaxs:
            providedXMaxs = providedXMaxs.split("\n")
            for i in range(len(providedXMaxs)):
                fitXMaxs[i] = float(providedXMaxs[i])
        for allFitArgs in cfg["plot"].get("fit").split("\n"):
            fitArgs = allFitArgs.split()
            # TODO : Fit args?
            currFitParams, currFitErrors = plotFit(
                chosenDatasets[int(fitArgs[1])],
                fitArgs[0],
                axes,
                fitPoints=int(cfg["plot"].get("fit-points", 100)),
                fitLabel=fitLabels[fitIndex],
                showParams=cfg["plot"].getboolean("fit-show-params", True),
                showError=cfg["plot"].getboolean("fit-show-error", True),
                fitColorCycle=fitColorIterator,
                fitLinestyleCycle=fitLinestyleIterator,
                paramsPlacement=cfg["plot"].get("params-placement", False),
                paramsOffset=len(prevFitParams),
                xMin=fitXMins[fitIndex],
                xMax=fitXMaxs[fitIndex],
                dirtyRun=cfg["plot"].getboolean("fit-dirty-run", False),
                fitIndex=fitIndex
                )
            fitIndex += 1
            prevFitParams += list(currFitParams)
            prevFitErrors += list(currFitErrors)
            fitParamLengths.append(len(currFitParams))
        # Save fit params, if required
        fitSaveName = cfg["plot"].get("fit-savepoint", False)
        if fitSaveName:
            fitSaveArgs = fitSaveName.split()
            # No context name nor dataset name, only format and target filename (optional)
            fitFormatName = fitSaveArgs[0]
            fitFileName = "fit.dat"
            fitParserArgs = False
            if len(fitSaveArgs) > 1:
                fitFileName = fitSaveArgs[1]
            if len(fitSaveArgs) > 2:
                fitParserArgs = " ".join(fitSaveArgs[2:])
            # Regularize to dataset - take the first fit as determination
            dataset = []
            for j in range(fitParamLengths[0]):
                dataset.append([])
                # Append for both value and error
                dataset.append([])
            fitNumCols = fitParamLengths[0]
            paramOffset = 0
            for i in range(len(fitParamLengths)):
                for j in range(fitNumCols):
                    dataset[2*j].append(prevFitParams[paramOffset + j])
                    dataset[2*j+1].append(prevFitErrors[paramOffset + j])
                paramOffset += fitParamLengths[i]
            # Dataset regularized, output
            writeFile(fitFileName, fitFormatName, dataset, fitParserArgs)
    # Handle decorations for main axes
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
            axes, datasets = decorations[decorationSplit[0]](axes, datasets, decorationSplit[1:])
    # Move the legend render here, even after decorations (which can also be annotated)
    if plotOptions["legend"]:
        if len(plotOptions["legend-pos"]) == 1:
            # Apply the same location and number of columns for each legend
            legendArgs = plotOptions["legend-pos"][0].split()
            if len(legendArgs) == 4:
                axes.legend(loc=" ".join(legendArgs[:-2]), ncol=plotOptions["legend-cols"][0], bbox_to_anchor=tuple(map(float, legendArgs[-2:])))
            else:
                axes.legend(loc=plotOptions["legend-pos"][0], ncol=plotOptions["legend-cols"][0])
        else:
            # Split the legend - now need that the number of lines and legend entries are the same
            handles, labels = axes.get_legend_handles_labels()
            # First, organize line handles into list with the same positions - use dictionary
            legendsOrganized = {}
            currentLocation = 0
            for i in range(len(handles)):
                if plotOptions["legend-pos"][i] in legendsOrganized:
                    legendsOrganized[plotOptions["legend-pos"][i]]["handles"].append(handles[i])
                else:
                    # Create new descriptor object
                    legendsOrganized[plotOptions["legend-pos"][i]] = {}
                    legendsOrganized[plotOptions["legend-pos"][i]]["handles"] = [handles[i]]
                    if currentLocation < len(plotOptions["legend-cols"]):
                        legendsOrganized[plotOptions["legend-pos"][i]]["cols"] = plotOptions["legend-cols"][currentLocation]
                        currentLocation += 1
                    else:
                        legendsOrganized[plotOptions["legend-pos"][i]]["cols"] = 1
            legendArtists = []
            for legendLoc in legendsOrganized:
                if len(legendLoc.split()) <= 2:
                    # Only loc is provided
                    legendArtists.append(axes.legend(handles=legendsOrganized[legendLoc]["handles"], loc=legendLoc, ncol=legendsOrganized[legendLoc]["cols"]))
                else:
                    # Loc and bbox are provided
                    legendLocOnly = " ".join(legendLoc.split()[:-2])
                    legendBBOXOnly = tuple(map(float, legendLoc.split()[-2:]))
                    legendArtists.append(axes.legend(handles=legendsOrganized[legendLoc]["handles"], loc=legendLocOnly, bbox_to_anchor=legendBBOXOnly, ncol=legendsOrganized[legendLoc]["cols"]))
            # Finally, add overwritten artists back to the axes
            for i in range(len(legendArtists)-1):
                axes.add_artist(legendArtists[i])
    # If an inset directive is present, add an inset to the current axes
    if cfg["plot"].get("inset", False):
        insetLines = cfg["plot"].get("inset").split("\n")
        for i in range(len(insetLines)):
            insetArgs = insetLines[i].split()
            # Arguments are xpos, ypos, xwidth, ywidth
            insetAxes = axes.inset_axes(list(map(float, insetArgs[1:])))
            fromConfig(insetArgs[0], axes=insetAxes, figure=figure, datasets=datasets)
    if cfg["plot"].get("overlay", False):
        # Split by any whitespace
        overlayLines = cfg["plot"].get("overlay").split()
        for i in range(len(overlayLines)):
            # Apply a second graph on top of this one
            fromConfig(overlayLines[i], axes=axes, figure=figure, datasets=datasets)
    if cfg["plot"].get("twinx", False):
        # Plot another dataset sharing the same x axis but different y axis
        # Always, only a single twinx makes sense - provide no arguments
        fromConfig(cfg["plot"].get("twinx"), axes=axes.twinx(), figure=figure, datasets=datasets)
    if cfg["plot"].get("twiny", False):
        # same as twinx, but for shared y-axis
        fromConfig(cfg["plot"].get("twiny"), axes=axes.twiny(), figure=figure, datasets=datasets)
    # If axes are provided, assume figure is printed somewhere else
    # TODO : Is this a reasonable assumption?
    if axesGiven:
        return True
    if plotOptions["figfile"]:
        # Can output the same figure in different formats
        for figFileName in plotOptions["figfile"].split():
            plt.savefig(figFileName, bbox_inches="tight", dpi=int(cfg["plot"].get("dpi", "300")))
    else:
        plt.show()
    return figure
