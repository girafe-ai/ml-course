
def get_action_value(mdp, state_values, state, action, gamma):
    """ Computes Q(s,a) as in formula above """

    # YOUR CODE HERE
    res = 0.
    for loop_state in mdp.get_all_states():
        res += (mdp.get_transition_prob(state, action, loop_state) * 
                (mdp.get_reward(state, action, loop_state) + gamma * state_values[loop_state]))
        
    return res