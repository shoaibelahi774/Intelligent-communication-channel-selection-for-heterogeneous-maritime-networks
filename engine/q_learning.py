import random
import collections


class QLearningAgent:

    def __init__(
        self,
        n_actions,
        alpha=0.1,     
        gamma=0.9,      
        epsilon=0.2,    
        epsilon_decay=0.995,    
        epsilon_min=0.01        
    ):
        self.n_actions     = n_actions
        self.alpha         = alpha
        self.gamma         = gamma
        self.epsilon       = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min   = epsilon_min
        self.q_table = collections.defaultdict(lambda: [0.0] * self.n_actions)
        self.visit_counts = collections.defaultdict(lambda: [0] * self.n_actions)



    def _bin_latency(self, latency_ms):
        if latency_ms < 100:
            return 0    
        elif latency_ms < 500:
            return 1    
        else:
            return 2    

    def _bin_bandwidth(self, bandwidth_mbps):
        if bandwidth_mbps < 10:
            return 0    
        elif bandwidth_mbps < 50:
            return 1    
        else:
            return 2    

    def get_state(self, channel, packet):
        latency_bin   = self._bin_latency(channel.latency)
        bandwidth_bin = self._bin_bandwidth(channel.bandwidth)
        priority      = packet.priority     # 1, 2, or 3
        return (latency_bin, bandwidth_bin, priority)

    
    def select_action(self, state, available_indices):
        if not available_indices:
            return None
        if random.random() < self.epsilon:
            return random.choice(available_indices)
        else:
            q_values = self.q_table[state]
            max_q = max(q_values[i] for i in available_indices)
            best_actions = [i for i in available_indices if q_values[i] == max_q]
            return random.choice(best_actions)


    def update(self, state, action, reward, next_state, available_next_indices):
        current_q = self.q_table[state][action]

        if available_next_indices:
            next_q_values  = self.q_table[next_state]
            best_next_q    = max(next_q_values[i] for i in available_next_indices)
        else:
            best_next_q = 0.0
        new_q = current_q + self.alpha * (
            reward + self.gamma * best_next_q - current_q
        )

        self.q_table[state][action] = new_q
        self.visit_counts[state][action] += 1
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def compute_reward(self, channel, packet):
        delay_penalty = channel.latency / 1000
        cost_penalty  = (channel.cost * packet.size) / 5
        reward        = channel.stability - delay_penalty - cost_penalty
        return max(-1.0, min(1.0, reward))

    def print_q_table(self, channel_names):
        latency_labels   = {0: "low-latency", 1: "medium-lat", 2: "high-lat"}
        bandwidth_labels = {0: "low-bandwidth",  1: "medium-bw",  2: "high-bw"}
        priority_labels  = {1: "background", 2: "normal", 3: "critical"}
        print("\n--- Q-Table Summary (visited states only) ---")
        print(f"{'State':<38} {'Channel':<24} {'Q-value':>8}  {'Visits':>6}")
        print("-" * 80)

        for state, q_values in sorted(self.q_table.items()):
            lat_lbl  = latency_labels.get(state[0], "?")
            bw_lbl   = bandwidth_labels.get(state[1], "?")
            pri_lbl  = priority_labels.get(state[2], "?")
            state_str = f"({lat_lbl}, {bw_lbl}, {pri_lbl})"

            for action_idx, q_val in enumerate(q_values):
                visits = self.visit_counts[state][action_idx]
                if visits > 0:
                    ch_name = channel_names[action_idx] if action_idx < len(channel_names) else str(action_idx)
                    print(f"{state_str:<38} {ch_name:<24} {q_val:>8.4f}  {visits:>6}")

        print(f"\nEpsilon (exploration rate): {self.epsilon:.4f}")
        print("-" * 80)