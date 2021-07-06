import numpy as np
import json


def get_cfg_as_sampling():
    with open("../cfg.json", "r") as f:
        sample_matrix_base = json.load(f)["data_filter"]["sampling_method_x"]
        sample_matrix_base = np.array(sample_matrix_base)
        print(sample_matrix_base)
        # sample_matrix_x = sample_matrix_base[:, 0]
        # sample_matrix_y = sample_matrix_base[:, 1]
        sample_matrix = np.append(
            sample_matrix_base[:, 0:1], sample_matrix_base[:, 1:2], axis=1)
        for sample in sample_matrix:
            # get spec point from depth frame
            print(sample)
