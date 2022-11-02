import os
from datetime import datetime

class Configuration:

    c = None

    def __init__(self, dataset, prefix, measure, sampling_size, p, conf_id, method, sampling_method, attr_thres, export_sampled=False):
        self.id = conf_id
        self.dataset = dataset
        self.prefix = prefix
        self.measure = measure
        self.sampling_size = sampling_size
        self.p = p
        self.export_sampled = export_sampled
        self.method = method
        self.sampling_method = sampling_method
        self.attr_thres = attr_thres
    def export(self, path):
        with open(path, "w") as fp:
            fp.write("timestamp: " + str(datetime.now()))
            fp.write("\n")
            fp.write("conf_id: " + str(self.id))
            fp.write("\n")
            fp.write("dataset: " + str(self.dataset))
            fp.write("\n")
            fp.write("prefix: " + str(self.prefix))
            fp.write("\n")
            fp.write("measure: " + str(self.measure))
            fp.write("\n")
            fp.write("sampling_size: " + str(self.sampling_size))
            fp.write("\n")
            fp.write("p: " + str(self.p))
            fp.write("\n")
            fp.write("attr_thres: " + str(self.attr_thres))
            fp.write("\n")
            fp.write("method: " + self.method)
            fp.write("\n")
            fp.write("sampling_method: " + self.sampling_method)
            fp.write("\n")
            fp.write("export_sampled: " + str(self.export_sampled))