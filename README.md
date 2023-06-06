# 

Hi! I'm a 19-year-old HSE student majoring in economics, with a keen interest in data science and data analytics. Over the past year, I have focused on learning Python and data-oriented libraries such as **Pandas**, **sklearn**, **Numpy**, **plotly**, **matplotlib**, etc. 

I have participated in two Kaggle competitions: **banking scoring** and **prediction of user churn**. While studying at the CMF, I built a few functions that make it easy to **import macro data into Python** and even create a **gif with a distribution of the selected macro variable on the map**. 

Currently, I'm a **graduate program student at CMF**, a **Deep Learning School student**, and a **School of Analytics student**. Below, I will describe the files that contain my projects.

Also I participated in a few team projects: solving Sber time series prediction and replication of macro paper in the field of auto correlations correlations. 

1. *GIF maker* is a Python script that creates a choropleth GIF visualizing the change of a selected variable across time for a selection of countries using World Bank data. The script pivots the data, sorts it by country, and converts country names to ISO3 codes. It then creates a choropleth visualization for each year using Plotly, saves each frame as a PNG file, and creates a GIF from the PNGs using ImageIO. Finally, it trims the GIF using MoviePy and saves the output as a new GIF. The giffer function takes two arguments: the name of the variable to plot and the name of the output file.

2. *example.gif* - This GIF shows the distribution of Gini coefficient on the map over 50 years.

3. *Binar variable maker* is a Python script that creates a distribution of the difference between medians of target variables in separated groups, divided by values of all the other available variables. This approach provides an opportunity to reduce the dimension of the data and reduce time required for machine learning education.

4. *Presentation's notebook* - calculations for presentation below and adaptive linear regression algorithm.
5. *Conference presentation* - presentation of project answering on 5 questions: 
- Is the inequality homogeneous? 
- Which variables are the best predictors?
-  Which binary variables are the best predictors? 
- Does the geographical factor play any role in predicting inequality?
Also in presentation there is a description of adaptive linear regression.
6. *Macro_Replication_Baxter-King and Macro_Task_Replication* - notebooks with calculations for article replication and direct replication of the [article](https://www.ecb.europa.eu/pub/pdf/scpwps/ecbwp095.pdf) itself accordingly. **Macro_Replication_Baxter-King** is what I was responsible for and **Macro_Task_Replication** is a result of our teamwork.
7. *Sber_TimeSeries.ipynb* our team developed a solution for predicting the number and timing of delivery orders for SberMarket and optimizing the number of couriers using the simplex method. I was responsible for the time-series prediction task and utilized the fbprophet library to achieve this goal.
8. *CMF_Scoring_Kaggle.ipynb* is a demonstration of my initial work in machine learning. I used random forest, xgboost and simple decision tree models. The notebook also includes visualizations of ROC-AUC curves and cross-validation scores.
9. *DLS_prediction_of_user_churn_Kaggle* - is a notebook that presents a prediction of consumer outflow using binarized variables and visualization of the train dataset on subplot. The prediction is achieved through the use of pipeline, random forest, catboost, and xgboost, with an ROC-AUC score of around 0.85.
10. [The last part](https://colab.research.google.com/drive/1NLmjmqKmsfP6zsaiePSqd3djddoiR29Q?usp=sharing) is a solution for building a funnel chart, divided by months and weeks for quests company requesting data from an external database. Also I implemented a dynamic funnel that changes by month.
