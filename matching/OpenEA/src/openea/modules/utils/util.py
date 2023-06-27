import time
import os
import sys
from datetime import datetime

import tensorflow as tf


def load_session():
    # config = tf.ConfigProto()
    # config.gpu_options.allow_growth = True
    config = tf.ConfigProto(intra_op_parallelism_threads=38, 
                        inter_op_parallelism_threads=2, 
                        allow_soft_placement=True,
                        device_count = {'CPU': 38})
    return tf.Session(config=config)


def merge_dic(dic1, dic2):
    return {**dic1, **dic2}


def task_divide(idx, n):
    total = len(idx)
    if n <= 0 or 0 == total:
        return [idx]
    if n > total:
        return [idx]
    elif n == total:
        return [[i] for i in idx]
    else:
        j = total // n
        tasks = []
        for i in range(0, (n - 1) * j, j):
            tasks.append(idx[i:i + j])
        tasks.append(idx[(n - 1) * j:])
        return tasks


def generate_out_folder(args, out_folder, training_data_path, div_path, method_name):
    # params = training_data_path.strip('/').split('/')
    # print(out_folder, training_data_path, params, div_path, method_name)
    # path = params[-1]
    dataset = args.dataset.replace("_ready", "").replace("_sampled", "")
    dest = out_folder
    postfix = dest.split("/")[-1]
    dest = dest.replace(postfix, "")
    if not os.path.exists(dest):
        os.makedirs(dest)
    sys.stdout=open(dest + "/log" + "_NO_CSLS_" + str(datetime.now()),"w")
    print("results output folder:", dest)
    return out_folder
