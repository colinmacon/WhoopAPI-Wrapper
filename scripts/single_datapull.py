#!/usr/bin/python3

# Config script to readin scripts from parent folder 
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import packages needed to run
from time import sleep
from whoop import *
scrub = CleanWhoop()

'''
Script for pulling all raw data -> exporting it -> cleaning it -> exporting to clean folder 
This will be needed when you want to pull a singular timeframe of data
'''

# ------------------------------------------------------------------------------
#           TODO user is going to want to define variables  this area 
# ------------------------------------------------------------------------------

# Specify your start and end dates to use 
start = "2022-07-24T01:00:00.000Z"
end = "2022-08-07T01:00:00.000Z"

# HR range must be smaller to avoid bad response
hr_start = "2022-08-03T01:00:00.000Z"
hr_end = "2022-08-07T01:00:00.000Z"

hr_freq = "60" # Default | "6" "600" are the other options
itteration_pause = 2.5 # time to sleep between API calls 


# Setting up basic paths to use 
# NOTE you are going to want to leave this so the script finds the creds.json file in home path
os.chdir("..") # cd to home folder 
base_path = os.getcwd()
data_folder = "data" # Set parent folder name for data 

# NOTE if already created just skips, but can comment out 
create_folders(f"{base_path}/{data_folder}")

# ------------------------------------------------------------------------------
#                     Get Data - Pandas DataFrames
# ------------------------------------------------------------------------------

# SimpleSetup .json file 
ss = SimpleSetup() # NOTE use custom file name -> SimpleSetup("custon_creds.json")
userid, token = ss.run()
sleep(2.5) # Just giving the system some time before we try to access the API

# NOTE alrentative: Whoop API quick access refreshes everytime
# Reccomend to load the email and pass as env variables or from config file
#userid, token = refresh_token(email, password)

# Firing up the WHoopAPI
wapi = WhoopAPI(userid, token) # Start Whoop API

# Test the session to see if your creds pass
wapi.test_session()

# Return your info in pandas df 
pi_df = wapi.profile_info() # Nothing specified will return pandas df
pi_df.to_csv(f"{base_path}/{data_folder}/csvs/records/profile_info.csv", sep=",", index=False)

# All activities that Whoop has avaliable
si_df = wapi.sport_info_mapping() # Nothing specified will return pandas df
si_df.to_csv(f"{base_path}/{data_folder}/csvs/records/sports_info.csv", sep=",", index=False)


# Cycles, Recovery, V2 Activities, Workouts (Activities)
c_df, r_df, s_df, v2_df, w_df = wapi.get_all(start, end) # Default is ‘df’

# -------------------------   Export Raw data    -------------------------------
c_df.to_csv(f"{base_path}/{data_folder}/csvs/records/cycles/{start}_{end}.csv", sep=",", index=False)
r_df.to_csv(f"{base_path}/{data_folder}/csvs/records/recovery/{start}_{end}.csv", sep=",", index=False)
s_df.to_csv(f"{base_path}/{data_folder}/csvs/records/sleeps/{start}_{end}.csv", sep=",", index=False)
w_df.to_csv(f"{base_path}/{data_folder}/csvs/records/workouts/{start}_{end}.csv", sep=",", index=False)

sleep(itteration_pause) # Giving API a break 

# Return a specific df - 'cycles', 'recovery', 'sleeps', 'v2_activities', 'workouts'
# c_df2 = wapi.get_specific_df(start, end, 'cycles')
# r_df2 = wapi.get_specific_df(start, end, 'recovery')
# s_df2 = wapi.get_specific_df(start, end, 'sleeps')
# v2_df2 = wapi.get_specific_df(start, end, 'v2_activities')
# w_df2 = wapi.get_specific_df(start, end, 'workouts')

# ------------------------------------------------------------------------------
# ----------------   Heart Rate Data - Pandas DataFrames   ---------------------
# ------------------------------------------------------------------------------

# Frequency = 60 (default) | Other options "6", "60", "600" (seconds)
hr_df = wapi.get_hr_data(hr_start, hr_end, hr_freq)
hr_df.to_csv(f"{base_path}/{data_folder}/csvs/hr_data/{hr_start}_{hr_end}.csv", sep=",", index=False)

sleep(itteration_pause) # Giving API a break 


# ------------------------------------------------------------------------------
# -----------------            Clean Data              -------------------------
# ------------------------------------------------------------------------------

cc_df = scrub.cycles(c_df) #Cycles Cleaned df |  c_df from wapi.get_all() | wapi.get_specific_df(start, end, "cycles")
rc_df = scrub.recovery(r_df) #Recovery Cleaned df |  r_df from wapi.get_all() | wapi.get_specific_df(start, end, "recovery")
sc_df = scrub.sleeps(s_df) #  Sleeps Cleaned df | s_df from wapi.get_all() | wapi.get_specific_df(start, end, "sleeps")
wc_df = scrub.workouts(w_df) # Workouts Cleaned df | w_df from wapi.get_all() | wapi.get_specific_df(start, end, "workouts")
# NOTE Takes the WORKOUTS CLEANED df not raw data | needs the dtypes from the cleaned data
gwc_df = scrub.group_workouts(wc_df) # Grouped Workouts Cleaned df

# Cycles, Recovery, Sleeps, Workouts (NOT grouped this will be done for us)
master_df = scrub.create_overall_df(cc_df,  rc_df,  sc_df,  wc_df)

hrc_df = scrub.hr(hr_df) # lean Heart Rate df'' | hr_df from wapi.get_hr_data()

# ------------------------------------------------------------------------------
# -------------------------   Export Clean Data     ----------------------------
# ------------------------------------------------------------------------------

# NOTE using pickle in order to save types | Except for profile info and sports info
cc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/cycles/{start}_{end}.csv") 
rc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/recovery/{start}_{end}.csv")
sc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/sleeps/{start}_{end}.csv")
wc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/workouts/{start}_{end}.csv")
gwc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/grouped_workouts/{start}_{end}.csv")

master_df.to_pickle(f"{base_path}/{data_folder}/clean/master/{start}_{end}.csv")

hrc_df.to_pickle(f"{base_path}/{data_folder}/clean/hr_data/{hr_start}_{hr_end}.csv")

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
#                           Get Data - Jsons
# ------------------------------------------------------------------------------

# Profile info 
# pi_json = wapi.profile_info('json') # Json version
# sleep(2.5) # Giving API a break 

# All activities that Whoop has avaliable
# si_json = wapi.sport_info_mapping('json') 
# sleep(2.5) # Giving API a break 

# Cycles, Recovery, V2 Activities, Workouts (Activities) as embedded JSON
# all_records_json = wapi.get_all(start, end, 'json') # Default is ‘df’ can also use ‘json’
# sleep(5) # Giving API a break 

# Frequency = 60 (default) | Other options "6", "60", "600" (seconds)
# hr_json = wapi.get_hr_data(hr_start, hr_end, output_type='json')
# sleep(5) # Giving API a break 

# ------------------------------------------------------------------------------
# -----------------         Export JSONs Data     ----------------------------
# ------------------------------------------------------------------------------

# ave_json(pi_json, f"{base_path}/{data_folder}/jsons/profile_info.json")
# save_json(si_json, f"{base_path}/{data_folder}/jsons/sports_info.json")
# save_json(all_records_json, f"{base_path}/{data_folder}/jsons/records/{start}_{end}.json")
# save_json(hr_json, f"{base_path}/{data_folder}/jsons/hr_data/{start}_{end}.json")


print("\n\nProgram Complete: All data has been returned, combined, cleaned, and exported")
