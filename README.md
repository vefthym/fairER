# FairER demo: Fairness-Aware and Explainable Entity Resolution

*A video presentation of our system was submitted as supplementary material. It is also located in "demo_video/new_demo_video.mkv" of this repository*

## Installation
```bash
cd fairER/installation
conda env create --file demo.yml
conda env create --file demo_bert_int.yml
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
conda activate demo
cd ../matching/OpenEA
pip install -e .
```

## Run
```bash
conda activate demo
export PYTHONPATH=$PYTHONPATH:/home/<username>/fairER/
python web/run.py
```

## Datasets
1. Please click the "Download Datasets" button after the successfull running of the app.
2. Download "2016-10-des_dict" from https://github.com/kosugi11037/bert-int and place it to resources/Datasets
3. Download "wiki-news-300d-1M.vec" from https://fasttext.cc/docs/en/english-vectors.html and place it to matching/OpenEA/run
