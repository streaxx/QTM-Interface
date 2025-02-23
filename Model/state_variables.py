from sys_params import *
from parts.utils import *

# initialize the initial stakeholders
initial_stakeholders = generate_agents(stakeholder_name_mapping)

# initialize the initial liquidity pool
initial_liquidity_pool = initialize_dex_liquidity()

# initialize the initial token economy
initial_token_economy = generate_initial_token_economy_metrics()

# initialize the initial user adoption
initial_user_adoption = initialize_user_adoption()

# initialize the initial business assumptions
business_assumptions = initialize_business_assumptions()

# initialize the initial standard utilities
utilities = initialize_utilities()



# compose the initial state
initial_state = {
    'date': convert_date(sys_param),
    'agents': initial_stakeholders,
    'liquidity_pool': initial_liquidity_pool,
    'token_economy': initial_token_economy,
    'user_adoption': initial_user_adoption,
    'business_assumptions': business_assumptions,
    'utilities': utilities 
}
