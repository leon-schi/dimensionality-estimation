# Code for 'Real-World Networks are Low-Dimensional: Theoretical and Practical Assessment'

## Data

Real-world networks used for the experiments are listed in the file `network_list` together with links where they can be found (due to space restrictions, we only include links to the networks instead of the networks themselves). In addition to the networks listed there, we further use the dataset of Bläsius and Fischbeck of 3006 real-world networks avalable at https://zenodo.org/records/8058432. Our dataset described by `network_list` consists of a mix of networks from the SNAP dataset and Network Repository with sizes between 10k and 4M nodes. Most of thema are social, citation, collaboration or biological networks and some of them are also part of [previous work](https://www.nature.com/articles/s41467-022-33685-z) regarding dimensionality estimation. 

## How to run

You can either run `run_local.sh` to run the experiments locally (which requires python 3 installed) or `run_docker.sh` which builds and executes a docker image with the experiments. The sripts will load all the graphs from the `supplementary_data` folder and execute the test for $w_c$ in the range $2, 300$, which covers the range of the average degrees of all our networks. When it is done, it will create a file named `results.pkl` in the `results` directory that can be read using python joblib and contains the test results for each $w_c$ (starting at the lowest $w_c$) and the associated sizes of the induced subgraph of nodes of estimated weight $[w_0, c w_0]$.

The test results can then be loaded using 

```
r = joblib.load('results/results.pkl')
```

where `r` is a dictionary containing the network names as keys, whereby each entry is again a dictionary with keys `test_values` and `sizes` contiaining a list of the test outcomes and associated sizes of the induced subgraph of nodes of estimated weight $[w_0, c w_0]$, respectively (we use $c = 1.33$ as predicted by theory).
