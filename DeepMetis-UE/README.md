# DeepMetis: UnityEyes

## General Information ##
This folder contains the application of the DeepMetis approach to the eye gaze prediction problem.
This tool is developed in Python on top of the DEAP evolutionary computation framework. It has been tested on a Windows machine equipped with a i9 processor, 32 GB of memory, and an Nvidia GPU GeForce RTX 2080 Ti with 11GB of dedicated memory.

## Step 1: Configure the environment ##

This tool needs the UnityEyes and Sikuli to be installed on the machine where it is running. 

### Python Installation ###

### UnityEyes Installation and Configuration ###

A free version of UnityEyes can be found at https://www.cl.cam.ac.uk/research/rainbow/projects/unityeyes/.

### Sikuli Installation and Configuration ###

A free version of Sikuli can be found at ...

#### Other Dependencies ###

To easily install the dependencies with pip, we suggest to create a dedicated virtual environment and run the command:

```pip install -r requirements.txt```

## Step 2: Run DeepMetis

Use the following commands to start a fast run of DeepMetis-UE:

```
python test.py
python main.py
```

> NOTE: The user must not interact with the pc during the run

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


