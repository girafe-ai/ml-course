def get_action_value(mdp, state_values, state, action, gamma):
    """ Computes Q(s,a) as in formula above """
    
    accumulator = 0.
    # YOUR CODE HERE
    for next_state, prob in mdp.get_next_states(state, action).items():
        transition_reward = mdp.get_reward(state, action, next_state)
        accumulator += prob * (transition_reward + gamma * state_values[next_state])
    return accumulator