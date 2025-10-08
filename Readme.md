# CSVC-PSO: 基于支持向量分类器的粒子群优化算法

[![GitHub](https://img.shields.io/badge/GitHub-gaomn/CSVC--PSO-blue)](https://github.com/gaomn/CSVC-PSO)
[![Paper](https://img.shields.io/badge/Paper-IEEE%20SSCI%202023-red)](https://ieeexplore.ieee.org/)

[English](README_EN.md) | [中文](readme.md)

## 📄 论文信息

本仓库是以下论文的官方实现：

**"A Clustering-Based Support Vector Classifier for Dynamic Time-Linkage Optimization"**

*发表于: IEEE Symposium Series on Computational Intelligence (SSCI) 2023*

### 引用格式

如果您在研究中使用了本代码，请引用我们的论文：

```bibtex
@inproceedings{gao2023csvc,
  title={A Clustering-Based Support Vector Classifier for Dynamic Time-Linkage Optimization},
  author={Gao, M. and Liu, X.-F. and Zhan, Z.-H. and Zhang, J.},
  booktitle={2023 IEEE Symposium Series on Computational Intelligence (SSCI)},
  year={2023},
  pages={953--958},
  address={Mexico City, Mexico},
  doi={10.1109/SSCI52147.2023.10371998},
  organization={IEEE}
}
```

## 摘要

本项目实现并测试了基于支持向量分类器的粒子群优化 (CSVC-PSO) 算法，并在动态多峰基准 (Moving Peaks Benchmark, MPB) 问题上进行了测试。该项目旨在研究和评估支持向量分类器在动态优化问题中的有效性。

## 主要特点

- **多算法对比**: CSVC-PSO、标准PSO和最优解三种算法的对比
- **动态基准测试**: 使用动态多峰基准问题进行算法评估
- **自动化实验管理**: 支持多参数配置和实验结果的自动保存
- **并行处理**: 利用多进程并行执行实验以提高效率
- **可视化工具**: 提供自动化的结果可视化工具

## 🚀 快速开始

```bash
# 创建conda环境
conda create --name cldm python=3.9
conda activate cldm

# 安装依赖
pip install -r requirements.txt

# 运行项目
python main.py
```

## 主要代码文件

- `main.py`: 项目的主执行脚本，负责初始化参数、设置实验、运行优化算法并保存结果
- `configs.py`: 定义和管理所有实验参数，使用 `argparse` 库进行配置
- `csvc_component/`: 核心算法组件目录
  - `demo.py`: 包含 `CSVC_PSO`, `Optimal`, `PSO_only` 等高层算法的实现逻辑
- `draw_tool/`: 包含用于结果可视化的工具

## 参数配置

所有实验参数都在 `configs.py` 文件中通过 `argparse` 定义。您可以直接修改此文件中的默认值，或者在运行 `main.py` 时通过命令行参数来覆盖它们。

### 主要参数类别

- **MPB 环境参数**: `s_dim`, `x_dim`, `x_bound`, `peak_num`, `peak_h`, `peak_w`, `peak_sigma`, `time_fac`, `max_step`, `bt_type` 等
- **PSO 算法参数**: `Population_size`, `Iteration_number`, `Inertia_weight`, `Individual_learning_factor`, `Social_learning_factor`, `Max_vel` 等
- **模型特定参数**: `if_crossing`, `if_detection`, `mode`, `delta`, `svm_kernel` 等
- **训练和实验参数**: `rand_seed`, `MPB_seed`, `filename`, `sample_num`, `b_list`, `bt_type_list`, `bt_change`, `using_multiprocessing` 等

### 重点参数说明

- `--using_multiprocessing` (布尔型, 默认: `True`): 是否使用多进程并行运行多个样本实验
- `--bt_type_list` (字符串列表, 默认: `['linear']`): 基础环境类型列表，可选值：`'linear'`, `'sin'`, `'cir'`
- `--b_list` (列表, 默认: `[100]`): 时间因子 `b` 的列表，影响 MPB 环境中时链特性的强度
- `--sample_num` (整型, 默认: `10`): 每个参数组合下独立运行的样本数量

## 数据保存

实验结果和生成的数据主要保存在 `data_save/` 目录下：

- **运行数据**: 每个实验运行的详细数据以 CSV 文件的形式保存在 `data_save/run_data/{timestamp}_{mode}/{bt_type}_b{b_value}/` 路径下
- **图形数据**: 实验结果的可视化图表会保存在 `data_save/fig_data/` 目录下

## 详细安装步骤

### 1. 安装 Conda

如果您尚未安装 Conda，请根据您的操作系统从以下链接下载并安装 Miniconda (推荐) 或 Anaconda：

- Miniconda: [https://docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html)
- Anaconda: [https://www.anaconda.com/products/distribution](https://www.anaconda.com/products/distribution)

### 2. 创建并激活 Conda 环境

```bash
# 进入项目根目录
cd path/to/your/project/all_in_cldm/codes/all_methods/csvc_pso

# 创建一个新的 conda 环境 (命名为 cldm)，并指定 Python 版本 (3.9)
conda create --name cldm python=3.9

# 激活新创建的环境
conda activate cldm
```

### 3. 安装依赖包

```bash
pip install -r requirements.txt
```

### 4. 运行代码

```bash
python main.py
```

您可以根据需要在命令后附加参数以修改默认配置，例如：

```bash
python main.py --mode csvc --sample_num 5 --using_multiprocessing True --bt_type_list linear sin --b_list 50 100
```

## 注意事项

- 确保您的计算机有足够的 CPU核心数 和 内存 来运行实验，特别是当 `using_multiprocessing` 设置为 `True` 且 `sample_num` 较大时
- 代码中会保留2个核心不被多进程池使用。如果您的计算机核心数较少，可能需要调整此值以避免资源耗尽
- 实验可能需要较长时间运行，具体取决于参数配置和迭代次数

## 项目结构

```
csvc_pso/
├── main.py                 # 主执行脚本
├── configs.py              # 参数配置文件
├── requirements.txt        # 依赖包列表
├── csvc_component/         # 核心算法组件
│   ├── CSVC_Model.py      # CSVC模型实现
│   ├── MPB.py             # 动态多峰基准
│   ├── PSO.py             # 粒子群优化算法
│   ├── Pearsonr.py        # 皮尔逊相关性
│   ├── buffer.py          # 数据缓冲区
│   └── demo.py            # 高层算法实现
├── draw_tool/              # 可视化工具
│   ├── draw.py            # 绘图函数
│   ├── test_all.py        # 测试工具
│   └── utils.py           # 工具函数
└── data_save/              # 保存的实验数据
    ├── run_data/          # 原始实验结果
    ├── fig_data/          # 生成的图表
    └── step_fig/          # 分步图表
```

## 许可证

本项目采用开源许可证发布。详情请参阅LICENSE文件。

## 致谢

本研究工作发表于IEEE SSCI 2023会议。感谢审稿人的宝贵意见和建议。

## 联系方式

如有任何问题或建议，欢迎通过GitHub Issues联系我们。
