import random


class Channel:
    def __init__(self, name, latency, bandwidth, cost, stability):
        self.name = name
        self.latency = latency          # in ms
        self.bandwidth = bandwidth      # in Mbps
        self.cost = cost                # cost per MB
        self.stability = stability      # 0 to 1
        self.available = True

    def fluctuate(self):
        """Simulate dynamic network condition changes."""
        self.latency += random.uniform(-5, 5)
        self.bandwidth += random.uniform(-10, 10)

        # Keep values realistic
        self.latency = max(1, self.latency)
        self.bandwidth = max(1, self.bandwidth)

    def simulate_failure(self):
        """Randomly simulate link failure based on stability."""
        self.available = random.random() < self.stability

    def get_status(self):
        return {
            "name": self.name,
            "latency": self.latency,
            "bandwidth": self.bandwidth,
            "cost": self.cost,
            "stability": self.stability,
            "available": self.available
        }
