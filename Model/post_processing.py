import pandas as pd

def postprocessing(df):
    '''
    Definition:
    Refine and extract metrics from the simulation
    
    Parameters:
    df: simulation dataframe
    '''
    # subset to last substep
    df = df[df['substep'] == df.substep.max()] 

    # Get the ABM results
    timesteps = df.timestep
    date = df.date

    agent_ds = df.agents
    liquidity_pool_ds = df.liquidity_pool
    token_economy_ds = df.token_economy
    user_adoption_ds = df.user_adoption
    business_assumptions_ds = df.business_assumptions
    meta_bucket_allocations_ds = df.meta_bucket_allocations
    
    # Create an analysis dataset
    data = (pd.DataFrame({'timestep': timesteps,
                          'date': date,
                          'run': df.run,
                          'agents': agent_ds,
                          'liquidity_pool': liquidity_pool_ds,
                          'token_economy': token_economy_ds,
                          'user_adoption':user_adoption_ds,
                          'meta_bucket_allocations':meta_bucket_allocations_ds
                          })
           )

    ## Token Economy
    data['circulating_supply'] = token_economy_ds.map(lambda s: s["circulating_supply"])
    
    ## Agent quantity
    for key in agent_ds[agent_ds.keys()[0]]:
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_agents'] = agent_ds.map(lambda s: sum([1 for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

    ## agents tokens quantitiy
    for key in agent_ds[agent_ds.keys()[0]]:
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_tokens'] = agent_ds.map(lambda s: sum([agent['tokens'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

    ## agents usd_funds quantitiy
    for key in agent_ds[agent_ds.keys()[0]]:
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_usd_funds'] = agent_ds.map(lambda s: sum([agent['usd_funds'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

    ## agents tokens apr locked quantity
    for key in agent_ds[agent_ds.keys()[0]]:
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_tokens_apr_locked'] = agent_ds.map(lambda s: sum([agent['tokens_apr_locked'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

    ## agents tokens buyback locked quantity
    for key in agent_ds[agent_ds.keys()[0]]:
        data[agent_ds[agent_ds.keys()[0]][key]['name']+'_tokens_buyback_locked'] = agent_ds.map(lambda s: sum([agent['tokens_buyback_locked'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))

    ## agents tokens vested quantity
    for key in agent_ds[agent_ds.keys()[0]]:
            data[agent_ds[agent_ds.keys()[0]][key]['name']+'_tokens_vested'] = agent_ds.map(lambda s: sum([agent['tokens_vested'] for agent in s.values() if agent['name'] == agent_ds[agent_ds.keys()[0]][key]['name']]))


    ## user adoption
    for key in user_adoption_ds[user_adoption_ds.keys()[0]]:
        key_values = user_adoption_ds.apply(lambda s: s.get(key))
        data[key] = key_values


    cash_balance = business_assumptions_ds.apply(lambda s: s.get('cash_balance'))
    data['cash_balance'] = cash_balance
    
    return data