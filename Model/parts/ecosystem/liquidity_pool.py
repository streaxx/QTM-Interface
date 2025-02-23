import numpy as np

from parts.utils import *

# POLICY FUNCTIONS
def initialize_liquidity_pool(params, substep, state_history, prev_state, **kwargs):
    """
    Function to initialize the liquidity pool in the first timestep
    """
    # parameters
    required_usdc = params['initial_required_usdc']
    required_tokens = params['initial_lp_token_allocation']

    # state variables
    current_month = prev_state['timestep']
    liquidity_pool = prev_state['liquidity_pool']

    if current_month == 0:
        print('Initializing the liquidity pool...')
        constant_product = required_usdc * required_tokens
        token_price = required_usdc / required_tokens

        # initialize the liquidity pool from the system parameters
        liquidity_pool['lp_tokens'] = required_tokens
        liquidity_pool['lp_usdc'] = required_usdc
        liquidity_pool['lp_constant_product'] = constant_product
        liquidity_pool['lp_token_price'] = token_price

        # check if required funds are available from funds raised
        sum_of_raised_capital = calculate_raised_capital(params)

        if required_usdc > sum_of_raised_capital:
            raise ValueError(f'The required funds to seed the DEX liquidity are {required_usdc}, '
                             f'which is higher than the sum of raised capital {sum_of_raised_capital}!')
        
        return {'liquidity_pool': liquidity_pool}
    else:
        return {'liquidity_pool': prev_state['liquidity_pool']}

def liquidity_pool_tx1_after_adoption(params, substep, state_history, prev_state, **kwargs):
    """
    Function to calculate the liquidity pool after the adoption buys
    """

    # parameters
    token_lp_weight = 0.5
    usdc_lp_weight = 0.5

    # state variables
    liquidity_pool = prev_state['liquidity_pool'].copy()
    user_adoption = prev_state['user_adoption'].copy()
    token_buys = user_adoption['ua_token_buys']

    # policy variables
    lp_tokens = liquidity_pool['lp_tokens']
    lp_usdc = liquidity_pool['lp_usdc']
    constant_product = liquidity_pool['lp_constant_product']
    token_price = liquidity_pool['lp_token_price']

    # policy logic
    # calculate the liquidity pool after the adoption buys
    lp_tokens = lp_tokens - lp_tokens * (1 - (lp_usdc / (lp_usdc + token_buys))**(usdc_lp_weight/token_lp_weight))
    lp_usdc = lp_usdc + token_buys

    token_price = lp_usdc / lp_tokens

    error_message = (
    f'The constant product is not allowed to change after adoption buys! '
    f'Old constant product: {constant_product} New constant product: {lp_usdc * lp_tokens}')
    
    np.testing.assert_allclose(constant_product, lp_usdc * lp_tokens, rtol=0.001, err_msg=error_message)

    return {'lp_tokens': lp_tokens, 'lp_usdc': lp_usdc, 'lp_constant_product': constant_product, 'lp_token_price': token_price, 'tx': 1}

def liquidity_pool_tx2_after_vesting_sell(params, substep, state_history, prev_state, **kwargs):
    """
    Function to calculate the liquidity pool after the vesting sell
    """

    # parameters
    token_lp_weight = 0.5
    usdc_lp_weight = 0.5

    # state variables
    liquidity_pool = prev_state['liquidity_pool'].copy()
    agents = prev_state['agents'].copy()
    token_economy = prev_state['token_economy'].copy()

    # policy variables
    lp_tokens = liquidity_pool['lp_tokens']
    lp_usdc = liquidity_pool['lp_usdc']
    constant_product = liquidity_pool['lp_constant_product']
    token_price = liquidity_pool['lp_token_price']
    selling_allocation = token_economy['te_selling_allocation']

    # policy logic
    # get amount of tokens to be sold by agents from vesting + airdrops + incentivisation
    tokens_to_sell = 0
    agent_sell_from_holding_dict = {}
    a_selling_tokens_sum = 0
    a_selling_from_holding_tokens_sum = 0
    for agent in agents:
        # selling from vesting + airdrops + incentivisation allocations
        tokens_to_sell += agents[agent]['a_selling_tokens'] + agents[agent]['a_selling_from_holding_tokens']
        a_selling_tokens_sum += agents[agent]['a_selling_tokens']
        a_selling_from_holding_tokens_sum += agents[agent]['a_selling_from_holding_tokens']
    
    # consistency check for the amount of tokens to be sold being equivalent to meta bucket selling allocation
    error_message = (
    f'The amount of tokens to be sold {tokens_to_sell} '
    f'is not equal to the meta bucket selling allocation {selling_allocation}!')
    
    np.testing.assert_allclose(tokens_to_sell, selling_allocation, rtol=0.001, err_msg=error_message)

    # calculate the liquidity pool after the vesting sells
    lp_usdc = lp_usdc - lp_usdc * (1 - (lp_tokens / (lp_tokens + tokens_to_sell))**(token_lp_weight/usdc_lp_weight))
    lp_tokens = lp_tokens + tokens_to_sell


    token_price = lp_usdc / lp_tokens

    error_message = (
    f'The constant product is not allowed to change after adoption buys! '
    f'Old constant product: {constant_product} New constant product: {lp_usdc * lp_tokens}')
    
    np.testing.assert_allclose(constant_product, lp_usdc * lp_tokens, rtol=0.001, err_msg=error_message)
        
    return {'lp_tokens': lp_tokens, 'lp_usdc': lp_usdc, 'lp_constant_product': constant_product, 'lp_token_price': token_price,
            'agent_sell_from_holding_dict': agent_sell_from_holding_dict, 'tx': 2}

def liquidity_pool_tx3_after_liquidity_addition(params, substep, state_history, prev_state, **kwargs):
    """
    Function to calculate the liquidity pool after liquidity addition
    """

    # parameters

    # state variables
    liquidity_pool = prev_state['liquidity_pool'].copy()
    agents = prev_state['agents'].copy()

    # policy variables
    lp_tokens = liquidity_pool['lp_tokens']
    lp_usdc = liquidity_pool['lp_usdc']
    constant_product = liquidity_pool['lp_constant_product']
    token_price = liquidity_pool['lp_token_price']

    # policy logic
    # get amount of tokens to be used for liquidity mining
    tokens_for_liquidity = 0
    for agent in agents:
        tokens_for_liquidity += (agents[agent]['a_tokens_liquidity_mining'] - agents[agent]['a_tokens_liquidity_mining_remove'])

    # calculate the liquidity pool after the vesting sells
    lp_usdc = lp_usdc + tokens_for_liquidity * token_price
    lp_tokens = lp_tokens + tokens_for_liquidity

    # ensure that token price can never be negative
    token_price = max(lp_usdc / lp_tokens, 0)
    constant_product = lp_usdc * lp_tokens
        
    return {'lp_tokens': lp_tokens, 'lp_usdc': lp_usdc, 'lp_constant_product': constant_product, 'lp_token_price': token_price, 'tx': 3}

def liquidity_pool_tx4_after_buyback(params, substep, state_history, prev_state, **kwargs):
    """
    Function to calculate the liquidity pool after buyback
    """

    # parameters
    token_lp_weight = 0.5
    usdc_lp_weight = 0.5

    # state variables
    liquidity_pool = prev_state['liquidity_pool'].copy()
    business_assumptions = prev_state['business_assumptions'].copy()

    # policy variables
    lp_tokens = liquidity_pool['lp_tokens']
    lp_usdc = liquidity_pool['lp_usdc']
    constant_product = liquidity_pool['lp_constant_product']
    token_price = liquidity_pool['lp_token_price']
    buybacks_usd = business_assumptions['ba_buybacks_usd']

    # policy logic
    # calculate the liquidity pool after buyback
    lp_tokens = lp_tokens - lp_tokens * (1 - (lp_usdc / (lp_usdc + buybacks_usd))**(usdc_lp_weight/token_lp_weight))
    lp_usdc = lp_usdc + buybacks_usd

    token_price = lp_usdc / lp_tokens
    
    error_message = (
    f'The constant product is not allowed to change after adoption buys! '
    f'Old constant product: {constant_product} New constant product: {lp_usdc * lp_tokens}')
    
    np.testing.assert_allclose(constant_product, lp_usdc * lp_tokens, rtol=0.001, err_msg=error_message)
    
    return {'lp_tokens': lp_tokens, 'lp_usdc': lp_usdc, 'lp_constant_product': constant_product, 'lp_token_price': token_price, 'tx': 4}


# STATE UPDATE FUNCTIONS
def update_lp_after_lp_seeding(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agents based on the changes in business funds to seed the liquidity pool.
    """
    # get policy inputs
    updated_liquidity_pool = policy_input['liquidity_pool']

    return ('liquidity_pool', updated_liquidity_pool)

def update_agents_tx1_after_adoption(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agents after the adoption buys
    """
    # state variables
    liquidity_pool = prev_state['liquidity_pool'].copy()
    updated_agents = prev_state['agents'].copy()


    # get policy inputs
    new_lp_tokens = policy_input['lp_tokens']

    # update variables
    old_lp_tokens = liquidity_pool['lp_tokens']

    # update logic
    bought_tokens = old_lp_tokens - new_lp_tokens

    # distribute the bought tokens to the market_investors agents
    market_investors = sum([1 for agent in updated_agents if (updated_agents[agent]['a_type'] == 'market_investors')])
    for agent in updated_agents:
        if updated_agents[agent]['a_type'] == 'market_investors':
            
            bought_tokens_per_market_investor = bought_tokens / market_investors

            updated_agents[agent]['a_tokens'] += bought_tokens_per_market_investor

    return ('agents', updated_agents)

def update_agents_tx2_after_vesting_sell(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agents after the adoption buys
    """
    # state variables
    updated_agents = prev_state['agents'].copy()

    # get policy inputs
    agent_sell_from_holding_dict = policy_input['agent_sell_from_holding_dict']

    # update agents token balances as they sell from their holdings of the last timestep
    for agent in updated_agents:
        if updated_agents[agent]['a_type'] != 'protocol_bucket':

            updated_agents[agent]['a_tokens'] -= agent_sell_from_holding_dict[agent]

    return ('agents', updated_agents)

def update_liquidity_pool_after_transaction(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the liquidity pool after the adoption buys
    """
    # parameters
    initial_token_price = params['initial_token_price']

    # state variables
    updated_liquidity_pool = prev_state['liquidity_pool']

    # get policy inputs
    lp_tokens = policy_input['lp_tokens']
    lp_usdc = policy_input['lp_usdc']
    constant_product = policy_input['lp_constant_product']
    token_price = policy_input['lp_token_price']
    tx = policy_input['tx']
    
    # prepare volatility calculation
    if policy_input['tx'] == 1:
        updated_liquidity_pool['lp_token_price_max'] = token_price
        updated_liquidity_pool['lp_token_price_min'] = token_price
    elif policy_input['tx'] in [2, 3, 4]:
        updated_liquidity_pool['lp_token_price_max'] = np.max([updated_liquidity_pool['lp_token_price_max'], token_price, [initial_token_price if prev_state['timestep'] == 1 else 0][0]])
        updated_liquidity_pool['lp_token_price_min'] = np.min([updated_liquidity_pool['lp_token_price_min'], token_price, [initial_token_price if prev_state['timestep'] == 1 else 1e20][0]])

    # update logic
    updated_liquidity_pool['lp_tokens'] = lp_tokens
    updated_liquidity_pool['lp_usdc'] = lp_usdc
    updated_liquidity_pool['lp_constant_product'] = constant_product
    updated_liquidity_pool['lp_token_price'] = token_price
    updated_liquidity_pool['lp_valuation'] = lp_usdc + lp_tokens * token_price
    updated_liquidity_pool['lp_volatility'] = ((updated_liquidity_pool['lp_token_price_max'] - updated_liquidity_pool['lp_token_price_min'])
                                            / updated_liquidity_pool['lp_token_price_max'] * 100)

    #Special 2 variables
    if tx == 1:
        updated_liquidity_pool['lp_tokens_after_adoption'] = lp_tokens
    elif tx == 3:
        updated_liquidity_pool['lp_tokens_after_liquidity_addition'] = lp_tokens
    elif tx == 4:
        updated_liquidity_pool['lp_tokens_after_buyback'] = lp_tokens

    return ('liquidity_pool', updated_liquidity_pool)
