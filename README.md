# Memory-Working-Directory

This repository contains all my works for my DataMining Project
On the topic: *_Mining educational data to improve student orientation in university_* :

For this project, I've used python , pandas ,seaborn, matplotlib , statsmodels and sklearn  to analyze student marks dataset for my university and try to discover  what are criteria student use to choose theirs departments when they start university, after that i use sklearn to predict GCPA in each of students wih theirs marks , the field they study and their secondary school .
I successfully predicted the CGPA by stacking 5 differents regressors (Ridge , Lasso, Elastic Net , Linear SVR and Rbf SVR )and get a RMSE of 10%.

And finally i'm building a web app (a Flask APi ) that suggests a new student theirs orientation according to those info i use to predict the CGPA

The Flask App Is under The Floder /GradePredictorApp and will be put live soon

All the work can be found in floder /notebook the important notebook are the following:
- DataExplorationDraft1.ipynb
- PredictiveModelBuilding.ipynb
- OuputPreparationDraf1.ipynb


Use can use jupyter notebook viewer to visaulise them easily , find it here:https://nbviewer.jupyter.org
feel free to make sugest via pull request!
Thanks!

NB: The latex report of this work can be found in another repository here if you are intrested (but the report is in french )
Sorry for Bad English and Bad Documentation but Anyway Will improve it soon

