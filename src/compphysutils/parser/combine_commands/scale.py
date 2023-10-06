import argparse

def parseRange(rangeString):
    # First, split by commas
    commaSplit = rangeString.split(",")
    # If the element in comma split has - in it, it is a range, and needs to be filled
    cols = []
    for elem in commaSplit:
        if "-" in elem:
            # Fill the range
            borders = elem.split("-")
            minimum = borders[0]
            maximum = borders[1]
            # Maximum is inclusive
            for i in range(int(minimum), int(maximum)+1):
                cols.append(i)
        else:
            # Only convert
            cols.append(int(elem))
    return cols

ap = argparse.ArgumentParser(description="Scale given columns/rows by given amount")
ap.add_argument("--row_range", default=False, type=parseRange, help="The range of rows on which the scaling is applied (i.e. 10-14,16) [default : scale all rows]")
ap.add_argument("new_name", help="Name of the dataset where the scaled coordinates will be stored. Columns are stored in the order of arguments.")
ap.add_argument("col_triples", nargs="*", metavar="dataset indexRange amount", default=False, help="Column coordinates and amount by which to scale the values in the column. Coordinates are given as dataset name and index, value is given as floating number. Must always come in triples. [default : no changes to any dataset]")

def command(datasets, argString):
    args = ap.parse_args(argString)
    if args.col_triples:
        if len(args.col_triples) % 3 != 0:
            raise IndexError("Wrong number of arguments in the translate combine command.")
        else:
            datasets[args.new_name] = []
            if args.row_range:
                rows = args.row_range
            else:
                rows = range(len(datasets[args.col_triples[0]][0]))
            for i in range(len(datasets[args.col_triples[0]])):
                scaling = False
                scaleAmount = 1.0
                datasets[args.new_name].append([])
                # Search for relevant entry in col_triples
                for k in range(0, len(args.col_triples), 3):
                    col_range = parseRange(args.col_triples[k+1])
                    if i in col_range:
                        # Valid scale
                        scaleAmount = float(args.col_triples[k+2])
                        scaling = True
                        break
                for j in rows:
                    if scaling:
                        datasets[args.new_name][-1].append(datasets[args.col_triples[0]][i][j] * scaleAmount)
                    else:
                        # This ensures that even non-numeric entries are copied
                        datasets[args.new_name][-1].append(datasets[args.col_triples[0]][i][j])
    return datasets
