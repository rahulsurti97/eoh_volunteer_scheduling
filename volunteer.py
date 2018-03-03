from termcolor import colored


class Volunteer(object):
    def __init__(self, email, hours_requested, station_preferences, timeslots_requested):
        self.email = email
        self.station_preferences = station_preferences
        total_hrs = 0
        for time, timeslot in timeslots_requested.items():
            total_hrs += timeslot.length

        self.hours_requested = min(hours_requested, total_hrs)
        self.timeslots_requested = timeslots_requested
        self.timeslots_used = set()
        self.original_hours = hours_requested

    def use_timeslot(self, time):
        if time in self.timeslots_used:
            # print('ALREADY USED TIMESLOT', time)
            return False

        if time not in self.timeslots_requested:
            # print('TIMESLOT NOT REQUESTED', time)
            return False

        if self.hours_requested - self.timeslots_requested[time].length < -2:
            # print('TIMESLOT HOURS', self.timeslots_requested[time].length, 'MORE THAN REQUESTED HOURS', self.hours_requested)
            return False

        self.timeslots_used.add(time)
        self.hours_requested -= self.timeslots_requested[time].length
        return True

    def undo_timeslot(self, time):
        if time not in self.timeslots_used:
            # print('NOT USED TIMESLOT', time)
            return False

        if self.hours_requested + self.timeslots_requested[time].length > self.original_hours:
            print(timeslot, self.hours_requested, "EXCEEDING ORIGINAL HOURS", self.original_hours)
            return False

        self.timeslots_used.remove(time)
        self.hours_requested += self.timeslots_requested[time].length
        return True

    def to_string(self):
        print(colored(self.email, 'magenta'))
        print('\tHours Requested', colored(self.original_hours, 'yellow'))
        print('\tHours Remaining', colored(self.hours_requested, 'yellow'))

        print('\tStation Preferences:')
        for s in self.station_preferences:
            print('\t\t' + colored(s, 'green'))

        print('\tTimeslots Available:')
        for t, v in self.timeslots_requested.items():
            if t in self.timeslots_used:
                print('\t\t' + v.to_string(), 'used')
            else:
                print('\t\t' + v.to_string())
