<!-- README.md: WhoopAPI-Wrapper | Author: Colin Macon | License: MIT -->
<a id="top"></a> 

&nbsp;


<div align="center">


  [![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/downloads/)![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white) 
  ![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)

  ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black)![macOS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)

  ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)

</div>

&nbsp;

---

&nbsp;

<p align="center">
<img src="https://i.imgur.com/xpkgw71.png">
</p>


&nbsp;

<!-- PROJECT LOGO -->

<div align="center">
  <p align="center">
    Python API Wrapper for the <a href="https://app.swaggerhub.com/apis/DovOps/whoop-unofficial-api/2.0.1"><strong>Unofficial Whoop API</strong></a>
    <br />
    .
    .
    .
    <br />
    <a href="https://colinmacon.com"><strong>Explore the walkthrough tutorial »</strong></a>
  </p>
</div>

<div align="center">

  [![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

</div>

&nbsp;

---

&nbsp;


<!-- TABLE OF CONTENTS -->
<details >
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#api-overview">API Overview</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#basics">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#basics">Basics</a></li>
        <li><a href="#user-api-setup">User API Setup</a></li>
        <li><a href="#alternative">Alternative</a></li>
      </ul>
    <li><a href="#finding-your-first-instance-of-data">Finding your first instance of data</a></li>
      <ul>
        <li><a href="#option-1">Option 1</a></li>
        <li><a href="#option-2">Option 2</a></li>
      </ul>
    <li><a href="#examples">Examples</a></li> 
      <ul>
        <li><a href="#general">General</a></li>
        <li><a href="#data-pull">Data Pull</a></li>
        <li><a href="#combing-raw-data">Combing raw data</a></li>
      </ul>
    <li><a href="#autorun">AutoRun</a></li>
    <li><a href="#independent-use">Independent Use</a></li>
      <ul>
        <li><a href="#data-pull">Data Pull</a></li>
        <li><a href="#cleaning">Cleaning</a></li>
      </ul>
    <li><a href="#graphs">Graphs</a></li>
      <ul>
        <li><a href="#graph-examples">Graph Examples</a></li>
          <ul>
            <li><a href="#cycles">Cycles</a></li>
            <li><a href="#recovery">Recovery</a></li>
            <li><a href="#sleeps">Sleeps</a></li>
            <li><a href="#workouts">Workouts</a></li>
            <li><a href="#heart-rate">Heart Rate</a></li>
          </ul>
      </ul>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

&nbsp;

---

&nbsp;


# API Overview 



The Whoop API Wrapperis essentially broken down into 6 major categories:

1. **Cycles** - daily overview
2. **Recovery** - resting overview
3. **Sleeps** - detail of rest (Sleep & Naps)
4. **V2 Activities** - (I returned no data  here)
5. **Activities** - detail of Running, Hiking, Weightlifting, etc...
6. **Heart Rate series** - granular HR time-series info



&nbsp;

> **Note**: Every endpoint from the reverse engineered [Unofficial Whoop API](https://app.swaggerhub.com/apis/DovOps/whoop-unofficial-api/2.0.1) has **NOT** been built out. This project started off by just returning the basic information from the API for personal use. However, the code has been expanded since then and a large portion of the API endpoints are available here. If you would like to add to the code please feel free to make it your own.

> All data uses the API URL: https://api-7.whoop.com 



---

&nbsp;

## Getting Started

---

&nbsp;

### Prerequisites

---

&nbsp;



> All code was built using Python 3.10.5 on both Mac OS & Linux systems 
> -  Other versions of python may work but have not been tested



&nbsp;


### Installation

---

&nbsp;

1. Clone the repo
    ```sh
    # Clone repo 
    git clone https://github.com/colinmacon/WhoopAPI-Wrapper.git

    # cd into project
    cd WhoopAPI-Wrapper 
    ```

&nbsp;

2. Create virtual environment



- Virtualenv users
    ```sh
    # Create virtual env
    virtualenv -p /usr/bin/python3.10.5 <my_env_name> 

    # Activate env
    source <my_env_name>/bin/activate 

    #Install requirements
    pip install -r requirements.txt 
    ```


- Pipenv users
  ```sh
  # Should find and install requirements.txt as well 
  pipenv install --python 3.10.5

  # If not use:
  pipenv install -r requirements.txt #Install requirements

   ```

<p align="right">(<a href="#top">back to top</a>)</p>




---

&nbsp;


## Usage

---

&nbsp;

### Basics 

---

&nbsp;

- **Import class**

  ```python
  # Contains all the classes and methods we are going to need to start
  from whoop import *
  ```

&nbsp;

- **Setting up a folder structure to send all of our data to later**
    - *I recommend this if you to store your data, but you can choose to do so another way if you would like*



  ```python
  import os 

  os.chdir("..") # cd to parent folder so our data isn't in /scripts
  base_path = os.getcwd() # /WhoopAPI folder (can also specify your own path)
  desired_folder_name = "data" # Name of parent folder you want to create
  create_folders(f"{base_path}/{desired_folder_name}")
  ```

  ```sh
  # Creates the following structure 
  .
  ├── clean
  │   ├── hr_data
  │   ├── master
  │   └── records
  │       ├── cycles
  │       ├── grouped_workouts
  │       ├── recovery
  │       ├── sleeps
  │       ├── v2
  │       └── workouts
  ├── csvs
  │   ├── hr_data
  │   └── records
  │       ├── cycles
  │       ├── recovery
  │       ├── sleeps
  │       ├── v2
  │       └── workouts
  ├── graphs
  │   ├── cycles
  │   ├── hr
  │   ├── recovery
  │   ├── sleeps
  │   ├── v2
  │   └── workouts
  └── jsons
      ├── hr_data
      └── records
  ```
&nbsp;

### User API Setup

---

-  For the sake of simplicity you can import and run **SimpleSetup()** to get you started
- SimpleSetup creates a .json file named by the user or *creds.json* by default. No need to do anything but run SimpleSetup as it will prompt you for your Whoop email and password in the terminal
- SimpleSetup retrieves and tests your API *UserID* and *Token* to see if it is still valid and will refresh your credentials if not upon start
- All you need to do is make sure you have the correct .json filename and path entered as a parameter 
  - leaving it blank creates creds.json in current path as mentioned

  &nbsp;
  - **SimpleSetup(json_filename="creds.json", api_url="https://api-7.whoop.com)**
  ```python
  # Using default params
  ss = SimpleSetup() # Custom location example -> ss = SimpleSetup('/Users/me/custompath/customnmae.json') 
  userid, token = ss.run()

  ```

  - Example output upon first run
  ```sh
    Credentials json file not found...
    Creating creds.json

    Username not found in creds.json
    please enter account e-mail: email@gmail.com

    Password not found in creds.json
    Please enter account password:

  ```
&nbsp;

### Alternative

---

- you can run **refresh_token()** which will generate a new API token for you each time it is called 

  ```python
  email = '' # or load as sys variables
  password = ''
  userid, token = refresh_token(email, password)
  ```

  > **Note**: please be aware that **refresh_token()** will generate a new token and **NOT** store it in your .json file. You can store your credentials another way if you would like and from experience they should last for awhile, but can be refreshed multiple times if you choose to go that route.


<p align="right">(<a href="#top">back to top</a>)</p>


---

&nbsp;


## Finding your first instance of data

---

&nbsp;

#### Option 1

---

&nbsp;

- Go into your Whoop App -> Press "Today"  (as shown) -> Find earliest date (light blue-grey)
   > **Note**: Blue text with dot  represents Day Strain 10.0+ (NOT your first day)


<p align="center">
<img style="float: center;" src="https://i.imgur.com/5HUBI4F.png" width="300">
</p>

<p align="center">
<img src="https://i.imgur.com/6kCyxhl.png" width="300">
</p>

---

&nbsp;

&nbsp;


#### Option 2

---

&nbsp;

- Go to Whoop.com -> login -> click on the calendar -> find the first instance of your data. 

  - Using my account as an example:


    ![Calendar View](https://i.imgur.com/SAzAKQC.png"Calendar")


    ![Data Start](https://i.imgur.com/DDxTv6o.png "HR")

    > We see that my earliest start would be ""2022-05-03T22:09:00.000Z" whereas my updatedAt value from *profile_info()* was "2022-05-03T23:32:44.163Z" so you may have to play around with your start date in order to get the data you need. Reason being the API will not return a successful response if your dates are outside the bounds of the data it has or if you try to return too much data at once. Therefore I would recommend returning about a month of data at a time and then concatenate the results.



<p align="right">(<a href="#top">back to top</a>)</p>


---

&nbsp;

&nbsp;

## Examples

---

&nbsp;


> **Note**: All output_type parameters are set to 'df' by default returning a Pandas DataFrame, but 'json' may also be passed if you want to return the raw response from the API


&nbsp;


### General 

---

&nbsp;



  **test_session()**
  - confirms your API creds are working before running an entire script

    ```python
    wapi.test_session()

    # Output
    '''
    --  Attempting to connect to API now  --
    -----  Session succesfully started  -----
    -----------------------------------------

    -- API Credentials Approved for: ---

      Colin Macon - (CJwns)
      Pittsburgh, PA - US
      Membership Status: active
    '''
    ```
  ---

  &nbsp;

  &nbsp;

  **profile_info()**
  - Your personal account information

    ```python
    pi_df = wapi.profile_info() # Nothing specified will return pandas df
    ```
  ---

- *Example output*: 
  |      id | avatarUrl                                                                                                                                   | createdAt                | updatedAt                | firstName   | lastName   | city       | country   | adminDivision   | fullName   | email               | username   | concealed   | membershipStatus   | preferences_performanceOptimizationAssessment   |   preferences_performanceOptimizationDayOfWeek | privacyProfile_overview   | privacyProfile_intensity   | privacyProfile_recovery   | privacyProfile_sleep   | privacyProfile_stats   | privacyProfile_comps   |
  |--------:|:--------------------------------------------------------------------------------------------------------------------------------------------|:-------------------------|:-------------------------|:------------|:-----------|:-----------|:----------|:----------------|:-----------|:--------------------|:-----------|:------------|:-------------------|:------------------------------------------------|-----------------------------------------------:|:--------------------------|:---------------------------|:--------------------------|:-----------------------|:-----------------------|:-----------------------|
  | 12345678 | https://s3-us-west-2.amazonaws.com/avatars.whoop.com/uploads/uploads/user/12345678 | 2022-04-07T21:22:55.578Z | 2022-05-03T23:32:44.163Z | Colin         | Macon      | Pittsburgh | US        | PA              | Colin Macon   | inbox@gmail.com | CJwns      | False       | active             | True                                            |                                              1 | all                       | all                        | all                       | all                    | all                    | all                    |



  ---

  &nbsp;

  &nbsp;

**sport_info_mapping()**
  - Data Dicitionary of all of Whoops activities with ID

    ```python
    si_df = wapi.sport_info_mapping() # Nothing specified will return pandas df
    ```
    ---

- *Example output*: 

    |   id | icon_svg_url                                                                        | created_at                   | updated_at                   | name       | icon_url                                                                            | category           | activity_type_internal_name   | has_gps   | is_current   | has_survey   |
    |-----:|:------------------------------------------------------------------------------------|:-----------------------------|:-----------------------------|:-----------|:------------------------------------------------------------------------------------|:-------------------|:------------------------------|:----------|:-------------|:-------------|
    |    0 | https://s3-us-west-2.amazonaws.com/icons.whoop.com/mobile/activities/running.svg    | 2014-02-11T10:07:16.000+0000 | 2022-06-03T20:06:46.581+0000 | Running    | https://s3-us-west-2.amazonaws.com/icons.whoop.com/mobile/activities/running.png    | cardiovascular     |                               | True      | True         | True         |
    |    1 | https://s3-us-west-2.amazonaws.com/icons.whoop.com/mobile/activities/cycling.svg    | 2014-02-11T10:07:16.000+0000 | 2022-06-03T20:06:45.713+0000 | Cycling    | https://s3-us-west-2.amazonaws.com/icons.whoop.com/mobile/activities/cycling.png    | cardiovascular     |                               | True      | True         | True         |
    |   16 | https://s3-us-west-2.amazonaws.com/icons.whoop.com/mobile/activities/baseball.svg   | 2014-02-11T10:07:16.000+0000 | 2022-06-03T20:06:45.511+0000 | Baseball   | https://s3-us-west-2.amazonaws.com/icons.whoop.com/mobile/activities/baseball.png   | non-cardiovascular |                               | False     | True         | True         |
    |   17 | https://s3-us-west-2.amazonaws.com/icons.whoop.com/mobile/activities/basketball.svg | 2014-02-11T10:07:16.000+0000 | 2022-06-03T20:06:45.527+0000 | Basketball | https://s3-us-west-2.amazonaws.com/icons.whoop.com/mobile/activities/basketball.png | cardiovascular     |                               | False     | True         | True         |
    |   18 | https://s3-us-west-2.amazonaws.com/icons.whoop.com/mobile/activities/crew.svg       | 2014-02-11T10:07:16.000+0000 | 2022-06-03T20:06:46.540+0000 | Rowing     | https://s3-us-west-2.amazonaws.com/icons.whoop.com/mobile/activities/crew.png       | cardiovascular     |                               | True      | True         | True         |


  ---

  &nbsp;

  &nbsp;


### Data Pull


---

  > **Note**: start and end parameters are to entered as a string in Complete ISO-8601 date format

&nbsp;

- For a **single time period** please use **single_datapull.py** in /scripts and specify the following variables:

  ```python
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
  base_path = os.getcwd() # Set base path as var
  data_folder = "data" # Set parent folder name for data 
  ```

---

&nbsp;



- For a **multiple time periods** please use **multi_datapull.py** in /scripts and specify the following variables:
  - (Similar to *single_datapull.py*)


  ```python
  # Specify your start and end dates to use 
  user_start_string = "2022-05-03T23:32:44.163Z"
  user_end_string = "yesterday" # Use custom timestamp or "yesterday" to pull up to yesterday's data

  # NOTE hr_freq "6" needs shorter hr_range_skip _days | "600" can use wider range
  hr_range_skip_days = 5 
  hr_freq = "60" # Default | "6" "600" are the other options
  itteration_pause = 2.5 # time to sleep between API calls 

  # Setting up basic paths to use 
  # NOTE you are going to want to leave this so the script finds the creds.json file in home path
  os.chdir("..") # cd to home folder 
  base_path = os.getcwd() # Set base path as var
  data_folder = "data" # Set parent folder name for data 
  ```

  > **Note**: You may potentially have to fill in some gaps with exact start and end dates using *single_datapull.py* as dates can be tricky with them not being in your local timezone and figuring out whether or not to account for daylight savings.
  >  - (all insturctions are located within the scripts)

---

&nbsp;

&nbsp;

### Combing raw data 

---


- If you elected to export your data into csvs using the folder structure created by **create_folders()** you can use **combine_indy_export.py** in order to concatenate, clean, and export your data into pickle format (saves dtypes)

- **combine_indy_export_py**

  ```python
  # NOTE you need to specify your start and end dates 
  # as the combined files will use these dates for the end of the filename
  start = "2021-12-28"
  end = "2022-08-06"

  # Setting up basic paths to use 
  # NOTE you are going to want to leave this so the script finds /data folder (or custom name you created)
  os.chdir("..") # cd to home folder 
  base_path = os.getcwd() # can overwrite with custom path
  data_folder = "data" # Set parent folder name for data 

  # 'clean' folder for pickle | csvs for raw data (based on create_folders() function) 
  folder_type = "csvs"
  ```


<p align="right">(<a href="#top">back to top</a>)</p>



&nbsp;

---

&nbsp;


## AutoRun

---

- **cli_autorun.py**
  - Simply run the script and follow the prompts in the terminal 
  - You will need your timestamp from the first intance of your data or the script will use the `updatedAt` date from your profile_info df 
  - All raw data will pulled, cleaned, and exported based on user inputs 
    - Graphs can be created as well in .png or .html format 
      - (excluding HR Series Graph)

  > **Note**: this script is meant to be used to return large periods of data easily. If you do not have certain information in the dfs (such as workout data) returned the cleaning and graphing portion will cause the script to fail 

&nbsp;

- Example Use
  ```
   _       ____                         __  __            _________            __   ___    ____  ____
  | |     / / /_  ____  ____  ____     / / / /___  ____  / __/ __(_)________ _/ /  /   |  / __ \/  _/
  | | /| / / __ \/ __ \/ __ \/ __ \   / / / / __ \/ __ \/ /_/ /_/ / ___/ __ `/ /  / /| | / /_/ // /
  | |/ |/ / / / / /_/ / /_/ / /_/ /  / /_/ / / / / /_/ / __/ __/ / /__/ /_/ / /  / ___ |/ ____// /
  |__/|__/_/ /_/\____/\____/ .___/   \____/_/ /_/\____/_/ /_/ /_/\___/\__,_/_/  /_/  |_/_/   /___/
                          /_/

  [?] Whoop account email address: email@gmail.com
  [?] Whoop account password: ***********************

  Timestamp of first data
  (without converting to local time),
  Ex: 2022-02-01T22:45:00.000Z = 2022-02-01 10:45PM UTC
  [?] Leave blank to use Whoop Profile Info 'updatedAt' date: 2022-05-03T23:32:44.163Z

  Timestamp of last data you want to pull 
  Ex: 2022-08-01T01:00:00.000Z
  [?] Leave blank to use yesterday's date: 
  [?] Name your folder where the data will be saved: data
  [?] Name your credentials file where UserID and Token will be stored (Ex: creds.json): creds.json
  [?] Frquency of Heart Rate data (seconds): 60
    6
  > 60
    600

  [?] Amount of time to sleep inbetween API calls: 2.5
  [?] Clean your data?: Yes
  > Yes
    No

  [?] Create graphs?: Yes
  > Yes
    No

  [?] Static (.png) or Interactive (.html) graphs?: html
    png
  > html

  Raw data will be stored at data/csvs/records/..
  Pulling data for 2022-05-03T23:32:44.163Z -  now
  -------------------------------------------------------------------------------------------------

  
  ```



<p align="right">(<a href="#top">back to top</a>)</p>


&nbsp;

---

&nbsp;


## Independent Use

---


&nbsp;

&nbsp;

### Data Pull

---


&nbsp;

- Setup 
  - Import WhoopAPI from whoop.py in home directory 

  ```python
  from whoop import *

  # Call the WhoopAPI class and pass your userid and token
  wapi = WhoopAPI(userid, token) # Start Whoop API 
  ```

---

&nbsp;

-  **get_all(start, end, output_type)**
    - This will return the majority of the data available to you in the API (Cycles, Recovery, Sleeps, V2 activities, and Activities (I use the alias Workouts - Running, Hiking, Weightlifting, etc...)



    ```python
    # Specifying new start and end dates that I have data for 
    start = "2022-05-03T23:32:44.163Z"
    end = "2022-05-31T01:00:00.000Z"
    # Cycles, Recovery, V2 Activities, Workouts (Activities)
    c_df, r_df, s_df, v2_df, w_df = wapi.get_all(start, end) # Default is ‘df’ can also use ‘json’
    ```


    > **Note**: V2_Activities has never returned any data for me and that is the reason it isn't shown as an example output.

&nbsp;

---

&nbsp;


- **get_specific_df(start, end, df_name)**
  - If you **don't** want to return all of that information you can select to return a singluar Pandas DataFrame by name with this function. 


  ```python
  # Avalibale df_names: 'cycles',  'recovery',  'sleeps',  'v2_activities',  'workouts'
  # Cycles as an example
  c_df2 = wapi.get_specific_df(start, end, "cycles")
  ```
  > **Note**: json output is not avaliable for this function


&nbsp;

---

&nbsp;

- **get_hr_data(start, end, frequency, output_type)**
  - Returns a time-series of TZ time and HR (Beats per Minute) at specific timestamp
Frequency options (seconds): **"6", "60", "600"** | Default = "60"

  ```python
  # Shorter time range for HR to we don't return a bad response
  hr_start  =  "2022-05-14T01:00:00.000Z"
  hr_end  =  "2022-05-19T01:00:00.000Z"

  # Default's of 60 seconds and df output due to not specifying all params
  hr_df  =  wapi.get_hr_data(hr_start, hr_end) # frequency="60", output_type='df' by default 
  ```
  > **Note**: notice we have specified a shorter time-frame as the API will only return so much data at once. Passing a frequency of 6 seconds requires a shorter time-frame whereas 600 can accept a larger one. 
  
  > Here I am using the default of "60" with a 5 day range. *If you would like to get ALL of your data you can put multiple ranges into lists and loop through with a sleep()* or use the hr section of *multi_datapull.py* in /scripts
  <p align="right">(<a href="#top">back to top</a>)</p>


---


&nbsp;


&nbsp;


### Cleaning

---

&nbsp;

> **IMPORTANT!!!** These methods are hardcoded, but being a user of the code I will try my best to keep things up to date to insure nothing breaks and CleanWhoop() remains usable. 

- You will also notice the methods do the following:
  -  drop rows that only contains NaNs | fill remaining NaNs
  -  drop duplicated rows 
  - convert column dtypes
  - convert kilojoules to calories (where applicable)
  -  convert timestamps to your local time 
  - order data from oldest -> most recent date
  - In some cases add columns extracted from timestamps such as:
    -  Month Name, Year, Month, Week and Day number, Hour, Minute, etc... 
    *(This is handy for analysis, but may not be needed on a user by user basis)* 
  - Break apart columns with embedded lists as values


---

&nbsp;

### Intialize CleanWhoop()

---

&nbsp;

- Setup
  ```python
  from whoop import * # Should already be done from pulling data
  scrub = CleanWhoop() # Init CleanWhoop() as scrub
  ```

---

&nbsp;

- Cleaning the main data 
  - **cycles(df)**
  ```python
  # Cycles Cleaned df
  cc_df = scrub.cycles(c_df) # c_df from wapi.get_all() | wapi.get_specific_df(start, end, "cycles")
  ```

  - **recovery(df)** 
  ```python
  # Recovery Cleaned df
  rc_df = scrub.recovery(r_df) # r_df from wapi.get_all() | wapi.get_specific_df(start, end, "recovery")
  ```

  - **sleeps(df)** 
  ```python
  # Sleeps Cleaned df
  sc_df = scrub.sleeps(s_df) # s_df from wapi.get_all() | wapi.get_specific_df(start, end, "sleeps")
  ```

  - **workouts(df)**
  ```python
  # Workouts Cleaned df
  wc_df = scrub.workouts(w_df) # w_df from wapi.get_all() | wapi.get_specific_df(start, end, "workouts")
  ```

---

&nbsp;


- **group_workouts(df)**
  - When going through the data I noticed that you can have multiple workouts in a day. If you want to put all of your information as 1 day = 1 row were going to have to group the information into a singular record per day with this method:

  ```python
  # Grouped Workouts Cleaned df
  gwc_df = scrub.group_workouts(wc_df)
  ```
  > Takes the WORKOUTS CLEANED df not raw data | needs the dtypes from the cleaned data

---

&nbsp;


- **hr(df)**

  - Cleans HR time-series data as follows:
    - drops all duplicate rows
    - converts timestamp to local time
    - adds date timestamp column without HH:MM:SS.ms
    - adds year, month, week, and day number
    - adds hour, minute, second, microsecond columns 
    - sorts data from oldest -> newest date

  ```python
  # Clean Heart Rate df
  hrc_df = scrub.hr(hr_df) # hr_df from wapi.get_hr_data()
  ```

---

&nbsp;


- **create_overall_df(self, cycles_df, recovery_df, sleeps_df, workouts_df)**


  - Method takes in all data with the exception of V2 activities (no data returned) and survey responses
    - groups workouts by day internally using the group_workouts() method above
    - Sleeps are split into Non-Naps and Naps as I didn't want to group these instances
      - sleeps and naps are separated and then joined on the same row based on the day they occurred 
    - Duplicate columns and columns only containing one value are dropped
    - prefixes are assigned based on data type (cycles = c_, recovery = r_, etc...) 
      - This avoids column names ending in _x or _y and makes it a bit easier to understand where the data came from


  > Input the cleaned dfs from above into this function as the dtypes and column names from cleaning are needed to join the data 
    
  ```python
  # Cycles, Recovery, Sleeps, Workouts (NOT grouped this will be done for us)
  master_df = scrub.create_overall_df(c_df,  r_df,  s_df,  w_df)
  ```

<p align="right">(<a href="#top">back to top</a>)</p>

---

&nbsp;

&nbsp;

## Graphs 

---


- All graphs can be exported using your cleaned data as the dtypes and certain column names created from the cleaning process are needed
- All code can be found in **charts.py** which contains the class **VisableWhoop()**
  - **export_charts.py** has pre-written code for you to export the graphs as either .png or .html files

  > **Note**: *VisableWhoop()* allows you to export the graphs as .png (static) or .html (interactive) format, but jupyter notebooks are also avaliable in /jup_notebooks folder that have all of these graphs as well


  > **Graph notes**: with the exception of the first two graphs in **VisableWhoop()** all graphs are interactive thanks to the plotly library when opened using a broswer 

  > Further instructions are available in **export_charts.py** in /scripts 

  ```python
  graphs = VisableWhoop(cycles_df, recovery_df, workouts_df, sports_info_df, sleeps_df, False, hr_df) # Run All
  ```

&nbsp;

---

&nbsp;



### Graph Examples 

---


> **Note**: All graphs available are not shown here. This section is to simply display some of the graphs that you can export using this repo

&nbsp;

#### Cycles

---

- **Scaled Strain per Day**
	-	Viewing daily Scaled Strain which mimics the graph found in the app
		-	The difference here is we can view more days and interact with the graph

  > scaled_strain() in VisbaleWhoop


  ![Scaled Strain per Day ](https://i.imgur.com/GGLAa8h.png"ScaledStrain")
[Datapane Link](https://datapane.com/reports/OkpRy63/scaledstrain-perday/)

&nbsp;

- **Max & Average HR per Day**
	- Viewing how our Max HR affects our Average HR through time

  > max_avg_hr() in VisbaleWhoop


  ![Max & Average HR per Day](https://i.imgur.com/Y3QJLOv.png"MaxAvgHR")
[Datapane Link](https://datapane.com/reports/EkaMXbk/max-avg-hrperday/)

---

&nbsp;

&nbsp;

#### Recovery

---

- **Sleep and Wake Times**
	- The time you fell asleep and woke up
	- Viewing the overall consistency of your sleep patterns 

  > sleep_wake() in VisableWhoop()


  ![Sleep and Wake Times](https://i.imgur.com/jyWSKI5.png"SleepWakeTimes")
[Datapane Link](https://datapane.com/reports/Xknb4Kk/sleepwaketimes/)

&nbsp;


- **Recovery Score**
	- `recovery_score`: your overall recovery score on the home screen in the app

  > recovery_score() in VisableWhoop


  ![Recovery Score](https://i.imgur.com/874gZSp.png"RecoveryScore")
[Datapane Link](https://datapane.com/reports/mA2W483/recoveryscore/)

---

&nbsp;

&nbsp;

#### Sleeps

---


- **Sleep Stage Durations**
	-   `light_sleep_duration`: light sleep in milliseconds
	-   `rem_sleep_duration`: REM sleep in milliseconds
	-   `slow_wave_sleep_duration`: SWS in milliseconds
	-   `wake_duration`: complete time you spend awake in bed in milliseconds
	-   `arousal_time`: how long you spend in bed after waking up in milliseconds
	-  All columns we're converted to hours and formatted for view 

  > sleep_stage_durations() in VisableWhoop


  ![Sleep Stage Durations](https://i.imgur.com/rYRYxwG.png"SleepStageDur")
[Datapane Link](https://datapane.com/reports/VkBaMa7/sleepstagedurations/)

&nbsp;

- **Sleep Need vs Actual Sleep**
	- `sleep_need`: [calculated by Whoop](https://support.whoop.com/WHOOP_Data/Sleep/How_Sleep_Need_is_Calculated)
	- Actual Sleep: the amount of time you actually slept

  > sleep_need_actual() in VisableWhoop


  ![Sleep Need vs Actual Sleep](https://i.imgur.com/7DGMbqG.png"SleepNeedActual")
[Datapane Link](https://datapane.com/reports/9Ax1OK3/sleepneed-vs-actual/)

---

&nbsp;

&nbsp;

#### Workouts 

---


- **Zone Duration % by Date**
	- In training zones are often used to maximize your efficiency 
		- This graph shows the amount of time spent in each zone 

  > zone_duration() in VisableWhoop


  ![Zone Duration % by Date](https://i.imgur.com/dJ9A8gZ.png"WorkoutZoneDur")
[Datapane Link](https://datapane.com/reports/8AVpbR7/zonedurations/)

&nbsp;

- **Average Heart Rate per Activity**
	- Different types of activities often result in different types of fitness  
	- This chart shows the summary set of average heart rate by activity type 

  > workout_hr() in VisableWhoop


  ![Average Heart Rate per Activity](https://i.imgur.com/2Ee9hPj.png"AverageHeartRateperActivity")
[Datapane Link](https://datapane.com/reports/d7dgxn3/workout-hr-byactivity/)

---

&nbsp;

&nbsp;


#### Heart Rate

---

- **Heart Rate Series Data**
	- A simple graph to show your heart rate through a specified time-frame
	 
	- **It is highly recommend to filter your** *hr_df* **to a small range i.e. 1 day to avoid freezing your machine**

  > hr_series() in VisableWhoop


   ![HR Series](https://i.imgur.com/9NusrAX.png"HRSeries")
[Datapane Link](https://datapane.com/reports/43gaPvk/heartrateseries/)






<p align="right">(<a href="#top">back to top</a>)</p>


&nbsp;

---

&nbsp;



## License

[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/) 



&nbsp;

---

&nbsp;

## Resources
---

| Description | Link |
| ------ | ------ |
| Unofficial Whoop API - endpoints |  https://app.swaggerhub.com/apis/DovOps/whoop-unofficial-api/2.0.1|
| How to get your Whoop data |  https://bla.sh/whoop-api/|
| unofficalWhoopAPI - python | https://github.com/ianm199/unofficialWhoopAPI |
| Python 3 script to export WHOOP recovery data | https://gist.github.com/jkreileder/459cf1936e099e2e521cee7d2d4b7acb |

&nbsp;

---

&nbsp;

## Contact


&nbsp;

<center>

[![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/colinmacon) [![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/colin-macon-b91a85165/) [<img src="https://img.shields.io/badge/PORTFOLIO_SITE-orange.svg?logo=LOGO" width="140">](https://colinmacon.com)

</center>

<p align="right"></p>


&nbsp;

---
---

