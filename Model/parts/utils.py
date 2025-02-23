import numpy as np
import math
import uuid
import random
import sys
import os
from datetime import datetime
from typing import *
import pandas as pd
import json
import sqlite3

# Helper Functions
def convert_date(sys_param):
    if "." in sys_param['launch_date'][0]:
        return datetime.strptime(sys_param['launch_date'][0],'%d.%m.%y')
    elif "/" in sys_param:
        return datetime.strptime(sys_param['launch_date'][0],'%d/%m/%Y')

def calculate_raised_capital(param):
    """
    Calculate the overall raised capital from the initial investors.
    """

    raised_capital = 0
    # calculate the raised capital for all investors in sys_param where "_raised" is in the key
    raised_capital = sum([param[key] if ("_raised" in key) else 0 for key in param])

    return raised_capital

# Initialization
def new_agent(stakeholder_name: str, stakeholder_type: str, usd_funds: float,
              tokens: float, tokens_vested: float, tokens_vested_cum: float, 
              tokens_airdropped: float, tokens_airdropped_cum: float, tokens_incentivised: float, tokens_incentivised_cum: float,
              tokens_apr_locked: float, tokens_apr_locked_cum: float, tokens_apr_locked_remove: float, tokens_apr_locked_rewards: float,
              tokens_buyback_locked: float, tokens_buyback_locked_cum: float, tokens_buyback_locked_remove: float, tokens_buyback_locked_rewards: float,
              tokens_staking_vesting_locked: float, tokens_staking_vesting_locked_cum: float, tokens_staking_vesting_locked_remove: float, tokens_staking_vesting_locked_rewards: float,
              tokens_liquidity_mining: float, tokens_liquidity_mining_cum: float, tokens_liquidity_mining_remove: float, tokens_liquidity_mining_rewards: float,
              tokens_transferred: float, tokens_transferred_cum: float, tokens_burned: float, tokens_burned_cum: float,
              selling_tokens: float, utility_tokens: float, selling_from_holding_tokens: float, utility_from_holding_tokens: float,
              holding_from_holding_tokens: float, holding_tokens: float, actions: dict, current_action: str) -> dict:
    """
    Function to create a new agent aka stakeholder for the token ecosystem.
    """

    agent = {'a_name': stakeholder_name, # seed, advisor, reserve, incentivisation, staking_vesting, market_investors, etc.
             'a_type': stakeholder_type, # early_investor, protocol_bucket, market_investors, airdrop_receiver, incentivisation_receiver
             'a_usd_funds': usd_funds, # amount of USD funds available to this stakeholder (not applicalbe/used in the current version)
             'a_tokens': tokens, # amount of held tokens by this stakeholder group
             'a_tokens_vested': tokens_vested, # amount of vested tokens per timestep
             'a_tokens_vested_cum': tokens_vested_cum, # amount of vested tokens cumulatively
             'a_tokens_airdropped': tokens_airdropped, # amount of airdropped tokens per timestep
             'a_tokens_airdropped_cum': tokens_airdropped_cum, # amount of airdropped tokens cumulatively
             'a_tokens_incentivised': tokens_incentivised, # amount of incentivised tokens per timestep
             'a_tokens_incentivised_cum': tokens_incentivised_cum, # amount of incentivised tokens cumulatively
             'a_tokens_apr_locked': tokens_apr_locked, # amount of tokens locked for APR per timestep
             'a_tokens_apr_locked_cum': tokens_apr_locked_cum, # amount of tokens locked for APR cumulatively
             'a_tokens_apr_locked_remove': tokens_apr_locked_remove, # amount of tokens removed from staking for base apr
             'a_tokens_apr_locked_rewards': tokens_apr_locked_rewards, # amount of token rewards for staking for base apr
             'a_tokens_buyback_locked': tokens_buyback_locked, # amount of tokens locked for buyback per timestep
             'a_tokens_buyback_locked_cum': tokens_buyback_locked_cum, # amount of tokens locked for buyback cumulatively
             'a_tokens_buyback_locked_remove': tokens_buyback_locked_remove, # amount of tokens removed from staking for buyback share
             'a_tokens_buyback_locked_rewards': tokens_buyback_locked_rewards, # amount of token rewards for staking for buyback share
             'a_tokens_staking_vesting_locked': tokens_staking_vesting_locked, # amount of tokens locked for staking vesting per timestep
             'a_tokens_staking_vesting_locked_cum': tokens_staking_vesting_locked_cum, # amount of tokens locked for staking vesting cumulatively
             'a_tokens_staking_vesting_locked_remove': tokens_staking_vesting_locked_remove, # amount of tokens removed from staking for staking vesting
             'a_tokens_staking_vesting_locked_rewards': tokens_staking_vesting_locked_rewards, # amount of token rewards for staking for staking vesting
             'a_tokens_liquidity_mining': tokens_liquidity_mining, # amount of tokens locked for liquidity mining per timestep
             'a_tokens_liquidity_mining_cum': tokens_liquidity_mining_cum, # amount of tokens locked for liquidity mining cumulatively
             'a_tokens_liquidity_mining_remove': tokens_liquidity_mining_remove, # amount of tokens removed from liquidity mining
             'a_tokens_liquidity_mining_rewards': tokens_liquidity_mining_rewards, # amount of token rewards for liquidity mining
             'a_tokens_transferred': tokens_transferred, # amount of tokens transferred per timestep
             'a_tokens_transferred_cum': tokens_transferred_cum, # amount of tokens transferred cumulatively
             'a_tokens_burned': tokens_burned, # amount of tokens burned per timestep
             'a_tokens_burned_cum': tokens_burned_cum, # amount of tokens burned cumulatively
             'a_selling_tokens': selling_tokens, # agent meta bucket selling allocations
             'a_utility_tokens': utility_tokens, # agent meta bucket utility allocations
             'a_holding_tokens': holding_tokens, # agent meta bucket holding allocations
             'a_selling_from_holding_tokens': selling_from_holding_tokens, # selling from holding allocations
             'a_utility_from_holding_tokens': utility_from_holding_tokens, # utility from holding allocations
             'a_holding_from_holding_tokens': holding_from_holding_tokens, # holding from holding allocations
             'a_actions': actions, # dictionary of actions taken by this stakeholder
             'a_current_action': current_action # current action taken by this stakeholder
             }
    return agent


def generate_agents(stakeholder_name_mapping: dict) -> dict:
    """
    Initialize all token ecosystem agents aka stakeholders.
    """

    initial_agents = {}
    for stakeholder_name, stakeholder_type in stakeholder_name_mapping.items():
        initial_agents[uuid.uuid4()] = new_agent(stakeholder_name = stakeholder_name,
                                    stakeholder_type = stakeholder_type,
                                    usd_funds = 0,
                                    tokens = 0,
                                    tokens_vested = 0,
                                    tokens_vested_cum = 0,
                                    tokens_airdropped = 0,
                                    tokens_airdropped_cum = 0,
                                    tokens_incentivised = 0,
                                    tokens_incentivised_cum = 0,
                                    tokens_apr_locked = 0,
                                    tokens_apr_locked_cum = 0,
                                    tokens_apr_locked_remove = 0,
                                    tokens_apr_locked_rewards = 0,
                                    tokens_buyback_locked = 0,
                                    tokens_buyback_locked_cum = 0,
                                    tokens_buyback_locked_remove = 0,
                                    tokens_buyback_locked_rewards = 0,
                                    tokens_staking_vesting_locked = 0,
                                    tokens_staking_vesting_locked_cum = 0,
                                    tokens_staking_vesting_locked_remove = 0,
                                    tokens_staking_vesting_locked_rewards = 0,
                                    tokens_liquidity_mining = 0,
                                    tokens_liquidity_mining_cum = 0,
                                    tokens_liquidity_mining_remove = 0,
                                    tokens_liquidity_mining_rewards = 0,
                                    tokens_transferred = 0,
                                    tokens_transferred_cum = 0,
                                    tokens_burned = 0,
                                    tokens_burned_cum = 0,
                                    selling_tokens = 0,
                                    utility_tokens = 0,
                                    holding_tokens = 0,
                                    selling_from_holding_tokens = 0,
                                    utility_from_holding_tokens = 0,
                                    holding_from_holding_tokens = 0,
                                    actions = {},
                                    current_action = 'hold')
    return initial_agents

def create_parameter_list(parameter_name, not_iterable_parameters, init_value, min, max, intervals):
    """
    Create list of parameters for parameter sweep based on the QTM input tab 'cadCAD_inputs'.
    """

    if parameter_name in not_iterable_parameters:
        return [init_value.replace(",","").replace("%","")]
    else:
        try:
            if type(init_value) == str:
                init_value = float(init_value.replace(",","").replace("%",""))
            if type(min) == str:
                min = float(min.replace(",","").replace("%",""))
            if type(max) == str:
                max = float(max.replace(",","").replace("%",""))
            if type(intervals) == str and intervals != '':
                intervals = int(float(intervals.replace(",","")).replace("%",""))
        except ValueError:
            return [init_value]
        if math.isnan(min) or math.isnan(max) or math.isnan(intervals) or max<=min:
            if max<=min:
                print("Maximum parameter boundary is lower than minimum parameter boundary: Min: ", min, "; Max:", max, ". Using initial value ", init_value, " instead.")
            return [float(init_value)]
        else:
            if math.isnan(intervals):
                return [float(init_value)]
            else:
                return list(np.linspace(min, max, int(intervals)))

def compose_initial_parameters(QTM_inputs, not_iterable_parameters):
    """
    Compose all initial parameter sets from the Quantitative Token Model inputs tab 'cadCAD_inputs'.
    """

    initial_parameters = {}
    for index, row in QTM_inputs.iterrows():
        parameter_name = row['Parameter Name'].lower().replace(' ', '_').replace('/', '').replace('(', '').replace(')', '')
        initial_parameters[parameter_name] = create_parameter_list(parameter_name, not_iterable_parameters, row['Initial Value'], row['Min'], row['Max'], row['Interval Steps'])
    return initial_parameters

def calculate_investor_allocation(sys_param, stakeholder_name):
    """
    Calculate the initial token allocation of a specific stakeholder considering bonus amounts.
    """
    token_launch_price = [x / y for x in sys_param["public_sale_valuation"] for y in sys_param["initial_total_supply"]]
    effective_token_price = [np.min([x / (1+y/100), z / a]) for x in token_launch_price for y in sys_param[stakeholder_name+"_bonus"] for z in sys_param[stakeholder_name+"_valuation"] for a in sys_param["initial_total_supply"] for a in sys_param["initial_total_supply"]]
    tokens = [x / y for x in sys_param[stakeholder_name+"_raised"] for y in effective_token_price]
    allocation = [x / y for x in tokens for y in sys_param['initial_total_supply']]
    
    return allocation

def calc_initial_lp_tokens(agent_token_allocations, sys_param):
    """
    Calculate the amount of tokens initially allocated to the DEX liquidity pool.
    """

    allocation_sum = []
    # get max length of possible raised_capital parameters
    max_length = max([len(agent_token_allocations[key]) for key in agent_token_allocations])
    
    # calculate the raised capital for all possible parameter list combinations in sys_param where "_raised" is in the key
    for i in range(max_length):
        allocation_sum.append(sum([agent_token_allocations[key][i] if (i < len(agent_token_allocations[key])) else agent_token_allocations[key][-1] for key in agent_token_allocations]))
    
    lp_token_allocation = [(1 - x) * y for x in allocation_sum for y in sys_param['initial_total_supply']]

    return lp_token_allocation


def initialize_dex_liquidity():
    """
    Initialize the DEX liquidity pool.
    """
    liquidity_pool = {
        'lp_tokens' : 0, # amount of native protocol tokens in LP
        'lp_usdc' : 0, # amount of USDC in LP
        'lp_constant_product' : 0, # constant product of LP tokens and USDC
        'lp_token_price' : 0, # price of LP token
        'lp_valuation': 0, # valuation of LP tokens
        'lp_volatility': 0, # volatility of LP tokens
        'lp_token_price_max': 0, # max price of LP token
        'lp_token_price_min': 0, # min price of LP token
        'lp_tokens_after_adoption': 0, # tokens after adoption tx 1
        'lp_tokens_after_liquidity_addition':0, # Token after liquidity addition tx 3
        'lp_tokens_after_buyback': 0 # tokens after buy back tx 4
    }

    return liquidity_pool

def generate_initial_token_economy_metrics():
    """
    Set the initial token economy metrics, such as MC, FDV MC, circ. supply, and tokens locked.
    """
    token_economy = {
        'te_total_supply' : 0, # total token supply in existence
        'te_circulating_supply' : 0, # circulating token supply
        'te_unvested_supply': 0, # unvested token tupply
        'te_holding_supply' : 0, # supply of tokens held by agents
        'te_MC' : 0, # market capitalization
        'te_FDV_MC' : 0, # fully diluted market capitalization
        'te_selling_perc': 0, # percentage of tokens sold
        'te_utility_perc': 0, # percentage of tokens used for utility
        'te_holding_perc': 0, # percentage of tokens held
        'te_remove_perc': 0, # percentage of tokens removed
        'te_selling_allocation': 0, # from vesting + airdrops + incentivisation
        'te_utility_allocation': 0, # from vesting + airdrops + incentivisation
        'te_holding_allocation': 0, # from vesting + airdrops + incentivisation
        'te_selling_allocation_cum': 0, # from vesting + airdrops + incentivisation
        'te_utility_allocation_cum': 0, # from vesting + airdrops + incentivisation
        'te_holding_allocation_cum': 0, # from vesting + airdrops + incentivisation
        'te_tokens_vested_cum': 0, # tokens vested cumulatively
        'te_tokens_burned': 0, # tokens burned
        'te_tokens_burned_cum': 0, # tokens burned cumulatively
        'te_tokens_burned_usd': 0, # tokens burned in USD
        'te_minted_tokens' : 0, # tokens minted
        'te_minted_tokens_cum': 0, # tokens minted cumulatively
        'te_minted_tokens_usd': 0, # tokens minted in USD
        'te_incentivised_tokens' : 0, # tokens incentivised
        'te_incentivised_tokens_usd' : 0, # tokens incentivised in USD
        'te_incentivised_tokens_cum' : 0, # tokens incentivised cumulatively
        'te_airdrop_tokens' : 0, # tokens airdropped
        'te_airdrop_tokens_usd' : 0, # tokens airdropped in USD
        'te_airdrop_tokens_cum' : 0 # tokens airdropped cumulatively
    }

    return token_economy

def initialize_user_adoption():
    """
    Initialize the user adoption metrics.
    """
    user_adoption = {
    'ua_product_users': 0, # amount of product users
    'ua_token_holders': 0, # amount of token holders
    'ua_product_revenue':0, # product revenue
    'ua_token_buys': 0 # amount of effective token buys
    }

    return user_adoption

def initialize_business_assumptions():
    """
    Initialize the business assumptions metrics.
    """
    business_assumptions = {
    'ba_cash_balance': 0, ## cash balance of the company
    'ba_buybacks_usd': 0 ## buybacks in USD per month
    }

    return business_assumptions


def initialize_utilities():
    """
    Initialize the utility meta bucket metrics.
    """
    utilities = {
    'u_staking_base_apr_allocation':0, # staking base apr allocation per timestep
    'u_staking_base_apr_allocation_cum':0, # staking base apr allocation cumulatively
    'u_staking_base_apr_remove':0, # staking base apr token removal
    'u_staking_base_apr_rewards': 0, # staking token rewards
    'u_buyback_from_revenue_share_usd': 0, # buyback from revenue share in USD
    'u_staking_revenue_share_allocation': 0, # staking revenue share token allocation per timestep
    'u_staking_revenue_share_allocation_cum': 0, # staking revenue share token allocation cumulatively
    'u_staking_revenue_share_remove': 0, # staking revenue share token removal
    'u_staking_revenue_share_rewards':0, # revenue sharing rewards
    'u_staking_vesting_allocation': 0, # staking vesting token allocation per timestep
    'u_staking_vesting_allocation_cum': 0, # staking vesting token allocation cumulatively
    'u_staking_vesting_remove': 0, # staking vesting token removal
    'u_staking_vesting_rewards':0, # staking vesting rewards
    'u_liquidity_mining_rewards': 0, # liquidity mining rewards
    'u_liquidity_mining_allocation': 0, # liquidity mining token allocation per timestep
    'u_liquidity_mining_allocation_cum': 0, # liquidity mining token allocation cumulatively
    'u_liquidity_mining_allocation_remove': 0, # liquidity mining token removal
    'u_burning_allocation': 0, # burning token allocation per timestep
    'u_burning_allocation_cum': 0, # burning token allocation cumulatively
    'u_holding_allocation': 0, # holding token allocation per timestep from utility bucket
    'u_holding_allocation_cum': 0, # holding token allocation cumulatively from utility bucket
    'u_holding_rewards':0, # holding token rewards
    'u_transfer_allocation':0, # transfer token allocation per timestep
    'u_transfer_allocation_cum': 0, # transfer token allocation cumulatively
    }

    return utilities


### TEST FUNCTIONS ###
def test_timeseries(data, data_key, data_row_multiplier, QTM_data_tables, QTM_row, relative_tolerance=0.001, timestep_cut_off=0, shift=0):
    # get amount of accounted for timesteps
    n_timesteps = len(QTM_data_tables.iloc[QTM_row-2].values[2:-1]) - [len(QTM_data_tables.iloc[QTM_row-2].values[2:-1])-timestep_cut_off if timestep_cut_off > 0 else 0][0] - shift

    print("Testing "+data_key+" of radCad timeseries simulation at QTM row "+str(QTM_row)+" ("+QTM_data_tables.iloc[QTM_row-2].values[1]+") for "+str(n_timesteps)+" / "+str(len(QTM_data_tables.iloc[QTM_row-2].values[2:-1]))+" timesteps...")
    
    for i in range(n_timesteps):
        # get testing values
        QTM_data_table_value = float(QTM_data_tables.iloc[QTM_row-2].values[2:-1][i].replace(",",""))
        radCAD_value = float(data[data_key].values[i+shift]) * data_row_multiplier

        # assert the values
        error_message = ("radCad simulation value "+data_key+" = "+ str(radCAD_value)
        + " at timestep "+str(i+1)+" is not equal to the QTM data table value "+ str(QTM_data_table_value)+" at row "+str(QTM_row)
        +" and date "+str(QTM_data_tables.iloc[3].values[2:-1][i])+". The difference is "+str(radCAD_value - QTM_data_table_value)+" or "
        +str([radCAD_value/QTM_data_table_value * 100 if QTM_data_table_value!= 0 else "NaN"][0])+"%.")

        if QTM_data_table_value == 0:
            if np.abs(radCAD_value) < relative_tolerance:
                pass
        elif radCAD_value == 0:
            if np.abs(QTM_data_table_value) < relative_tolerance:
                pass
        else:
            np.testing.assert_allclose(radCAD_value, QTM_data_table_value, rtol=relative_tolerance, err_msg=error_message)
    if n_timesteps == len(QTM_data_tables.iloc[QTM_row-2].values[2:-1]):
        print(u'\u2713'+" Test passed!")
    else:
        print("("+u'\u2713'+") Test passed for "+str(n_timesteps)+" / "+str(len(QTM_data_tables.iloc[QTM_row-2].values[2:-1]))+" timesteps!")
    print("------------------------------------")

def import_dummy_data(row, timestep):
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Go two folders up
    parent_dir = os.path.abspath(os.path.join(os.path.abspath(os.path.join(current_dir, os.pardir)), os.pardir))

    QTM_data_tables = pd.read_csv(parent_dir+'/data/Quantitative_Token_Model_V1.88_radCad_integration - Data Tables.csv')

    QTM_row = row
    QTM_data_table_value = float(QTM_data_tables.iloc[QTM_row-2].values[2:-1][timestep].replace(",",""))
    
    return  QTM_data_table_value

def convert_to_json(x):
    try:
        return json.dumps(x)
    except:
        return x
