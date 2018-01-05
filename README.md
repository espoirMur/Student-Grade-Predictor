# Memory-Working-Directory

In the digital age, Tera-bytes of data is generated per the second by Mobiles devices, digitals photographs, web documents, facebook updates, tweets, blogs, user-generated, Transactions, sensors data, surveillance data, queries, clicks, browsing;cheap storage has made possible to maintain this data, but it has been unused while it contains useful information and insights, that why we need data mining: **_the process of analyzing large amounts of data in an effort to find correlations, patterns, and insights_**

Many research has been made on the use of data mining in industries such as telecoms, insurances, banks, etc but education domain has been unexplored that why we decided to works on the topic: _**Mining educational dataset to improve student orientation at the university**_

We tried to answer his question: **_How can we use modern data mining technics to provide universities tools that can help them to improve new student orientation ?_** To answer that question we have conducted this research by following the cross-industry standard process for data mining.

We have collected data from the information system called University Administrative Tool (UAT) for Université Libre des Pays des Grands Lacs (ULPGL) and our initial dataset had 9606 rows and 22 columns which represent the records of data for each student who studied at ULPGL from 2012 to 2016 , based on that dataset we discovered how student are distributed by gender, option, school, and percentage in the national examination, etc

We have used statistics test (chi-square ,Analysis of variance (ANOVA), Pearson correlation)and predictive models to analyze student marks and try to discover what are criteria students use to choose their departments when they start university, after that we predicted Cumulative Grade Point Average
(CGPA) in with their marks, the field they studied and their secondary school name in each department of ULPGL by stacking 3 different regressors models and 2 different SVM models.

We evaluated the final model by using cross-validation and RMSE and found a score of less than 10% in each department. And finally we have built a web application that suggests a new student their orientation according to the CGPA predicted.
we used those libraries and frameworks: python, pandas, matplotlib,Seaborn, flask numpy and sklearn for this work.


The Flask App Is under The Folder /GradePredictorApp and will be put live soon

All the work can be found in floder /notebook the important notebook are the following:
- DataExplorationDraft1.ipynb
- PredictiveModelBuilding.ipynb
- OuputPreparationDraf1.ipynb

The dataset is in /dataset

Use can use jupyter notebook viewer to visualize them easily, find it here:https://nbviewer.jupyter.org
feel free to make suggestions via pull request!
Thanks!

NB: The latex report of this work can be found in another repository here if you are interested (but the report is in French )
