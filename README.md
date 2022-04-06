## FairER

This file contains techical information on how to setup and run FairER on Linux OS using Python (3.9).

Before running the code: 
* install the DeepMatcher package using the command: `pip install deepmatcher` (see note for Windows 10/11 users at the end), 
* install all the packages that Mojito requires to run, using the command: `pip install -r fairER/mojito/requirements.txt`
* download the [Datasets from DeepMatcher](https://github.com/anhaidgroup/deepmatcher/blob/master/Datasets.md).
* process the downloaded datasets by running the `read_datasets.py` file and changing the dataset name to the one you wish to process.
* to use our pre-defined settings, you may also need to install the gender-guesser library using `pip install gender-guesser`

The main file of FairER is main_fairER.py. The FA*IR and traditional ER baselines are in the files main_fair.py and main_unfair.py, respectively.

To run FairER you need to specify certaing arguments while calling main_fairER.py:
1. the first argument specifies the path containing the labeled data (e.g.: resources/deepmatcher/Structured/),
2. the second argument specifies how the training file is named (e.g.: joined_train.csv),
3. the third argument specifies how the validation file is named (e.g.: joined_valid.csv),
4. the fourth argument specifies how the testing file is named (e.g.: joined_test.csv),
5. the fifth argument specifies if we need explanation for our model (1: for True, 0: for False).

What an example of calling main_fairER.py looks like:
`python main_fairER.py resources/deepmatcher/Structured/ joined_train.csv joined_valid.csv joined_test.csv 1`
(This currently runs on all the default settings and hyperparameters)

If you want to change any hyperparameters before training the DeepMatcher's model, locate to `matching/run_deepmatcher.py` and edit the `train_or_load_pretrained_moded` function to your desires.
For example, if you want to change the number of epochs, at the line `model.run_train(train, validation, best_save_path=os.path.join(data_path, model_name), epochs=epochs)`, change epochs to desired number and the same goes for model_name(changes the model's save name).
**Before training a new model, remember to move or delete any old model from the data directory or it will be loaded as pre-trained, instead of training a new one.**

If you want to change the score margins on the explanation charts, locate to `matching/run_deepmatcher_w_explainer.py`. Under the `run` funtion, modify the lines 
```Python
chart(tp_result, (1, 1, 1), (-0.6, 0.4), title = "chart_tp")
chart(tn_result, (1, 1, 1), (-0.6, 0.4), title = "chart_tn")
```
instead of (-0.6, 0.4), to what you want the minimum and maximum attributes' scores to be.

**Running DeepMatcher on Windows 10/11**: To install deepmatcher on Windows 10/11: run `pip install git+https://github.com/anhaidgroup/deepmatcher#egg=deepmatcher`. <br/>
Also update deepmatcher/data/field.py, and two more files in the same folder to "from torchtext.legacy import data". In case you encounter problems installing fastText on Windows, this post might be useful: https://stackoverflow.com/questions/51683015/unable-to-install-fasttext-for-python-on-windows .



In case of problems or questions, please report an issue, or contact Vasilis Efthymiou (vefthym AT ics DOT forth DOT gr).
