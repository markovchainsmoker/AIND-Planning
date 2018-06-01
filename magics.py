#enable multi-variable printing
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

#can be configured for all instances of Jupyter (Notebook and Console), 
#in a file ~/.ipython/profile_default/ipython_config.py
c = get_config()
c.InteractiveShell.ast_node_interactivity = "all"


#set environment variables without having to restart
%env NEW_ENV_VAR=1
%env JUPYTER_CONFIG_DIR=./jupyter/ jupyter notebook

#passing variables between notebooks
%store var
del var
#retrieve in a different notebook
%store -r data

#prepending a variable with '?' to get documentation
?str.replace()

#This will list all magics
#http://ipython.readthedocs.io/en/stable/interactive/magics.html
%lsmagic

#run a different notebook
%run ./two-histograms.ipynb

#load
%load ./hello_world.py

#list globals of type(str)
%who str

#time single run
%%time
import time
for _ in range(1000):
    time.sleep(0.01)# sleep for 0.01 seconds

#average of 100 runs   
import numpy
%timeit numpy.random.normal(size=100)

#write to file
%%writefile pythoncode.py

import numpy
def append_if_not_exists(arr, x):
    if x not in arr:
        arr.append(x)

def some_useless_slow_function():
    arr = list()
    for i in range(10000):
        x = numpy.random.randint(0, 10000)
        append_if_not_exists(arr, x)
        
#read from file
%pycat pythoncode.py

#debugger
#https://docs.python.org/3.5/library/pdb.html
#https://docs.python.org/3.5/library/pdb.html#debugger-commands
%pdb

def pick_and_take():
    picked = numpy.random.randint(0, 1000)
    
    
# By adding a semicolon at the end, the output is suppressed.
%matplotlib inline
from matplotlib import pyplot as plt
import numpy
x = numpy.linspace(0, 1, 1000)**1.5
plt.hist(x);
    raise NotImplementedError()
pick_and_take()


#shell commands
!ls *.csv
!pip install numpy
!pip list | grep pandas

#mathjax
\\( P(A \mid B) = \frac{P(B \mid A) \, P(A)}{P(B)} \\)

#run diffent kernel (bash,HTML,python2,python3)
%%bash
for i in {1..5}
do
   echo "i is $i"
done

#can even install R kernel
conda install -c r r-essentials

#multicursor support: hold Alt whhile dragging

#create presentation 
conda install -c damianavila82 rise

jupyter-nbextension install rise --py --sys-prefix
jupyter-nbextension enable rise --py --sys-prefix


#show thumbnails
import os
from IPython.display import display, Image
names = [f for f in os.listdir('../images/ml_demonstrations/') if f.endswith('.png')]
for name in names[:5]:
    display(Image('../images/ml_demonstrations/' + name, width=100))

#..or better through bash
names = !ls ../images/ml_demonstrations/*.png
names[:5]
