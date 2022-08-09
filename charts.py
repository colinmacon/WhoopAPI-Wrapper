#!/usr/bin/python3

import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd 

import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go
import plotly.express as px
import seaborn as sns

# Function to format timestamp into HH:MM for grpah view
def f(x):
    ts = x.total_seconds()
    hours, remainder = divmod(ts, 3600)
    minutes, seconds = divmod(remainder, 60)
    return ('{:02d}:{:02d}').format(int(hours), int(minutes)) 


class VisableWhoop:
    def __init__(self, cycles_df=None, recovery_df=None, workouts_df=None, sports_info_df=None, sleeps_df=None, naps=False, hr_df=None):

# ----------------------        Cycles Setup     ------------------------------

        if cycles_df is not None:
            
            self.cycles_df = cycles_df
        
        else:
            pass
        
# ----------------------        Recovery Setup     -----------------------------
        if recovery_df is not None:
            
            self.recovery_df = recovery_df

            # Merging cycles and recovery to make two recovery charts
            self.c_temp = self.cycles_df.add_prefix("c_")
            self.r_temp = self.recovery_df.add_prefix("r_")
            self.cr_df = pd.merge(self.c_temp, self.r_temp, how="left", left_on="c_cycle_id", right_on="r_cycle_id")
        
            self.cr_df.replace({'NaT': ''}, inplace=True)
            self.cr_df.replace({np.nan: ''}, inplace=True)

            # Adding in helper columns for day_start
            self.recovery_df['ds_date'] = pd.to_datetime(self.recovery_df['during_start'], unit='ms').dt.date 
            self.recovery_df['ds_frmt_time'] = pd.to_datetime(self.recovery_df["during_start"], unit='ms').dt.strftime('%I:%M:%S %p')
            self.recovery_df['ds_ampm'] = pd.to_datetime(self.recovery_df["during_start"], unit='ms').dt.strftime('%I %p')

            self.recovery_df['de_date'] = pd.to_datetime(self.recovery_df['during_end'], unit='ms').dt.date 
            self.recovery_df['de_frmt_time'] = pd.to_datetime(self.recovery_df["during_end"], unit='ms').dt.strftime('%I:%M:%S %p')
            self.recovery_df['de_ampm'] = pd.to_datetime(self.recovery_df["during_end"], unit='ms').dt.strftime('%I %p')
        
        else:
            pass
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# ----------------------        Workouts Setup     -----------------------------
        if workouts_df is not None:
            
            self.workouts_df = pd.merge(workouts_df, sports_info_df[['id','name']], how='left', left_on='sport_id', right_on='id')
            self.workouts_df['total_workout_time_min'] = self.workouts_df.tot_sec_diff / 60
            self.workouts_df["cycle_start_dayname"] = self.workouts_df["cycle_start"].dt.day_name()
            self.workouts_df["cycle_start_monthname"] = self.workouts_df["cycle_start"].dt.month_name()
        
        else:
            pass
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# ----------------------        Sleeps Setup     -------------------------------
        if sleeps_df is not None:
            self.sleeps_df = sleeps_df
            
            self.sleeps_df['light_sleep_dur_frmt'] = pd.to_timedelta(self.sleeps_df['light_sleep_duration'], unit='ms').apply(f)
            self.sleeps_df['slow_wave_sleep_dur_frmt'] = pd.to_timedelta(self.sleeps_df.slow_wave_sleep_duration, unit='ms').apply(f)
            self.sleeps_df['rem_sleep_dur_frmt'] = pd.to_timedelta(self.sleeps_df.rem_sleep_duration, unit='ms').apply(f)
            self.sleeps_df['wake_dur_frmt'] = pd.to_timedelta(self.sleeps_df.wake_duration, unit='ms').apply(f)
            self.sleeps_df['arousal_time_frmt'] = pd.to_timedelta(self.sleeps_df.arousal_time, unit='ms').apply(f)


            self.sleeps_df = self.sleeps_df.assign(lsd_hrs = self.sleeps_df["light_sleep_duration"]/3600000)
            self.sleeps_df = self.sleeps_df.assign(sws_hrs = self.sleeps_df["slow_wave_sleep_duration"]/3600000)
            self.sleeps_df = self.sleeps_df.assign(rem_hrs = self.sleeps_df["rem_sleep_duration"]/3600000)
            self.sleeps_df = self.sleeps_df.assign(wake_hrs = self.sleeps_df["wake_duration"]/3600000)
            self.sleeps_df = self.sleeps_df.assign(ar_hrs = self.sleeps_df["arousal_time"]/3600000)
            
            
            # Changing col names for presentation 
            self.sleeps_df = self.sleeps_df.rename(columns={'lsd_hrs': 'Light Sleep HRs', 'sws_hrs': 'Slow Wave HRs',
                                    'rem_hrs': 'REM Sleep HRs', 'wake_hrs': 'Wake HRs',
                                    'ar_hrs': 'Arousal Time HRs'})
            self.sleeps_df["cycle_start_dayname"] = self.sleeps_df["cycle_start"].dt.day_name()
            
            self.sleeps_df['quality_duration_frmt'] = pd.to_timedelta(self.sleeps_df.quality_duration, unit='ms').apply(f)
            self.sleeps_df = self.sleeps_df.assign(qaulitydur_hrs = self.sleeps_df["quality_duration"]/3600000)

            # create a column with timedelta as total hours, as a float type
            self.sleeps_df['total_sleep_sec'] = (self.sleeps_df.during_end - self.sleeps_df.during_start) / pd.Timedelta(seconds=1)
            self.sleeps_df['total_sleep_sec'] = self.sleeps_df['total_sleep_sec'].astype('float64') 
            self.sleeps_df['total_sleep_hrs'] = self.sleeps_df.total_sleep_sec / 3600

            self.sleeps_df['total_sleep_need_hrs'] = self.sleeps_df.sleep_need / 3600000
            self.sleeps_df['total_sleep_need_hrs_frmt'] = pd.to_timedelta(self.sleeps_df.sleep_need, unit='ms').apply(f)

            if naps == True:
                self.sleeps_df = self.sleeps_df[self.sleeps_df["is_nap"]==True]
            elif naps == False:
                self.sleeps_df = self.sleeps_df[self.sleeps_df["is_nap"]==False]
            else:
                pass
        else:
            pass
# ------------------------------------------------------------------------------

# ----------------------     Heart Rate Setup     ------------------------------

        if hr_df is not None:
            
            self.hr_df = hr_df
        
        else:
            pass


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------



# ----------------------        CYCLES GRAPHS      -----------------------------

    def strain_vs_scaled(self, save_path="Strain_vs_ScaledStrain.png"):
        sns.scatterplot(data = self.cycles_df, x = "day_strain", y = "scaled_strain", hue='day_avg_heart_rate', size='day_max_heart_rate', legend = False)

        plt.xlabel("Day Strain", size=11)
        plt.ylabel("Day Scaled Strain", size=11)
        plt.title("Strain vs Scaled Strain", size=16)
        plt.savefig(save_path)
        plt.clf()



    def cals_vs_strain(self, save_path="CalsBurned_vs_ScaledStrain.png"):

        sns.scatterplot(data=self.cycles_df, x="calories", y="scaled_strain", hue="StrainCategory", hue_order = ['extreme', 'high', 'medium', 'light', 'minimal'])

        plt.xlabel("Calories", size=11)
        plt.ylabel("Scaled Strain", size=11)
        plt.title("Calories Burned vs Scaled Strain", size=16)
        plt.savefig(save_path)
        plt.clf()



    def max_avg_hr(self, save_path="Max_AVG_HRperDay.png"):

        fig = go.Figure()

        fig.add_trace(go.Scatter(
        x=self.cycles_df.days_start,
        y=self.cycles_df["day_max_heart_rate"],
        mode="markers+lines",
        name = "Max HR",
        text = "Max HR:" + self.cycles_df['days_start'].astype('string') + " - " + self.cycles_df['day_max_heart_rate'].astype('string'),
        hoverinfo = 'text'))

        fig.add_trace(go.Scatter(
        x=self.cycles_df.days_start,
        y=self.cycles_df["day_avg_heart_rate"],
        mode="markers+lines",
        name = "Avg HR",
        text = "Avg HR:" + self.cycles_df['days_start'].astype('string') + " - " + self.cycles_df['day_avg_heart_rate'].astype('string'),
        hoverinfo = 'text'))

        fig.update_xaxes(title='Date')
        fig.update_yaxes(title='BPMs')
        fig.update_layout(title_text='Max & Average HR per Day', title_x=0.5)
        
        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



    def scaled_strain(self, save_path="ScaledStrain_perDay.png"):
        
        self.cycles_df['scaled_strain'] = self.cycles_df['scaled_strain'].apply(lambda x: round(x, 2))
        
        fig = px.bar(self.cycles_df, x='days_start', y='scaled_strain',
                labels={'days_start': 'Date', 'scaled_strain':'Scaled Strain'})


        fig.update_traces(text = self.cycles_df.scaled_strain, textposition = "outside")
        fig.update_layout(title_text='Scaled Strain per Day', title_x=0.5)

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



    def cals_burned(self, save_path="CalsBurned_perDay.png"):
        
        fig = px.bar(self.cycles_df, x='days_start', y='calories',
                    labels={'days_start': 'Date', 'calories':'Calories Burned'})

        fig.update_traces(text = self.cycles_df.calories, textposition = "outside")
        fig.update_layout(title_text='Calories Burned per Day', title_x=0.5)

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# ----------------------       RECOVERY GRAPHS      -----------------------------

    def sleep_wake(self, save_path="SleepWakeTimes.png"):

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.recovery_df.ds_date,
            y=self.recovery_df["ds_ampm"],
            mode="markers+lines",
            name = "Sleep Start",
            text = self.recovery_df['ds_date'].astype('string') + " - " + self.recovery_df['ds_frmt_time'].astype('string'),
            hoverinfo = 'text'))

        fig.add_trace(go.Scatter(
            x=self.recovery_df.ds_date,
            y=self.recovery_df["de_ampm"],
            mode="markers+lines",
            name = "Wake Time",
            text = self.recovery_df['de_date'].astype('string') + " - " + self.recovery_df['de_frmt_time'].astype('string'),
            hoverinfo = 'text'))

        fig.update_yaxes(categoryorder='array', categoryarray= ['05 PM', '06 PM', '07PM','08 PM','09 PM', '10 PM', '11 PM', '12 AM', '01 AM', '02 AM', '03 AM', '04 AM',
                                                                '05 AM', '06 AM', '07 AM', '08 AM', '09 AM', '10 AM', '11 AM', '12 PM',
                                                                '01 PM', '02 PM', '03 PM', '04 PM'])

        fig.update_layout(title_text='Sleep and Wake Times', title_x=0.5)
        fig.update_xaxes(title='Date')
        fig.update_yaxes(title='Time')

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



    def recovery_score(self, save_path="RecoveryScore.png"):
        

        # Mapping categories to strain ranges
        bins = [0, 33, 66, np.inf]
        names = ['red', 'yellow', 'lightgreen']

        self.recovery_df['RecoveryCategory'] = pd.cut(self.recovery_df['score'], bins, labels=names)


        fig = px.bar(self.recovery_df, x='de_date', y='score',
                    labels={'de_date': 'Date', 'score':'Recovery Score'})

        fig.update_traces(text = self.recovery_df.score, textposition = "outside", marker_color=self.recovery_df["RecoveryCategory"])
        fig.update_layout(title_text='Recovery Score by Day', title_x=0.5)
        
        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")


    def covid_prob(self, save_path="CovidProb.png"):
        
        self.recovery_df['prob_covid'] = self.recovery_df['prob_covid'].fillna(0)

        fig = px.line(self.recovery_df, x='de_date', y="prob_covid",
                    labels={'de_date': 'Date', 'prob_covid':'Covid Probability'})

        fig.layout.yaxis.tickformat = ',.0%'
        fig.update_layout(title_text='Covid Probability', title_x=0.5)

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



    def hrv(self, save_path="HRV.png"):
        
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.recovery_df.ds_date,
            y=self.recovery_df["hrv_rmssd"],
            mode="markers+lines"))

        fig.update_layout(title_text='HRV (RMSSD)', title_x=0.5)
        fig.update_xaxes(title='Date')
        fig.update_yaxes(title='RMSSD')
        
        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")


        
    def resting_base_HR(self, save_path="RestingBase_HR.png"):
        
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.recovery_df.ds_date,
            y=self.recovery_df["resting_heart_rate"],
            mode="markers+lines",
            name = "Resting HR",
            text = self.recovery_df['resting_heart_rate'].astype('string'),
            hoverinfo = 'text'))

        fig.add_trace(go.Scatter(
            x=self.recovery_df.ds_date,
            y=self.recovery_df["hr_baseline"],
            mode="markers+lines",
            name = "Baseline HR",
            text = self.recovery_df['hr_baseline'].astype('string'),
            hoverinfo = 'text'))

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



    # NOTE Whoop 4.0 only 
    def skintemp_spo(self, save_path="SkinTemp_SPO.png"):

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.recovery_df.ds_date,
            y=self.recovery_df["skin_temp_fahrenheit"],
            mode="markers+lines",
            name = "Skin Temp (Fahrenheit)",
            text = self.recovery_df['skin_temp_fahrenheit'].astype('string'),
            hoverinfo = 'text'))

        fig.add_trace(go.Scatter(
            x=self.recovery_df.ds_date,
            y=self.recovery_df["spo2"],
            mode="markers+lines",
            name = "SPO2",
            text = self.recovery_df['spo2'].astype('string'),
            hoverinfo = 'text'))

        fig.update_layout(title_text='Skin Temp (F) & SPO2', title_x=0.5)

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



    def hr_breakdown(self, save_path="HR_Breakdown.png"):

        self.cr_df["r_resting_heart_rate"] = pd.to_numeric(self.cr_df["r_resting_heart_rate"])
        
        fig = px.bar(self.cr_df, x='c_days_start', y=['c_day_avg_heart_rate', 'c_day_max_heart_rate', 'r_resting_heart_rate'], orientation = "v",
        barmode = 'group',)

        newnames = {'c_day_avg_heart_rate':'Day Avg HR', 'c_day_max_heart_rate': 'Day MAX HR', 'r_resting_heart_rate':'Resting HR'}
        fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
        fig.update_layout(title_text='Heart Rate Stats by Day', title_x=0.5, xaxis_title="", yaxis_title="Heart Rate", legend_title="HR Type")
        

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



    def scaledstrain_recovery(self, save_path="ScaledStrain_RecoveryScore.png"):
        
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.cr_df.c_days_start,
            y=self.cr_df["c_scaled_strain"],
            mode="markers+lines",
            name = "Scaled Straint",
            text = self.cr_df['c_scaled_strain'].round(2),
            hoverinfo = 'text',
            yaxis="y1"))


        fig.add_trace(go.Scatter(
            x=self.cr_df.c_days_start,
            y=self.cr_df["r_score"],
            mode="markers+lines",
            name = "Recovery Score",
            text = self.cr_df['r_score'],
            hoverinfo = 'text',
            yaxis="y2"))

        # Create axis objects
        fig.update_layout(
            xaxis=dict(
            domain=[.2, 1]
            ),
            yaxis=dict(                         
                title="Scaled Strain", 
                titlefont=dict(
                    color="#d99b16" 
                ),
                tickfont=dict(
                    color="#d99b16"
                )
            ),
            yaxis2=dict(
                title="Recovery Score", 
                titlefont=dict(
                    color="#f70f13"  
                ),
                tickfont=dict(
                    color="#f70f13"
                ),
                anchor="free", 
                overlaying="y",
                side="left",
                position=0.15
            ),
            title_text='Scaled Strain & Recovery Score', title_x=0.5,
            )

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------


# ----------------------       WORKOUTS GRAPHS       ----------------------------


    def zone_duration(self, save_path="ZoneDurations.png"):

        zone_gb_df = self.workouts_df.groupby(["cycle_id", "cycle_start"])["Zone1", "Zone2", "Zone3", "Zone4", "Zone5", "Zone6"].sum().reset_index()

        only_zone_df = zone_gb_df[["Zone1", "Zone2", "Zone3", "Zone4", "Zone5", "Zone6"]]

        zone_gb_df["row_sum"] = only_zone_df.sum(axis=1)

        zone_gb_df["Zone1_pct"] = (zone_gb_df['Zone1'] / zone_gb_df["row_sum"])
        zone_gb_df["Zone2_pct"] = (zone_gb_df['Zone2'] / zone_gb_df["row_sum"]) 
        zone_gb_df["Zone3_pct"] = (zone_gb_df['Zone3'] / zone_gb_df["row_sum"]) 
        zone_gb_df["Zone4_pct"] = (zone_gb_df['Zone4'] / zone_gb_df["row_sum"])
        zone_gb_df["Zone5_pct"] = (zone_gb_df['Zone5'] / zone_gb_df["row_sum"])
        zone_gb_df["Zone6_pct"] = (zone_gb_df['Zone6'] / zone_gb_df["row_sum"])

        plot = go.Figure()

        plot.add_trace(go.Scatter(
            name = 'Zone 6 - (90-100%)',
            x = zone_gb_df["cycle_start"],
            y = zone_gb_df["Zone6_pct"],
            stackgroup='one'
            ))
        plot.add_trace(go.Scatter(
            name = 'Zone 5 - (80-89%)',
            x = zone_gb_df["cycle_start"],
            y = zone_gb_df["Zone5_pct"],
            stackgroup='one'
            ))
        plot.add_trace(go.Scatter(
            name = 'Zone 4 - (70-79%)',
            x = zone_gb_df["cycle_start"],
            y = zone_gb_df["Zone4_pct"],
            stackgroup='one'
            ))
        plot.add_trace(go.Scatter(
            name = 'Zone 3 - (60-69%)',
            x = zone_gb_df["cycle_start"],
            y = zone_gb_df["Zone3_pct"],
            stackgroup='one'
            ))
        plot.add_trace(go.Scatter(
            name = 'Zone 2 - (50-59%)',
            x = zone_gb_df["cycle_start"],
            y = zone_gb_df["Zone2_pct"],
            stackgroup='one'
            ))
        plot.add_trace(go.Scatter(
            name = 'Zone 1 - (0-49%)',
            x = zone_gb_df["cycle_start"],
            y = zone_gb_df["Zone1_pct"],
            stackgroup='one'
            ))


        plot.layout.yaxis.tickformat = ',.0%'
        plot.update_xaxes(title='Date')
        plot.update_yaxes(title='Zone Duration %')
        plot.update_layout(title_text="Zone Duration % by Date", title_x=0.5)
        
        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            plot.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(plot, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")




    def activity_count(self, save_path="ActivityCountBar.png"):
        
        counts = self.workouts_df['name'].value_counts().rename_axis('name').reset_index(name='count')

        fig = px.bar(counts,
                    x='name',
                    y='count',
                    title='Test',
                    color='name',
                    barmode='stack')

        fig.update_layout(title_text='Count of Activities by Type', title_x=0.5,
                        xaxis_title="Activity", yaxis_title="Count", legend_title="Activity Type")

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



    def workout_duration(self, save_path="WorkoutDurationHist.png"):

        fig = px.histogram(self.workouts_df, x="total_workout_time_min", color="name")

        fig.update_traces(overwrite=True, marker={"opacity": 0.4}) 
        fig.update_layout(barmode='overlay', title_text='Workout Duration (min)',
                        title_x=0.5, xaxis_title="Minutes", yaxis_title="Count",
                        legend_title="Activity Type")
        

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



    def workout_duration_day(self, save_path="Workout_HR_Day.png"):

        fig = px.box(self.workouts_df, x="cycle_start_dayname", y="total_workout_time_min", color="name",
                    labels={
                        "total_workout_time_min": "Minutes",
                        "cycle_start_dayname": ""},
                    category_orders={"cycle_start_dayname": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]})

        fig.update_traces(quartilemethod="exclusive")
        fig.update_layout(title_text='Daily Workout Duration by Day', title_x=0.5,
                        legend_title="Workout Type")
        
        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")




    def workout_hr(self, save_path="Workout_HR_Activity.png"):
        
        fig = px.box(self.workouts_df, x="name", y=["average_heart_rate"], color="name")


        fig.update_traces(quartilemethod="exclusive")
        fig.update_layout(title_text='Average Heart Rate per Activity', title_x=0.5,
                        xaxis_title="Activity Name", yaxis_title="Average Heart Rate", legend_title="Activity Type")
        
        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# ----------------------       SLEEPS GRAPHS       -----------------------------


    def sleep_stage_durations(self, save_path="SleepStageDurations.png"):
        
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.sleeps_df.cycle_start,
            y=self.sleeps_df["Light Sleep HRs"],
            stackgroup='one',
            text = self.sleeps_df['cycle_start'].astype('string') + " - " +self.sleeps_df['light_sleep_dur_frmt'].astype('string'),
            hoverinfo = 'text',
            name = "Light Sleep Duration"))


        fig.add_trace(go.Scatter(
            x=self.sleeps_df.cycle_start,
            y=self.sleeps_df["Slow Wave HRs"],
            stackgroup='one',
            text = self.sleeps_df['cycle_start'].astype('string') + " - " +self.sleeps_df['slow_wave_sleep_dur_frmt'].astype('string'),
            hoverinfo = 'text',
            name = "Slow Wave Sleep Duration"))

        fig.add_trace(go.Scatter(
            x=self.sleeps_df.cycle_start,
            y=self.sleeps_df["REM Sleep HRs"],
            stackgroup='one',
            text = self.sleeps_df['cycle_start'].astype('string') + " - " +self.sleeps_df['rem_sleep_dur_frmt'].astype('string'),
            hoverinfo = 'text',
            name = "REM Sleep Duration"))

        fig.add_trace(go.Scatter(
            x=self.sleeps_df.cycle_start,
            y=self.sleeps_df["Wake HRs"],
            stackgroup='one',
            text = self.sleeps_df['cycle_start'].astype('string') + " - " +self.sleeps_df['wake_dur_frmt'].astype('string'),
            hoverinfo = 'text',
            name = "Wake Duration"))

        fig.add_trace(go.Scatter(
            x=self.sleeps_df.cycle_start,
            y=self.sleeps_df["Arousal Time HRs"],
            stackgroup='one',
            text = self.sleeps_df['cycle_start'].astype('string') + " - " +self.sleeps_df['arousal_time_frmt'].astype('string'),
            hoverinfo = 'text',
            name = "Arousal Time"))


        fig.update_xaxes(title='Date')
        fig.update_yaxes(title='Hours')
        fig.update_layout(title_text="Sleep Stage Durations", title_x=0.5)
        
        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



            

    def sleep_stage_daily(self, save_path="SleepStageDaily.png"):
        
        sleep_stages_df2 = self.sleeps_df.melt(id_vars="cycle_start_dayname", value_vars=["Light Sleep HRs", "Slow Wave HRs", "REM Sleep HRs", "Wake HRs", "Arousal Time HRs"])

        fig = px.box(sleep_stages_df2, x="cycle_start_dayname", y="value", color="variable",
                    labels={
                        "value": "Hours",
                        "cycle_start_dayname": ""},
                    color_discrete_map = {
                        'Light Sleep HRs' : 'blue',
                        'Slow Wave HRs' : 'orange',
                        'REM Sleep HRs' : 'green',
                        'Wake HRs' : 'red'})


        fig.update_traces(quartilemethod="exclusive") # or "inclusive", or "linear" by default
        fig.update_xaxes(categoryorder='array', categoryarray= ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        fig.update_layout(title_text='Sleep Stage Duration by Day', title_x=0.5, legend_title="Sleep Stage Type")

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")




    def resp_rate(self, save_path="Respiratory_Rate.png"):

        fig = go.Figure()

        fig.add_trace(go.Scatter(
        x=self.sleeps_df.cycle_start,
        y=self.sleeps_df["respiratory_rate"],
        mode="markers+lines",
        text = self.sleeps_df['respiratory_rate'].round(2),
        hoverinfo = 'text'))

        fig.update_layout(title_text='Respiratory Rate', title_x=0.5)
        fig.update_xaxes(title='Date')
        fig.update_yaxes(title='Breaths per Min')
        
        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")


            
    # NOTE naps set to False
    def sleep_score(self, save_path="SleepScore.png"):

        fig = px.bar(self.sleeps_df, x='cycle_start', y='score',
                    labels={'cycle_start': 'Date', 'score':'Sleep Score'})

        fig.update_traces(text = self.sleeps_df.score, textposition = "outside")
        fig.update_layout(title_text='Sleep Score by Day', title_x=0.5)
        
        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



    def sleep_need_debt(self, save_path="SleepNeed_SleepDebt.png"):

        self.sleeps_df = self.sleeps_df.assign(debtpre_hrs = self.sleeps_df["debt_pre"]/3600000)
        self.sleeps_df = self.sleeps_df.assign(debtpost_hrs = self.sleeps_df["debt_post"]/3600000)

        fig = px.bar(self.sleeps_df, x='cycle_start', y=['debtpre_hrs', 'debtpost_hrs'], orientation = "v",  barmode = 'group',)

        newnames = {'debtpre_hrs':'Pre-Sleep Debt', 'debtpost_hrs': 'Post-Sleep Debt'}
        fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))
        fig.update_layout(title_text='Pre & Post Sleep Debt', title_x=0.5, xaxis_title="Date", yaxis_title="Hours", legend_title="Debt Stage")
        
        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



    def timeinbed_qualitydur(self, save_path="TimeInBed_QualityDuration.png"):

        self.sleeps_df['time_in_bed_frmt'] = pd.to_timedelta(self.sleeps_df.time_in_bed, unit='ms').apply(f)
        self.sleeps_df['quality_duration_frmt'] = pd.to_timedelta(self.sleeps_df.quality_duration, unit='ms').apply(f)


        self.sleeps_df = self.sleeps_df.assign(timeinbed_hrs = self.sleeps_df["time_in_bed"]/3600000)
        self.sleeps_df = self.sleeps_df.assign(qaulitydur_hrs = self.sleeps_df["quality_duration"]/3600000)


        fig = px.bar(self.sleeps_df, x='cycle_start', y=['timeinbed_hrs', 'qaulitydur_hrs'])

        newnames = {'timeinbed_hrs':'Time in Bed', 'qaulitydur_hrs': 'Quality Duration'}
        fig.for_each_trace(lambda t: t.update(name = newnames[t.name]))


        fig.update_layout(barmode='overlay')
        fig.update_layout(title_text='Total Time in Bed vs Quality Duration', title_x=0.5, xaxis_title="Date", yaxis_title="Hours")
        
        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



    def sleep_stages_hist(self, save_path="SleepStages_Hist.png"):
        
        sleep_stages_df = self.sleeps_df.melt(id_vars="cycle_start", value_vars=["Light Sleep HRs", "Slow Wave HRs", "REM Sleep HRs", "Wake HRs", "Arousal Time HRs"])


        fig = px.histogram(sleep_stages_df, x="value", color="variable")

        fig.update_traces(overwrite=True, marker={"opacity": 0.4}) 
        fig.update_layout(barmode='overlay', title_text='Sleep Stages', title_x=0.5, legend_title="Sleep Stage Type",
                        xaxis_title="Hours", yaxis_title="Count")

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")



    # NOTE naps set to False
    def sleep_need_actual(self, save_path="SleepNeed_vs_Actual.png"):

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=self.sleeps_df.cycle_start,
            y=self.sleeps_df["qaulitydur_hrs"],
            mode="markers+lines",
            name = "Total Sleep",
            text = self.sleeps_df['cycle_start'].astype('string') + " - " + self.sleeps_df['quality_duration_frmt'].astype('string'),
            hoverinfo = 'text'))


        fig.add_trace(go.Scatter(
            x=self.sleeps_df.cycle_start,
            y=self.sleeps_df["total_sleep_need_hrs"],
            mode="markers+lines",
            name = "Sleep Need",
            line=dict(color="#90EE90"),
            text = self.sleeps_df['cycle_start'].astype('string') + " - " + self.sleeps_df['total_sleep_need_hrs_frmt'].astype('string'),
            hoverinfo = 'text'))

        fig.update_layout(title_text='Sleep Need vs Actual Sleep', title_x=0.5)
        fig.update_xaxes(title='Date')
        fig.update_yaxes(title='BPMs')

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")

# ----------------------     Heart Rate Graph     ------------------------------

    def hr_series(self, save_path="HeartRateSeries.png"):
        
        fig = go.Figure()

        fig.add_trace(go.Scatter(
        x=self.hr_df.time,
        y=self.hr_df["bpm"],
        mode="markers+lines",
        name = "Heart Rate",
        text = "HR:" + self.hr_df['time'].astype('string') + " - " + self.hr_df['bpm'].astype('string'),
        hoverinfo = 'text'))

        fig.update_xaxes(title='Date')
        fig.update_yaxes(title='Heart Rate')
        fig.update_layout(title_text='Heart Rate Series Data', title_x=0.5)

        # Saving file based on png or html
        check_png = save_path[-4:]
        check_html = save_path[-5:]
        
        if check_png == '.png':
            fig.write_image(save_path)
        elif check_html == '.html':
            plotly.offline.plot(fig, filename = save_path, auto_open=False)
        else:
            print("Please specify type as 'png' or 'html'")


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# Creating a function to save all just to clean up autorun script 

    def save_all_graphs(self, base_path, file_type=".png"):

# ----------------------        CYCLES GRAPHS      -----------------------------
        
        # Default .png, but specifying path to /data foldergraphs.strain_vs_scaled(f"{data_folder}/cycles/Strain_vs_ScaledStrain.png") # .png only
        self.strain_vs_scaled(f"{base_path}/cycles/Strain_vs_ScaledStrain.png") #.png only
        self.cals_vs_strain(f"{base_path}/cycles/CalsBurned_vs_ScaledStrain.png") #.png only
        self.max_avg_hr(f"{base_path}/cycles/Max_AVG_HRperDay{file_type}")
        self.scaled_strain(f"{base_path}/cycles/ScaledStrain_perDay{file_type}")
        self.cals_burned(f"{base_path}/cycles/CalsBurned_perDay{file_type}")

# ----------------------        RECOVERY GRAPHS      ---------------------------

        # Default .png, but specifying path to /data folder
        self.sleep_wake(f"{base_path}/recovery/SleepWakeTimes{file_type}")
        self.recovery_score(f"{base_path}/recovery/RecoveryScore{file_type}")
        self.covid_prob(f"{base_path}/recovery/CovidProb{file_type}")
        self.hrv(f"{base_path}/recovery/HRV{file_type}")
        self.resting_base_HR(f"{base_path}/recovery/RestingBase_HR{file_type}")
        self.skintemp_spo(f"{base_path}/recovery/SkinTemp_SPO{file_type}")
        self.hr_breakdown(f"{base_path}/recovery/HR_Breakdown{file_type}")
        self.scaledstrain_recovery(f"{base_path}/recovery/ScaledStrain_RecoveryScore{file_type}")

# ---------------------        WORKOUT GRAPHS        ---------------------------

        # Default .png, but specifying path to /data folder
        self.zone_duration(f"{base_path}/workouts/ZoneDurations{file_type}")
        self.activity_count(f"{base_path}/workouts/ActivityCountBar{file_type}")
        self.workout_duration(f"{base_path}/workouts/WorkoutDurationHist{file_type}")
        self.workout_duration_day(f"{base_path}/workouts/Workout_HR_Day{file_type}")
        self.workout_hr(f"{base_path}/workouts/Workout_HR_Activity{file_type}")

# ----------------------        SLEEPS GRAPHS        ---------------------------

        # Default .png, but specifying path to /data folder
        self.sleep_stage_durations(f"{base_path}/sleeps/SleepStageDurations{file_type}")
        self.sleep_stage_daily(f"{base_path}/sleeps/SleepStageDaily{file_type}")
        self.resp_rate(f"{base_path}/sleeps/Respiratory_Rate{file_type}")
        self.sleep_score(f"{base_path}/sleeps/SleepScore{file_type}") # NOTE set naps=False to mimic app view
        self.sleep_need_debt(f"{base_path}/sleeps/SleepNeed_SleepDebt{file_type}")
        self.timeinbed_qualitydur(f"{base_path}/sleeps/TimeInBed_QualityDuration{file_type}")
        self.sleep_stages_hist(f"{base_path}/sleeps/SleepStages_Hist{file_type}")
        self.sleep_need_actual(f"{base_path}/sleeps/SleepNeed_vs_Actual{file_type}") # NOTE set naps=False to mimic app view
