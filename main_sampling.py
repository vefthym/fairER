import sys
import os

from numpy import array
from sampling.start_sampling import start_sampling

from sampling.Configuration import Configuration
from sampling.utils import Utils


if __name__ == '__main__':

    args = sys.argv[1:]

    if args[0] == "sampling_ext":
        conf_array = {
            "conf_-1_ext": {
                "p": 0.15,
                "attr_thres": 2
            },
            "conf_0_ext": {
                "p": 0,
                "attr_thres": 2
            },
            "conf_1_ext": {
                "p": 0.15,
                "attr_thres": 2
            },
            "conf_2_ext": {
                "p": 0.50,
                "attr_thres": 2
            },
            "conf_3_ext": {
                "p": 0.85,
                "attr_thres": 2
            },
            "conf_4_ext": {
                "p": 1.0,
                "attr_thres": 2
            },
        }
        conf_id = args[1]
        method = args[2]
        conf = Configuration("D_Y_15K_V1", "", "useless", 100, conf_array[conf_id]["p"], conf_id, method, "SUSIE_ext", conf_array[conf_id]["attr_thres"], export_sampled=True)
        start_sampling(conf)

    # Convert OpenEA-based datasets' attributes to be compatible to RREA
    if args[0] == "convert_attributes":
        Utils.convert_attributes("D_Y_15K_V1")

    # TODO
    # convert sampled data of RREA to be compatible with OpenEA methods
    # if args[0] == "convert_sampling":
    #     conf_id = args[1]
    #     Utils.convert_sampling(conf_id, "D_Y_15K_V1")