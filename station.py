from termcolor import colored


class Station():
    def __init__(self, name, timeslots_available, volunteers=set()):
        self.name = name
        self.timeslots_available = timeslots_available
        self.volunteers = volunteers

    def to_string(self):
        print(colored(self.name, 'magenta'))

        print('\tTimeslots Available:')
        for t, v in self.timeslots_available.items():
            print('\t\t' + v.to_string())

        print('\tVolunteers Assigned:')
        for v in self.volunteers:
            print('\t\t' + colored(v.email, 'magenta'))

    def assign_volunteer(self, volunteer, time):
        if self.timeslots_available[time].spots_left <= 0:
            print('TIMESLOT ' + colored(time, 'red') + ' FULL')
            return False

        if volunteer.use_timeslot(time):
            self.volunteers.add(volunteer)
            self.timeslots_available[time].spots_left -= 1

    def remove_volunteer(self, volunteer, time):
        if self.timeslots_available[time].spots_left == self.timeslots_available[time].capacity:
            print('TIMESLOT ' + colored(time, 'red') + ' EMPTY')
            return False

        if volunteer.undo_timeslot(time):
            self.volunteers.remove(volunteer)
            self.timeslots_available[time].spots_left += 1
