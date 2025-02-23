# POLICY FUNCTIONS
def generate_agent_behavior(params, substep, state_history, prev_state, **kwargs):
    """
    Define the agent behavior for each agent type
    """
    if params['agent_behavior'] == 'stochastic':
        """
        Define the agent behavior for each agent type for the stochastic agent behavior
        Agent actions are based on a weighted random choices.
        """
        agent_behavior_dict = {
            'angle': {
                'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                'remove_locked_tokens': params['avg_token_utility_removal'],
            },
            'seed': {
                'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                'remove_locked_tokens': params['avg_token_utility_removal'],
            },
            'presale_1': {
                'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                'remove_locked_tokens': params['avg_token_utility_removal'],
            },
            'presale_2': {
                'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                'remove_locked_tokens': params['avg_token_utility_removal'],
            },
            'public_sale': {
                'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                'remove_locked_tokens': params['avg_token_utility_removal'],
            },
            'team': {
                'trade': params['avg_token_selling_allocation']-params['avg_token_utility_removal']/3,
                'hold': params['avg_token_holding_allocation']-params['avg_token_utility_removal']/3,
                'utility': params['avg_token_utility_allocation']-params['avg_token_utility_removal']/3,
                'remove_locked_tokens': params['avg_token_utility_removal'],
            },
            'reserve': {
                'trade': 0,
                'hold': 50,
                'utility': 0,
                'remove_locked_tokens': 0,
                'incentivise': 50
            },
            'community': {
                'trade': 0,
                'hold': 100,
                'utility': 0,
                'remove_locked_tokens': 0,
                'incentivise': 0
            },
            'foundation': {
                'trade': 0,
                'hold': 100,
                'utility': 0,
                'remove_locked_tokens': 0,
                'incentivise': 0
            },
            'incentivisation': {
                'trade': 0,
                'hold': 100,
                'utility': 0,
                'remove_locked_tokens': 0,
                'incentivise': 0
            },
            'staking_vesting_allocation': {
                'trade': 0,
                'hold': 100,
                'utility': 0,
                'remove_locked_tokens': 0,
                'incentivise': 0
            },
            'market_investors': {
                'trade': 60,
                'hold': 10,
                'utility': 25,
                'remove_locked_tokens': 5,
                'incentivise': 0
            }
        }
    
    elif params['agent_behavior'] == 'static':
        """
        Define the agent behavior for each agent type for the static 1:1 QTM behavior
        ToDo: Consistency checks of correct meta bucket and utility share amounts, which should be 100% in total for each agent type
        """
        agents = prev_state['agents'].copy()
        
        # initialize agent behavior dictionary
        agent_behavior_dict = {}

        # populate agent behavior dictionary
        for agent in agents:
            agent_behavior_dict[agent] = {
                'sell': params['avg_token_selling_allocation'],
                'hold': params['avg_token_holding_allocation'],
                'utility': params['avg_token_utility_allocation'],
                'remove_locked_tokens': params['avg_token_utility_removal'],
                'locking_apr': params['lock_share'],
                'locking_buyback': params['lock_buyback_distribute_share'],
                'liquidity': params['liquidity_mining_share'],
                'transfer': params['transfer_share'],
                'burning': params['burning_share']
            }

    return {'agent_behavior_dict': agent_behavior_dict}

def agent_token_allocations(params, substep, state_history, prev_state, **kwargs):
    """
    Define the meta bucket token allocations of all agents with respect to 'sell' 'hold' and 'utility'
    """

    # get state variables
    agents = prev_state['agents']

    # initialize meta bucket token allocations
    meta_bucket_allocations= {
        'selling': 0,
        'holding': 0,
        'utility': 0,
        'removed': 0
    }

    utility_bucket_allocations = {
        'locking_apr': 0,
        'locking_buyback': 0,
        'liquidity': 0,
        'transfer': 0,
        'burn': 0
    }

    # update agent token allocations and update the meta bucket allocations w.r.t. each agents contribution
    # note that protocol buckets are not used for meta bucket allocations
    agent_allocations = {}
    for agent in agents:
        if agents[agent]['a_type'] != 'protocol_bucket':
            # get agent static behavior percentages
            selling_perc = agents[agent]['a_actions']['sell']
            utility_perc = agents[agent]['a_actions']['utility']
            hold_perc = agents[agent]['a_actions']['hold']
            remove_perc = agents[agent]['a_actions']['remove_locked_tokens']
            locking_apr_perc = agents[agent]['a_actions']['locking_apr']
            locking_buyback_share_perc = agents[agent]['a_actions']['locking_buyback']
            liquidity_perc = agents[agent]['a_actions']['liquidity']
            transfer_perc = agents[agent]['a_actions']['transfer']
            burn_perc = agents[agent]['a_actions']['burning']

            # calculate corresponding absolute token amounts for meta buckets
            # agent meta bucket allocations are based on the agents vested tokens
            sell_tokens = agents[agent]['a_tokens_vested'] * selling_perc/100
            utility_tokens = agents[agent]['a_tokens_vested'] * utility_perc/100
            holding_tokens = agents[agent]['a_tokens_vested'] * hold_perc/100
            removed_locked_apr_tokens = agents[agent]['a_tokens_apr_locked'] * remove_perc/100
            removed_locked_buyback_tokens = agents[agent]['a_tokens_buyback_locked'] * remove_perc/100
            removed_liquidity_tokens = agents[agent]['a_tokens_liquidity_mining'] * remove_perc/100
            removed_tokens = removed_locked_apr_tokens + removed_locked_buyback_tokens + removed_liquidity_tokens 
            locked_apr_tokens = utility_tokens * locking_apr_perc/100
            locked_buyback_tokens = utility_tokens * locking_buyback_share_perc/100
            liquidity_tokens = utility_tokens * liquidity_perc/100
            transfer_tokens = utility_tokens * transfer_perc/100
            burn_tokens = utility_tokens * burn_perc/100

            # populate meta bucket allocations
            meta_bucket_allocations['selling'] += sell_tokens
            meta_bucket_allocations['holding'] += agents[agent]['a_tokens'] - sell_tokens - utility_tokens + removed_tokens
            meta_bucket_allocations['utility'] += utility_tokens
            meta_bucket_allocations['removed'] += removed_tokens

            # populate utility bucket allocations
            utility_bucket_allocations['locking_apr'] += locked_apr_tokens
            utility_bucket_allocations['locking_buyback'] += locked_buyback_tokens
            utility_bucket_allocations['liquidity'] += liquidity_tokens
            utility_bucket_allocations['transfer'] += transfer_tokens
            utility_bucket_allocations['burn'] += burn_tokens

        else:
            # calculate corresponding absolute token amounts for meta buckets
            sell_tokens = 0
            utility_tokens = 0
            removed_tokens = 0
            locked_apr_tokens = 0
            locked_buyback_tokens = 0
            liquidity_tokens = 0
            transfer_tokens = 0
            burn_tokens = 0
        
        # update agent token allocations
        agent_allocations[agent] = {
            'selling': sell_tokens,
            'holding': holding_tokens,
            'utility': utility_tokens,
            'removed': removed_tokens,
            'locking_apr': locked_apr_tokens,
            'locking_buyback': locked_buyback_tokens,
            'liquidity': liquidity_tokens,
            'transfer': transfer_tokens,
            'burn': burn_tokens
        }

    return {'meta_bucket_allocations': meta_bucket_allocations, 'utility_bucket_allocations': utility_bucket_allocations, 'agent_allocations': agent_allocations}


# STATE UPDATE FUNCTIONS
def update_agent_behavior(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agent behaviors
    """
    updated_agents = prev_state['agents']
    agent_behavior_dict = policy_input['agent_behavior_dict']

    for key in updated_agents:
        updated_agents[key]['a_actions'] = agent_behavior_dict[key]

    return ('agents', updated_agents)

def update_agent_token_allocations(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the agent token allocations
    """
    updated_agents = prev_state['agents'].copy()
    agent_allocations = policy_input['agent_allocations']

    for key, value in updated_agents.items():
        # check if agent has enough tokens for meta bucket allocations

        if updated_agents[key]['a_tokens'] - agent_allocations[key]['selling'] - agent_allocations[key]['utility'] + agent_allocations[key]['removed'] < 0:
            raise ValueError('Agent ', updated_agents[key]['a_name'], ' has less tokens: ', updated_agents[key]['a_tokens'], ' than planned selling allocation ', agent_allocations[key]['selling'],
                             ' and utility allocation ', agent_allocations[key]['utility'], ' plus removing allocation ', agent_allocations[key]['removed'], ' combined!')
        
        # update agent token allocations
        updated_agents[key]['a_selling_tokens'] = agent_allocations[key]['selling']
        updated_agents[key]['a_utility_tokens'] = agent_allocations[key]['utility']
        updated_agents[key]['a_holding_tokens'] = agent_allocations[key]['holding']
        updated_agents[key]['a_tokens'] = updated_agents[key]['a_tokens'] - agent_allocations[key]['selling'] - agent_allocations[key]['utility'] + agent_allocations[key]['removed']
        updated_agents[key]['a_tokens_apr_locked'] = updated_agents[key]['a_tokens_apr_locked'] + agent_allocations[key]['locking_apr']
        updated_agents[key]['a_tokens_buyback_locked'] = updated_agents[key]['a_tokens_buyback_locked'] + agent_allocations[key]['locking_buyback']
        updated_agents[key]['a_tokens_liquidity_mining'] = updated_agents[key]['a_tokens_liquidity_mining'] + agent_allocations[key]['liquidity']
        updated_agents[key]['a_tokens_transferred'] = updated_agents[key]['a_tokens_transferred'] + agent_allocations[key]['transfer']
        updated_agents[key]['a_tokens_burned'] = updated_agents[key]['a_tokens_burned'] + agent_allocations[key]['burn']


    return ('agents', updated_agents)




def update_meta_bucket_allocations(params, substep, state_history, prev_state, policy_input, **kwargs):
    """
    Function to update the meta bucket allocations
    """
    updated_meta_bucket_allocations = policy_input['meta_bucket_allocations']
    return ('meta_bucket_allocations',updated_meta_bucket_allocations)
