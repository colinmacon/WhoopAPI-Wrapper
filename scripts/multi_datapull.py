#!/usr/bin/python3

# Config script to readin scripts from parent folder 
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import packages needed to run
from tqdm.contrib import tzip
from time import sleep
from whoop import *
scrub = CleanWhoop()


'''
Script for pulling all raw data -> exporting it -> cleaning it -> exporting to clean folder 
This will be needed when you have a lot of data to pull at once
'''
# ------------------------------------------------------------------------------
#           TODO user is going to want to define variables  this area 
# ------------------------------------------------------------------------------

user_start_string = "2022-05-03T23:32:44.163Z"
user_end_string = "yesterday"

# NOTE hr_freq "6" needs shorter hr_range_skip _days | "600" can use wider range
hr_range_skip_days = 5 
hr_freq = "60" # Default | "6" "600" are the other options
itteration_pause = 2.5 # time to sleep between API calls 

# Setting up basic paths to use 
# NOTE you are going to want to leave this so the script finds the creds.json file in home path
os.chdir("..") # cd to home folder 
base_path = os.getcwd()
data_folder = "data" # Set parent folder name for data 

# NOTE if already created just skips, but can comment out 
create_folders(f"{base_path}/{data_folder}") # Create our folder structure to save the data to 

# ------------------------------------------------------------------------------
#                             Date Interval Setup
# ------------------------------------------------------------------------------

start_dates, end_dates = get_records_date_ranges(user_start_string, user_end_string)
hr_start_dates, hr_end_dates = get_hr_date_ranges(user_start_string, user_end_string, hr_range_skip_days)

print(f"\n{'-'*100}\n{'-'*100}\n")
print(f"Data pull start date range:\n{start_dates[0]} - {end_dates[-1]}\nTotal iterations: {len(start_dates)}\n\n{'-'*100}\n\n\nHeart Rate data pull start date range:\n{hr_start_dates[0]} - {hr_end_dates[-1]}\nTotal iterations: {len(hr_start_dates)}")
print(f"\n\n{'-'*100}\n{'-'*100}\n\n")

# ------------------------------------------------------------------------------
#                           General API - Setup
# ------------------------------------------------------------------------------

# SimpleSetup .json file 
ss = SimpleSetup() # NOTE use custom file name -> SimpleSetup("custon_creds.json")
userid, token = ss.run()
sleep(2.5) # Just giving the system some time before we try to access the API


# NOTE alrentative: Whoop API quick access refreshes everytime
# Reccomend to load the email and pass as env variables or from config file
#userid, token = refresh_token(email, password)

wapi = WhoopAPI(userid, token )# Firing up the WHoopAPI

# ------------------------------------------------------------------------------
#                      Get Data - Pandas DataFrames
# ------------------------------------------------------------------------------

# Creating empty lists to append csvs to later
cycles_dfs = []
recovery_dfs = []
sleeps_dfs = []
v2_dfs = []
workouts_dfs = []

# ------------------           Main Records Data             -------------------
# Pulling data records data 
for start, end in tzip(start_dates, end_dates, desc='Cycles, Recovery, Sleeps, V2 Activities, Workouts data pull '):
    # Cycles, Recovery, V2 Activities, Workouts (Activities)
    c_df, r_df, s_df, v2_df, w_df = wapi.get_all(start, end) # Default is ‘df’
    
    # Sending all raw data to csvs 
    c_df.to_csv(f"{base_path}/{data_folder}/csvs/records/cycles/{start}_{end}.csv", sep=",", index=False)
    r_df.to_csv(f"{base_path}/{data_folder}/csvs/records/recovery/{start}_{end}.csv", sep=",", index=False)
    s_df.to_csv(f"{base_path}/{data_folder}/csvs/records/sleeps/{start}_{end}.csv", sep=",", index=False)
    w_df.to_csv(f"{base_path}/{data_folder}/csvs/records/workouts/{start}_{end}.csv", sep=",", index=False)
    
    # Appending data to master list 
    cycles_dfs.append(c_df)
    recovery_dfs.append(r_df)
    sleeps_dfs.append(s_df)
    v2_dfs.append(v2_df)
    workouts_dfs.append(w_df)
    sleep(itteration_pause) # Giving API a break 

# concatenate lists of dataframes into master dfs 
master_cycles = pd.concat(cycles_dfs, ignore_index=True)  
master_recovery = pd.concat(recovery_dfs, ignore_index=True)  
master_sleeps = pd.concat(sleeps_dfs, ignore_index=True)  
master_v2 = pd.concat(v2_dfs, ignore_index=True)  
master_workouts = pd.concat(workouts_dfs, ignore_index=True)  

print(f"\nAll raw csv files for Cycles, Recovery, Sleeps, V2 Activities, Workouts has been exported to:\n{base_path}/{data_folder}\n")

# -------------------------       Clean Data        ----------------------------
cc_df = scrub.cycles(master_cycles) # c_df from wapi.get_all() | wapi.get_specific_df(start, end, "cycles")
rc_df = scrub.recovery(master_recovery) # r_df from wapi.get_all() | wapi.get_specific_df(start, end, "recovery")
sc_df = scrub.sleeps(master_sleeps) # s_df from wapi.get_all() | wapi.get_specific_df(start, end, "sleeps")
wc_df = scrub.workouts(master_workouts) # w_df from wapi.get_all() | wapi.get_specific_df(start, end, "workouts")
gwc_df = scrub.group_workouts(wc_df)
master_df = scrub.create_overall_df(cc_df,  rc_df,  sc_df,  wc_df)

# -------------------------       Export Data        ---------------------------
cc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/cycles/{start_dates[0]}_{end_dates[-1]}.csv") 
rc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/recovery/{start_dates[0]}_{end_dates[-1]}.csv")
sc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/sleeps/{start_dates[0]}_{end_dates[-1]}.csv")
wc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/workouts/{start_dates[0]}_{end_dates[-1]}.csv")
gwc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/grouped_workouts/{start_dates[0]}_{end_dates[-1]}.csv")
master_df.to_pickle(f"{base_path}/{data_folder}/clean/master/{start_dates[0]}_{end_dates[-1]}.csv")

print(f"\nData has been cleaned and exported to:\n{base_path}/{data_folder}/clean\n")


# ------------------------------------------------------------------------------
# ------------------           Heart Rate Data               -------------------
# ------------------------------------------------------------------------------

# Creating master list to append hr data to 
hr_dfs = []
# Pulling HR data 
for hr_start, hr_end in tzip(hr_start_dates, hr_end_dates, desc='Heart Rate data pull '):
    try:
        # Frequency = 60 (default) | Other options "6", "60", "600" (seconds)
        hr_df = wapi.get_hr_data(hr_start, hr_end, frequency=hr_freq)
        hr_df.to_csv(f"{base_path}/{data_folder}/csvs/hr_data/{hr_start}_{hr_end}.csv", sep=",", index=False)
        hr_dfs.append(hr_df)
        sleep(itteration_pause) # Giving API a break 
    except:
        pass

print(f"\nAll raw csv files for Heart Rate data have been exported to:\n{base_path}/{data_folder}\n")

# concatenate lists of dataframes
master_hr = pd.concat(hr_dfs, ignore_index=True)  
hrc_df = scrub.hr(master_hr) # hr_df from wapi.get_hr_data()
hrc_df.to_pickle(f"{base_path}/{data_folder}/clean/hr_data/{hr_start_dates[0]}_{hr_end_dates[-1]}.csv")

print(f"\nHeart Rate data has been cleaned and exported to:\n{base_path}/{data_folder}/clean\n")


# ------------------------------------------------------------------------------
#                           Get Data - Jsons
# ------------------------------------------------------------------------------

# Cycles, Recovery, V2 Activities, Workouts (Activities) as embedded JSON
# Pulling data records data 
'''
for start, end in tzip(start_dates, end_dates, desc='Cycles, Recovery, Sleeps, V2 Activities, Workouts data pull '):
    all_records_json = wapi.get_all(start, end, 'json') # Default is ‘df’ can also use ‘json’
    save_json(all_records_json, f"{base_path}/{data_folder}/jsons/records/{start}_{end}.json")
    sleep(itteration_pause) # Giving API a break 

'''
# Frequency = 60 (default) | Other options "6", "60", "600" (seconds)
# Pulling HR data 
'''
for hr_start, hr_end in tzip(hr_start_dates, hr_end_dates, desc='Heart Rate data pull '):
    try:
        hr_json = wapi.get_hr_data(hr_start, hr_end, output_type='json')
        save_json(hr_json, f"{base_path}/{data_folder}/jsons/hr_data/{start}_{end}.json")
        sleep(itteration_pause) # Giving API a break 
    except:
        pass
'''



print("\n\nProgram Complete: All data has been returned, combined, cleaned, and exported")
