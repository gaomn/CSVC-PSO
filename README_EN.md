# CSVC-PSO Project

[English](README_EN.md) | [中文](readme.md)

## Introduction

This project implements and tests the Support Vector Classifier-based Particle Swarm Optimization (CSVC-PSO) algorithm on Moving Peaks Benchmark (MPB) problems. The project aims to research and evaluate the effectiveness of support vector classifiers in dynamic optimization problems.

### Key Features

* Implements comparison between CSVC-PSO, standard PSO, and optimal solution algorithms
* Uses Moving Peaks Benchmark problems for algorithm evaluation
* Supports multi-parameter configuration and automatic result saving
* Utilizes multi-process parallel execution for improved efficiency
* Provides automated result visualization tools

## Main Code Files

* `main.py`: Main execution script of the project. Responsible for initializing parameters, setting up experiments, running optimization algorithms, and saving results.
* `configs.py`: Defines and manages all experimental parameters using the `argparse` library.
* `csvc_component/`: Directory containing core algorithm components:
  * `demo.py`: Contains implementation logic for high-level algorithms like `CSVC_PSO`, `Optimal`, `PSO_only`, etc.
* `draw_tool/`: Contains tools for result visualization.

## Parameter Configuration

All experimental parameters are defined in the `configs.py` file using `argparse`. You can directly modify the default values in this file or override them through command-line arguments when running `main.py`.

### Main Parameter Categories

* **MPB Environment Parameters**: `s_dim`, `x_dim`, `x_bound`, `peak_num`, `peak_h`, `peak_w`, `peak_sigma`, `time_fac`, `max_step`, `bt_type`, etc.
* **PSO Algorithm Parameters**: `Population_size`, `Iteration_number`, `Inertia_weight`, `Individual_learning_factor`, `Social_learning_factor`, `Max_vel`, etc.
* **Model-Specific Parameters**: `if_crossing`, `if_detection`, `mode`, `delta`, `svm_kernel`, etc.
* **Training and Experiment Parameters**: `rand_seed`, `MPB_seed`, `filename`, `sample_num`, `b_list`, `bt_type_list`, `bt_change`, `using_multiprocessing`, etc.

### Key Training and Experiment Parameters

The following are important training and experiment parameters defined in `configs.py`:

* `--using_multiprocessing` (Boolean, default: `True`): Whether to use multi-process parallel execution for multiple sample experiments. Setting to `True` can significantly speed up large-scale experiments.
* `--bt_type_list` (String list, default: `['linear']`): List of base environment types. Options: `'linear'`, `'sin'`, `'cir'`.
* `--b_list` (List, default: `[100]`): List of time factor `b` values, affecting the strength of time-linkage characteristics in MPB environment.
* `--sample_num` (Integer, default: `10`): Number of independent runs for each parameter combination.

## Data Storage

Experimental results and generated data are primarily saved in the `data_save/` directory:

* **Run Data**:
  * Detailed data from each experimental run is saved as CSV files in `data_save/run_data/{timestamp}_{mode}/{bt_type}_b{b_value}/` path.
  * Parameters for each experimental configuration are saved in the `parameters.txt` file in the corresponding directory.
* **Figure Data**:
  * Visualization charts of experimental results are saved in the `data_save/fig_data/` directory.

## How to Run the Code

### 1. Install Conda

If you haven't installed Conda yet, please download and install Miniconda (recommended) or Anaconda from the following links according to your operating system:

* Miniconda: [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
* Anaconda: [https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution)

After installation, ensure that the `conda` command is available in your terminal.

### 2. Create and Activate Conda Environment

Open a terminal (e.g., Anaconda Prompt, PowerShell, Git Bash, etc.) and execute the following commands:

```bash
# Navigate to project root directory
cd path/to/your/project/all_in_cldm/codes/all_methods/csvc_pso

# Create a new conda environment (named cldm) with Python 3.9
conda create --name cldm python=3.9

# Activate the newly created environment
conda activate cldm
```

### 3. Install Dependencies

In the activated `cldm` environment, install all required third-party libraries using the project's `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Run the Code

Once everything is ready, you can run the main script `main.py` to start the experiment:

```bash
python main.py
```

You can append parameters after the command to modify the default configuration as needed, for example:

```bash
python main.py --mode csvc --sample_num 5 --using_multiprocessing True --bt_type_list linear sin --b_list 50 100
```

### Important Notes

* Ensure your computer has sufficient CPU cores and memory to run the experiments, especially when `using_multiprocessing` is set to `True` and `sample_num` is large.
* The code reserves 2 cores that are not used by the multiprocessing pool. If your computer has fewer cores, you may need to adjust this value to avoid resource exhaustion.
* Experiments may take a considerable amount of time to run, depending on parameter configuration and iteration count.

## Project Structure

```
csvc_pso/
├── main.py                 # Main execution script
├── configs.py              # Parameter configuration
├── requirements.txt        # Dependencies
├── csvc_component/         # Core algorithm components
│   ├── CSVC_Model.py      # CSVC model implementation
│   ├── MPB.py             # Moving Peaks Benchmark
│   ├── PSO.py             # Particle Swarm Optimization
│   ├── Pearsonr.py        # Pearson correlation
│   ├── buffer.py          # Data buffer
│   └── demo.py            # High-level algorithm implementations
├── draw_tool/              # Visualization tools
│   ├── draw.py            # Drawing functions
│   ├── test_all.py        # Testing utilities
│   └── utils.py           # Utility functions
└── data_save/              # Saved experimental data
    ├── run_data/          # Raw experimental results
    ├── fig_data/          # Generated figures
    └── step_fig/          # Step-by-step figures
```

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

This project is open source. Please refer to the license file for details.