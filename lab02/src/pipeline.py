import pandas as pd
import numpy as np
import pickle as pkl
from os import listdir, rename
from os.path import isfile, join

# relative paths to data, the data is not on git due to size
path_prefix = "lab02/data/"
path_day = ["day1/", "day2/"]
path_batch_result = []
for i in range(1, 11):
    if i < 10:
        path_batch_result.append("batch0" + str(i) + "/results/")
    else:
        path_batch_result.append("batch" + str(i) + "/results/")

# dict of paths to results by day
path_result_by_day = {0: [], 1: []}
# day
for i in range(len(path_day)):
    # batches
    for j in range(len(path_batch_result)):
        # prefix + day + batch
        path_result_by_day[i].append(path_prefix + path_day[i] + path_batch_result[j])

path_data_by_day = {0: [], 1: []}
for i in range(len(path_result_by_day)):
    for path in path_result_by_day[i]:
        try:
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        except:
            continue
        for j in range(len(onlyfiles)):
            path_data_by_day[i].append(path + onlyfiles[j])


def fix_file_naming(day=1):
    """In data/day1 the results were fixed to be stored under the same
    naming-convention as data/day2."""

    concern = path_result_by_day[day]
    for path in concern:
        try:
            onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
            for result in onlyfiles:
                suffix = result[-6:]
                rename(path + result, path + "r" + suffix)
        except:
            print("skipped: ", path)


def generate_data():
    """Returns a dict with data samples. Keys Map to Days, Days contain
    samples obtained that day."""
    data = dict()
    for i in range(len(path_data_by_day)):
        key = path_day[i][:-1]
        data[key] = []
        for path in path_data_by_day[i]:
            data[key].append(pd.read_csv(path, sep="\t", skiprows=1))
            data[key][-1] = data[key][-1].to_numpy()
    return data


def store_data(storePath, data):
    """Packs the data into a .pkl file."""
    file = open(storePath, "wb")
    pkl.dump(data, file)
    file.close()
    print("Data stored in {}".format(storePath))


def setup_data_package():
    storePath = "lab02/data/readings.pkl"
    data = generate_data()
    store_data(storePath, data)


if __name__ == "__main__":
    setup_data_package()
    pass
