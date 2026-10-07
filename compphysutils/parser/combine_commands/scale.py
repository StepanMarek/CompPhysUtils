import argparse
from ..parser import parse_ranges, point_transformation_bounds

ap = argparse.ArgumentParser(description="Scale given columns/rows by given amount")
ap.add_argument("--row_range", default=":", type=parse_ranges, help="The slice range of rows on which the scaling is applied (e.g. 10,12:15,2:5:2,4) [default : ':', i.e. scale all rows]")
ap.add_argument("--all_cols", action="store_true", help="Store all columns from each dataset, only scaling the ones explicitly used.")
ap.add_argument("new_name", help="Name of the dataset where the scaled coordinates will be stored. Columns are stored in the order of arguments.")
ap.add_argument("col_triples", nargs="*", metavar="dataset index_slice_range amount", default=False, help="Column coordinates and amount by which to scale the values in the column. Coordinates are given as dataset name and index, value is given as floating number. Value can have m instead of a minus sign, which tends to break the parser. Must always come in triples. [default : no changes to any dataset]")

def command(datasets, argString):
    args = ap.parse_args(argString)
    if args.col_triples:
        if len(args.col_triples) % 3 != 0:
            raise IndexError("Wrong number of arguments in the translate combine command.")
        else:
            datasets[args.new_name] = []
            cols, rows, col_scaling, row_scaling = point_transformation_bounds(args.row_range, args.col_triples, datasets, all_cols=args.all_cols)
            # Do the scaling
            for i in range(len(cols)):
                for col in cols[i]:
                    datasets[args.new_name].append([])
                    # All rows are replicated, just some are not scaled
                    for row in range(len(datasets[args.col_triples[3*i]][col])):
                        val = datasets[args.col_triples[3*i]][col][row]
                        if col_scaling[i][col] and row_scaling[row]:
                            factor = args.col_triples[3*i+2]
                            if factor[0] == "m":
                                factor = -float(factor[1:])
                            else:
                                factor = float(factor)
                            val = val * factor
                        datasets[args.new_name][-1].append(val)
    return datasets
