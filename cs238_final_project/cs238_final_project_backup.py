import math
import numpy as np
import pandas as pd
import random
from itertools import product


combinations = [list(range(3)) for _ in range(9)]
all_states = list(set(product(*combinations)))
print(all_states)


def check_win(player, board):
    if np.all(board[0,:] == player):
        return True
    elif np.all(board[1,:] == player): 
        return True
    elif np.all(board[2,:] == player):
        return True
    elif np.all(board[:,0] == player):
        return True
    elif np.all(board[:,1] == player):
        return True
    elif np.all(board[:,2] == player):
        return True
    elif np.all(board.diagonal()==player):
        return True
    elif  np.all(np.fliplr(board).diagonal()==player):
        return True
    return False


#simulation with player X

master_states_res = []
master_actions_res = []
master_rewards_res = []
master_next_states_res = []

current_player = "X"
opponent_player = "O"

for num_sims in range(100000):
    empty_board = np.array(['-']*9).reshape(3,3)
    board = empty_board

    current_turn = "X"
    x,y = np.where(board == '-')
    possible_actions = [(x,y) for x,y in zip(x,y)]
    avail_positions = [(x,y) for x,y in zip(x,y)]
    print(possible_actions)

    empty_state_ind = all_states.index((0,0,0,0,0,0,0,0,0))
    states_res = [empty_state_ind]
    actions_res = []
    next_states_res = []

    while (not check_win(current_player, board) and not check_win(opponent_player, board) and ("-" in board)):
        # choose random move
        rand_pos = random.choice(avail_positions)
        board[rand_pos[0]][rand_pos[1]] = current_turn
        avail_positions.remove(rand_pos)

        # if it's our current player's turn (not opponent's turn)
        if current_turn == current_player: 
            # assign action to result
            actions_res.append(possible_actions.index(rand_pos))

            # get the tuple of the current state
            cur_state = [0,0,0,0,0,0,0,0,0]
            cur_flat_board = board.flatten()
            for i in range(len(cur_flat_board)):
                if cur_flat_board[i] == "X":
                    cur_state[i] = 1
                elif cur_flat_board[i] == "O":
                    cur_state[i] = 2
            cur_state = tuple(cur_state)

            # assign states to results
            cur_state_ind = all_states.index(cur_state)
            states_res.append(cur_state_ind)
            next_states_res.append(cur_state_ind)


        # switch to other player for next turn
        if current_turn == "X":
            current_turn = "O"
        else:
            current_turn = "X"
        print(board)

    # remove last element of states_res because we overshot
    states_res.pop()

    # assign appropriate reward       
    if check_win(current_player, board):
        reward = 1
    elif check_win(opponent_player, board):
        reward = -1
    else:
        reward = 0
    rewards_res = [reward] * len(actions_res)
    print(rewards_res)

    # add to master results
    master_states_res.extend(states_res)
    master_actions_res.extend(actions_res)
    master_rewards_res.extend(rewards_res)
    master_next_states_res.extend(next_states_res)

print(master_states_res)
print(master_actions_res)
print(master_rewards_res)
print(master_next_states_res)

# make dataframe of master results

results_df = pd.DataFrame({"s": master_states_res, 
                           "a": master_actions_res,
                           "r": master_rewards_res,
                           "sp": master_next_states_res})
print(results_df)

# write dataframe to csv file
results_df.to_csv("simulation_results_player_x", encoding='utf-8', index=False)