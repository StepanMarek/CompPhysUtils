import argparse
from compphysutils.graphics.plotter import fromConfig

argparser = argparse.ArgumentParser(description="Plots the graph described in the config file.")
argparser.add_argument("configfilenames", nargs="+", help="name of the config file(s) to process")

def main():
    args = argparser.parse_args()
    for filename in args.configfilenames:
        # TODO : Clearing of figures?
    	fromConfig(filename)
