import numpy as np
import random
from BoardHeuristics_UNMEGRED import is_goal, list_moves
from InfusionBoardUtils import InfusionBoard as iboard

# Hyperparameters
alpha = 0.1  # Learning rate
gamma = 0.9  # Discount factor
epsilon = 0.1  # Exploration rate

# Q-Table (state-action pairs)
Q = {}

# Updated reward function
def get_reward(state, action, num_steps):
    """
    Reward logic based on the number of steps and the outcome of forge_item.
    """

    summedRewards = 0

    # Check the current state.
    board, metrics = state.forge_item()

    # If the action is supposed to end the round...
    if action == "state.forge_item()":
        starAddCount = 40 if metrics["num_stars"] == 10 else metrics["num_stars"] * 2
        starAddCount = -1000 if metrics['num_stars'] > 10 else starAddCount
        
        if 20 <= num_steps <= 50:
            numActionsReward = 100  # Large reward for efficiency
        elif num_steps > 100:
            numActionsReward = -200  # Huge penalty for exceeding 100 steps
        else:
            numActionsReward = 50 - abs(num_steps - 5)  # Penalize too few or too many steps
        
        summedRewards = starAddCount+numActionsReward

        return summedRewards

    
    next_state = take_action(state, action)
    #print(next_state)
    new_board, new_metrics = next_state.forge_item()

    ### HEURISTIC VALUES ###
    newStarWeight = 40
    nebulaNovaConvertWeight = 10

    # Make these small. We don't want double-counting to be too prevalent.
    blackHoleDestroysNovaWeight = -4
    failedNovaWeight = -4
    failedNebulaWeight = -4

    # These two need to be small by design.
    costIncreaseWeight = -1
    netNewPlasmaWeight = 5

    # Finding values for each heuristic

    new_stars_count = new_metrics["num_stars"] - metrics["num_stars"]
    nebula_convert_count = new_metrics["activated_nova_nebulas"] - metrics["activated_nova_nebulas"]
    
    # We expect these to decrease between state-action pairs.
    failed_nova_count = new_metrics["nova_no_star_change"] - metrics["nova_no_star_change"]
    failed_nebula_count = new_metrics["nebula_no_nova_created"] - metrics["nebula_no_nova_created"]
    black_hole_destroys_nova_count = new_metrics["nova_destroyed_by_blackhole"] - metrics["nova_destroyed_by_blackhole"]

    # These are going to be positive.
    cost_increase = new_metrics["stardust_spent"] - metrics["stardust_spent"]
    net_new_plasma = new_metrics["new_plasma"] - metrics["new_plasma"]

    # Now we do a cross product of weights to values.
    heuristicRewards = (
        new_stars_count * newStarWeight +
        nebula_convert_count * nebulaNovaConvertWeight +
        black_hole_destroys_nova_count * blackHoleDestroysNovaWeight +
        failed_nova_count * failedNovaWeight +
        failed_nebula_count * failedNebulaWeight +
        cost_increase * costIncreaseWeight +
        net_new_plasma * netNewPlasmaWeight
    )

    summedRewards = heuristicRewards + numActionsReward
    print(summedRewards)

    return summedRewards
   

# Initialize Q-value if not already done
def get_q_value(state, action):
    return Q.get((state, action), 0)

# Update Q-value
def update_q_value(state, action, reward, next_state):
    max_next_q = max([get_q_value(next_state, a) for a in list_moves(next_state)], default=0)
    current_q = get_q_value(state, action)
    new_q = current_q + alpha * (reward + gamma * max_next_q - current_q)
    Q[(state, action)] = new_q

# Transition to the next state
def take_action(state, action):
    new_state = state.copy()

    if action[:21] in ["new_state.change_type", "new_state.change_time"]
        x = int(action[22])
        y = int(action[24])
        if action[:21] == "new_state.change_type":
            type = action[26]
        elif action[:21] == "new_state.change_time":

    new_state = eval(action)
    return new_state

# Updated training loop with action counter
def train(initial_state, is_goal, max_steps=100, episodes=1000):
    for episode in range(episodes):
        state = initial_state
        num_steps = 0  # Reset step counter for each episode
        while num_steps <= max_steps:
            num_steps += 1

            # Choose action (epsilon-greedy strategy)
            valid_actions = list_moves(state)
            
            if random.uniform(0, 1) < epsilon:
                action = random.choice(valid_actions)  # Explore
            else:
                action = max(valid_actions, key=lambda a: get_q_value(state, a), default=None)  # Exploit
            
            print(action)
            # Take action and observe next state
            if action == "state.forge_item()":
                reward = get_reward(state, action, num_steps)
                next_state_parts, metrics = state.forge_item()
                next_state = iboard(0,0,0,True,next_state_parts[0], next_state_parts[1])

                #print(next_state)
                # Update Q-value
                update_q_value(state, action, reward, next_state)

                # End episode
                break
            else:
                next_state = take_action(state, action)
                reward = get_reward(state, action, num_steps)
            
            # Update Q-value
            update_q_value(state, action, reward, next_state)
            
            # Check for end condition
            if is_goal(state):
                break  # End the episode
            
            # Move to the next state
            state = next_state
        
        # Optional: Log the outcome of the episode
        print(f"Episode {episode + 1}: Steps = {num_steps}, Goal = {is_goal(state)}")


# Example usage
if __name__ == "__main__":
    # Define initial_state, is_goal, list_moves, etc.
    initial_state = iboard(40,2,2)

    train(initial_state, is_goal)
