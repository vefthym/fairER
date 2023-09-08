import argparse
import sys
import time

from openea.modules.args.args_hander import check_args, load_args
from openea.modules.load.kgs import read_kgs_from_folder
from openea.expriment.approaches_without_attribute import JAPE
from openea.expriment.approaches_without_attribute import AttrE
from openea.expriment.approaches_without_attribute import IMUSE
from openea.expriment.approaches_without_attribute import MultiKE
from openea.expriment.approaches_without_attribute import GCN_Align
from openea.expriment.approaches_without_attribute import RDGCN
from openea.models.basic_model import BasicModel


class ModelFamily(object):
    BasicModel = BasicModel

    JAPE = JAPE
    AttrE = AttrE
    IMUSE = IMUSE
    MultiKE = MultiKE
    GCN_Align = GCN_Align
    RDGCN = RDGCN


def get_model(model_name):
    return getattr(ModelFamily, model_name)


if __name__ == '__main__':
   args = load_args(sys.argv[1])
   if "conf_" in args.conf_id:
        args.training_data = args.training_data + args.dataset + '/' + args.conf_id + '/'
   else:
        args.training_data = args.training_data + args.dataset + '/'

   print(args)
   kgs = read_kgs_from_folder(args.training_data, args.dataset_division, args.alignment_module, args.ordered)
   model = get_model(args.embedding_module)()
   model.set_args(args)
   model.set_kgs(kgs)
   model.init()
   model.run()
   model.test()
   model.save()
   print("Total run time = {:.3f} s.".format(time.time() - t))
