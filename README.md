# FairER demo: Fairness-Aware and Explainable Entity Resolution

*A video presentation of our system was submitted as supplementary material. It is also located in "demo_video/new_demo_video.mkv" of this repository*

The source code for the paper:

Vasilis Efthymiou, Kostas Stefanidis, Evaggelia Pitoura, Vassilis Christophides. FairER: Entity Resolution with Fairness Constraints. CIKM 2021 (short) [[pdf]](https://github.com/vefthym/fairER/blob/main/CIKM2021short_fairER_CR.pdf) [[slides]](https://github.com/vefthym/fairER/blob/main/FairER-slides.pdf) [[poster]](https://github.com/vefthym/fairER/blob/main/FairER_poster.pdf)

which is part of the project <a href="https://isl.ics.forth.gr/ResponsibleER/">ResponsibleER: Responsible by Design Entity Resolution</a>, 
funded by the <a href="https://www.elidek.gr/en/homepage/">Hellenic Foundation for Research and Innovation</a>.

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
1. Please click the "Download Datasets" button after the successfull running of the app.
2. Download "2016-10-des_dict" from https://github.com/kosugi11037/bert-int and place it to resources/Datasets
3. Download "wiki-news-300d-1M.vec" from https://fasttext.cc/docs/en/english-vectors.html and place it to matching/OpenEA/run

In case of problems or questions, please report an issue, or contact Vasilis Efthymiou (vefthym AT ics DOT forth DOT gr).
