# 🎁 Toy Distribution Optimization

A project developed for the **Analysis and Synthesis of Algorithms** course.

## 📖 Overview

This project optimizes the distribution of Christmas toys to children around the world.

Given a set of factories, countries, production limits, export constraints, and children's toy requests, the program computes the maximum number of children whose requests can be satisfied while respecting all distribution constraints.

The solution is modeled and solved as a linear programming optimization problem using PuLP.

## ✨ Features

* 🎁 Toy request allocation
* 🏭 Factory stock management
* 🌍 Country export constraints
* ⚖️ Minimum distribution guarantees per country
* 📈 Optimization of satisfied requests
* 🧮 Linear programming model using PuLP

## 🛠️ Built With

* Python
* PuLP

## ⚙️ Installation

Install PuLP:

```bash
pip install pulp
```

Optionally, install the GLPK solver:

```bash
sudo apt-get install glpk-utils
```

## ▶️ Running

Run the program using:

```bash
python3 project.py < input.txt
```

## 📄 Additional Information

For a detailed description of the project requirements, please refer to the project specification PDF included in this repository.
