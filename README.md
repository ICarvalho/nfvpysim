# nfvpysim - NFV Python Simulator for SFC
 
nfvpysim is a Python-based discrete-event simulator used to assess VNF placement schemes in Service Function Chaining. 



# nfvpysim - main steps

* At first, it is required to generate the datasets for HODs extraction. To do that, use generate_requests_trace_drive.py in scenarios folder. 
* Data preparation: Still in scenarios folder, run hon_training_data.py to generata the traning data which will be used by HOD-EXTRACTOR Algorithm. 
* Run HON.py for HOD extraction using the training dataset. The output are the VNFs sequences and their corresponding probability values. 
* In network.py, allocate the top-k sequences obtained previously, in which k determines the number of VNF sequences to be randomly placed in the top-k nfv-nodes of the topology. 
* in root file, set the parameters in the corresponding configuration file (random_sfc, sfc_by_len or var_len_sfc), including the topologies used, the placement schemes and number of requests and metrics to be evaluated. 

# Usage

```
nfvpysim run --results <RESULTS_FILE> <CONF_FILE>
```

*RESULTS_FILE*: It is a python pickle contaning the simulation results.

*CONF_FILE*: The configuration file with all the simulation settting, parameters and metrics. 

# Plotting the results.

``` 
 python <PLOT_RESULTS_FILE>  --results <RESULTS_FILE> --output OUTPUT_DIR  <CONF_FILE>
```

*PLOT_RESULTS_FILE*: python file to plot according to the used configuration file;

*RESULTS_FILE*: It is a python pickle contaning the simulation results.

*CONF_FILE*: The configuration file with all the simulation settting, parameters and metrics
