import argparse
from ..parser import parse_ranges, ranges_to_indices

ap = argparse.ArgumentParser(prog="average", description="Takes average along the row axis")

ap.add_argument("--rows", "-r", dest="row_range", default=":", required=False, type=parse_ranges, help="Specify range of rows which to use. By default, all rows are used. Unspecified rows are disregarded.")

def command(dataset, arg_string):
    args = ap.parse_args(arg_string)
    new_set = []
    rows = ranges_to_indices(args.row_range, dataset[0])
    N = len(rows)
    for i in range(len(dataset)):
        # This should do correct type conversion, if needed
        row_sum = 0 * dataset[i][0]
        for range_index in range(len(args.row_range)):
            row_sum += sum(dataset[i][args.row_range[range_index]])
        new_set.append([row_sum / N])
    return new_set
