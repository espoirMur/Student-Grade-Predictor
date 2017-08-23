import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge,Lasso,ElasticNet,LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.svm import LinearSVR,SVR
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib

class PredictiveModelBuilding(object):
    """

    docstring for PredictiveModelByilding
    this class will handle all pipeline for a preeictive modele building
    in the chapter of my machine learning project ,
    it will train differents modele, encode data,scale data, and so on

    """
    def __init__(self, dataset, encoderFunction):

        if isinstance(dataset, pd.DataFrame):
            self.dataset = dataset
            self.training_set = pd.DataFrame()
            self.test_set = pd.DataFrame()
            self.predictive_models = {}
            self.x_train = pd.DataFrame()
            self.x_test = pd.DataFrame()
            self.y_train = pd.Series()
            self.y_test = pd.Series()
            self.dataset_bin, self.encoders=encoderFunction(dataset, catCol=['SCHOOL_RIGHT', 'OPTION_RIGHT'], numCol=['DIPPERC', 'CGPA', 'EchecRatio'])
            self.dataset_bin.reset_index(inplace=True)
            ridge_reg = Ridge(alpha=1, solver="cholesky", fit_intercept=False)
            linSVM_reg = LinearSVR(dual=False, fit_intercept=False,loss='squared_epsilon_insensitive')
            rbfSVM_reg = SVR(verbose=True)
            lasso_reg = Lasso(alpha=1e-05, max_iter=10000, fit_intercept=False)
            elastic_reg = ElasticNet(alpha=1e-05, max_iter=10000, l1_ratio=0.5)
            self.predictive_models[ridge_reg.__class__.__name__] = ridge_reg
            self.predictive_models[linSVM_reg.__class__.__name__] = linSVM_reg
            self.predictive_models[rbfSVM_reg.__class__.__name__] = rbfSVM_reg
            self.predictive_models[lasso_reg.__class__.__name__] = lasso_reg
            self.predictive_models[elastic_reg.__class__.__name__] = elastic_reg
            self.stacker = LinearRegression(normalize=True)
        else:
            raise TypeError('need only a DataFrame')

    def scale(self, num_cols):

        """
        this function will scale the values of GPA and DIP percentage
        by divide them by 100

        """
        self.dataset_bin.loc[:, num_cols[0]] = self.dataset_bin[num_cols[0]]/100
        self.dataset_bin.loc[:, num_cols[1]] = self.dataset_bin[num_cols[1]]/100

    def split(self):

        """
        the function will split the dataset into a train and a test one"
         and return x_train and x_Test

        """
        split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=4)
        for train_index, test_index in split.split(self.dataset_bin, self.dataset_bin.EchecRatio):
            self.training_set = self.dataset_bin.loc[train_index]
            self.test_set = self.dataset_bin.loc[test_index]
        self.training_set.set_index(keys='ID', inplace=True)
        self.test_set.set_index(keys='ID', inplace=True)
        self.x_train = self.training_set.CGPA
        self.x_train = self.training_set.drop(labels=['CGPA', 'EchecRatio'], axis=1)
        self.y_test = self.test_set.CGPA
        self.x_test = self.test_set.drop(labels=['CGPA', 'EchecRatio'], axis=1)
        train_descrption = self.training_set.describe()[['DIPPERC', 'CGPA']]
        test_description = self.test_set.describe()[['DIPPERC', 'CGPA']]
        return train_descrption, test_description

    def train(self):
        """will train diverents models with x , y pass in parametes"""
        predictions = {}
        for clf in self.predictive_models.values():
            clf.fit(self.x_train, self.y_train)
            predictions[clf.__class__.__name__] = clf.predict(self.x_train)
        predicted_values = pd.DataFrame.from_dict(predictions, dtype=np.float)
        predicted_values.set_index(self.y_train.index, inplace=True)
        predicted_values.loc[:, 'RealValue'] = self.y_train
        return predicted_values

    def predict_test(self):
        """predict values from the test set"""

        predictions = {}
        for clf in self.predictive_models.values():
            predictions[clf.__class__.__name__] = clf.predict(self.x_test)
        predicted_values = pd.DataFrame.from_dict(predictions, dtype=np.float)
        predicted_values.set_index(self.y_test.index, inplace=True)
        predicted_values.loc[:, 'RealValue'] = self.y_test
        return predicted_values

    def predict_new(self, new_student_data):
        """
        this call will handle predictions for new values,
        but frirst it will endcode them nand then try to predict
        start first by handling categorical values

        """

        option_encoder = self.encoders['OPTION_RIGHT']
        school_encoder = self.encoders['SCHOOL_RIGHT']
        options = pd.DataFrame(
        data=dict(zip(option_encoder.classes_, option_encoder.transform(new_student_data[['OPTION_RIGHT']])[0])),
            index=new_student_data.index, columns=option_encoder.classes_)
        schools = pd.DataFrame(data=dict(zip(school_encoder.classes_, school_encoder.transform(new_student_data[['SCHOOL_RIGHT']])[0])),index=new_student_data.index, columns=school_encoder.classes_)
        schools.reset_index(inplace=True)
        options.reset_index(inplace=True)
        new_dataset = pd.merge(options, schools, on='index')
        new_dataset['DIPPERC'] = new_student_data['DIPPERC']
        new_dataset.set_index(keys=['index'], inplace=True)
        predictions = {}
        for clf in self.predictive_models.values():
            predictions[clf.__class__.__name__] = clf.predict(new_dataset)
        predicted_values = pd.DataFrame.from_dict(predictions, dtype=np.float)
        predicted_values.set_index(new_dataset.index, inplace=True)
        predicted_values.loc[:, 'finalOutput'] = self.stacker.predict(predicted_values)
        return predicted_values

    def evaluate(self, model, sur):
        """

        this function will first do a evaluation of a model and return
        the RMSE score of it and some data and their labels the function
        can evaluate on trainset and also on test_set

        """
        if sur == 'train':
            some_data = self.x_train.iloc[:5]
            some_labels = self.y_train.iloc[:5]
            print("Predictions:\t", self.predictive_models[model].predict(some_data))
            print("Labels:\t\t", list(some_labels))
            cgpa_predictions = self.predictive_models[model].predict(self.x_train)
            lin_mse = mean_squared_error(self.y_train, cgpa_predictions)
            lin_rmse = np.sqrt(lin_mse)
            return lin_rmse
        elif sur == 'test':
            some_data = self.x_test.iloc[:5]
            some_labels = self.y_test.iloc[:5]
            print("Predictions:\t", self.predictive_models[model].predict(some_data))
            print("Labels:\t\t", list(some_labels))
            cgpa_predictions = self.predictive_models[model].predict(self.x_test)
            lin_mse = mean_squared_error(self.y_test, cgpa_predictions)
            lin_rmse = np.sqrt(lin_mse)
            return lin_rmse

    def cross_evaluate(self, model):
        """this one will perfom a cross validation of the model"""
        scores = cross_val_score(self.predictive_models[model], self.x_train, self.y_train, scoring="neg_mean_squared_error", cv=10)
        rmse_scores = np.sqrt(-scores)
        return rmse_scores, rmse_scores.std(), rmse_scores.mean()

    def ensembel_methods(self, predicted_values):
        """
        this method will get a dataframe of predicted values by diffrents classifier and will return
        the value compute by  a linear regression between the 3 values and RMSE
        """
        x_new = predicted_values.drop(labels="RealValue", axis=1)
        y_new = predicted_values.RealValue
        self.stacker.fit(x_new, y_new)
        final_predict = self.stacker.predict(predicted_values.drop(labels="RealValue", axis=1))
        predicted_values.loc[:, 'finalPredict'] = final_predict
        rmse_ensemble = np.sqrt(mean_squared_error(predicted_values.RealValue, final_predict))
        return predicted_values, rmse_ensemble

    def save_models(self, departement):
        """after all job we will save the models"""
        name = ''
        for reg in self.predictive_models.values():
            name = departement+reg.__class__.__name__
            joblib.dump(reg, "../predictivesModels/"+name+".pkl")
        joblib.dump(self, "../predictivesModels/Classes/"+departement+".pkl")
