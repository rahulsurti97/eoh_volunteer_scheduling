import pandas as pd
import numpy as np
import pprint
from volunteer import *
from timeslot import *
from station import *


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


def main():
    vol_reg = pd.read_csv('vol_reg.csv')
    vol_reg = vol_reg.drop('Saturday (10th March 2018) [Row 3]', axis=1)
    vol_reg.columns = col_names

    for col in times:
        vol_reg[col] = vol_reg[col].replace(np.nan, '')
        vol_reg[col] = vol_reg[col].replace('Available', col)

    combined = vol_reg
    combined['availability'] = combined[times].apply(lambda x: ''.join(x).strip(), axis=1)
    combined = combined.drop(times, axis=1)
    combined = combined[['email', 'availability', 'hours', 'first_pref', 'second_pref', 'third_pref']]

    combined = combined.set_index('email').to_dict()
    availability = combined['availability']
    hours = combined['hours']
    first_pref = combined['first_pref']
    second_pref = combined['second_pref']
    third_pref = combined['third_pref']
    pref = {k: [v, second_pref[k], third_pref[k]] for k, v in first_pref.items()}

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

    volunteers = {k: generate_hrs(k, v) for k, v in hours.items()}

    all_volunteers = list()

    for email, info in volunteers.items():
        timeslots = [Timeslot(timeslot, length) for timeslot, length in info[2]]
        timeslots = {timeslot: Timeslot(timeslot, length) for timeslot, length in info[2]}
        vol = Volunteer(email, hours_requested=info[0], station_preferences=info[1], timeslots_requested=timeslots)
        all_volunteers.append(vol)

    all_volunteers = sorted(all_volunteers, key=lambda x: x.hours_requested, reverse=True)
    for v in all_volunteers:
        v.to_string()

    times_filtered = [list(filter(None, time.split('|')))[0] for time in times]

    stations = pd.read_csv('stations.csv')
    stations = stations.set_index('Stations')
    stations.columns = times_filtered
    stations = stations.T
    stations_dict = stations.to_dict()

    def remove_empty_slots(slot_dict):
        return {timeslot: Timeslot(timeslot, capacity=capacity) for timeslot, capacity in slot_dict.items() if capacity != 0}
        # return {k: v for k, v in slot_dict.items() if v != 0}

    stations = [Station(name, remove_empty_slots(timeslot)) for name, timeslot in stations_dict.items()]
    # for s in stations:
    #     s.to_string()
    #
    test_vol = all_volunteers[169]
    # test_vol.use_timeslot()
    test_vol.to_string()
    stations[0].to_string()
    stations[0].assign_volunteer(test_vol, 'fri_03-09-2018_14-15')
    stations[0].to_string()
    stations[0].remove_volunteer(test_vol, 'fri_03-09-2018_14-15')
    stations[0].to_string()

    # test_vol.undo_timeslot('fri_03-09-2018_14-15')
    # test_vol.to_string()


if __name__ == '__main__':
    main()
