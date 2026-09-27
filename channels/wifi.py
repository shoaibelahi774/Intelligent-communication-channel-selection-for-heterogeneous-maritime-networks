from channels.channel import Channel


class WiFi(Channel):
    def __init__(self):
        super().__init__(
            name="WiFi",
            latency=10,
            bandwidth=200,
            cost=0.5,
            stability=0.5
        )
