The source code for the paper:


Vasilis Efthymiou, Kostas Stefanidis, Evaggelia Pitoura, Vassilis Christophides. FairER: Entity Resolution with Fairness Constraints. CIKM 2021 (short) [[pdf]](https://github.com/vefthym/fairER/blob/main/CIKM2021short_fairER_CR.pdf) [[slides]](https://github.com/vefthym/fairER/blob/main/FairER-slides.pdf) [[poster]](https://github.com/vefthym/fairER/blob/main/FairER_poster.pdf)

which is part of the project <a href="https://isl.ics.forth.gr/ResponsibleER/">ResponsibleER: Responsible by Design Entity Resolution</a>, 
funded by the <a href="https://www.elidek.gr/en/homepage/">Hellenic Foundation for Research and Innovation</a>.


**Public API and UI (demo with restricted functionality)**:<br/>
Before installing and running the code locally, with its full functionality, you may be interested in checking the public version with limited functionality, hosted at <a href="https://isl.ics.forth.gr/fairER/">https://isl.ics.forth.gr/fairER/</a>. There, you can also find the <a href="https://isl.ics.forth.gr/fairER/services-manual">API ("Services Manual")</a>, along with executable examples. 


**Instructions for running the code locally**:<br/>
First, make sure that you have installed on your computer:<br/>
-Python (3.9 – recommended)<br/>
-Microsoft Visual C++ (for Windows OS only)

Then, you have to install all the required packages, using the command:<br/>
`pip install -r requirements.txt`

This allows a user to avoid the hassle of individually installing each required library, as well as resolving potential compatibility issues (since the library versions in the requirements file have been tested and found to be fully functional). 

Now you can run the local version using the command:<br/>
`python web/run.py`

To open the app on your default browser, open the URL <a href="http://127.0.0.1:5000">http://127.0.0.1:5000</a> (you can use Ctrl+Click to open it from the terminal).

During the first run, the datasets are not present in the system, so you have to click the "Download" button from the Web UI,  in order to download the datasets from DeepMatcher. This is a more convenient way than the alternative option of downloading each dataset individually, which is still applicable (if disk space is an issue). 

Finally, it is also recommended to use a system with more than 12GB of RAM, otherwise the system may be unstable.


In case of problems or questions, please report an issue, or contact Vasilis Efthymiou (vefthym AT ics DOT forth DOT gr).
