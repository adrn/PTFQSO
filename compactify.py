""" Join all of the text files Maria sent into a few """

import glob
import os
import numpy as np
import numpy.lib.recfunctions as nprf

# get root names
root_names = [os.path.basename(f).split(".txt")[0].split("_")[0]
              for f in glob.glob("data/DownloadTxtFiles/*.txt")]
root_names = np.unique(root_names)

# for each root name, grab all files and join into one
for root_name in root_names:
    file_list = glob.glob("data/DownloadTxtFiles/{0}*.txt".format(root_name))

    if len(file_list) == 1:
        continue

    for filename in file_list:
        d = np.genfromtxt(filename, dtype=None)
        try:
            alldata = nprf.stack_arrays((alldata, d),usemask=False)
        except NameError:
            alldata = d.copy()

    # write all data to a single file
    np.savetxt("data/Spring2015/{0}.txt".format(root_name), alldata, fmt="%s")
