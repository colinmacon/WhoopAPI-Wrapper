#!/usr/bin/python3

# Config script to readin scripts from parent folder 
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import packages needed to run
import glob 
from whoop import concat_dfs
from whoop import CleanWhoop
scrub = CleanWhoop()

'''
Script for combing all raw csv data -> cleaning it -> exporting to clean folder 
This will be needed when you want update clean dfs by concatenating raw csv files 
'''
# ------------------------------------------------------------------------------
#                             General- Setup
# ------------------------------------------------------------------------------
# NOTE you need to specify your start and end dates 
# as the combined files will use these dates for the end of the filename
start = "2021-12-27"
end = "2022-08-01"

# Setting up basic paths to use 
# NOTE you are going to want to leave this so the script finds /data folder (or custom name you created)
os.chdir("..") # cd to home folder 
base_path = os.getcwd() # can overwrite with custom path
data_folder = "data" # Set parent folder name for data 

# 'clean' folder for pickle | csvs for raw data (based on create_folders() function) 
folder_type = "csvs"


# ------------------------------------------------------------------------------
#                              Read-in Files
# ------------------------------------------------------------------------------

# Getting list of all files in paths
cyclesf = glob.glob(os.path.join(f"{base_path}/{data_folder}/{folder_type}/records/cycles", "*.csv"))
recoveryf = glob.glob(os.path.join(f"{base_path}/{data_folder}/{folder_type}/records/recovery", "*.csv"))
sleepsf = glob.glob(os.path.join(f"{base_path}/{data_folder}/{folder_type}/records/sleeps", "*.csv"))
workoutsf = glob.glob(os.path.join(f"{base_path}/{data_folder}/{folder_type}/records/workouts", "*.csv"))

# NOTE only for PICKLE
#grouped_workoutsf = glob.glob(os.path.join(f"{base_path}/{data_folder}/{folder_type}/records/grouped_workouts", "*.csv"))

hr_files = glob.glob(os.path.join(f"{base_path}/{data_folder}/{folder_type}/hr_data", "*.csv")) # HR 

# v2f = glob.glob(os.path.join(f"{base_path}/{data_folder}/{folder_type}/records/v2", "*.csv")) # No data for V2 

# ------------------------------------------------------------------------------
#                              Read-in CSVs
# ------------------------------------------------------------------------------

# Creating master csv for each data type
mcycles = concat_dfs(cyclesf) # Cycles
mrecovery = concat_dfs(recoveryf) # Recovery
msleeps = concat_dfs(sleepsf) # Sleeps
m_workouts = concat_dfs(workoutsf) # Workouts
mhr = concat_dfs(hr_files) # HR

# m_v2 = pd.concat((pd.read_csv(f) for f in v2f), ignore_index=True) # NO data for V2 

# -------------------     CSV Needs to be cleaned     --------------------------

# Cleaning data 
cc_df = scrub.cycles(mcycles) # Cycles
rc_df = scrub.recovery(mrecovery) # Recovery
sc_df = scrub.sleeps(msleeps) # Sleeps
wc_df = scrub.workouts(m_workouts) # Workouts
master_df = scrub.create_overall_df(cc_df,  rc_df,  sc_df,  wc_df) # Creating one df from all dfs 

gwc_df = scrub.group_workouts(wc_df) # Grouping workouts incase needed

hrc_df = scrub.hr(mhr) # HR 


# ------------------------------------------------------------------------------
#                Read-in Pickle (data doesn't need to be cleaned)
# ------------------------------------------------------------------------------

# Creating master csv for each data type

# cc_df = pd.concat((pd.read_pickle(f) for f in cyclesf), ignore_index=True)
# rc_df = pd.concat((pd.read_pickle(f) for f in recoveryf), ignore_index=True)
# sc_df = pd.concat((pd.read_pickle(f) for f in sleepsf), ignore_index=True)
# m_v2 = pd.concat((pd.read_pickle(f) for f in v2f), ignore_index=True)

# wc_df = pd.concat((pd.read_pickle(f) for f in workoutsf), ignore_index=True)
# gwc_df = pd.concat((pd.read_pickle(f) for f in grouped_workoutsf), ignore_index=True)

# hrc_df = pd.concat((pd.read_pickle(f) for f in hr_files), ignore_index=True)


# ------------------------------------------------------------------------------
#                                  Export
# ------------------------------------------------------------------------------

# Input standard cleaned workouts 
# NOTE function will automatically group workouts and seperate sleeps from naps to avoid dup lines

# start end specified at top of script (can remove or change if you want custom export name)

cc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/cycles/{start}_{end}.csv") # Cycles
rc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/recovery/{start}_{end}.csv") # Recovery
sc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/sleeps/{start}_{end}.csv") # Sleeps
wc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/workouts/{start}_{end}.csv") # Workouts
gwc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/grouped_workouts/{start}_{end}.csv")  # Grouped Workouts

master_df.to_pickle(f"{base_path}/{data_folder}/clean/master/{start}_{end}.csv") # All data

hrc_df.to_pickle(f"{base_path}/{data_folder}/clean/hr_data/{start}_{end}.csv")  # HR 


print("\n\nProgram Complete: All data has been combined and exported")
