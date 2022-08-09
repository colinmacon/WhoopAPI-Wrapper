#!/usr/bin/python3

import os 
import sys
import getpass
import json
import calendar
from dateutil.rrule import *
from datetime import datetime, date, timedelta
import pandas as pd 
import pandas.io.common
from tzlocal import get_localzone_name

import requests
from requests import Session
import numpy as np 
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from pandas.core.common import SettingWithCopyWarning
warnings.simplefilter(action="ignore", category=SettingWithCopyWarning)



# Function needed for HR data interval 
def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta

# Set date ranges to get records data 
def get_records_date_ranges(user_start_string, user_end_string="yesterday"):
    userStartFormat = datetime.strptime(user_start_string, "%Y-%m-%dT%H:%M:%S.%fZ") # Convert to datetime to extract elements 
    yesterday = date.today() - timedelta(days=1) # yesterdays date
    yesterday_frmt = yesterday.strftime('%Y-%m-%dT01:00:00.000Z') # formatting to match Whoop format 

    # Getting the last day of the month from user_start_string
    lastDayOfMonth = date(userStartFormat.year, userStartFormat.month, calendar.monthrange(userStartFormat.year, userStartFormat.month)[1])
    firstDayofNextMonth = lastDayOfMonth + timedelta(1) # First day of the very next month

    # Setting ranges based on params
    if user_end_string == "yesterday":
        # Setting date range from first day of next month to start of current month
        date_range = [day.strftime('%Y-%m-%dT01:00:00.000Z') for day in rrule(MONTHLY, dtstart=date(firstDayofNextMonth.year, firstDayofNextMonth.month, firstDayofNextMonth.day), until=date.today() - timedelta(1))]
        # Appending start date and yesterdays date to lists 
        date_range.insert(0, user_start_string) # User start date goes at 0 position in list 
        date_range.append(yesterday_frmt) # Yesterday goes at the end 
    else:
        userEndFormat = datetime.strptime(user_end_string, "%Y-%m-%dT%H:%M:%S.%fZ") # Convert to datetime to extract elements 
        date_range = [day.strftime('%Y-%m-%dT01:00:00.000Z') for day in rrule(MONTHLY, dtstart=date(firstDayofNextMonth.year, firstDayofNextMonth.month, firstDayofNextMonth.day),
                                                                                        until=date(userEndFormat.year, userEndFormat.month, userEndFormat.day))]
        # Appending start date and yesterdays date to lists 
        date_range.insert(0, user_start_string) # User start date goes at 0 position in list 
        date_range.append(user_end_string) # Yesterday goes at the end 

    # Dropping duplicates incase we added dates that were already in the list
    cleaned_date_range = [i for n, i in enumerate(date_range) if i not in date_range[:n]] 

    # Setting the start and end dates to be a full month range accounting for custom user_start_date and yesterdays date
    start_dates = cleaned_date_range[:-1]
    end_dates = cleaned_date_range[1:]
    
    return start_dates, end_dates

# Set date ranges to get HR data 
def get_hr_date_ranges(user_start_string, user_end_string="yesterday", hr_range_skip_days=5):
    userStartFormat = datetime.strptime(user_start_string, "%Y-%m-%dT%H:%M:%S.%fZ") # Convert to datetime to extract elements 
    yesterday = date.today() - timedelta(days=1) # yesterdays date
    yesterday_frmt = yesterday.strftime('%Y-%m-%dT01:00:00.000Z') # formatting to match Whoop format 

    # Setting up Heart Rate range 
    hr_range = []
    if user_end_string == "yesterday":
        
        for result in perdelta(date(userStartFormat.year, userStartFormat.month, userStartFormat.day),
                            date.today() - timedelta(1), timedelta(days=hr_range_skip_days)):
            hr_range.append(result.strftime('%Y-%m-%dT01:00:00.000Z'))

        # User start date goes at 0 position in list 
        hr_range.pop(0) # Removing unformatted start date to acvoid error
        hr_range.insert(0, user_start_string) # Inserting the users start date 
        hr_range.append(yesterday_frmt) # Yesterday goes at the end 

    else:
        userEndFormat = datetime.strptime(user_end_string, "%Y-%m-%dT%H:%M:%S.%fZ")
        for result in perdelta(date(userStartFormat.year, userStartFormat.month, userStartFormat.day),
                            (date(userEndFormat.year, userEndFormat.month, userEndFormat.day)),
                            timedelta(days=hr_range_skip_days)):
            hr_range.append(result.strftime('%Y-%m-%dT01:00:00.000Z'))

        # User start date goes at 0 position in list 
        hr_range.pop(0) # Removing unformatted start date to acvoid error
        hr_range.insert(0, user_start_string) # Inserting the users start date 
        hr_range.append(user_end_string) # Yesterday goes at the end 
        
    # Dropping duplicates incase we added dates that were already in the list
    cleaned_hr_date_range = [i for n, i in enumerate(hr_range) if i not in hr_range[:n]] 

    # Setting start and end dates 
    hr_start_dates = cleaned_hr_date_range[:-1]
    hr_end_dates = cleaned_hr_date_range[1:]

    return hr_start_dates, hr_end_dates


def create_folders(folder_path):

    base_dir = os.getcwd()
    
    # CSVs dir & sub dirs paths
    sub_dir1 = "csvs"
    sub_dir1_1 = sub_dir1 + "/records"
    sub_dir1_1_1 = sub_dir1_1 + "/cycles"
    sub_dir1_1_2 = sub_dir1_1 + "/recovery"
    sub_dir1_1_3 = sub_dir1_1 + "/sleeps"
    sub_dir1_1_4 = sub_dir1_1 + "/v2"
    sub_dir1_1_5 = sub_dir1_1 + "/workouts"
    sub_dir1_2 = sub_dir1 + "/hr_data"

    # JSON dir & sub dirs paths
    sub_dir2 = "jsons"
    sub_dir2_1 = sub_dir2 + "/records"
    sub_dir2_2 = sub_dir2 + "/hr_data"
    
    # clean data dir
    sub_dir3 = "clean"
    sub_dir3_3 = sub_dir3 + "/master"
    sub_dir3_1 = sub_dir3 + "/records"
    sub_dir3_1_1 = sub_dir3_1 + "/cycles"
    sub_dir3_1_2 = sub_dir3_1 + "/recovery"
    sub_dir3_1_3 = sub_dir3_1 + "/sleeps"
    sub_dir3_1_4 = sub_dir3_1 + "/v2"
    sub_dir3_1_5 = sub_dir3_1 + "/workouts"
    sub_dir3_1_6 = sub_dir3_1 + "/grouped_workouts"
    sub_dir3_2 = sub_dir3 + "/hr_data"
    
    # saved grpahs
    sub_dir4 = "graphs"
    sub_dir4_1 = sub_dir4 + "/cycles"
    sub_dir4_2 = sub_dir4 + "/recovery"
    sub_dir4_3 = sub_dir4 + "/sleeps"
    sub_dir4_4 = sub_dir4 + "/v2"
    sub_dir4_5 = sub_dir4 + "/workouts"
    sub_dir4_6 = sub_dir4 + "/hr"

    all_folders = [sub_dir1, sub_dir1_1, sub_dir1_1_1, sub_dir1_1_2, sub_dir1_1_3, sub_dir1_1_4, sub_dir1_1_5, sub_dir1_2, 
                    sub_dir2, sub_dir2_1, sub_dir2_2,
                    sub_dir3, sub_dir3_1, sub_dir3_1_1, sub_dir3_1_2, sub_dir3_1_3, sub_dir3_1_4, sub_dir3_1_5, sub_dir3_1_6, sub_dir3_2, sub_dir3_3,
                    sub_dir4, sub_dir4_1, sub_dir4_2, sub_dir4_3, sub_dir4_4, sub_dir4_5, sub_dir4_6]
    # Create base dir 
    try:
        os.makedirs(folder_path)
        print(f"Created Directory: '{folder_path}'")
    except FileExistsError:
        # directory already exists
        pass

    # cd into base dir 
    os.chdir(folder_path)

    for f in all_folders:
        try:
            os.makedirs(f)
            print(f"Created Directory: '{f}'")
        except FileExistsError:
            # directory already exists
            pass

    os.chdir(base_dir)


def save_json(json_data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)


def refresh_token(email, password, api_base_url="https://api-7.whoop.com"):
    try:
        token_response = requests.post(
        url=f"{api_base_url}/oauth/token",
        headers={"Content-Type": "application/json; charset=utf-8",},
        data=json.dumps({"username": email,
                        "password": password,
                        "issueRefresh": True,
                        "grant_type": "password"}))


        user_id = token_response.json()['user']['id']
        access_token = token_response.json()['access_token']

    except Exception as e:
        print(f"Could not refresh API Token for {email}\n\n{e}")

    finally:
        return user_id, access_token

def concat_dfs(files_list):
    dfs = []
    for i in range(0,len(files_list)):
        try:
            df = pd.read_csv(files_list[i])
            dfs.append(df)
        except pandas.errors.EmptyDataError:
            head, tail = os.path.split(files_list[i])
            print(f"Skipping empty file : {tail}")
            
    master_df = pd.concat(dfs)
    return master_df 


class CleanWhoop:

    def __init__(self):
        self.local_zone = get_localzone_name()
        
        
    def create_overall_df(self, cycles_df, recovery_df, sleeps_df, workouts_df):
        
        grouped_workouts_df = self.group_workouts(workouts_df)
            
        naps_df = sleeps_df[sleeps_df["is_nap"]==True]
        sleeps_df = sleeps_df[sleeps_df["is_nap"]==False]

        cycles_df = cycles_df.add_prefix("c_")
        recovery_df = recovery_df.add_prefix("r_")
        sleeps_df = sleeps_df.add_prefix("s_")
        naps_df = naps_df.add_prefix("n_")
        grouped_workouts_df = grouped_workouts_df.add_prefix("gw_")
        
        # Putting cycles and recovery back together
        m1 = pd.merge(cycles_df, recovery_df, how="left", left_on="c_cycle_id", right_on="r_cycle_id")
        # Sleeps and naps df 
        m2 = pd.merge(sleeps_df, naps_df, how="left", left_on="s_cycle_id", right_on="n_cycle_id")
        # Putting first two merges together
        m3 = pd.merge(m1, m2, how="left", left_on="c_cycle_id", right_on="s_cycle_id")
        # Adding on grouped workouts because you can have multiple workouts in a day 
        m4 = pd.merge(m3, grouped_workouts_df, how="left", left_on="c_cycle_id", right_on="gw_cycle_id")

        
        export_df = m4.T.drop_duplicates().T # Drop dup cols ignoring name
        export_df.replace({'NaT': 0}, inplace=True) # Drop all rows and cols that are all nan
        export_df.replace({np.nan: 0}, inplace=True)
        
        # If a col only contains one value drop it 
        for col in export_df.columns:
            if len(export_df[col].unique()) == 1:
                export_df.drop(col,inplace=True,axis=1)
        
        return export_df
    
    
    def cycles(self, df):
        
        # Dropping rows that only contain nans
        df = df.dropna(axis=0, how='all')
        
        df.drop_duplicates(keep="last", inplace=True)

        # Converting types 
        df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_convert(self.local_zone)
        df['updated_at'] = pd.to_datetime(df['updated_at']).dt.tz_convert(self.local_zone)
        df['predicted_end'] = pd.to_datetime(df['predicted_end']).dt.tz_convert(self.local_zone)

        df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_localize(None)
        df['updated_at'] = pd.to_datetime(df['updated_at']).dt.tz_localize(None)
        df['predicted_end'] = pd.to_datetime(df['predicted_end']).dt.tz_localize(None)


        # Breaking apart 'during' column and converting time to user timezone
        df["during"] = df["during"].astype('str') 
        df["during"] = df["during"].apply(lambda x: x.replace('[','').replace(')','').replace("'",'')) 
        df[['during_start', 'during_end']] = df["during"].str.split(',', expand=True)

        df['during_start'] = pd.to_datetime(df['during_start']).dt.tz_convert(self.local_zone)
        df['during_end'] = pd.to_datetime(df['during_end']).dt.tz_convert(self.local_zone)

        df['during_start'] = pd.to_datetime(df['during_start']).dt.tz_localize(None)
        df['during_end'] = pd.to_datetime(df['during_end']).dt.tz_localize(None)

        df["days"] = df["days"].astype("string")
        df["days"] = df["days"].apply(lambda x: x.replace('[','').replace(')','').replace("'",'')) 
        df[['days_start', 'days_end']] = df["days"].str.split(',', expand=True)
        df['days_start'] = pd.to_datetime(df['days_start'], errors='coerce', format='%Y-%m-%d')
        df['days_end'] = pd.to_datetime(df['days_end'], errors='coerce', format='%Y-%m-%d')
        df.drop("days", axis=1, inplace=True)
        df.drop("during", axis=1, inplace=True)


        df["data_state"] = df["data_state"].astype('string') 
        # Sorting data by start date and resetting index 
        df = df.sort_values(by='days_start', ascending=True)
        df = df.reset_index(drop=True)

        # Adding in some columns that can be helpful
        df = df.assign(calories = df["day_kilojoules"]/4.184) # Convert kilojules to cals
        df['calories']= df['calories'].values.astype(np.int64) # Convert cals to whole number 

        # Mapping categories to strain ranges
        bins = [0, 8, 10, 14, 18, np.inf]
        names = ['minimal', 'light', 'medium', 'high', 'extreme']

        df['StrainCategory'] = pd.cut(df['scaled_strain'], bins, labels=names)

        # Adding in helper columns for day_start
        df['day_number'] = df['days_start'].dt.day
        df['week_number'] = df['days_start'].dt.isocalendar().week
        df['month_number'] = df['days_start'].dt.month
        df['year_number'] = df['days_start'].dt.year
        
        df.columns = df.columns.str.replace('id', 'cycle_id')
        
        df = df.sort_values(by='during_start', ascending=True)
        df = df.reset_index(drop=True)
        
        return df 

    def group_workouts(self, df):
        
        
        # create a column with timedelta as total hours, as a float type
        df['tot_sec_diff'] = (df.during_end - df.during_start) / pd.Timedelta(seconds=1)
        df['tot_sec_diff'] = df['tot_sec_diff'].astype('float64') 

        sum_gb = df.groupby(["cycle_id", "cycle_start"])["intensity_score", "distance", "raw_intensity_score", "altitude_gain", "altitude_change", "kilojoules", "Zone1", "Zone2", "Zone3", "Zone4", "Zone5", "Zone6"].sum().reset_index()

        rest_gb = df.groupby(["cycle_id", "cycle_start"]).agg({'sport_id':'count', 'max_heart_rate':'max', 'during_start': np.min, 'during_end': np.max, "tot_sec_diff": "sum"}).reset_index()

        merge = pd.merge(sum_gb, rest_gb, on="cycle_id")

        merge.drop(['cycle_start_y'], axis = 1, inplace = True, errors = 'ignore')

        new_col_names = ['cycle_id', 'cycle_start', 'intensity_score_total', 'distance_total', 'raw_intensity_score_total',
                        'altitude_gain_total', 'altitude_change_total', 'kilojoules_total', 'Zone1_total', 'Zone2_total',
                        'Zone3_total', 'Zone4_total', 'Zone5_total', 'Zone6_total', 'number_workouts', 'max_heart_rate_overall',
                        'earliest_workout_start', 'latest_workout_end', 'tot_sec_diff']
        
        merge.columns = new_col_names
        
        merge['tot_sec_diff'] = merge['tot_sec_diff'].astype('float64') 
        merge['total_duration'] = pd.to_datetime(merge["tot_sec_diff"], unit='s').dt.strftime("%H:%M:%S")   
        
        # Adding in some columns that can be helpful
        merge = merge.assign(calories_total = merge["kilojoules_total"]/4.184) # Convert kilojules to cals
        merge['calories_total']= merge['calories_total'].values.astype(np.int64) # Convert cals to whole number 


        return merge
    
    
    def hr(self, df):

        df['time'] = pd.to_datetime(df['time']).dt.tz_convert(self.local_zone)
        df['time'] = pd.to_datetime(df['time']).dt.tz_localize(None)

        df = df.dropna(axis=0, how='all')
        df.drop_duplicates(keep="last", inplace=True)
        
        df['date'] = pd.to_datetime(df['time'], unit='ms').dt.date 
        df['yr'] = df['time'].dt.year
        df['month'] = df['time'].dt.month
        df['week'] = df['time'].dt.isocalendar().week
        df['day'] = df['time'].dt.day


        # Adding in helper columns for day_start
        df['timestamp'] = pd.to_datetime(df['time'], unit='ms').dt.time 
        df['hour'] = pd.to_datetime(df['time'], unit='ms').dt.hour 
        df['min'] = pd.to_datetime(df['time'], unit='ms').dt.minute 
        df['sec'] = pd.to_datetime(df['time'], unit='ms').dt.second
        df['ms'] = pd.to_datetime(df['time'], unit='ms').dt.microsecond

        # Sorting data by start date and resetting index 
        df = df.sort_values(by='time', ascending=True)
        df = df.reset_index(drop=True)

        return df

    def recovery(self, df):
        
        
        # Dropping rows that only contain nans
        df = df.dropna(axis=0, how='all')

        df.drop_duplicates(keep="last", inplace=True)
        
        # Converting date columns to current timezone  
        df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_convert(self.local_zone)
        df['updated_at'] = pd.to_datetime(df['updated_at']).dt.tz_convert(self.local_zone)
        df['date'] = pd.to_datetime(df['date']).dt.tz_convert(self.local_zone)

        df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_localize(None)
        df['updated_at'] = pd.to_datetime(df['updated_at']).dt.tz_localize(None)
        df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)

        # Breaking apart 'during' column and converting time to user timezone
        df["during"] = df["during"].astype('str') 
        df["during"] = df["during"].apply(lambda x: x.replace('[','').replace(')','').replace("'",'')) 
        df[['during_start', 'during_end']] = df["during"].str.split(',', expand=True)

        df['during_start'] = pd.to_datetime(df['during_start']).dt.tz_convert(self.local_zone)
        df['during_end'] = pd.to_datetime(df['during_end']).dt.tz_convert(self.local_zone)

        df['during_start'] = pd.to_datetime(df['during_start']).dt.tz_localize(None)
        df['during_end'] = pd.to_datetime(df['during_end']).dt.tz_localize(None)
        df.drop("during", axis=1, inplace=True) # Dropping original columns
        
        # Will only exist in Whoop 4.0 data 
        if 'skin_temp_celsius' in df.columns:
            df = df.assign(skin_temp_fahrenheit = (df["skin_temp_celsius"]*1.8) + 32) # Convert celsius to fahrenheit
        else:
            df["skin_temp_celsius"] = 0.0
            df["skin_temp_fahrenheit"] = 0.0
            
        # Will only exist in Whoop 4.0 data 
        if 'spo2' in df.columns:
            pass
        else:
            df["spo2"] = 0.0

        # Converting types
        df["state"] = df["state"].astype('string') 
        df["responded"] = df["responded"].astype('bool') 
        df["calibrating"] = df["calibrating"].astype('bool') 
        df["from_sws"] = df["from_sws"].astype('bool') 
        df['cycle_id']= df['cycle_id'].values.astype(np.int64) 
        df['sleep_id']= df['sleep_id'].values.astype(np.int64) 
        df['user_id']= df['user_id'].values.astype(np.int64) 
        df['id']= df['id'].values.astype(np.int64) 
        
        df = df.fillna(0) # Fill NaN with 0
        # Converting floats to ints
        cols = ["score","resting_heart_rate","rhr_component","hrv_component","skin_temp_fahrenheit"]
        df[cols] = df[cols].astype(int)
        
        # Sorting data by start date and resetting index 
        df = df.sort_values(by='during_start', ascending=True)
        df = df.reset_index(drop=True)

        # Return clean df
        return df 

    def sleeps(self, df):

        # Dropping rows that only contain nans
        df = df.dropna(axis=0, how='all')
        
        df.drop_duplicates(keep="last", inplace=True)
        
        # Converting date columns to current timezone  
        df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_convert(self.local_zone)
        df['updated_at'] = pd.to_datetime(df['updated_at']).dt.tz_convert(self.local_zone)

        df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_localize(None)
        df['updated_at'] = pd.to_datetime(df['updated_at']).dt.tz_localize(None)

        # Breaking apart 'during' column and converting time to user timezone
        df["during"] = df["during"].astype('str') 
        df["during"] = df["during"].apply(lambda x: x.replace('[','').replace(')','').replace("'",'')) 
        df[['during_start', 'during_end']] = df["during"].str.split(',', expand=True)

        df['during_start'] = pd.to_datetime(df['during_start']).dt.tz_convert(self.local_zone)
        df['during_end'] = pd.to_datetime(df['during_end']).dt.tz_convert(self.local_zone)

        df['during_start'] = pd.to_datetime(df['during_start']).dt.tz_localize(None)
        df['during_end'] = pd.to_datetime(df['during_end']).dt.tz_localize(None)
        df.drop("during", axis=1, inplace=True) # Dropping original columns

        # Breaking apart 'optimal_sleep_times' column and converting time to user timezone
        df["optimal_sleep_times"] = df["optimal_sleep_times"].astype('str') 
        df["optimal_sleep_times"] = df["optimal_sleep_times"].apply(lambda x: x.replace('[','').replace(')','').replace("'",'')) 
        df[['optimal_sleep_time_start', 'optimal_sleep_time_end']] = df["optimal_sleep_times"].str.split(',', expand=True)

        df['optimal_sleep_time_start'] = pd.to_datetime(df['optimal_sleep_time_start'], errors="coerce").dt.tz_convert(self.local_zone)
        df['optimal_sleep_time_end'] = pd.to_datetime(df['optimal_sleep_time_end'], errors="coerce").dt.tz_convert(self.local_zone)

        df['optimal_sleep_time_start'] = pd.to_datetime(df['optimal_sleep_time_start']).dt.tz_localize(None)
        df['optimal_sleep_time_end'] = pd.to_datetime(df['optimal_sleep_time_end']).dt.tz_localize(None)
        df.drop("optimal_sleep_times", axis=1, inplace=True) # Dropping original columns

        # Breaking apart 'cycle.days' column and converting column to datetime
        df["cycle.days"] = df["cycle.days"].astype('str') 
        df["cycle.days"] = df["cycle.days"].apply(lambda x: x.replace('[','').replace(')','').replace("'",'')) 
        df[['cycle_start', 'cycle_end']] = df["cycle.days"].str.split(',', expand=True)
        df['cycle_start'] = pd.to_datetime(df['cycle_start'])
        df['cycle_end'] = pd.to_datetime(df['cycle_end'])
        df.drop("cycle.days", axis=1, inplace=True) # Dropping original columns

            
        df = df.fillna(0) # Fill NaN with 0
        
        
        # Converting types
        df["algo_version"] = df["algo_version"].astype('string') 
        df["state"] = df["state"].astype('string') 
        df["source"] = df["source"].astype('string') 

        cols = ["quality_duration", "latency", "debt_pre", "debt_post", "need_from_strain", "sleep_need", "habitual_sleep_need", "disturbances", "time_in_bed", "light_sleep_duration",
                "slow_wave_sleep_duration", "rem_sleep_duration", "cycles_count", "wake_duration", "arousal_time", "in_sleep_efficiency",
                "credit_from_naps", "sleep_consistency", "projected_score", "projected_sleep"]

        df[cols] = df[cols].astype(int)
        
        # Sorting data by start date and resetting index 
        df = df.sort_values(by='during_start', ascending=True)
        df = df.reset_index(drop=True)

        # Return clean df
        return df 

    def workouts(self, df):

        # Converting date columns to current timezone  
        df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_convert(self.local_zone)
        df['updated_at'] = pd.to_datetime(df['updated_at']).dt.tz_convert(self.local_zone)

        df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_localize(None)
        df['updated_at'] = pd.to_datetime(df['updated_at']).dt.tz_localize(None)

        df["zone_durations"] = df["zone_durations"].astype('str') 
        df["zone_durations"] = df["zone_durations"].apply(lambda x: x.replace('[','').replace(']','')) 
        df[['Zone1', 'Zone2', 'Zone3', 'Zone4', 'Zone5', 'Zone6']] = df["zone_durations"].str.split(',', expand=True)
        df["Zone1"] = pd.to_numeric(df["Zone1"])
        df["Zone2"] = pd.to_numeric(df["Zone2"])
        df["Zone3"] = pd.to_numeric(df["Zone3"])
        df["Zone4"] = pd.to_numeric(df["Zone4"])
        df["Zone5"] = pd.to_numeric(df["Zone5"])
        df["Zone6"] = pd.to_numeric(df["Zone6"])
        df.drop("zone_durations", axis=1, inplace=True)

        # Breaking apart 'during' column and converting time to user timezone
        df["during"] = df["during"].astype('str') 
        df["during"] = df["during"].apply(lambda x: x.replace('[','').replace(')','').replace("'",'')) 
        df[['during_start', 'during_end']] = df["during"].str.split(',', expand=True)

        df['during_start'] = pd.to_datetime(df['during_start']).dt.tz_convert(self.local_zone)
        df['during_end'] = pd.to_datetime(df['during_end']).dt.tz_convert(self.local_zone)

        df['during_start'] = pd.to_datetime(df['during_start']).dt.tz_localize(None)
        df['during_end'] = pd.to_datetime(df['during_end']).dt.tz_localize(None)
        df.drop("during", axis=1, inplace=True) # Dropping original columns

        # Breaking apart 'cycle.days' column and converting column to datetime
        df["cycle.days"] = df["cycle.days"].astype('str') 
        df["cycle.days"] = df["cycle.days"].apply(lambda x: x.replace('[','').replace(')','').replace("'",'')) 
        df[['cycle_start', 'cycle_end']] = df["cycle.days"].str.split(',', expand=True)
        df['cycle_start'] = pd.to_datetime(df['cycle_start'])
        df['cycle_end'] = pd.to_datetime(df['cycle_end'])
        df.drop("cycle.days", axis=1, inplace=True) # Dropping original columns

        # Converting types
        df["state"] = df["state"].astype('string') 
        df["source"] = df["source"].astype('string') 

        # Adding in some columns that can be helpful
        df = df.assign(calories = df["kilojoules"]/4.184) # Convert kilojules to cals
        df['calories']= df['calories'].values.astype(np.int64) # Convert cals to whole number 
        df.replace(to_replace=[None], value=0, inplace=True)

        # Sorting data by start date and resetting index 
        
        # Dropping columns and rows that only contain nans
        #df = df.dropna(axis=1, how='all')
        df = df.dropna(axis=0, how='all')
        df = df.fillna(0) # Fill NaN with 0


        df.drop_duplicates(keep="last", inplace=True)

        df = df.sort_values(by='during_start', ascending=True)
        df = df.reset_index(drop=True)

        # Return clean df
        return df 


class SimpleSetup:
    def __init__(self, json_filename="creds.json", api_url="https://api-7.whoop.com",):

        self.api_url = api_url
        self.json_filename = json_filename


    def check_creds_file_exists(self):
        try:
            with open(self.json_filename, 'r') as f:
                data = json.load(f)

            print(f"{self.json_filename} file found loading in user information\n")

        except IOError:
            print(f"Credentials json file not found...\nCreating {self.json_filename}")
            start_data = {"username": "", "password": "", "user_id": 0, "access_token": ""}

            # Saving dict as json file
            with open(self.json_filename, 'w') as f:
                json.dump(start_data, f, ensure_ascii=False, indent=4)

    def load_creds_file(self):
        with open(self.json_filename, 'r') as f:
            self.data = json.load(f)

        self.username = self.data['username']
        self.password = self.data['password']
        self.user_id = self.data['user_id']
        self.access_token = self.data['access_token']

    def refresh_token(self):
        try:
            response = requests.post(
            url="https://api-7.whoop.com/oauth/token",
            headers={"Content-Type": "application/json; charset=utf-8",},
            data=json.dumps({"username": self.username,
                            "password": self.password,
                            "issueRefresh": True,
                            "grant_type": "password"}))

            access_token = response.json()['access_token']
            user_id = response.json()['user']['id']


            self.data['user_id'] = user_id
            self.data['access_token'] = access_token

            # Save
            with open(self.json_filename, 'w') as fp:
                json.dump(self.data, fp)

            print(f"User ID and Access Token have been refreshed and saved to {self.json_filename}")

        except Exception as e:
            print(f"\n\nFailed to return Whoop API\nPlease try updating username (email) and passowrd in json file\n\n{e}")

    def attempt_connection(self):
            try:
                print("\n--  Attempting to connect to API now  --")
                session = Session()
                session.headers.update({
                'Content-Type': 'application/json; charset=utf-8',
                'Authorization': f'Bearer {self.access_token}',})
                self.connection_status = session.get(f'{self.api_url}/users/{self.user_id}')
                

            except Exception as e:
                print(f"\n\nCould not connect to Whoop API\n\n{e}")


    def confirm_login_info(self):
        self.load_creds_file()

        if self.username == "":
            print(f"\nUsername not found in {self.json_filename}")
            self.data['username'] = input("please enter account e-mail: ")
            # Save username to file
            with open(self.json_filename, 'w') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)

        if self.password == "":
            print(f"\nPassword not found in {self.json_filename}")
            self.data["password"] = getpass.getpass("Please enter account password: ")
            # Sacve password to file
            with open(self.json_filename, 'w') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)

        elif self.username and self.password != "":
            print(f"Username and Passowrd information found in {self.json_filename}")
            
        else:
            print("Error reading username | password from .json file")


    def confirm_creds(self):
        self.load_creds_file()
        
        if self.user_id == 0 or self.access_token == "":
            print(f"\nUser ID not found in {self.json_filename} refreshing API creds now")
            self.refresh_token()

        elif self.user_id != 0 and self.access_token != "":
            print(f"\nUser ID and API Token information found in {self.json_filename}\nSetting up Whoop API Token now...")
            self.attempt_connection()

            print(f"--  API connection status code: {self.connection_status.status_code}  --")
            if self.connection_status.status_code == 200:
                print("Current API Token connection successful\n\n")
            else:
                print("\nFailed to connect with current user credentials\nAttempting to refresh API Credentials now")
                self.refresh_token()
                self.attempt_connection()
                print("    ----  API Token refreshed  ----\n\n")
            
        else:
            print("Error getting API creds for your user_id and access_token from .json file")

    def run(self):
        self.check_creds_file_exists()
        self.confirm_login_info()
        self.confirm_creds()
        self.load_creds_file()
        return self.user_id, self.access_token


class WhoopAPI:
    __session = None
    __connection_status = None


    def __init__(self, user_id=None, api_token=None, api_url="https://api-7.whoop.com",):

        self.user_id = user_id
        self.api_token = api_token
        self.api_url = api_url


    @property
    def session(self):
        if self.__session is None:
            self.__session = Session()
            self.__session.headers.update({
                'Content-Type': 'application/json; charset=utf-8',
                'Authorization': f'Bearer {self.api_token}',
                })

        return self.__session

    @property
    def connection_status(self):
        if self.__connection_status is None:
            try:
                print("\n\n--  Attempting to connect to API now  --")
                self.__connection_status = self.session.get(f'{self.api_url}/users/{self.user_id}')
                print("-----  Session succesfully started  -----")
                print("-----------------------------------------\n")

            except Exception as e:
                print(f"Could not connect to Whoop API\n\n{e}")

        return self.__connection_status

    def test_session(self):

        if self.connection_status.status_code == 200:
            
            profile_info = self.session.get(f'{self.api_url}/users/{self.user_id}')
            profile_info = profile_info.json()

            print(f"-- API Credentials Approved for: ---\n")
            print(f"   {profile_info['fullName']} - ({profile_info['username']})\n   {profile_info['city']}, {profile_info['adminDivision']} - {profile_info['country']}\n   Membership Status: {profile_info['membershipStatus']}\n")

        elif self.connection_status.status_code == 403:
            print("--- Invalid API Token ---\nPlease run refresh_token('email_address', 'password') to refresh")

        else:
            print(f"API Connection Failed\n{self.connection_status.status_code}\n{self.connection_status.reason}\n")


# -----------------------------------------------------------------------------------------------------------------

    def profile_info(self, output_type='df'):
        try:
            json_profile_info = self.session.get(f'{self.api_url}/users/{self.user_id}')
            json_profile_info = json_profile_info.json()
            profile_info_df = pd.json_normalize(json_profile_info,max_level=0)

            pi_df2 = pd.json_normalize(profile_info_df['preferences'])
            pi_df3 = pd.json_normalize(profile_info_df['privacyProfile'])

            pi_df2 = pi_df2.add_prefix('preferences_')
            pi_df3 = pi_df3.add_prefix('privacyProfile_')
            profile_info_df = profile_info_df.drop(columns=['preferences', 'privacyProfile'])
            output_df = pd.concat([profile_info_df, pi_df2, pi_df3], axis=1)

        except Exception as e:
            print(f"Could not return profile_info_json info\\n(e)")

        finally:
            if output_type == 'df':
                return output_df

            elif output_type == 'json':
                return json_profile_info

            else:
                print(f"{output_type} is not supported please pass 'df' | 'json'")

# -----------------------------------------------------------------------------------------------------------------

    def sport_info_mapping(self, output_type='df'):
        try:
            sport_mapping_response = self.session.get(f'{self.api_url}/activities-service/v1/sports')
            sport_mapping_df = pd.DataFrame(sport_mapping_response.json())
            sport_mapping_df = sport_mapping_df.sort_values(by="id")
            sport_mapping_df = sport_mapping_df.reset_index(drop=True)

        except Exception as e:
            print(f"Failed to get sport mapping df\n\n(e)")

        finally:
            if output_type == 'df':
                return sport_mapping_df

            elif output_type == 'json':
                return sport_mapping_response.json()

            else:
                print(f"{output_type} is not supported please pass 'df' | 'json'")

# -----------------------------------------------------------------------------------------------------------------

    def get_json_cycles(self, start, end, verbose=False):

        try:

            # Cycles
            offset = 0
            total_count = sys.maxsize
            records = []
            while offset < total_count:
                response = self.session.get(
                    url=f'{self.api_url}/activities-service/v1/cycles/aggregate/range/{self.user_id}',
                    params={
                        'startTime': start,
                        'endTime': end,
                        'limit': 50,
                        'offset': offset
                    })
                if response.status_code != 200:
                    break

                records.extend(response.json()['records'])
                offset = response.json()['offset']
                total_count = response.json()['total_count']
                if verbose != False:
                    print(f'got {offset} of {total_count} items', end='\r')

            return records

        except Exception as e:
            print(f"Failed to get cycle records\n\n(e)")

        finally:
            return records

# -----------------------------------------------------------------------------------------------------------------

    def get_all(self, start, end, output_type='df'):

        try:
            cycles = pd.DataFrame()
            recovery = pd.DataFrame()
            sleeps = pd.DataFrame()
            v2_activities = pd.DataFrame()
            workouts = pd.DataFrame()

            records = self.get_json_cycles(start, end)
            records_data = pd.json_normalize(records)
            cycles_recovery_df = records_data.drop(columns=['sleeps', 'workouts', 'v2_activities'])
            cycles = cycles_recovery_df.filter(regex=r'^cycle.') 
            cycles.columns = cycles.columns.str.replace("cycle.", "")

            recovery =  cycles_recovery_df.filter(regex=r'^recovery.')
            recovery.columns = recovery.columns.str.replace("recovery.", "", regex=True)
            
            sleeps = pd.json_normalize(records, record_path=['sleeps'], meta=[['cycle', 'days']])

            v2_activities = pd.json_normalize(records, record_path=['v2_activities'], meta=[['cycle', 'days']])

            workouts = pd.json_normalize(records, record_path=['workouts'], meta=[['cycle', 'days']])

        except Exception as e:
            print(f"Failed to get cycle records\n\n(e)")
            
        finally:

            if output_type == 'df':
                return cycles, recovery, sleeps, v2_activities, workouts

            elif output_type == 'json':
                return records
            
            else:
                print(f"{output_type} is not supported please pass 'df' | 'json'")

# -----------------------------------------------------------------------------------------------------------------

    def get_specific_df(self, start, end, df_name):

        try:

            cycles = pd.DataFrame()
            recovery = pd.DataFrame()
            sleeps = pd.DataFrame()
            v2_activities = pd.DataFrame()
            workouts = pd.DataFrame()
            
            records = self.get_json_cycles(start, end)
            records_data = pd.json_normalize(records)
            cycles_recovery_df = records_data.drop(columns=['sleeps', 'workouts', 'v2_activities'])
            cycles = cycles_recovery_df.filter(regex=r'^cycle.') 
            cycles.columns = cycles.columns.str.replace("cycle.", "")

            recovery =  cycles_recovery_df.filter(regex=r'^recovery.')
            recovery.columns = recovery.columns.str.replace("recovery.", "", regex=True)
            
            sleeps = pd.json_normalize(records, record_path=['sleeps'], meta=[['cycle', 'days']])

            v2_activities = pd.json_normalize(records, record_path=['v2_activities'], meta=[['cycle', 'days']])

            workouts = pd.json_normalize(records, record_path=['workouts'], meta=[['cycle', 'days']])


        except Exception as e:
            print(f"Failed to get cycle records\n\n(e)")
            
        finally:
            
            all_df_vars = [cycles, recovery, sleeps, v2_activities, workouts]
            all_df_names = ['cycles', 'recovery', 'sleeps', 'v2_activities', 'workouts']
            index = [idx for idx, s in enumerate(all_df_names) if df_name in s][0]
            return  all_df_vars[index]

# -----------------------------------------------------------------------------------------------------------------


    def get_hr_data(self, start, end, frequency="60", output_type='df'):

        try:
            hr_series_response = self.session.get(url=f'{self.api_url}/users/{self.user_id}/metrics/heart_rate',
                            params={
                                'start': start,
                                'end': end,
                                "step": frequency, # every 6 seconds, 6 or 60 or 600
                                }
                            )

        except Exception as e:
            print(f"Could not return heart rate df\n\n{e}")

        finally:
            if output_type == 'df':
                hr_series_df = pd.DataFrame.from_dict(hr_series_response.json()['values'])
                hr_series_df['time'] = pd.to_datetime(hr_series_df['time'], unit='ms', utc=True)
                hr_series_df = hr_series_df.rename(columns={'data': 'bpm'})

                return hr_series_df

            elif output_type == 'json':          
                return hr_series_response.json()['values']
            

            else:
                print(f"{output_type} is not supported please pass 'df' | 'json'")

# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
