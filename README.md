# Spotify-Track-Analytics-Popularity-Prediction

The Credit Card Customer Churn Analysis project examines the factors that influence customer churn in the credit card industry. Using Explanatory Data Analysis (EDA) and visualization, we will try to identify patterns that distinguish loyal customers from probable churners. 

# ![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)

## Content
* [Readme.md](https://github.com/YShutko/CodeInstitute_Project1_BankChurners/blob/main/README.md)
* [Kanban Project Board](https://github.com/users/YShutko/projects/3)
* [Datasets](https://github.com/YShutko/CodeInstitute_Project1_BankChurners/tree/main/Data) original and cleaned
* [Jupyter notebook](https://github.com/YShutko/CodeInstitute_Project1_BankChurners/blob/main/jupyter_notebooks/HackatonProject1.ipynb)
* [Plotly plots](https://github.com/YShutko/CodeInstitute_Project1_BankChurners/tree/main/Plots) (Plotly plots could not be depicted on Github Jupyter Notebook)

## Dataset Content
The data set used for this project: project: [Kaggle](https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers). The BankChurners dataset contains records of credit card customers, including demographic information (age, gender, marital status, education, income), account details (card type, credit limit, tenure), and transaction behavior (transaction amounts and counts). The dataset also includes a target variable "Attrition_Flag", which indicates whether a customer is an existing customer or an attrited customer.
BankChurners.csv dataset consists of following columns:
* CLIENTNUM: Client number. Unique identifier for the customer holding the account.
* Attrition_Flag: Internal event (customer activity) variable - "Existing Customer" or "Attrited Customer".
* Customer_Age: Demographic variable - Customer's Age in Years
* Gender: Demographic variable - M=Male, F=Female.
* Dependent_count: Demographic variable - Number of dependents.
* Education_Level: Demographic variable - Educational Qualification of the account holder (example: high school, college graduate, etc.).
* Marital_Status: Demographic variable - Married, Single, Divorced, Unknown.
* Income_Category: Demographic variable - Annual Income Category of the account holder (< $40K, $40K - 60K, $60K - $80K, $80K-$120K >).
* Card_Category: Product Variable - Type of Card (Blue, Silver, Gold, Platinum).
* Months_on_book: Period of relationship with bank.
* Mobths_Inactive_12_mon: Inactive period.
* Total_Relationship_Count: This is the number of products/accounts a customer has with the bank.
* Contacts_Count_12_mon: This is the number of contacts (interactions) the customer had with the bank in the last 12 months.
* and etc.

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
