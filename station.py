from termcolor import colored


class Station():
    def __init__(self, name, timeslots_available, volunteers=set()):
        self.name = name
        self.timeslots_available = timeslots_available
        # self.volunteers = volunteers

    def to_string(self):
        print(colored(self.name, 'magenta'))

        print('\tTimeslots Available:')
        for time, timeslot in self.timeslots_available.items():
            print('\t\t' + timeslot.to_string())
            for v in timeslot.volunteers_assigned:
                print('\t\t\t' + colored(v.email, 'magenta'))

    def assign_volunteer(self, volunteer, time):
        if time not in self.timeslots_available:
            # print('TIMESLOT ' + colored(time, 'red') + ' NOT AVAILABLE')
            return False

        if self.timeslots_available[time].spots_left <= 0:
            # print('TIMESLOT ' + colored(time, 'red') + ' FULL')
            return False

        # print('\nTIMESLOT ' + colored(time, 'red'))
        # for v in self.timeslots_available[time].volunteers_assigned:
        #     print('\t', v.email)

        # print(self.timeslots_available[time].volunteers_assigned)
        if volunteer.use_timeslot(time):
            self.timeslots_available[time].spots_left -= 1
            # print('adding volunteer', volunteer)
            self.timeslots_available[time].volunteers_assigned.add(volunteer)

        # for v in self.timeslots_available[time].volunteers_assigned:
        #     print('\t', v.email)

    def remove_volunteer(self, volunteer, time):
        if time not in self.timeslots_available:
            # print('TIMESLOT ' + colored(time, 'red') + ' NOT AVAILABLE')
            return False

        if self.timeslots_available[time].spots_left == self.timeslots_available[time].capacity:
            # print('TIMESLOT ' + colored(time, 'red') + ' EMPTY')
            return False

        if volunteer.undo_timeslot(time):
            self.timeslots_available[time].spots_left += 1
            self.timeslots_available[time].volunteers_assigned.remove(volunteer)
