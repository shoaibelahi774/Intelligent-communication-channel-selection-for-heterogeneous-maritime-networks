from channels.channel import Channel


class ShortRangeRadio(Channel):
    def __init__(self):
        super().__init__(
            name="Short-Range Radio",
            latency=5,
            bandwidth=5,
            cost=0.1,
            stability=0.4
        )
