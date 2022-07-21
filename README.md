The source code for the paper: 

Vasilis Efthymiou, Kostas Stefanidis, Evaggelia Pitoura, Vassilis Christophides. FairER: Entity Resolution with Fairness Constraints. CIKM 2021 (short) [[pdf]](https://github.com/vefthym/fairER/blob/main/CIKM2021short_fairER_CR.pdf) [[slides]](https://github.com/vefthym/fairER/blob/main/FairER-slides.pdf) [[poster]](https://github.com/vefthym/fairER/blob/main/FairER_poster.pdf)

which is part of the project <a href="https://isl.ics.forth.gr/ResponsibleER/">ResponsibleER: Responsible by Design Entity Resolution</a>, 
funded by the <a href="https://www.elidek.gr/en/homepage/">Hellenic Foundation for Research and Innovation</a>.


Instructions:
First of all, make sure that you have installed on your computer:
-Python (3.9 – recommended)
-Microsoft Visual C++ (for Windows OS only)

Then you have to install all the required packages, using the command:
pip install -r requirements.txt

This allows a user to avoid the hassle of individually installing each required library, as well as resolving potential compatibility issues (since the library versions in the requirements file have been tested and found to be fully functional). 

Now you can run local version using the command:
python web/run.py

To open the app on your default browser, open the URL http://127.0.0.1:5000 (you can use Ctrl+Click to open it from the terminal).

During the first run, the datasets are not present in the system, so you have to click the Download button from the Web UI,  in order to download the datasets from DeepMatcher. This is a more convenient way than the alternative option of downloading each dataset individually, which is still applicable (if disk space is an issue). 

Finally, it is also recommended to use a system with more than 12GB of RAM, otherwise the system may be unstable.

In case of problems or questions, please report an issue, or contact Vasilis Efthymiou (vefthym _AT_ ics _DOT_ forth _DOT_ gr).
