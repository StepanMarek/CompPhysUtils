import argparse

ap = argparse.ArgumentParser(description="Combines two mos files into a single mos file that represents orthogonal sum of the orbitals. Order matters.")
ap.add_argument("new_dataset", help="Name of the newly created dataset, in mos format.")
ap.add_argument("mos_one", help="Name of the dataset (energy included) of the first molecule.")
ap.add_argument("mos_two", help="Name of the dataset (energy included) of the second molecule.")

def command(datasets, argString):
    # Combines two molecules orthogonally
    # That means that there is explicitly no overlap between the saos in the mos states
    args = ap.parse_args(argString)
    nsaos_one = len(datasets[args.mos_one][0])
    nsaos_two = len(datasets[args.mos_two][0])
    # Start writing the new dataset
    new_dataset = []
    # Create all columns
    for j in range(nsaos_one + nsaos_two + 1):
        new_dataset.append([])
        # Create all rows
        for i in range(nsaos_one + nsaos_two):
            new_dataset[-1].append(0.0)
    # Replicate molecule one energies
    for i in range(nsaos_one):
        new_dataset[0][i] = datasets[args.mos_one][0][i]
    # Replicate molecule two energies
    for i in range(nsaos_one, nsaos_one + nsaos_two):
        new_dataset[0][i] = datasets[args.mos_two][0][i-nsaos_one]
    # In the first phase, we are replicating the first molecule
    for i in range(1, nsaos_one+1):
        for j in range(nsaos_one):
            new_dataset[i][j] = datasets[args.mos_one][i][j]
    # In the second phase, we are replicating second molecule
    for i in range(nsaos_one + 1, nsaos_one + nsaos_two + 1):
        for j in range(nsaos_one, nsaos_one + nsaos_two):
            new_dataset[i][j] = datasets[args.mos_two][i-nsaos_one][j-nsaos_one]
    # Assign to all datasets
    datasets[args.new_dataset] = new_dataset
    return datasets
