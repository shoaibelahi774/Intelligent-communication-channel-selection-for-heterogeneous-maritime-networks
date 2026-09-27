import time
from simulator.environment import Environment
from simulator.data_packet import DataPacket
from engine.evaluator import Evaluator
from engine.q_learning import QLearningAgent
from engine.decision import DecisionEngine 

def run_simulation(steps=20):
    env       = Environment()
    evaluator = Evaluator()
    decision_engine = DecisionEngine(threshold=0.05)  

    all_channels  = env.get_all_channels()
    channel_names = [ch.name for ch in all_channels]
    n_actions     = len(all_channels)

    # Q-Learning agent
    agent = QLearningAgent(
        n_actions     = n_actions,
        alpha         = 0.1,
        gamma         = 0.9,
        epsilon       = 0.3,      
        epsilon_decay = 0.99,
        epsilon_min   = 0.01
    )

    print("\n" + "=" * 50)
    print("    Maritime Communication Simulation  ")
    print("=" * 50)

    prev_state  = None
    prev_action = None
    prev_reward = None

    for step in range(1, steps + 1):

        print(f"\n--------- Time Step {step} ---------")

        env.update()

        packet = DataPacket.generate_random_packet()
        print(f"Packet: type={packet.packet_type:<12} size={packet.size:.2f} MB  priority={packet.priority}")

        available_channels = env.get_available_channels()

        if not available_channels:
            print("No channels available — skipping step.")
            time.sleep(1)
            continue

        available_indices = [all_channels.index(ch) for ch in available_channels]

        _, ranked = evaluator.evaluate(available_channels)
        best_channel  = ranked[0][0]
        current_state = agent.get_state(best_channel, packet)

        agent_chosen_index   = agent.select_action(current_state, available_indices)
        agent_chosen_channel = all_channels[agent_chosen_index]
        agent_chosen_q_val   = agent.q_table[current_state][agent_chosen_index]

        final_channel, switched = decision_engine.decide(agent_chosen_channel, agent_chosen_q_val)
        final_index = all_channels.index(final_channel)

        print("\nChannel Status Table:")
        print("-" * 115)
        print(f"{'Channel':<22}{'Latency(ms)':<14}{'Bandwidth(Mbps)':<18}"
              f"{'Cost':<8}{'Stability':<12}{'Score':<10}{'Avail':<8}{'Q-Value':<10}")
        print("-" * 115)

        for ch, score in ranked:
            idx    = all_channels.index(ch)
            q_val  = agent.q_table[current_state][idx]
            
            marker = ""
            if ch == final_channel and ch == agent_chosen_channel:
                marker = " Selected "
            elif ch == final_channel:
                marker = " Selected (Hysteresis Guard maintained previous)"
            elif ch == agent_chosen_channel:
                marker = " Agent Wanted (Rejected by Hysteresis)"
                
            print(f"{ch.name:<22}{ch.latency:<14.2f}{ch.bandwidth:<18.2f}"
                  f"{ch.cost:<8.2f}{ch.stability:<12.2f}{score:<10.3f}"
                  f"{str(ch.available):<8}{q_val:<10.4f}{marker}")

        print("-" * 115)

        if switched and step > 1:
            print(f"Hysteresis Switch Triggered: Moved to {final_channel.name}")

        if final_channel.bandwidth < 10 and packet.packet_type != "critical":
            print(f"Bandwidth low on {final_channel.name} non-critical packet delayed.")
            time.sleep(0.5)
            continue

        print(f"Transmitting via : {final_channel.name}")

        reward = agent.compute_reward(final_channel, packet)
        print(f"Reward  : {reward:.4f}  |  Epsilon: {agent.epsilon:.4f}")

        if prev_state is not None:
            next_available_indices = [all_channels.index(ch) for ch in env.get_available_channels()]
            agent.update(
                state                  = prev_state,
                action                 = prev_action,
                reward                 = prev_reward,
                next_state             = current_state,
                available_next_indices = next_available_indices
            )

        prev_state  = current_state
        prev_action = final_index
        prev_reward = reward

        time.sleep(1.5)

    if prev_state is not None:
        agent.update(
            state                  = prev_state,
            action                 = prev_action,
            reward                 = prev_reward,
            next_state             = prev_state,
            available_next_indices = [all_channels.index(ch) for ch in env.get_available_channels()]
        )

    agent.print_q_table(channel_names)

    print("\nSimulation complete.\n")


if __name__ == "__main__":
    run_simulation(steps=50)