import pandas as pd
import numpy as np
import pprint
from volunteer import *
from timeslot import *
from station import *
import heapq as hq


pd.options.mode.chained_assignment = None
pd.set_option('max_colwidth', -1)
pp = pprint.PrettyPrinter(indent=4)

col_names = ['timestamp',
             'email',
             'name',
             'illinois_email',
             'phone',
             'shirt_size',
             'rso',
             'first_pref',
             'second_pref',
             'third_pref',
             'hours',
             'tue_03-06-2018_17-20|',
             'tue_03-06-2018_20-23|',
             'wed_03-07-2018_9-12|',
             'wed_03-07-2018_12-15|',
             'wed_03-07-2018_15-17|',
             'wed_03-07-2018_17-20|',
             'wed_03-07-2018_20-23|',
             'thu_03-08-2018_9-12|',
             'thu_03-08-2018_12-15|',
             'thu_03-08-2018_15-18|',
             'thu_03-08-2018_18-20|',
             'thu_03-08-2018_20-22|',
             'fri_03-09-2018_7-8|',
             'fri_03-09-2018_8-9|',
             'fri_03-09-2018_9-10|',
             'fri_03-09-2018_10-11|',
             'fri_03-09-2018_11-12|',
             'fri_03-09-2018_12-13|',
             'fri_03-09-2018_13-14|',
             'fri_03-09-2018_14-15|',
             'fri_03-09-2018_15-16|',
             'fri_03-09-2018_16-17|',
             'sat_03-10-2018_7-8|',
             'sat_03-10-2018_8-9|',
             'sat_03-10-2018_9-10|',
             'sat_03-10-2018_10-11|',
             'sat_03-10-2018_11-12|',
             'sat_03-10-2018_12-13|',
             'sat_03-10-2018_13-14|',
             'sat_03-10-2018_14-15|',
             'sat_03-10-2018_15-16|',
             'sat_03-10-2018_16-17|',
             'sat_03-10-2018_17-18|',
             'sun_03-11-2018_8-11|',
             'sun_03-11-2018_11-14|',
             'sun_03-11-2018_14-16|',
             'sun_03-11-2018_16-18',
             ]

times = ['tue_03-06-2018_17-20|',
         'tue_03-06-2018_20-23|',
         'wed_03-07-2018_9-12|',
         'wed_03-07-2018_12-15|',
         'wed_03-07-2018_15-17|',
         'wed_03-07-2018_17-20|',
         'wed_03-07-2018_20-23|',
         'thu_03-08-2018_9-12|',
         'thu_03-08-2018_12-15|',
         'thu_03-08-2018_15-18|',
         'thu_03-08-2018_18-20|',
         'thu_03-08-2018_20-22|',
         'fri_03-09-2018_7-8|',
         'fri_03-09-2018_8-9|',
         'fri_03-09-2018_9-10|',
         'fri_03-09-2018_10-11|',
         'fri_03-09-2018_11-12|',
         'fri_03-09-2018_12-13|',
         'fri_03-09-2018_13-14|',
         'fri_03-09-2018_14-15|',
         'fri_03-09-2018_15-16|',
         'fri_03-09-2018_16-17|',
         'sat_03-10-2018_7-8|',
         'sat_03-10-2018_8-9|',
         'sat_03-10-2018_9-10|',
         'sat_03-10-2018_10-11|',
         'sat_03-10-2018_11-12|',
         'sat_03-10-2018_12-13|',
         'sat_03-10-2018_13-14|',
         'sat_03-10-2018_14-15|',
         'sat_03-10-2018_15-16|',
         'sat_03-10-2018_16-17|',
         'sat_03-10-2018_17-18|',
         'sun_03-11-2018_8-11|',
         'sun_03-11-2018_11-14|',
         'sun_03-11-2018_14-16|',
         'sun_03-11-2018_16-18',
         ]


def load_vol_reg():
    vol_reg = pd.read_csv('vol_reg.csv')
    vol_reg = vol_reg.drop('Saturday (10th March 2018) [Row 3]', axis=1)
    vol_reg.columns = col_names

    for col in times:
        vol_reg[col] = vol_reg[col].replace(np.nan, '')
        vol_reg[col] = vol_reg[col].replace('Available', col)

    vol_reg['availability'] = vol_reg[times].apply(lambda x: ''.join(x).strip(), axis=1)
    vol_reg = vol_reg.drop(times, axis=1)
    vol_reg = vol_reg[['email', 'availability', 'hours', 'first_pref', 'second_pref', 'third_pref']]
    vol_reg = vol_reg.set_index('email').to_dict()

    return vol_reg


def create_vol_dict(vol_reg):
    availability = vol_reg['availability']
    hours = vol_reg['hours']
    first_pref = vol_reg['first_pref']
    second_pref = vol_reg['second_pref']
    third_pref = vol_reg['third_pref']

    pref = dict()
    for k, v in first_pref.items():
        first = v if v != 'Advancement' else 'General Volunteer'
        second = second_pref[k] if second_pref[k] != 'Advancement' else 'General Volunteer'
        third = third_pref[k] if third_pref[k] != 'Advancement' else 'General Volunteer'
        pref[k] = [first, second, third]
    # pref = {k: [v, second_pref[k], third_pref[k]] for k, v in first_pref.items()}

    def compute_hrs(slot):
        time = slot.split('_')[2]
        split = time.split('-')
        start = int(split[0])
        end = int(split[1])
        return end - start

    def generate_hrs(k, v):
        avail = availability[k].split('|')
        avail = filter(None, avail)
        ret = [(a, compute_hrs(a)) for a in avail]
        return (v, pref[k], ret)

    vol_dict = {k: generate_hrs(k, v) for k, v in hours.items()}

    return vol_dict


def create_volunteers(vol_dict):
    volunteers = list()

# >>> heappush(h, (5, 'write code'))
# >>> heappush(h, (7, 'release product'))
# >>> heappush(h, (1, 'write spec'))
# >>> heappush(h, (3, 'create tests'))
# >>> heappop(h)

    for email, info in vol_dict.items():
        timeslots = [Timeslot(timeslot, length) for timeslot, length in info[2]]
        timeslots = {timeslot: Timeslot(timeslot, length) for timeslot, length in info[2]}
        vol = Volunteer(email, hours_requested=info[0], station_preferences=info[1], timeslots_requested=timeslots)
        volunteers.append(vol)

    volunteers = sorted(volunteers, key=lambda x: x.hours_requested, reverse=True)

    return volunteers


def get_volunteers():
    vol_reg = load_vol_reg()
    vol_dict = create_vol_dict(vol_reg)
    volunteers = create_volunteers(vol_dict)
    return volunteers


def get_stations():
    times_filtered = [list(filter(None, time.split('|')))[0] for time in times]

    stations = pd.read_csv('stations.csv')
    stations = stations.set_index('Stations')
    stations.columns = times_filtered
    stations = stations.T
    stations_dict = stations.to_dict()

    def remove_empty_slots(slot_dict):
        return {timeslot: Timeslot(timeslot, capacity=capacity) for timeslot, capacity in slot_dict.items() if capacity != 0}
        # return {k: v for k, v in slot_dict.items() if v != 0}

    stations = [Station(name, remove_empty_slots(timeslots)) for name, timeslots in stations_dict.items()]
    stations = {s.name: s for s in stations}
    return stations


def main():
    volunteers = get_volunteers()
    stations = get_stations()

    #
    # test_vol = volunteers[169]
    # test_station = stations[0]

    # test_vol.to_string()
    # test_station.to_string()

    # for t in test_station.timeslots_available:
    #     test_station.assign_volunteer(test_vol, t)

    # for t in test_station.timeslots_available:
    #     test_station.remove_volunteer(test_vol, t)

    # test_station.assign_volunteer(test_vol, 'fri_03-09-2018_14-15')
    # test_station.to_string()
    # test_station.remove_volunteer(test_vol, 'fri_03-09-2018_14-15')
    # test_station.to_string()

    # test_vol.undo_timeslot('fri_03-09-2018_14-15')
    # test_vol.to_string()

    for vol in volunteers:
        station = stations[vol.station_preferences[0]]
        for t, slot in vol.timeslots_requested.items():
            station.assign_volunteer(vol, t)

    for vol in volunteers:
        station = stations[vol.station_preferences[1]]
        for t, slot in vol.timeslots_requested.items():
            station.assign_volunteer(vol, t)

    for vol in volunteers:
        station = stations[vol.station_preferences[2]]
        for t, slot in vol.timeslots_requested.items():
            station.assign_volunteer(vol, t)

        # station.to_string()

        # print(vol.email, '\t\t', station.name)
    # for s, station in stations.items():
    #     station.to_string()

    # for vol in reversed(volunteers):
    #     vol.to_string()

    # stations['Discover EOH'].to_string()

    for s, station in stations.items():
        for time, timeslot in station.timeslots_available.items():
            if timeslot.spots_left > 0:
                for v in volunteers:
                    if time in v.timeslots_requested:
                        station.assign_volunteer(v, time)

    # for s, station in stations.items():
    #     for time, timeslot in station.timeslots_available.items():
    #         if timeslot.spots_left > 0:
    #             print(s, timeslot.to_string())

    for vol in reversed(volunteers):
        if vol.hours_requested > 0:
            vol.to_string()


if __name__ == '__main__':
    main()
