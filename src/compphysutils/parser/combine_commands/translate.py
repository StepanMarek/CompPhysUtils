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

ap = argparse.ArgumentParser(description="Translate given columns by given amounts.")
ap.add_argument("--all_cols", default=False, action="store_true", help="If given, stores all the columns not listed in the range unchanged and in the same order as in the original dataset. Uses the first dataset name as the target dataset. All columns in different datasets are ignored.")
ap.add_argument("--row_range", default=False, type=parseRange, help="The range of rows on which the translation is applied (i.e. 10-14,16) [default : translate all rows]")
ap.add_argument("new_name", help="Name of the dataset where the shifted coordinates will be stored. Columns are stored in the order of arguments.")
ap.add_argument("col_triples", nargs="*", metavar="dataset index amount", default=False, help="Column coordinates and amount by which to shift the values in the column. Coordinates are given as dataset name and index, value is given as floating number. Must always come in triples. [default : no changes to any dataset]")

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
            if not args.all_cols:
                for i in range(0,len(args.col_triples),3):
                    datasetName = args.col_triples[i]
                    columnIndex = int(args.col_triples[i+1])
                    shiftAmount = float(args.col_triples[i+2])
                    rows = range(len(datasets[datasetName][columnIndex]))
                    datasets[args.new_name].append([])
                    for j in rows:
                        datasets[args.new_name][-1].append(datasets[datasetName][columnIndex][j] + shiftAmount)
            else:
                for i in range(len(datasets[args.col_triples[0]])):
                    datasets[args.new_name].append([])
                    # Search for relevant entry in col_triples
                    for k in range(0, len(args.col_triples), 3):
                        if int(args.col_triples[k+1]) == i:
                            # Valid shift
                            shiftAmount = float(args.col_triples[k+2])
                        else:
                            # No valid shift
                            shiftAmount = False
                    for j in rows:
                        if shiftAmount:
                            datasets[args.new_name][-1].append(datasets[args.col_triples[0]][i][j] + shiftAmount)
                        else:
                            # This ensures that even non-numeric entries are copied
                            datasets[args.new_name][-1].append(datasets[args.col_triples[0]][i][j])
    return datasets
