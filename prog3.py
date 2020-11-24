# Ivan Viro
# AI Fall2020

import random
import sys

# As taken from the pseudo-code from the directions, 
# so I won't comment reasoning here (since it's already there)
def choose_action(state, actions_available, counts, totals, m, bottom, top):
    num_actions = len(actions_available)
    # Had to add condition to check if proposed action is avaiable in the state
    if any([True for count in counts if counts[count] == 0 
            and count.split(',')[1] in actions_available and count.split(',')[0] == state]):
        return [count.split(',')[1] for count in counts if counts[count] == 0
            and count.split(',')[1] in actions_available and count.split(',')[0] == state][0]
    # Modified the formula for average a bit here with what prof suggested in email
    average = [max(bottom, totals[str(state) + ',' + str(i)] / counts[str(state)
                                                                 + ',' + str(i)])
                for i in range(num_actions)]

    saverage = [.25 + .75*(average[i] - bottom) / (top - bottom) for i in range(num_actions)]
    
    keys = [key for key in list(counts.keys()) if key.split(',')[0] == str(state)]
    
    c = sum([counts[key] for key in keys])
    
    unnormalized_probability = [saverage[i]**(c/m) for i in range(num_actions)]
    
    norm = sum(unnormalized_probability)
    
    probability = [float(unnormalized_probability[i]/norm) for i in range(num_actions)]
    return random.choices(actions_available, weights=probability)


# When calculating during the output frequency
def get_best_action(counts, totals, states_and_actions, state):
    relevant_actions = [s_and_a for s_and_a in states_and_actions
                                if s_and_a.split(',')[0] == state]
    if len([counts[key] for key in relevant_actions if counts[key] == 0]) \
        == len(relevant_actions):
        return 'U'
    else:
        best_key = max([totals[key]/counts[key] for key in relevant_actions
                                                        if counts[key] != 0])
        return [key.split(',')[1] for key in relevant_actions 
                                  if counts[key] > 0 and 
                                     totals[key]/counts[key] == best_key][0]


def mdp(input_file):
    # Read the input values
    f = open(input_file)
    lines = [line.split(' ') for line in f.read().split("\n")]   
    num_non_terminal_states = lines[0][0]
    terminal_states = lines[0][1]
    rounds_to_play = int(lines[0][2])
    frequency_to_output = int(lines[0][3])
    m = float(lines[0][4])

    # Initializing the reward nodes/states
    terminal_rewards = {}
    for i in range(0, len(lines[1]), 2):
        terminal_rewards[lines[1][i]] = int(lines[1][i+1])

    # Initializing the main dictionary of states and actions
    non_terminal_states = {}
    for line in lines[2:]:
        [state, action] = line[0].split(':')
        action_dict = {}
        for i in range(1, len(line[1:]), 2):
            action_dict[line[i]] = float(line[i+1])
        if state not in non_terminal_states:
            non_terminal_states[state] = {a: action_dict for a in action}
        else:
            non_terminal_states[state][action] = action_dict

    # Initialize counts and totals
    states_and_actions = sum([
        [state + ',' + action for action in list(non_terminal_states[state].keys())]
        for state in list(non_terminal_states.keys())
    ], [])
    # TIL: dictionary comprehension
    counts = {x: 0 for x in states_and_actions}
    totals = {x: 0 for x in states_and_actions}
    local_counts = {x: 0 for x in states_and_actions}

    # The most useful place to check input-reading and overall probabilities
    # between states and actions \/ 
    for state in non_terminal_states:
        for action in non_terminal_states[state]:
            # print("state", state, "action", action, non_terminal_states[state][action])
            pass

    # Taken out of the choose_action function to not keep recalculating
    bottom = min(terminal_rewards.values())
    top = max(terminal_rewards.values())

    for i in range(1, rounds_to_play+1):

        # Unclear in homework directions whether to choose a state at random or not
        # at this step... I chose like this, but it ultimately shouldn't matter too much.
        for state in non_terminal_states:

            actions_available = list(non_terminal_states[state].keys())

            action = str(choose_action(state, actions_available, counts, totals, m, bottom, top)[0])

            result_state = random.choices(list(non_terminal_states[state][action].keys()), 
                                  weights=list(non_terminal_states[state][action].values()))[0]
            # Keeps track of sequences encountered, to later add up.
            sequences_in_round = {str(state) + ',' + str(action)}

            while result_state in non_terminal_states:
                state = result_state
                actions_available = list(non_terminal_states[state].keys())
                action = str(choose_action(state, actions_available, counts, totals, m, bottom, top)[0])

                result_state = random.choices(list(non_terminal_states[state][action].keys()), 
                                      weights=list(non_terminal_states[state][action].values()))[0]

                sequences_in_round.add(str(state) + ',' + str(action))

            # Once a result state is reached, update counts, totals, and potentially print.
            for key in sequences_in_round:
                counts[key] += 1

            # for key in [bit for bit in list(sequences_in_round.keys()) if counts[bit] > 0]:
            totals[key] += terminal_rewards[result_state]
    
            # Output when asked 
            if i % frequency_to_output == 0:
                best_actions = [[state, get_best_action(counts, totals, states_and_actions, state)]
                                for state in non_terminal_states]
                best_action = max([totals[key]/counts[key] for key in states_and_actions if counts[key] != 0])
                # Output
                print("After", str(i), "rounds")
                print("Count:")
                [print('[' + count + ']=' + str(counts[count]) + '. ') for count in counts]
                print("\nTotal:")
                [print('[' + total + ']=' + str(totals[total]) + '. ') for total in totals]
                print("\nBest action: ", end='')
                [print(str(action[0]) + ':' + str(action[1]), end='. ')
                    for action in best_actions]
                print()
            i += 1
        i -= 1


mdp(sys.argv[1])
