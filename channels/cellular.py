from channels.channel import Channel

class Cellular4G(Channel):
    def __init__(self):
        super().__init__(
            name="4G Cellular",
            latency=40,
            bandwidth=100,
            cost=1,
            stability=0.7
        )
