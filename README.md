# Spotify Track Analytics Popularity Prediction

# ![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)
<p align="center">
  <img src="ChatGPT Image Nov 11, 2025, 11_08_22 AM.png" alt="Project Logo" width="25%">
</p>
## Content
* [Readme.md](https://github.com/YShutko/spotify_track_analytics_popularity_prediction/blob/1eb084f166f61e2ec0c6dcf23cdb3fea6f7f3cb8/README.md)
* [Kanban Project Board](https://github.com/users/YShutko/projects/6)
* [Datasets](https://github.com/YShutko/CodeInstitute_Project1_BankChurners/tree/main/Data) original and cleaned
* [Jupyter notebook]()

## Dataset Content
The data set used for this project: [Kaggle](https://www.kaggle.com/datasets/maharshipandya/-spotify-tracks-dataset). TA collection of ~114,000 songs across 125 genres with features like danceability, energy, tempo, and popularity. Ideal for audio analysis, genre classification, and music trend exploration.

The dataset consists of the following columns:
* track_id: Unique Spotify identifier for each track.
* artists: List of artists performing the track, separated by semicolons.
* album_name: Title of the album where the track appears.
* track_name: Title of the song.
* popularity: Score from 0–100 based on recent play counts; higher means more popular.
* duration_ms: Length of the track in milliseconds.
* explicit: Indicates whether the track contains explicit content (True/False).
* danceability: Score (0.0–1.0) measuring how suitable the song is for dancing.
* energy: Score (0.0–1.0) reflecting intensity, speed, and loudness.
* key: Musical key using Pitch Class notation (0 = C, 1 = C♯/D♭, etc.).
* loudness: Overall volume of the track in decibels.
* mode: Indicates scale type (1 = major, 0 = minor).
* speechiness: Score estimating spoken content in the track.
* cousticness: Likelihood (0.0–1.0) that the song is acoustic.
* instrumentalness: Probability that the track has no vocals.
* liveness: Measures if the song was recorded live (higher = more live).
* valence: Positivity of the music (0.0 = sad, 1.0 = happy).
* tempo: Speed of the song in beats per minute (BPM).
time_signature: Musical meter (e.g. 4 = 4/4 time).
track_genre: Musical genre classification of the track.

## Business Requirements
The business needs to understand the drivers of credit card customer attrition to reduce churn and improve customer retention. Specifically, management requires clear visual insights that show how churn varies across customer segments (demographics, income, card type) and behavioral features (inactive months, dependents, tenure, transactions, credit limits).


## Hypothesis
 * Hypothesis 1: Customer churn is evenly distributed across card categories.
    Result: Rejected. Churn is concentrated almost entirely among Blue cardholders, while premium card customers (Gold, Platinum) show very low attrition.

* Hypothesis 2: Demographic characteristics (gender, marital status, education, income) are strong drivers of churn.
   Result: Rejected. Churn proportions are nearly identical across demographic groups, indicating these features alone have limited predictive power.

* Hypothesis 3: Inactivity (months inactive in the last 12 months) has no significant relationship with churn.
   Result: Rejected. Inactive months emerged as the strongest churn predictor, with attrited customers showing higher inactivity, wider variability, and more frequent outliers (≥4 inactive months).

* Hypothesis 4: Customers with dependents are equally likely to churn as those without.
   Result: Rejected. Attrited customers with dependents tend to be younger with shorter tenure, making dependents an additional risk factor when combined with other attributes.

* Hypothesis 5: Correlation patterns between features remain the same regardless of churn status.
   Result: Partially rejected. While the age–tenure correlation remains strong across groups, dependents and inactivity show notable shifts in correlation for attrited customers, highlighting their role as churn differentiators.

## Project Plan
* Data inspection & cleaning: preparing categorical and numerical features for analysis.
* Univariate analysis: target variable (Attrition_Flag) distribution.
* Bivariate analysis: exploring relationships between features and churn (Attrition_Flag).
* Correlation analysis: comparing numerical relationships across existing and attrited customers.
* Group comparisons: using difference heatmaps to highlight how patterns shift with churn.
* Visualization: interactive and static plots to present insights clearly.

## The rationale to map the business requirements to the Data Visualisations
The purpose of the visualisations was not only to explore the dataset but to directly answer the business questions around customer churn. By aligning each chart with a business requirement, the analysis becomes actionable for decision-makers:
* Churn Distribution Plot addresses the need to quantify the scale of attrition and confirm whether churn is a critical issue.
* Categorical Variable Visualisations (Gender, Education, Marital Status, Income, Card Category) provide clarity on which customer segments are most vulnerable, helping the business target retention campaigns more effectively.
* Correlation Heatmaps respond to the need for understanding feature relationships and ensure the business focuses on independent drivers rather than redundant information.
* Difference Heatmaps (Existing vs. Attrited Customers) meet the requirement of identifying how relationships change with churn, highlighting dependents and inactivity as distinguishing features.
* Inactive Months Boxplots and Histograms support the requirement to identify behavioral risk factors, showing inactivity as the strongest churn driver.
  
## Analysis techniques used
* Visual Studio Code
* Python
* Jupyter notebook
* ChatGPT

# Planning:
* GitHub [Project Board](https://github.com/users/YShutko/projects/3) was used to plan and track the progress.

## Main Data Analysis Libraries
* Pandas
* Numpy
* Plotly
* Seabon
* Matplotlib
 
## Credits 
* [The Code Institute](https://codeinstitute.net/) Learning Management System
* [VS Code](https://code.visualstudio.com/) was used to wite the code
* [ChatGPT](https://chatgpt.com/) was used to generate and debug code
* [README](https://github.com/Code-Institute-Solutions/da-README-template) template
* [Kaggle](https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers) data set was used for this project

# Acknowledgements
Thanks to our facilitator Emma Lamont, tutors Mark Briscoe, Roman Rakic, and Niel McEwan from the Code Institute for their assistance.
