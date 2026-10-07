import argparse
from ..parser import parse_ranges, point_transformation_bounds

ap = argparse.ArgumentParser(prog="translate", description="Translate given columns by given amounts.")
ap.add_argument("--all_cols", action="store_true", help="If given, stores all the columns not listed in the range unchanged and in the same order as in the original datasets.")
ap.add_argument("--row_range", default=":", type=parse_ranges, help="The range of rows on which the translation is applied (e.g. 10:15,16) [default : translate all rows]")
ap.add_argument("new_name", help="Name of the dataset where the shifted coordinates will be stored. Columns are stored in the order of arguments.")
ap.add_argument("col_triples", nargs="+", metavar="dataset index_range amount", default=False, help="Column coordinates and amount by which to shift the values in the column. Coordinates are given as dataset name and index range, value is given as floating number. Must always come in triples. Can write m instead of -, which breaks the parser. [default : no changes to any dataset]")

def command(datasets, arg_string):
    args = ap.parse_args(arg_string)
    if args.col_triples:
        if len(args.col_triples) % 3 != 0:
            raise IndexError("Wrong number of arguments in the translate combine command.")
        datasets[args.new_name] = []
        cols, rows, col_scaling, row_scaling = point_transformation_bounds(args.row_range, args.col_triples, datasets, all_cols=args.all_cols)
        for i in range(len(cols)):
            for col in cols[i]:
                datasets[args.new_name].append([])
                for row in range(len(datasets[args.col_triples[3*i]][col])):
                    val = datasets[args.col_triples[3*i]][col][row]
                    if col_scaling[i][col] and row_scaling[row]:
                        factor =args.col_triples[3*i+2]
                        if factor[0] == "m":
                            factor = -float(factor[1:])
                        else:
                            factor = float(factor)
                        val = val + factor
                    datasets[args.new_name][-1].append(val)
    return datasets
