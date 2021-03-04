
def get_action_value(mdp, state_values, state, action, gamma):
    """ Computes Q(s,a) as in formula above """

    # YOUR CODE HERE
    results = 0.
    for posible_state in mdp.get_all_states():
        transition_prob = mdp.get_transition_prob(state, action, posible_state)
        reward = mdp.get_reward(state, action, posible_state)
        state_value = state_values[posible_state]

        results += transition_prob * (reward + gamma * state_value)

    return results # < YOUR CODE >
