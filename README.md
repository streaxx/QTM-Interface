# Quantitative Token Model radCAD Integration

! This repository is a work in progress !

## Background

The [Quantitative Token Model (QTM)](https://outlierventures.io/quantitative-token-model-a-data-driven-approach-to-stay-ahead-of-the-game/) is an open source spreadsheet model developed by [Outlier Ventures](https://outlierventures.io/). It's purpose is to forecast key metrics of different token economies on a higher level by abstracting a set of often leveraged token utilities. It should be used for educational purposes only and not to derive any financial advise. The market making for the token is approximated by a DEX liquidity pool with [constant product relationship](https://balancer.fi/whitepaper.pdf).

## QTM Structure

![Quantitative Token Model](https://github.com/BlockBoy32/QTM-Interface/blob/main/images/Quantitative_Token_Model_Abstraction.jpeg?raw=true)

## Motivation for the radCAD Extension

The goal of the QTM radCAD integration is to extend and to improve the static high-level approach of the QTM spreadsheet model to a more flexible and dynamic one. With the radCad integration one should be able to perform parameter sweeps and optimizations. Furthermore it opens up the capabilities for more dynamic agent behaviors, Monte Carlo runs, and Markov decision trees, which reflect a more realistic approximation of a highly non-linear web3 token ecosystem. At a later stage there should also be a more accessible (web-based) UI.

## Development Roadmap

### V.1

- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Initialize the project, create the development roadmap & README.md
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Implement interface to the QTM spreadsheet parameters
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Update the postprocessing in the `post_processing.py` with respect to the new QTM parameters and conventions
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Update the plot functionallities in the `plots.py` with respect to the new parameter conventions
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the vesting policies
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the incentivisation module
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the airdrop module
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the static agent behavior
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the utility policies
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the liquidity pool interactions
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the user adoption policies
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test protocol bucket allocations
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Build and test the rest of token ecosystem KPIs / metrics
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Update the postprocessing w.r.t. the new implemented policies and corresponding state variables
- ![#c5f015](https://placehold.co/15x15/FFF266/FFF266.png) Web based UI for result output plots
- ![#c5f015](https://placehold.co/15x15/FFF266/FFF266.png) Improve function & overall code documentation
- ![#c5f015](https://placehold.co/15x15/FFF266/FFF266.png) Improve the robustness of all functions
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Improve the robustness of all model input parameter
- ![#c5f015](https://placehold.co/15x15/c5f015/c5f015.png) Staging tests of the whole model
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Develop risk analysis procedures
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Case studies & publishing first results in an article
- ![#c5f015](https://placehold.co/15x15/FFF266/FFF266.png) Write the documentation for the QTM and radCAD integration

### V.2

- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Build a web-based UI to create another input option
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Add more dynamic agent (behavior) policies
  - ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Stochastic agents
  - ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Intelligent agents I: Hard coded logics
  - ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Intelligent agents II: LLM driven decision making
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Parameter Optimization
  - ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Implement and test parameter sweep capabilities
  - ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) Add advanced optimization procedures

## Installation

Python 3.9 is recommended!

- Clone this repository to your local machine by `git clone https://github.com/BlockBoy32/QTM-Interface.git`
- Create a new Python environment in the projects directory by `python -m venv venv`
- Activate the new environment by `source venv/bin/activate`
- Install all required packages by `pip install -r requirements.txt`

## Usage

### Parameters

Most of the input parameters are contained in the `./data/Quantitative_Token_Model_V1.88_radCad_integration - radCAD_inputs.csv` file. It can be generated by saving the `cadCAD_integration` tab of the [QTM spreadsheet model](https://drive.google.com/drive/folders/1eSgm4NA1Izx9qhXd6sdveUKF5VFHY6py?usp=sharing) as `.csv` file and to replace it for the default parameter set `./data/Quantitative_Token_Model_V1.88_radCad_integration - radCAD_inputs.csv`.

Note that at the current development stage some aspects are still hard coded, such as some agents behaviors. This will become more flexible in future versions.

### Simulation Settings

The prescribed simulation timestep is fixed to 1 month.
The user can adjust the length of the simulation by changing the `TIMESTEPS` parameter in the `./Model/simulation.py` file.

### Run Simulations

- Go with your terminal to the `./Model/` directory.
- Run `python simulation.py` within the environment.

### Module Process Idea

Create a function that combines all of these into a single file

    1. Add parameters to ingest external data
    2. Function to intialize values in state variables
    3. The policy and state update functions
    4. Update state update block file
    5. Post processing and plots to display it
