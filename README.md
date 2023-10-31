# FairER: Fairness-Aware and Explainable Entity Resolution

The source code for the papers:

Nikolaos Fanourakis, Christos Kontousias, Vasilis Efthymiou, Vassilis Christophides and Dimitris Plexousakis. FairER demo: Fairness-Aware and Explainable Entity Resolution. ISWC 2023 [[pdf]](https://github.com/vefthym/fairER/blob/main/ISWC2023_fairer_demo.pdf) [[poster]]() [[demo video]](https://youtu.be/DTrf9sbmCZE) 

Vasilis Efthymiou, Kostas Stefanidis, Evaggelia Pitoura, Vassilis Christophides. FairER: Entity Resolution with Fairness Constraints. CIKM 2021 [[pdf]](https://github.com/vefthym/fairER/blob/main/CIKM2021short_fairER_CR.pdf) [[slides]](https://github.com/vefthym/fairER/blob/main/FairER-slides.pdf) [[poster]](https://github.com/vefthym/fairER/blob/main/FairER_poster.pdf)


which are parts of the project <a href="https://isl.ics.forth.gr/ResponsibleER/">ResponsibleER: Responsible by Design Entity Resolution</a>, 
funded by the <a href="https://www.elidek.gr/en/homepage/">Hellenic Foundation for Research and Innovation</a>.

*A video presentation of FairER demo is located in "demo_video/new_demo_video.mkv" of this repository; also available on [Youtube](https://youtu.be/DTrf9sbmCZE).*

**Public API and UI (demo with restricted functionality)**:<br/>
Before installing and running the code locally, with its full functionality, you may be interested in checking the public version with limited functionality, hosted at <a href="https://isl.ics.forth.gr/fairER/">https://isl.ics.forth.gr/fairER/</a>. There, you can also find the <a href="https://isl.ics.forth.gr/fairER/services-manual">API ("Services Manual")</a>, along with executable examples. 

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
1. Please click the "Download Datasets" button after the successfull installation of the app.
2. Download "2016-10-des_dict" from https://github.com/kosugi11037/bert-int and place it to resources/Datasets
3. Download "wiki-news-300d-1M.vec" from https://fasttext.cc/docs/en/english-vectors.html and place it to matching/OpenEA/run
