import sys
import os

from numpy import array
from sampling.start_sampling import start_sampling

from sampling.Configuration import Configuration
from sampling.utils import Utils


if __name__ == '__main__':

    args = sys.argv[1:]

    if args[0] == "sampling_only_p_ext":
        conf_array = {
            "conf_-1_only_p_ext": {
                "p": 0.15,
            },
            "conf_0_only_p_ext": {
                "p": 0,
            },
            "conf_1_only_p_ext": {
                "p": 0.15,
            },
            "conf_2_only_p_ext": {
                "p": 0.50,
            },
            "conf_3_only_p_ext": {
                "p": 0.85,
            },
            "conf_4_only_p_ext": {
                "p": 1.0,
            },
        }
        conf_id = args[1]
        method = args[2]
        conf = Configuration("D_Y_15K_V1", "", "useless", 1000, conf_array[conf_id]["p"], conf_id, method, "SUSIE_ext", export_sampled=True)
        start_sampling(conf)

    # TODO
    # if args[0] == "convert_sampling":
    #     conf_id = args[1]
    #     Utils.convert_sampling(conf_id, "D_Y_15K_V1")