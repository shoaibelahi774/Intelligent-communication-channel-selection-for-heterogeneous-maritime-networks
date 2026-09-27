from channels.channel import Channel


class GEOSatellite(Channel):
    def __init__(self):
        super().__init__(
            name="GEO Satellite",
            latency=600,
            bandwidth=20,
            cost=5,
            stability=0.95
        )


class LEOSatellite(Channel):
    def __init__(self):
        super().__init__(
            name="LEO Satellite",
            latency=80,
            bandwidth=50,
            cost=3,
            stability=0.85
        )
