from channels.satellite import GEOSatellite, LEOSatellite
from channels.cellular import Cellular4G
from channels.wifi import WiFi
from channels.radio import ShortRangeRadio


class Environment:
    def __init__(self):
        self.channels = [
            Cellular4G(),   
            WiFi(),
            ShortRangeRadio(),
            LEOSatellite(),
            GEOSatellite()
        ]

        self.time_step = 0

    def update(self):
        """
        Simulate environment change at each time step.
        """
        self.time_step += 1

        for channel in self.channels:
            channel.fluctuate()
            channel.simulate_failure()

    def get_available_channels(self):
        return [c for c in self.channels if c.available]

    def get_all_channels(self):
        return self.channels
