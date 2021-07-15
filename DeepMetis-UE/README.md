# DeepMetis: UnityEyes

## General Information ##
This folder contains the application of the DeepMetis approach to the eye gaze prediction problem.
This tool is developed in Python on top of the DEAP evolutionary computation framework. It has been tested on a Windows machine equipped with a i9 processor, 32 GB of memory, and an Nvidia GPU GeForce RTX 2080 Ti with 11GB of dedicated memory.

Due to the strict requirements and the dependency from screen resolution, we provide a VirtualBox virtual machine image. We selected VirtualBox since it should work on most operative systems, i.e. Mac OSX, Windows and Ubuntu. The virtual machine should be considered only for demo purposes. To carry on experiments, we suggest you to follow the [instructions on how to install DeepMetis-UnityEyes on a real machine](full_installation.md).

## Step 1: Configure the environment ##

This tool needs the UnityEyes and Sikuli to be installed on the machine where it is running. 

### Step 1.1: Java Installation ###

Download and install [Java SE 11](https://www.oracle.com/it/java/technologies/javase-jdk11-downloads.html). Official instructions [here](https://docs.oracle.com/en/java/javase/11/install/installation-jdk-microsoft-windows-platforms.html).

### Step 1.2: Python Installation ###

Install [_Python 3.7.9_](https://www.python.org/ftp/python/3.7.9/python-3.7.9-amd64.exe)

Check that you are using the correct version of python:
``` 
py.exe -V
```
This command should produce as output the following string: `Python 3.7.9`

To easily install the dependencies with pip, we suggest to create a dedicated virtual environment. For example, you can use `venv` and create a virtual environment called `.venv` inside the current folder (`DeepMetis-UE`):

```
python -m venv .venv
```

At this point, you need to activate the virtual environment:

``` 
.\.venv\Scripts\activate
```


At this point, upgrade `pip`:

```
py.exe -m pip install --upgrade pip

```

Update setuptools:
```
pip install setuptools --upgrade

```

Finally, install the other dependencies:
```
pip install -r requirements.txt
```


### Step 1.3: UnityEyes Installation and Configuration ###

* Download a free Windows version of UnityEyes from the [official website](https://www.cl.cam.ac.uk/research/rainbow/projects/unityeyes/data/UnityEyes_Windows.zip).  
* Edit the UNITYEYES_PATH in [properties.py](properties.py) by inserting the path to your UnityEyes folder. 
* Pin the UnityEyes application to the taskbar: [instructions here](https://support.microsoft.com/en-us/windows/pin-apps-and-folders-to-the-desktop-or-taskbar-f3c749fb-e298-4cf1-adda-7fd635df6bb0)

### Step 1.4: SikuliX Installation and Configuration ###

The folder Sikuli-jars contains a version of SikuliX downloaded from the [official website](http://sikulix.com). We use it to allow the interaction of DeepMetis with UnityEyes via GUI. SikuliX works based on scanning the screen for particular elements to interact with, for example, an app icon to click on. Therefore, for each system the user should provide screenshots of GUI widgets to interact with. As screen resolutions and colours might differ from one computer to another, the screenshots we provide with our SikuliX scripts might not work on other computers. In the following, we will provide instructions on how to re-capture these images. To this aim, we provide the whole window along with the specific widget to crop, i.e. the one highlighted with a pink frame.

* In the taskbar, take a screenshot of the highlighted component (i.e., UnityEyes icon) and save it as eye.png

![eye](../images/eye.PNG)

* Start UnityEyes and from the starting window take a screenshot of the highlighted component (i.e., play button) and save it as play.png

![play](../images/play.PNG)

* Press the play button and from the main window take a screenshot of the highlighted component (i.e., first edit text widget) and save it as first.png

![first](../images/first.PNG)

* From the UnityEyes' main window take a screenshot of the highlighted component (i.e., second edit text widget) and save it as second.png

![second](../images/second.PNG)

* From the UnityEyes' main window take a screenshot of the highlighted component (i.e., start button) and save it as start.png

![start](../images/start.PNG)

* From the UnityEyes' main window take a screenshot of the highlighted component (i.e., close window button) and save it as x.png

![X](../images/X.PNG)

* Save all the captured images in the [sikulix_scripts/unityeyes.sikuli folder](sikulix_scripts/unityeyes.sikuli/)


> **NOTE**: We already provided examples of these images in the [sikulix_scripts/unityeyes.sikuli folder](sikulix_scripts/unityeyes.sikuli/) but you most probably have to replace them to match your own screen resolution.

* Run the Sikulix IDE in [Sikulix_jars/sikulixide-2.0.4.jar](Sikulix_jars/) (you can simply double click on it). It will automatically install the Jython standalone version.
* Open [sikulix_scripts/unityeyes.sikuli/unityeyes.py](sikulix_scripts/unityeyes.sikuli/unityeyes.py) inside the Sikulix IDE.
* Press the Run button to verify that the Sikulix script is able to find and interact with all the GUI widgets

> **NOTE**: If Sikulix cannot find a widget, please capture it again (try to focus on the element and capture pixels that will always be present around the element).

> **NOTE**: Please note that a computer should have a monitor connected for SikuliX to work. Please, also note that pop-up windows (such as the notification of a low battery) can disrupt the work of SikuliX.


## Step 2: Run DeepMetis

Use the following command to start the SikuliX server:

```
python test.py
```

Use the following command to start a run of DeepMetis-UE:

```
python main.py
```

> NOTE: The user must not interact with the PC during the run

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


### Evaluate the augmented test set with DeepCrime

Once DeepMetis has generated inputs for the mutant, we check whether augmentation with these inputs makes the mutant killed.
First we run the evaluation step analogous to the one in DeepCrime with the initial test set, i.e. without adding the
generated inputs. Then, we augment the test set with generated inputs and run the evaluation again. To run the evaluation process,
please execute the following commands (please note that processing the inputs and evaluating the predictions will take some time):

```
cd evaluation
python evaluate_metis.py
cd ..
```

You will see two messages printed that would answer whether the mutant was killed by the original test set
andt by the augmented test set. The example:
```
Mutant killed by the original test set?: False

Mutant killed by the augmented test set?: True
```


## Step3: Replicate the results in the paper ##

At this step we provide scripts to extract the data reported in the paper from our overall experimental data.
All the experimental data is available in the subfolder named `experiments`. We have excluded the `.npy` files
of the generated images due to the size restrictions.

Run the following command to generate the UnityEyes data from Table 3 in the paper.

```
cd experiment
python replicate_table3.py
cd..
```

The script produces and saves the data for UnityEyes section of Table 3 to the file
named `summary.csv`. In addition, it generates the file `raw_data.csv` that provides information about each of 10 runs for each mutant.


Run the following command to generate the UnityEyes data from Table 4 in the paper. The produced the data for UnityEyes section of Table 4 is stored in the file named `leave_one_out.csv`.

```
cd experiment
python3 replicate_table4.py
cd ..
```

## Reuse DeepMetis ##

### Run DeepMetis for any mutant ###

To run DeepMetis for any UnityEyes mutant available, we first need to download mutated models generated by the DeepCrime tool. 
These models are available in the artifacts (deepcrime-unityeyes.zip) provided by the authors of DeepCrime paper at the following links:

https://zenodo.org/record/4737645

The artifacts contain `h5` files that names of which correspond to one of the 20 instances of a mutation operator run with a specific parameter. 
The names have the following structure: 

`{subject_name}_{mutation_operator}_MP_{parameter_value}_{instance_num}.h5`

> NOTE: For UnityEyes subject, the 'subjec_name' is 'lenet'.

For example, `lenet_add_noise_mutated0_MP_25.0_0.h5` corresponds to the first instance of the mutant generated by applying "Add Noise" operator to the 25%  of the training data. As noted before, each mutant has 20 instances. 

In our replication package we provide models for only one mutant (`lenet_add_activation_function_mutated0_MP_softsign_9` used at Step 2) due to the large size of `h5` files.

To run DeepMetis for some other mutant, copy the `h5` files that represent instances of that mutant to the folder `DeepMetis-UE/mutant_models`. 
The number of instances of the mutant copied into this folder correspond to the setting of the DeepMetis that you want to use,
i.e. if you copy 5 instances of the mutant then you will run DeepMetis in `1vs5` setting. Correspondingly, if you copy 10 instances then 
you will run DeepMetis in `1vs10` setting.
Once the desired number of instances has been copied, run the following command:

```
python main.py
```

### Explore all the data generated as part of the paper ###

We provide all the data collected during our experiments. The data in the folder `DeepMetis-UE/experiment`
in this git repository contains all the data except the images generated by the
test input generators. We excluded the images due to the overall size. However, we have uploaded all the data
including also images to Zenodo at the following link:

https://zenodo.org/record/{TO_BE_ADDED}

The data related to UnityEyes case study is located in the UE.zip file of the Zenodo submission. Once this file is unzipped the folder UE
will contain the following folders and files:

1. Folder `deepmetis` which contains 4 subfolders `deepmetis_1vs1`, `deepmetis_1vs5`, `deepmetis_1vs10`, `deepmetis_1vs20` that contain all the CSV files with intermediate results. The subfolders correspond to the
setting with which DeepMetis was run (i.e. `1vs1`, `1vs5`, `1vs10` and `1vs20`). Each of these subfolders contain 10 folders
for each of the 10 mutants used in our study. Each mutant folder contains the file `output.csv` and 10 folders named from 0 to 9 that correspond to each of the 10 runs. 
The file `output.csv` contains overall information about all 10 runs, indicating for each of them the number of inputs generated in the second column. For the mutation operators with 
range-based parameters in the second column it reports the outcome of the binary search for the augmented test set. In contrast, for the mutation operators with 
non range-based parameters it indicates whether the mutant becomes killed once the test set is augmented.
The folder for each run contains more detailed information such as the files generated by DeepCrime for each mutant. Moreover,
it contains the folder `results` that stores the output of DeepMetis. The structure of the DeepMetis' output is explained at Step 2.

2. Folder `deepjanus` has same structure as the folder `deepmetis` with the only difference being
the absence of setting specific folders such as `1vs1`, `1vs5`, `1vs10` and `1vs20`.

3. Folder `leave_one_out_RQ4` contains information regarding the experiments conducted for
RQ4. The folder contains CSV files with the results of the experiment for each of the 10 mutants. Each mutant file reports overall information for each of the 10 runs. The first column indicates the number of the population, the second - the number of DeepMetis generated inputs, the third shows whether the mutant got killed or not, the fourth and the fifth columns report p_value and effect size calculated by DeepCrime.

5. File `statistical_test_results.xlsx` reports p-values, effect size and confidence intervals calculated
when comparing DeepMetis to other input generation tools.

6. File `raw_data.csv` contains raw data regarding all the test input generators used 
in the study. Each column name has the structure `{mutation_operator}_{toolsetting}_{I or MS}`. The columns finishing with `I` report the number of inputs generated, while the columns finishing with `MS` indicate the mutation score or whether the mutant was killed. 
Step 3 of the replication package indicates how this file can be generated automatically.

7. File `summary.csv` contains UnityEyes data reported in Table 3 of the paper. Step 3 of the replication package indicates how this file can be generated automatically.
<!--
### Configure a different number of runs and mutants ###

The numbers of runs and mutants can be set in the launcher `main_launcher_examplerun.py`. The number of runs can be indicated by using parameter `-run_num`. DeepMetis runs in `1vs5` mode by default. The number of used mutant instances can be indicated using the parameter `-mutant_num`. For example, the following command will perform 3 runs of DeepMetis in `1vs10` mode:

```
python3 main_launcher_examplerun.py -run_num=3 -mutant_num=10
```
-->

## Troubleshooting ##

### ImportError: Could not find the DLL(s) msvcp140.dll ### 
This issue can be resolved by dowloading and installing [vc_redist.exe](https://support.microsoft.com/en-us/topic/the-latest-supported-visual-c-downloads-2647da03-1eea-4433-9aff-95f26a218cc0)

### python command is not recognised ###
If you have python installed by some other way, for example from executable installer, to run the scripts you may need to use 'py' command instead of 'python':
```
py main.py
```
