# Dependences
import pandas as pd
import numpy as np
import os
import sys
import traceback
import time

# radCAD
from radcad import Model, Simulation, Experiment
from radcad.engine import Engine, Backend


# Project dependences
# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one folder
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Append the parent directory to sys.path
sys.path.append(parent_dir)

from sys_params import *
import state_variables
import state_update_blocks
import sys_params
from parts.utils import *
from plots import *
from post_processing import *

import importlib
importlib.reload(state_variables)
importlib.reload(state_update_blocks)
importlib.reload(sys_params)

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go two folders up
parent_dir = os.path.abspath(os.path.join(os.path.abspath(os.path.join(current_dir, os.pardir)), os.pardir))

QTM_data_tables = pd.read_csv(parent_dir+'/data/Quantitative_Token_Model_V1.89_radCad_integration - Data Tables.csv')

if __name__ == '__main__'   :
    start_time = time.process_time()

    MONTE_CARLO_RUNS = 1
    TIMESTEPS = 12*10

    model = Model(initial_state=state_variables.initial_state, params=sys_params.sys_param, state_update_blocks=state_update_blocks.state_update_block)
    simulation = Simulation(model=model, timesteps=TIMESTEPS, runs=MONTE_CARLO_RUNS)

    result = simulation.run()
    df = pd.DataFrame(result)
    simulation_end_time = time.process_time()

    # post processing
    data_tx1 = postprocessing(df, substep=16) # after adoption buy lp tx
    data_tx2 = postprocessing(df, substep=19) # after vesting sell lp tx
    data_tx3 = postprocessing(df, substep=20) # after liquidity addition lp tx
    data_tx4 = postprocessing(df, substep=21) # after buyback lp tx
    postprocessing_one_start_time = time.process_time()
    data = postprocessing(df, substep=df.substep.max()) # at the end of the timestep = last substep
    postprocessing_all_end_time = time.process_time()


    ### BEGIN TESTS ###
    print("\n-------------------------------------------------------------------------------------------------------")
    print("\n-------------------------------------------## BEGIN TESTS ##-------------------------------------------")
    print("\n-------------------------------------------------------------------------------------------------------")
    print("\n")
    
    ### MODEL ###
    ## TEST ADOPTION ##
    print("\n-------------------------------------------## TEST ADOPTION ##-----------------------------------------")
    print("Testing adoption of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key='ua_product_users', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=7, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='ua_token_holders', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=8, relative_tolerance=0.003)

    
    ## TEST AGENT VESTING VALUES ##
    print("\n------------------------------------## TEST AGENT VESTING VALUES ##------------------------------------")
    print("Testing individual vesting values of radCad timeseries simulation against QTM data tables...")
    for i in range(len(stakeholder_names)-3):
        stakeholder = stakeholder_names[i]
        test_timeseries(data=data, data_key=stakeholder+"_a_tokens_vested", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=11+i, relative_tolerance=0.003)
    
    print("Testing cumulative vesting values of radCad timeseries simulation against QTM data tables...")
    for i in range(len(stakeholder_names)-3):
        stakeholder = stakeholder_names[i]
        test_timeseries(data=data, data_key=stakeholder+"_a_tokens_vested_cum", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=28+i, relative_tolerance=0.003)

    
    ## TEST FREE SUPPLY USAGE ##
    print("\n--------------------------------------## TEST FREE SUPPLY USAGE ##-------------------------------------")
    print("Testing free supply usage of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key='te_selling_perc', data_row_multiplier=100, QTM_data_tables=QTM_data_tables, QTM_row=45, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='te_utility_perc', data_row_multiplier=100, QTM_data_tables=QTM_data_tables, QTM_row=46, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='te_holding_perc', data_row_multiplier=100, QTM_data_tables=QTM_data_tables, QTM_row=47, relative_tolerance=0.003)


    ## TEST INCENTIVISATION ##
    print("\n---------------------------------------## TEST INCENTIVISATION ##--------------------------------------")
    print("Testing incentivisation of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key='te_minted_tokens', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=50, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='te_incentivised_tokens', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=51, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='te_incentivised_tokens_cum', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=52, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='te_incentivised_tokens_usd', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=54, relative_tolerance=0.004)


    ## TEST AIRDROPS ##
    print("\n------------------------------------------## TEST AIRDROPS ##------------------------------------------")
    print("Testing airdrops of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key='te_airdrop_tokens', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=57, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='te_airdrop_tokens_cum', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=59, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='te_airdrop_tokens_usd', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=61, relative_tolerance=0.003)


    ## TEST AGENT META BUCKET ALLOCATIONS ##
    print("\n--------------------------------## TEST AGENT META BUCKET ALLOCATIONS ##--------------------------------")
    print("Testing individual agent meta bucket allocations of radCad timeseries simulation against QTM data tables...")
    for i in range(len(stakeholder_names)-8):
        stakeholder = stakeholder_names[i]
        test_timeseries(data=data, data_key=stakeholder+"_a_selling_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=64+i, relative_tolerance=0.003)
        test_timeseries(data=data, data_key=stakeholder+"_a_utility_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=77+i, relative_tolerance=0.003)
        test_timeseries(data=data, data_key=stakeholder+"_a_holding_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=90+i, relative_tolerance=0.003)


    ## TEST META BUCKET ALLOCATION SUMS ##
    print("\n---------------------------------## TEST META BUCKET ALLOCATION SUMS ##---------------------------------")
    print("Testing meta bucket allocation sums of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key='te_selling_allocation', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=74, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='te_selling_allocation_cum', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=75, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='te_utility_allocation', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=87, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='te_utility_allocation_cum', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=88, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='te_holding_allocation', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=100, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='te_holding_allocation_cum', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=101, relative_tolerance=0.003)

    
    ## TEST META UTILITY SHARE ALLOCATIONS ##
    print("\n--------------------------------## TEST META UTILITY SHARE ALLOCATIONS ##-------------------------------")
    print("Testing meta utility share allocations of radCad timeseries simulation against QTM data tables...")
    # staking: apr
    test_timeseries(data=data, data_key='u_staking_base_apr_allocation', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=103, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='u_staking_base_apr_allocation_cum', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=110, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='u_staking_base_apr_rewards', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=162, relative_tolerance=0.003)
    
    # staking: revenue share
    test_timeseries(data=data, data_key='u_staking_revenue_share_allocation', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=104, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='u_staking_revenue_share_allocation_cum', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=111, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='u_staking_revenue_share_rewards', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=163, relative_tolerance=0.003)

    # staking: vesting schedule
    test_timeseries(data=data, data_key='u_staking_vesting_allocation', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=105, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='u_staking_vesting_allocation_cum', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=112, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='u_staking_vesting_rewards', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=164, relative_tolerance=0.003)
    
    # liquidity mining
    test_timeseries(data=data, data_key='u_liquidity_mining_allocation', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=106, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='u_liquidity_mining_allocation_cum', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=113, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='u_liquidity_mining_rewards', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=165, relative_tolerance=0.003)

    # burning
    test_timeseries(data=data, data_key='u_burning_allocation', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=107, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='u_burning_allocation_cum', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=114, relative_tolerance=0.003)
    # holding, cum comes later
    test_timeseries(data=data, data_key="u_holding_allocation", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=108, relative_tolerance=0.003)
    test_timeseries(data=data, data_key="u_holding_rewards", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=167, relative_tolerance=0.003)

    # transfer
    test_timeseries(data=data, data_key='u_transfer_allocation', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=109, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='u_transfer_allocation_cum', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=116, relative_tolerance=0.003)

    ## TEST ADOPTION 2 ##
    print("\n------------------------------------------## TEST ADOPTION 2 ##-----------------------------------------")
    print("Testing product revenue and token_buys of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key='ua_product_revenue', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=119, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='ua_token_buys', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=121, relative_tolerance=0.003)

    
    ## TEST TOKEN ALLOCATION REMOVAL ##
    print("\n-------------------------------## TEST TOKEN UTILITY REMOVAL ##------------------------------")
    print("Testing token utility removal of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key='te_remove_perc', data_row_multiplier=100, QTM_data_tables=QTM_data_tables, QTM_row=125, relative_tolerance=0.003)
    test_timeseries(data=data, data_key='u_staking_base_apr_remove', data_row_multiplier=-1, QTM_data_tables=QTM_data_tables, QTM_row=127, relative_tolerance=0.003, shift=1)
    test_timeseries(data=data, data_key='u_staking_revenue_share_remove', data_row_multiplier=-1, QTM_data_tables=QTM_data_tables, QTM_row=128, relative_tolerance=0.003, shift=1)
    test_timeseries(data=data, data_key='u_staking_vesting_remove', data_row_multiplier=-1, QTM_data_tables=QTM_data_tables, QTM_row=129, relative_tolerance=0.003, shift=1)
    test_timeseries(data=data, data_key='u_liquidity_mining_allocation_remove', data_row_multiplier=-1, QTM_data_tables=QTM_data_tables, QTM_row=130, relative_tolerance=0.003, shift=1)

    
    ## TEST BUYBACK FROM REVENUE SHARE FOR STAKERS ##
    print("\n----------------------------## TEST BUYBACK FROM REVENUE SHARE FOR STAKERS ##---------------------------")
    print("Testing token utility removal percentage of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key='u_buyback_from_revenue_share_usd', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=133, relative_tolerance=0.003)

    
    ## TEST SUM OF BUYBACKS ##
    print("\n----------------------------------------## TEST SUM OF BUYBACKS ##--------------------------------------")
    print("Testing sum of buybacks of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key='ba_buybacks_usd', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=137, relative_tolerance=0.003)

    ## TEST PROTOCOL BUCKET BURN ##
    print("\n----------------------------------------## TEST PROTOCOL BUCKET BURN ##--------------------------------------")
    print("Testing protocol bucket burn of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key='te_tokens_burned', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=141, relative_tolerance=0.003)


    ## TEST LIQUIDITY POOL TRANSACTIONS ##
    print("\n-------------------------------------## TEST LIQUIDITY POOL TRANSACTIONS ##-----------------------------------")
    print("Testing liquidity pool transactions of radCad timeseries simulation against QTM data tables...")
    print("Tx1 - after adoption..")
    test_timeseries(data=data_tx1, data_key='lp_tokens', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=144, relative_tolerance=0.003)
    test_timeseries(data=data_tx1, data_key='lp_usdc', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=145, relative_tolerance=0.003)
    test_timeseries(data=data_tx1, data_key='lp_token_price', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=146, relative_tolerance=0.003)
    print("Tx2 - after vesting sell..")
    test_timeseries(data=data_tx2, data_key='lp_tokens', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=147, relative_tolerance=0.003)
    test_timeseries(data=data_tx2, data_key='lp_usdc', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=148, relative_tolerance=0.003)
    test_timeseries(data=data_tx2, data_key='lp_token_price', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=149, relative_tolerance=0.003)
    print("Tx3 - after liquidity addition..")
    test_timeseries(data=data_tx3, data_key='lp_tokens', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=150, relative_tolerance=0.003)
    test_timeseries(data=data_tx3, data_key='lp_usdc', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=151, relative_tolerance=0.003)
    test_timeseries(data=data_tx3, data_key='lp_token_price', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=152, relative_tolerance=0.003)
    print("Tx4 - after buyback..")
    test_timeseries(data=data_tx4, data_key='lp_tokens', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=153, relative_tolerance=0.003)
    test_timeseries(data=data_tx4, data_key='lp_usdc', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=154, relative_tolerance=0.003)
    test_timeseries(data=data_tx4, data_key='lp_token_price', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=155, relative_tolerance=0.003)


    ## TEST LIQUIDITY POOL VALUATION AND VOLATILITY ##
    print("\n-------------------------------## TEST LIQUIDITY POOL VALUATION AND VOLATILITY ##------------------------------")
    print("Testing liquidity pool valuation and volatility of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key="lp_valuation", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=157, relative_tolerance=0.003)
    test_timeseries(data=data, data_key="lp_volatility", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=159, relative_tolerance=0.003)

    
    ## TEST CASH BALANCE ##
    print("\n-----------------------------------------## TEST CASH BALANCE ##----------------------------------------")
    print("Testing cash balance of radCad timeseries simulation against QTM data tables...")
    test_timeseries(data=data, data_key='ba_cash_balance', data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=189, relative_tolerance=0.003)


    ## Testing agent end balances ##
    test_timeseries(data=data, data_key="reserve_a_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=179, relative_tolerance=0.003)
    test_timeseries(data=data, data_key="community_a_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=180, relative_tolerance=0.003)
    test_timeseries(data=data, data_key="foundation_a_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=181, relative_tolerance=0.003)
    test_timeseries(data=data, data_key="incentivisation_a_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=182, relative_tolerance=0.003)
    test_timeseries(data=data, data_key="staking_vesting_a_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=183, relative_tolerance=0.003)
    test_timeseries(data=data, data_key="lp_tokens", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=184, relative_tolerance=0.003)
    test_timeseries(data=data, data_key="te_holding_supply", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=185, relative_tolerance=0.003)
    # circulating and vested supply
    test_timeseries(data=data, data_key="te_unvested_supply", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=186, relative_tolerance=0.003)
    test_timeseries(data=data, data_key="te_circulating_supply", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=187, relative_tolerance=0.003)
    # token valuations
    test_timeseries(data=data, data_key="lp_token_price", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=192, relative_tolerance=0.003)
    test_timeseries(data=data, data_key="te_MC", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=193, relative_tolerance=0.003)
    test_timeseries(data=data, data_key="te_FDV_MC", data_row_multiplier=1, QTM_data_tables=QTM_data_tables, QTM_row=194, relative_tolerance=0.003)


    ### END OF TESTS ###
    print("\n")
    print(u'\u2713'+" ALL TESTS PASSED!")
    print("\n------------------------------------")

    print("\n-------------------------------------------------------------------------------------------------------")
    print("\n-------------------------------------------## END OF TESTS ##-------------------------------------------")
    print("\n-------------------------------------------------------------------------------------------------------")
    print("\n")
    # display necessery time data
    print("Simulation time: ", simulation_end_time - start_time, " s")
    print("Post processing one dataframe time: ", postprocessing_all_end_time - postprocessing_one_start_time, " s")
    print("Post processing all dataframes time: ", postprocessing_all_end_time - simulation_end_time, " s")
    print("Whole Test time: ", time.process_time() - start_time, " s")
