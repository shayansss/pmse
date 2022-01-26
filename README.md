# PMSE: Pointwise Mean Squared Error
This repository contains the implementation and dataset files of the "PMSE" metric, described in our published paper, entitled "[A Pointwise Evaluation Metric to Visualize Errors in Machine Learning Surrogate Models](https://shayansss.github.io/files/2021_11.pdf)".

PMSE is a simple metric to visualize the correlations between the errors of the machine learning surrogates and corresponding numerical models. Here, we used a simple Keras neural network for surrogate modeling and a finite element method for numerical modeling. The idea is to accelerate the numerical simulation by the surrogate, which is evaluated via the PMSE, and other relevant metrics, during training.

## Citation
If this research data is useful for your work, kindly please consider citing our work ([DOI](http://dx.doi.org/10.3233/FAIA210386) | [PDF](https://shayansss.github.io/files/2021_11.pdf)):

```
@InProceedings{sajjadinia2021c,
    author = {Seyed Shayan Sajjadinia and Bruno Carpentieri and Gerhard A. Holzapfel},
    title = {A pointwise evaluation metric to visualize errors in machine learning surrogate models},
    booktitle = {Proceedings of CECNet 2021},
    series = {Frontiers in Artificial Intelligence and Applications},
    volume = 345,
    month = nov,
    year = 2021,
    editor = {Antonio J. Tall\'{o}n-Ballesteros},
    pages = {26-34},
    publisher = {IOS Press},
    doi  = {10.3233/faia210386},
}
```

## Software dependency
For the machine learning implementation:

- Python >= 3.8.8
- Jupyter Notebook >= 6.3.0
- matplotlib >= 3.3.4
- numpy >= 1.20.1
- scikit-learn >= 0.24.1
- tensorflow >= 2.5.0
- keras >= 2.4.3
- h5py = 2.10.0

For generation of datasets and contour plots:
- Abaqus/CAE >= 2020

## Installation
Download the archive file using `git clone https://github.com/shayansss/pmse`, and then, set the address of the root directory of the repository by changing the default values that are fed to: 1) the `parentFolder` variable in the `abaqus` function in the Jupyter Notebook file (i.e., `ml.ipynb`); 2) the `os.chdir` function in the Python files (i.e., `dataset_generation.py` and `Visualization.py`). Also, ensure that you have installed all the dependencies. The python libraries can be easily installed by Anaconda, while you need to only install the full version of the Abaqus/CAE (for visualization and data set generation). For more, please refer to their installation documentation.

## Dataset preparation
We provided all the datasets, including the inputs (in `input_2d.csv`), the outputs (in `output_2d.csv`), and the numerical data generation runtime per second (in `time_output_2d.csv`). All the rows refer to a machine learning sample in these files, except for the output dataset, in which we use several lines of rows for each sample as each row refers to a nodal point of the sample. In the Notebook file, the datasets are first loaded and reshaped, and then, they are normalized before training.

If you desire to generate the datasets by yourself, first delete the current CSV files, then use this command: `abaqus cae noGui=dataset_generation.py`, which automatically generates the datasets. Note that depending on your system it may take between minutes to hours to have all the datasets. 

## Experiment workflow
By running the Jupyter Notebook file, the model is trained by the `run` function, while we extract all the visualization data using `matplotlib`. In addition, for the PMSE, we use also the `Abaqus` function that calls Abaqus/CAE to save the contours via another script, i.e., `Visualization.py`. All the results are then saved in the root directory.

## Evaluation and expected results
While the model is trained, it automatically saves the errors over the test set in 6 groups every 40 epoch. These values are used to extract the snapshots of the absolute errors and PMSE contours, and also, to plot the mean squared errors and the box plot of the squared errors v.s. the number of epochs.

## Experiment customization
In the Jupyter Notebook file, you may change the arguments of the 'run' function to set a different architecture of the neural networks. You may also change the numerical model and physics problem, but for this, you should use `abq.cae` in Abaqus and update all the python scripts then. This is not trivial, and you may need to refer to the <a href="https://www.3ds.com/products-services/simulia/services-support/support/documentation/" target="_blank">Abaqus manual</a>.
