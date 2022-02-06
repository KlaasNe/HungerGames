from random import randint

import EventsEnum
from Singleton import Singleton


class Events:

    onepl = EventsEnum.OnePlayerEvents
    twopl = EventsEnum.TwoPlayerEvents

    def get_random_1p_event(self, category):
        return self.onepl[category][randint(0, len(self.onepl[category]) - 1)]

    def get_random_2p_event(self, category):
        return self.twopl[category][randint(0, len(self.twopl[category]) - 1)]
