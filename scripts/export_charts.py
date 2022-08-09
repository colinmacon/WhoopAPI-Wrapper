#!/usr/bin/python3

# Config script to readin scripts from parent folder 
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import packages needed to run
import pandas as pd 
from charts import VisableWhoop



# NOTE
# ----------------------     GENERAL NOTES      --------------------------------

# In order to run all please specifiy the following params with cleaned dfs 
# If you wish to only run one type you must specify param
#     -> ex:  df_you_loaded = pd.read_pickle("mycleanworkouts.csv")
#             graphs = VisableWhoop(workouts_df=df_you_loaded)

# naps param notes:        
#     - naps=False (naps will be excluded from graph)
#     - naps=True (only naps will be graphed)
#     naps=literally anything else (naps + sleeps graphed) 

# cycles graphs -> only cycles_df required
# recovery graphs -> cycles_df + recovery_df required
# workouts graphs -> workouts_df + sports_info_df required
# sleeps graphs -> only sleeps_df required & naps=False default

#  Init params overview:
#  VisableWhoop(cycles_df, recovery_df, workouts_df, sports_info_df, sleeps_df, naps=False):



# NOTE path is assuming you ran create_folders() 


# Setting up path
os.chdir("..") # cd to home folder 
base_path = os.getcwd() # can overwrite with custom path
clean_data_folder = "data" # Set parent folder where all your data is stored
save_graphs_folder = f"{clean_data_folder}/graphs" # Child folder of where to save graphs 
# NOTE use combine_indy_export.py to clean up file name or rename the files in data/clean on your own
# or just copy file one file name from data/clean/records/.. | all filenames should be the same 
base_file_name = "2021-12-27_2022-08-01.csv" # Should all be the same from other scripts


# Read in your cleaned data | Seperated based on dfs required for graphs 
cycles_df = pd.read_pickle(f"{clean_data_folder}/clean/records/cycles/{base_file_name}")
recovery_df = pd.read_pickle(f"{clean_data_folder}/clean/records/recovery/{base_file_name}")

workouts_df = pd.read_pickle(f"{clean_data_folder}/clean/records/workouts/{base_file_name}")
sports_info_df = pd.read_csv(f"{clean_data_folder}/csvs/records/sports_info.csv")

sleeps_df = pd.read_pickle(f"{clean_data_folder}/clean/records/sleeps/{base_file_name}")

hr_df = pd.read_pickle(f"{clean_data_folder}/clean/hr_data/{base_file_name}")

# NOTE HIGHLY Reccomend to filter hr_df between two dates 
hr_df = hr_df.loc[hr_df["time"].between("2022-07-25 01:00:00.000", "2022-07-25 23:59:00.000")]


# NOTE If you would like to filter off dates for other dfs here is an example of how to do that
# replace cycles_df with recovery_df, sleeps_df, or workouts_df (ALL use 'during_start')

# cycles_df = cycles_df.loc[cycles_df['during_start'] > '2022-05-01'] # cjx data  # All data after select date
#cycles_df = cycles_df.loc[cycles_df["during_start"].between("2022-05-01", "2022-05-12")] # Between two dates 



# graphs = VisableWhoop(cycles_df=cycles_df) # Specific run (DON'T FORGET TO COMMENT OUT OTHER METHODS)
graphs = VisableWhoop(cycles_df, recovery_df, workouts_df, sports_info_df, sleeps_df, False, hr_df) # Run All


# ----------------------     ALL GRAPHS AT ONCE      ---------------------------

# graphs.save_all_graphs(f"{data_folder}/graphs",".png") #pngs
# graphs.save_all_graphs(f"{data_folder}/graphs",".html") #html

# ------------------------------------------------------------------------------


# ----------------------    PICK | CHOOSE | EDIT      --------------------------
# --------------------------        HTMLs      ---------------------------------

# ----------------------        CYCLES GRAPHS      -----------------------------
graphs.strain_vs_scaled(f"{save_graphs_folder}/cycles/Strain_vs_ScaledStrain.png") #.png only
graphs.cals_vs_strain(f"{save_graphs_folder}/cycles/CalsBurned_vs_ScaledStrain.png") #.png only

# Save as .html - allows graph to be interactive (open with browser)
graphs.max_avg_hr(f"{save_graphs_folder}/cycles/Max_AVG_HRperDay.html")
graphs.scaled_strain(f"{save_graphs_folder}/cycles/ScaledStrain_perDay.html")
graphs.cals_burned(f"{save_graphs_folder}/cycles/CalsBurned_perDay.html")

# ----------------------        RECOVERY GRAPHS      ---------------------------
# Save as .html - allows graph to be interactive (open with browser)
graphs.sleep_wake(f"{save_graphs_folder}/recovery/SleepWakeTimes.html")
graphs.recovery_score(f"{save_graphs_folder}/recovery/RecoveryScore.html")
graphs.covid_prob(f"{save_graphs_folder}/recovery/CovidProb.html")
graphs.hrv(f"{save_graphs_folder}/recovery/HRV.html")
graphs.resting_base_HR(f"{save_graphs_folder}/recovery/RestingBase_HR.html")
graphs.skintemp_spo(f"{save_graphs_folder}/recovery/SkinTemp_SPO.html")
graphs.hr_breakdown(f"{save_graphs_folder}/recovery/HR_Breakdown.html")
graphs.scaledstrain_recovery(f"{save_graphs_folder}/recovery/ScaledStrain_RecoveryScore.html")

# ---------------------        WORKOUT GRAPHS        ---------------------------
# Save as .html - allows graph to be interactive (open with browser)
graphs.zone_duration(f"{save_graphs_folder}/workouts/ZoneDurations.html")
graphs.activity_count(f"{save_graphs_folder}/workouts/ActivityCountBar.html")
graphs.workout_duration(f"{save_graphs_folder}/workouts/WorkoutDurationHist.html")
graphs.workout_duration_day(f"{save_graphs_folder}/workouts/Workout_HR_Day.html")
graphs.workout_hr(f"{save_graphs_folder}/workouts/Workout_HR_Activity.html")

# ----------------------        SLEEPS GRAPHS        ---------------------------
# Save as .html - allows graph to be interactive (open with browser)
graphs.sleep_stage_durations(f"{save_graphs_folder}/sleeps/SleepStageDurations.html")
graphs.sleep_stage_daily(f"{save_graphs_folder}/sleeps/SleepStageDaily.html")
graphs.resp_rate(f"{save_graphs_folder}/sleeps/Respiratory_Rate.html")
graphs.sleep_score(f"{save_graphs_folder}/sleeps/SleepScore.html") # NOTE set naps=False to mimic app view
graphs.sleep_need_debt(f"{save_graphs_folder}/sleeps/SleepNeed_SleepDebt.html")
graphs.timeinbed_qualitydur(f"{save_graphs_folder}/sleeps/TimeInBed_QualityDuration.html")
graphs.sleep_stages_hist(f"{save_graphs_folder}/sleeps/SleepStages_Hist.html")
graphs.sleep_need_actual(f"{save_graphs_folder}/sleeps/SleepNeed_vs_Actual.html") # NOTE set naps=False to mimic app view

# ----------------------       HEART RATE GRAPHS        ------------------------
# Save as .html - allows graph to be interactive (open with browser)
graphs.hr_series(f"{save_graphs_folder}/hr/HeartRateSeries.html")


# --------------------------        PNGs      ----------------------------------
'''
# ----------------------        CYCLES GRAPHS      -----------------------------
graphs.strain_vs_scaled(f"{save_graphs_folder}/cycles/Strain_vs_ScaledStrain.png") #.png only
graphs.cals_vs_strain(f"{save_graphs_folder}/cycles/CalsBurned_vs_ScaledStrain.png") #.png only

graphs.max_avg_hr(f"{save_graphs_folder}/cycles/Max_AVG_HRperDay.png")
graphs.scaled_strain(f"{save_graphs_folder}/cycles/ScaledStrain_perDay.png")
graphs.cals_burned(f"{save_graphs_folder}/cycles/CalsBurned_perDay.png")

# ----------------------        RECOVERY GRAPHS      ---------------------------
graphs.sleep_wake(f"{save_graphs_folder}/recovery/SleepWakeTimes.png")
graphs.recovery_score(f"{save_graphs_folder}/recovery/RecoveryScore.png")
graphs.covid_prob(f"{save_graphs_folder}/recovery/CovidProb.png")
graphs.hrv(f"{save_graphs_folder}/recovery/HRV.png")
graphs.resting_base_HR(f"{save_graphs_folder}/recovery/RestingBase_HR.png")
graphs.skintemp_spo(f"{save_graphs_folder}/recovery/SkinTemp_SPO.png")
graphs.hr_breakdown(f"{save_graphs_folder}/recovery/HR_Breakdown.png")
graphs.scaledstrain_recovery(f"{save_graphs_folder}/recovery/ScaledStrain_RecoveryScore.png")

# ---------------------        WORKOUT GRAPHS        ---------------------------
graphs.zone_duration(f"{save_graphs_folder}/workouts/ZoneDurations.png")
graphs.activity_count(f"{save_graphs_folder}/workouts/ActivityCountBar.png")
graphs.workout_duration(f"{save_graphs_folder}/workouts/WorkoutDurationHist.png")
graphs.workout_duration_day(f"{save_graphs_folder}/workouts/Workout_HR_Day.png")
graphs.workout_hr(f"{save_graphs_folder}/workouts/Workout_HR_Activity.png")

# ----------------------        SLEEPS GRAPHS        ---------------------------
graphs.sleep_stage_durations(f"{save_graphs_folder}/sleeps/SleepStageDurations.png")
graphs.sleep_stage_daily(f"{save_graphs_folder}/sleeps/SleepStageDaily.png")
graphs.resp_rate(f"{save_graphs_folder}/sleeps/Respiratory_Rate.png")
graphs.sleep_score(f"{save_graphs_folder}/sleeps/SleepScore.png") # NOTE set naps=False to mimic app view
graphs.sleep_need_debt(f"{save_graphs_folder}/sleeps/SleepNeed_SleepDebt.png")
graphs.timeinbed_qualitydur(f"{save_graphs_folder}/sleeps/TimeInBed_QualityDuration.png")
graphs.sleep_stages_hist(f"{save_graphs_folder}/sleeps/SleepStages_Hist.png")
graphs.sleep_need_actual(f"{save_graphs_folder}/sleeps/SleepNeed_vs_Actual.png") # NOTE set naps=False to mimic app view

# ----------------------       HEART RATE GRAPHS        ------------------------
graphs.hr_series(f"{save_graphs_folder}/hr/HeartRateSeries.png")
'''

print("\n\nProgram Complete: All graphs have been exported")
