# DeepMetis-MNIST

## General Information ##
This folder contains the application of DeepMetis to the handwritten digit classification problem.
This tool is developed in Python on top of the DEAP evolutionary computation framework. It has been tested on a machine featuring an i7 processor, 16 GB of RAM, an Nvidia GeForce 940MX GPU with 2GB of memory, Ubuntu 18.04 (bionic) OS and python 3.6.

Follow the steps below to set up DeepMetis and validate its general functionality.


## Step 1: Configure the environment  ##

Pull our pre-configured Docker image for DeepMetis-MNIST:

``` 
docker pull p1ndsvin/metisbox
```

Run it by typing in the terminal the following commands:

```
docker run -it --rm p1ndsvin/metisbox
```

## Step 2: Run DeepMetis ##
Use the following commands to start a fast run of DeepMetis-MNIST:

```
cd DeepHyperion/DeepMetis-MNIST
python main.py
```

> NOTE: `properties.py` contains the tool configuration. You should edit this file to change the configuration. For example, if you want to run <i>DeepMetis-MNIST</i> with the same configuration as in the paper, you need to set the `NGEN` variable in `properties.py` to `1000`

When the run ends, on the console you should see a message like the following:

```
Final solution N is: X
GAME OVER

Process finished with exit code 0
```

where X is the number of generated mutant-killing inputs.

Moreover, DeepMetis will create a folder `results` which contains: 
* the archive of solutions (`archive` folder); 
* the final report (`report_final.json`);
* the configuration's description (`config.json`).
