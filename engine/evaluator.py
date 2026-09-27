from utils.normalizer import normalize


class Evaluator:
    def __init__(self):
        self.weights = {
            "bandwidth": 0.4,
            "latency":   0.3,
            "cost":      0.2,
            "stability": 0.1
        }

    def evaluate(self, channels):
        if not channels:
            return None, []

        latencies   = [c.latency   for c in channels]
        bandwidths  = [c.bandwidth for c in channels]
        costs       = [c.cost      for c in channels]
        stabilities = [c.stability for c in channels]

        min_lat,  max_lat  = min(latencies),   max(latencies)
        min_bw,   max_bw   = min(bandwidths),  max(bandwidths)
        min_cost, max_cost = min(costs),        max(costs)
        min_stab, max_stab = min(stabilities), max(stabilities)

        scored_channels = []

        for c in channels:
            latency_norm   = normalize(c.latency,   min_lat,  max_lat)
            bandwidth_norm = normalize(c.bandwidth, min_bw,   max_bw)
            cost_norm      = normalize(c.cost,      min_cost, max_cost)
            stability_norm = normalize(c.stability, min_stab, max_stab)

            score = (
                 self.weights["bandwidth"] * bandwidth_norm
                - self.weights["latency"]  * latency_norm
                - self.weights["cost"]     * cost_norm
                + self.weights["stability"]* stability_norm
            )
            scored_channels.append((c, score))

        scored_channels.sort(key=lambda x: x[1], reverse=True)
        best_channel, best_score = scored_channels[0]
        return best_channel, scored_channels
