from typing import Callable
import numpy as np
import json

from numpy.core.fromnumeric import sort


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


def iterate_in_2_list():
    cmds = [1, 2, 3, 4, 5]
    wheels = [5, 5, 5, 5, 5]
    ans = []
    for cmd, wheel in zip(cmds, wheels):
        ans.append(cmd + wheel)
    print(ans)


def generate_cmd(s) -> bytearray:
    s = int(s)
    data1 = (s >> 8) & 0xff
    data0 = s & 0xff
    return bytearray([0xaa, 0x4e, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xaa, 0x0c, data1, data0, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff])


def operation(s):
    return s**2

def abcd(aaaa):
    return aaaa["a"]

min([{"a": 2}, {"a": 1}, {"a": 3}], key=abcd)




def my_min(l, key=None):
    l.sort(key=key)
    return real

if __name__ == "__main__":
    import numpy as np
    ss = np.array([1, 2, 3, 4, 5])
    # ans = []
    # for s in ss:
    #     ans.append(generate_cmd(s))
    print(operation(ss))
