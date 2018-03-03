from termcolor import colored


class Timeslot(object):
    def __init__(self, time, length=0, capacity=0):
        self.time = time
        self.length = length
        self.capacity = capacity
        self.spots_left = capacity
        self.volunteers_assigned = set()

    def to_string(self):
        if self.length == 0:
            return colored(str(self.spots_left), 'blue') + ' spots at ' + colored(self.time, 'red')
        else:
            return colored(str(self.length), 'blue') + ' hr at ' + colored(self.time, 'yellow')
