class DecisionEngine:

    def __init__(self, threshold=0.05):
        self.current_channel   = None
        self.current_q_value   = 0.0
        self.threshold         = threshold  # lowered from 0.1 — Q-values are smaller numbers

    def decide(self, chosen_channel, chosen_q_value):
        switched = False

        # First step — no current channel yet
        if self.current_channel is None:
            self.current_channel = chosen_channel
            self.current_q_value = chosen_q_value
            switched = True

        else:
            # Current channel failed — must switch immediately
            if not self.current_channel.available:
                self.current_channel = chosen_channel
                self.current_q_value = chosen_q_value
                switched = True

            # Q-agent recommends a different channel AND it is meaningfully better
            elif (chosen_channel != self.current_channel and
                  chosen_q_value > self.current_q_value + self.threshold):
                self.current_channel = chosen_channel
                self.current_q_value = chosen_q_value
                switched = True

        return self.current_channel, switched

    def reset(self):
        self.current_channel = None
        self.current_q_value = 0.0