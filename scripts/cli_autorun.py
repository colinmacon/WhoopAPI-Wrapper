#!/usr/bin/python3

# Config script to readin scripts from parent folder 
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import packages needed to run
import pyfiglet
from termcolor import colored
import inquirer

import json
from tqdm.contrib import tzip
from time import sleep
from whoop import *
from charts import VisableWhoop
scrub = CleanWhoop()

# ------------------------------------------------------------------------------
#                             General- CLI SETUP
# ------------------------------------------------------------------------------

# Whoop Unoffical API
print(colored(pyfiglet.figlet_format("Whoop Unoffical API", font = "slant", width = 150),'red'))


questions1 = [
    inquirer.Text("email_addr", message="Whoop account email address"),
    inquirer.Password("password", message="Whoop account password"),
]
questions2 = [
    inquirer.Text("user_start_date", message="Leave blank to use Whoop Profile Info 'updatedAt' date"),
]
questions3 = [
    inquirer.Text("user_end_date", message="Leave blank to use yesterday's date"),
    inquirer.Text("data_folder", message="Name your folder where the data will be saved"),
    inquirer.Text("creds_file", message="Name your credentials file where UserID and Token will be stored (Ex: creds.json)"),
    inquirer.List('hr_freq',
                    message="Frquency of Heart Rate data (seconds)",
                    choices=["6", "60", "600"],
                    default="60"
                ),
    inquirer.Text("pause", message="Amount of time to sleep inbetween API calls"),
    inquirer.List("clean_data", message="Clean your data?", choices=["Yes", "No"], default="Yes"),
]

follow_up_questions = [
    inquirer.List("create_graphs", message="Create graphs?", choices=["Yes", "No"], default="Yes"),
]

follow_up_questions2 = [
    inquirer.List('graph_format',
                message="Static (.png) or Interactive (.html) graphs?",
                choices=["png", "html"],
                default="interactive"
            ),
]




# Answers from above
answers1 = inquirer.prompt(questions1)
print("\nTimestamp of first data\n(without converting to local time),\n Ex: 2022-02-01T22:45:00.000Z = 2022-02-01 10:45PM UTC")
answers2 = inquirer.prompt(questions2)
print("\nTimestamp of last data you want to pull \nEx: 2022-08-01T01:00:00.000Z")
answers3 = inquirer.prompt(questions3)

# Extracting answers 
email_input = answers1['email_addr']
password_input = answers1['password']
user_input_startdate = answers2['user_start_date']
user_input_enddate = answers3['user_end_date']
creds_input = answers3['creds_file']
data_folder = answers3['data_folder']
user_hr_freq = answers3['hr_freq']
itteration_pause_str = answers3['pause']
itteration_pause = float(itteration_pause_str) # convert str to float 
clean_data = answers3['clean_data']

# Conditional based on clean_data
if clean_data == "Yes":
    followup_answers = inquirer.prompt(follow_up_questions)
    create_user_graphs = followup_answers['create_graphs']

else:
    create_user_graphs = ""
    graph_format =""

# Conditional based on clean_data
if create_user_graphs == "Yes":
    followup_answers2 = inquirer.prompt(follow_up_questions2)
    graph_format = followup_answers2['graph_format']

else:
    pass

print(f"Raw data will be stored at {data_folder}/csvs/records/..\nPulling data for {user_input_startdate} - {user_input_enddate} now")                                    
print("-------------------------------------------------------------------------------------------------\n\n")

# ------------------------------------------------------------------------------
#                        General Setup - Whoop API
# ------------------------------------------------------------------------------

# Setting up basic paths to use 
# NOTE you are going to want to leave this so the script finds the creds.json file in home path
os.chdir("..") # cd to home folder 
base_path = os.getcwd()

# Create our folder structure to save the data to 
create_folders(f"{base_path}/{data_folder}")

# Setting up base values for json files 
try:
    with open(creds_input, 'r') as f:
        data = json.load(f)

    print(f"{creds_input} file found loading in user information\n")

except IOError:
    print(f"Credentials json file not found...\nCreating {creds_input}")
    start_data = {"username": email_input, "password": password_input, "user_id": 0, "access_token": ""}

    # Saving dict as json file
    with open(creds_input, 'w') as f:
        json.dump(start_data, f, ensure_ascii=False, indent=4)


print("\n")
# SimpleSetup .json file 
ss = SimpleSetup(creds_input) # NOTE use custom file name -> SimpleSetup("custon_creds.json")
userid, token = ss.run()
sleep(2.5) # Just giving the system some time before we try to access the API

#  ----------------------  Starting Whoop API   -------------------------------

wapi = WhoopAPI(userid, token) # Init Whoop API wrapper 


# Test the session to see if your creds pass
wapi.test_session()

# Return your info in pandas df 
pi_df = wapi.profile_info() # Nothing specified will return pandas df


# All activities that Whoop has avaliable
si_df = wapi.sport_info_mapping() # Nothing specified will return pandas df

# Saving our general information for user 
pi_df.to_csv(f"{base_path}/{data_folder}/csvs/records/profile_info.csv", sep=",", index=False)
print(f"Profile information has been saved as a csv to:\n{data_folder}/csvs/records/\n")

si_df.to_csv(f"{base_path}/{data_folder}/csvs/records/sports_info.csv", sep=",", index=False)
print(f"Whoop Activity Dictionary information saved as a csv to:\n{data_folder}/csvs/records/")

# Setting up HR time ranges based on user input 
if user_hr_freq == "6":
    hr_range_skip_days = 2 # Days to span timerange for HR data pull 
elif user_hr_freq == "60":
    hr_range_skip_days = 5 # Days to span timerange for HR data pull 
else:
    hr_range_skip_days = 7


# ------------------------------------------------------------------------------
#    General Data Pull Interval & Heart Rate Data Pull Interval - Setup
# ------------------------------------------------------------------------------

if user_input_startdate == '':
    user_start_string = pi_df.iloc[0]['updatedAt'] # Getting start data instance 
else:
    user_start_string = user_input_startdate
    
if user_input_enddate != '':
    user_end_string = user_input_enddate
else:
    user_end_string = "yesterday"


start_dates, end_dates = get_records_date_ranges(user_start_string, user_end_string)
hr_start_dates, hr_end_dates = get_hr_date_ranges(user_start_string, user_end_string, hr_range_skip_days)

print(f"\n{'-'*100}\n{'-'*100}\n")
print(f"Data pull start date range:\n{start_dates[0]} - {end_dates[-1]}\nTotal iterations: {len(start_dates)}\n\n{'-'*100}\n\n\nHeart Rate data pull start date range:\n{hr_start_dates[0]} - {hr_end_dates[-1]}\nTotal iterations: {len(hr_start_dates)}")
print(f"\n\n{'-'*100}\n{'-'*100}\n\n")


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


# ------------------------------------------------------------------------------
# ------------------           Heart Rate Data               -------------------
# ------------------------------------------------------------------------------

# Creating master list to append hr data to 
hr_dfs = []
# Pulling HR data 
for hr_start, hr_end in tzip(hr_start_dates, hr_end_dates, desc='Heart Rate data pull '):
    try:
        # Frequency = 60 (default) | Other options "6", "60", "600" (seconds)
        hr_df = wapi.get_hr_data(hr_start, hr_end, frequency=user_hr_freq)
        hr_df.to_csv(f"{base_path}/{data_folder}/csvs/hr_data/{hr_start}_{hr_end}.csv", sep=",", index=False)
        hr_dfs.append(hr_df)
        sleep(itteration_pause) # Giving API a break 
    except:
        pass

print(f"\nAll raw csv files for Heart Rate data have been exported to:\n{base_path}/{data_folder}\n")

# concatenate lists of dataframes
master_hr = pd.concat(hr_dfs, ignore_index=True)  
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------



# ------------------------------------------------------------------------------
# -----------------            Clean Data              -------------------------
# ------------------------------------------------------------------------------

if clean_data == "Yes":

    # -------------------------       Clean Data        ----------------------------
    cc_df = scrub.cycles(master_cycles) # c_df from wapi.get_all() | wapi.get_specific_df(start, end, "cycles")
    rc_df = scrub.recovery(master_recovery) # r_df from wapi.get_all() | wapi.get_specific_df(start, end, "recovery")
    sc_df = scrub.sleeps(master_sleeps) # s_df from wapi.get_all() | wapi.get_specific_df(start, end, "sleeps")
    wc_df = scrub.workouts(master_workouts) # w_df from wapi.get_all() | wapi.get_specific_df(start, end, "workouts")
    gwc_df = scrub.group_workouts(wc_df)
    master_df = scrub.create_overall_df(cc_df,  rc_df,  sc_df,  wc_df)
    hrc_df = scrub.hr(master_hr) # hr_df from wapi.get_hr_data()


    # -------------------------       Export Data        ---------------------------
    cc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/cycles/{start_dates[0]}_{end_dates[-1]}.csv") 
    rc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/recovery/{start_dates[0]}_{end_dates[-1]}.csv")
    sc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/sleeps/{start_dates[0]}_{end_dates[-1]}.csv")
    wc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/workouts/{start_dates[0]}_{end_dates[-1]}.csv")
    gwc_df.to_pickle(f"{base_path}/{data_folder}/clean/records/grouped_workouts/{start_dates[0]}_{end_dates[-1]}.csv")
    master_df.to_pickle(f"{base_path}/{data_folder}/clean/master/{start_dates[0]}_{end_dates[-1]}.csv")
    hrc_df.to_pickle(f"{base_path}/{data_folder}/clean/hr_data/{hr_start_dates[0]}_{hr_end_dates[-1]}.csv")

    print(f"\nAll data has been cleaned and exported to:\n{base_path}/{data_folder}/clean\n")

else:
    pass

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# -----------------            CREATE GRAPHS              ----------------------
# ------------------------------------------------------------------------------
# NOTE hr_series() excluded as the amount of data usually freezes machine
# please use export_charts.py or heart_rate.ipynb to setup and export this grpah

if create_user_graphs == "Yes" and graph_format == "png":
    graphs = VisableWhoop(cc_df, rc_df, wc_df, si_df, sc_df, False)
    graphs.save_all_graphs(f"{data_folder}/graphs",".png")
    print(f"\nAll grpahs have been created and exported to:\n{base_path}/{data_folder}/graphs\n")

elif create_user_graphs == "Yes" and graph_format == "html":
    graphs = VisableWhoop(cc_df, rc_df, wc_df, si_df, sc_df, False)
    graphs.save_all_graphs(f"{data_folder}/graphs",".html")
    print(f"\nAll grpahs have been created and exported to:\n{base_path}/{data_folder}/graphs\n")

else:
    pass
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

print(f"\n\nProgram Complete.... All exported files can be found in: {base_path}/{data_folder}")