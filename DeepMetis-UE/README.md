# DeepMetis: UnityEyes

## General Information ##
This folder contains the application of the DeepMetis approach to the eye gaze prediction problem.
This tool is developed in Python on top of the DEAP evolutionary computation framework. It has been tested on a Windows 10 machine equipped with a i9 processor, 32 GB of memory, and an Nvidia GPU GeForce RTX 2080 Ti with 11GB of dedicated memory.

Due to the strict requirements and the dependency from screen resolution, we provide a VirtualBox virtual machine image. We selected VirtualBox since it should work on most operative systems, i.e. Mac OSX, Windows and Ubuntu. The virtual machine should be considered only for demo purposes. To carry on experiments, we suggest you to follow the [instructions on how to install DeepMetis-UnityEyes on a real machine](full_installation.md).

## Step 1: Configure the Environment ##

This step is to configure DeepMetis on a virtual machine. If you want to do it on a real machine use the [following instructions](full_installation.md).

> NOTE: the size of the VM image is ~15 GBs

*Important Note:* We tested our VM image on three different Windows 10 machines and on a MacBook Pro with macOS 10.15 (Catalina). The VM is equipped with Windows 10 OS and we cannot guarantee DeepMetis-UE works with other Windows versions.    

To import the virtual image, you should install [Oracle VM VirtualBox 6.1.22](https://www.virtualbox.org/wiki/Downloads) for your platform and [VirtualBox 6.1.22 Oracle VM VirtualBox Extension Pack](https://download.virtualbox.org/virtualbox/6.1.22/Oracle_VM_VirtualBox_Extension_Pack-6.1.22.vbox-extpack).  

Download our [ova](https://usi365-my.sharepoint.com/:u:/g/personal/ricciv_usi_ch/ETSI_NV3zkdEqXTYl88hk5EBZFNw7gBOGMRnTaAjjS-OmA?e=yrMPCW).  

Import and start the virtual image. See the official instructions [here](https://docs.oracle.com/cd/E26217_01/E26796/html/qs-import-vm.html).   

Provide the password `ase2021` to the Windows 10 initial screen.

> NOTE: Please close other resource-demanding applications before running the virtual image


## Step 2: Run DeepMetis

> NOTE: Before starting a run of DeepMetis, ensure that you deleted or removed the folder named `results` in the DeepMetis-MNIST main folder, otherwise you can use the existing `results` to directly perform the [evaluation step.](#Evaluate-the-augmented-test-set-with-DeepCrime)

Open terminal and go in the directory where DeepMetis is installed. In the virtual machine, the command is the following:

```
cd C:\Users\ASE2021\deepmetis\DeepMetis-UE
```

If you used a virtual environment, as in the virtual machine, activate the virtual environment.

```
.\.venv\Scripts\activate
```

Use the following command to start the SikuliX server:

```
python test.py
```

Open another terminal instance and start a run of DeepMetis-UE:

```
cd C:\Users\ASE2021\deepmetis\DeepMetis-UE
.\.venv\Scripts\activate
python main.py
```

> NOTE: The user must not interact with the PC during the run

> NOTE: One run take up to 1 hour or more on a physical machine, depending on the hardware specifications of the machine (instead, on the virtual machine, it could more than 10 hours). Therefore in the VM, we configured a short run of 3 iterations that should take less time. To perform a longer run, the user should modify the value of the variable `NGEN` in `properties.py` to the desired number of iterations. As an example, to perform the same number of iteration of the experimental evaluation, NGEN should be set to 100

When the run ends, on the console you should see a message similar to the following:

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
generated inputs. Then, we augment the test set with generated inputs and run the evaluation again. To run the evaluation process, please execute the following commands (please note that processing the inputs and evaluating the predictions will take some time):

```
cd evaluation
python evaluate_metis.py
cd ..
```

You will see two messages printed that would answer whether the mutant was killed by the original test set
and by the augmented test set. The example:
```
Mutant killed by the original test set?: False

Mutant killed by the augmented test set?: True
```
> NOTE: with the VM, the evaluation will take > 5 minutes

> NOTE: Since a DeepMetis run can be long, we provide an example results folder in the VM named `results_old` placed in the DeepMetis-UE main folder. To use this instead of a user-generated results folder, the user should rename it from `results_old` to `results` and then run `evaluate_metis.py`.

## Step 3: Replicate the results in the paper ##

At this step we provide scripts to extract the data reported in the paper from our overall experimental data.
All the experimental data is available in the subfolder named `experiment`. We have excluded the `npy` files
of the generated images due to the size restrictions.

Run the following command to generate the UnityEyes data from Table 3 in the paper.

```
cd experiment
python replicate_table3.py
cd ..
```

The script produces and saves the data for UnityEyes section of Table 3 to the file
named `summary.csv`. In addition, it generates the file `raw_data.csv` that provides information about each of 10 runs for each mutant.


Run the following command to generate the UnityEyes data from Table 4 in the paper. The produced the data for UnityEyes section of Table 4 is stored in the file named `leave_one_out.csv`.

```
cd experiment
python replicate_table4.py
cd ..
```

## Reuse DeepMetis ##

### Run DeepMetis for any mutant ###

To run DeepMetis for any UnityEyes mutant available, we first need to download mutated models generated by the DeepCrime tool. 
These models are available in the artifacts (`deepcrime-unityeyes.zip`) provided by the authors of DeepCrime paper at the following link:

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

To apply DeepMetis to the mutants that were not used in our or DeepCrime's experiments, the user first needs
to generate them. The instructions on how to generate mutants using DeepCrime are provided in the tool's own replication package
available at the following link:

https://zenodo.org/record/4772465

Once  the `h5` files of the mutant are obtained, the process of running DeepMetis is the  same, i.e. we need (as per above instructions) to copy `h5` into corresponding folders and run 
`main.py`.

### Explore all the data generated as part of the paper ###

We provide all the data collected during our experiments. The data in the folder `DeepMetis-UE/experiment`
in this git repository contains all the data except the images generated by the
test input generators. We excluded the images due to the overall size. However, we have uploaded all the data
including also images to Zenodo at the following link:

https://zenodo.org/record/5105742

The data related to UnityEyes case study is located in the UE.zip file of the Zenodo submission. Once this file is unzipped, the folder UE
will contain the following folders and files:

1. Folder `DeepMetis` contains the raw results: images in `jpg` and `npy` formats and `json` files capturing specification of these images. The folder has the following structure:
  * `raw_results` subfolder stores raw results for each mutant that was used in the paper. In each mutant folder there are 4 subfolers `deepmetis_1vs1`, `deepmetis_1vs5`, `deepmetis_1vs10`, `deepmetis_1vs20` - one for each of the applied setting of the tool. Then, for each setting there are outputs for 10 runs stored in `result_i_` folder, where `_i_` corresponds to the number of the run. The structure of the DeepMetis output is explained at Step 2.

2. Folder `DeepJanus` that similarly to `DeepMetis` one contains the raw results generated by DeepJanus tool: images in `jpg` and `npy` formats and `json` files capturing specification of these images. The folder has the following structure:
  * `raw_results` subfolder stores raw results for each of the 10 runs. The structure of the results folder is similar to the one of DeepMetis, with the only difference that `archive` folder has 2 subfolders named `correct` and `incorrect` containing the images generated by DeepJanus that are correctly and incorrectly predicted by the model that was given to the tool for input generation.

3. Folder `experiment` that contains experimental data in the form results and evaluations saved in `CSV` files. It has the following structure:
  * Folder `deepmetis` which contains 4 subfolders `deepmetis_1vs1`, `deepmetis_1vs5`, `deepmetis_1vs10`, `deepmetis_1vs20` that contain all the CSV files with intermediate results. The subfolders correspond to the setting with which DeepMetis was run (i.e. `1vs1`, `1vs5`, `1vs10` and `1vs20`). Each of these subfolders contain 10 folders for each of the 10 mutants used in our study. Each mutant folder contains the file `output.csv` and 10 folders named from 0 to 9 that correspond to each of the 10 runs. The file `output.csv` contains overall information about all 10 runs, indicating for each of them the number of inputs generated in the second column. For the mutation operators with range-based parameters in the third column it reports the outcome of the binary search for the augmented test set. In contrast, for the mutation operators with non range-based parameters it indicates whether the mutant becomes killed once the test set is augmented.
The folder for each run contains more detailed information such as the files generated by DeepCrime for each mutant.

  * Folder `deepjanus` has same structure as the folder `deepmetis` with the only difference being the absence of setting specific folders such as `1vs1`, `1vs5`, `1vs10` and `1vs20`.

  * Folder `leave_one_out_RQ4` contains information regarding the experiments conducted for RQ4. The folder contains CSV files with the results of the experiment for each of the 10 mutants. Each mutant file reports overall information for each of the 10 runs. The first column indicates the number of the population, the second - the number of DeepMetis generated inputs, the third shows whether the mutant got killed or not, the fourth and the fifth columns report p_value and effect size calculated by DeepCrime.

  * File `statistical_test_results.xlsx` reports p-values, effect size and confidence intervals calculated when comparing DeepMetis to other input generation tools.

  * File `raw_data.csv` contains raw data regarding all the test input generators used in the study. Each column name has the structure `{mutation_operator}_{toolsetting}_{I or MS}`. The columns finishing with `I` report the number of inputs generated, while the columns finishing with `MS` indicate the mutation score or whether the mutant was killed.  Step 3 of the replication package indicates how this file can be generated automatically.

  * File `summary.csv` contains UnityEyes data reported in Table 3 of the paper. Step 3 of the replication package indicates how this file can be generated automatically.
 
  * File `leave_one_out.csv` contains UnityEyes data reported in Table 4 of the paper. Step 3 of the replication package indicates how this file can be generated automatically.
 

### Configure a different number of runs and mutants ###

To perform more runs of DeepMetis, i.e. use more than 1 initial population, please change the `NUM_RUNS` parameter in the `properties.py` file. It can take values from 1 to 10. The number of mutants used to perform the runs (the setting of the tool, for example `1vs5`) is defined by the number of mutated models that were put to the `mutant_models` folder. After setting the desired number of runs, to run DeepMetis please execute the following command:

```
python main_launcher.py

```


## Troubleshooting ##

### ImportError: Could not find the DLL(s) msvcp140.dll ### 
This issue can be resolved by dowloading and installing [vc_redist.exe](https://support.microsoft.com/en-us/topic/the-latest-supported-visual-c-downloads-2647da03-1eea-4433-9aff-95f26a218cc0)

### python command is not recognised ###
If you have python installed by some other way, for example from executable installer, to run the scripts you may need to use 'py' command instead of 'python':
```
py main.py
```

### VirtualBox fails to import the ova ###
Ensure to have downloaded also the [VirtualBox 6.1.22 Oracle VM VirtualBox Extension Pack](https://download.virtualbox.org/virtualbox/6.1.22/Oracle_VM_VirtualBox_Extension_Pack-6.1.22.vbox-extpack).

### DeepMetis runs up to the last iteration, but at the end of it shows an assertion error (the length of the solution list is not equal to that of the archive) ###
Ensure to have deleted or renamed the `results` folder before starting a DeepMetis run.

### SikuliX fails to correctly interact with the GUI ###
* Run the Sikulix IDE in [Sikulix_jars/sikulixide-2.0.4.jar](Sikulix_jars/) (you can simply double click on it). It will automatically install the Jython standalone version.
* Open [sikulix_scripts/unityeyes.sikuli/unityeyes.py](sikulix_scripts/unityeyes.sikuli/unityeyes.py) inside the Sikulix IDE.
* Press the Run button to verify that the Sikulix script is able to find and interact with all the GUI widgets
* Try to increase the wait times in the [sikulix_scripts/unityeyes.sikuli/unityeyes.py](sikulix_scripts/unityeyes.sikuli/unityeyes.py) script
