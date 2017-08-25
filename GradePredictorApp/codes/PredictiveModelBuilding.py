import pandas as pd
import numpy as np
from sklearn.linear_model import Ridge,Lasso,ElasticNet,LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.svm import LinearSVR,SVR
from sklearn.metrics import mean_squared_error
from sklearn.externals import joblib
from sklearn.preprocessing import LabelBinarizer

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
            self.dataset_bin, self.encoders = encoderFunction(dataset, cat_col=['SCHOOL_RIGHT', 'OPTION_RIGHT'], num_col=['DIPPERC', 'CGPA', 'EchecRatio'])
            self.dataset_bin.reset_index(inplace=True)
            ridge_reg = Ridge(alpha=1, solver="cholesky", fit_intercept=False, max_iter=20000)
            linSVM_reg = LinearSVR(dual=False, fit_intercept=False,loss='squared_epsilon_insensitive', max_iter=20000)
            rbfSVM_reg = SVR(verbose=True, max_iter=20000)
            lasso_reg = Lasso(alpha=1e-05, max_iter=20000, fit_intercept=False)
            elastic_reg = ElasticNet(alpha=1e-05, max_iter=20000, l1_ratio=0.5)
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
        self.y_train = self.training_set.CGPA
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
        schools = pd.DataFrame(data=dict(zip(school_encoder.classes_, school_encoder.transform(new_student_data[['SCHOOL_RIGHT']])[0])), index=new_student_data.index, columns=school_encoder.classes_)
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
        return predicted_values['finalOutput']

    def evaluate(self, model, sur):
        """

        this function will first do a evaluation of a model and return
        the rmse score of it and some data and their labels the function
        can evaluate on trainset and also on test_set

        """
        if sur == 'train':
            some_data = self.x_train.iloc[:5]
            some_labels = self.y_train.iloc[:5]
            print ("Predictions:\t", self.predictive_models[model].predict(some_data))
            print ("Labels:\t\t", list(some_labels))
            cgpa_predictions = self.predictive_models[model].predict(self.x_train)
            lin_mse = mean_squared_error(self.y_train, cgpa_predictions)
            lin_rmse = np.sqrt(lin_mse)
            return lin_rmse
        elif sur == 'test':
            some_data = self.x_test.iloc[:5]
            some_labels = self.y_test.iloc[:5]
            print ("Predictions:\t", self.predictive_models[model].predict(some_data))
            print ("Labels:\t\t", list(some_labels))
            cgpa_predictions = self.predictive_models[model].predict(self.x_test)
            lin_mse = mean_squared_error(self.y_test, cgpa_predictions)
            lin_rmse = np.sqrt(lin_mse)
            return lin_rmse

    def cross_evaluate(self, model):
        """this one will perfom a cross validation of the model"""
        scores = cross_val_score(self.predictive_models[model], self.x_train, self.y_train, scoring="neg_mean_squared_error", cv=10)
        rmse_scores = np.sqrt(-scores)
        return rmse_scores, rmse_scores.std(), rmse_scores.mean()

    def ensemble_methods(self, predicted_values):
        """
        this method will get a dataframe of predicted values by diffrents classifier and will return
        the value compute by  a linear regression between the 3 values and rmse
        """
        labels = ['ElasticNet', 'Lasso', 'LinearSVR', 'Ridge', 'SVR']
        x_new = predicted_values[labels]
        y_new = predicted_values.RealValue
        self.stacker.fit(x_new, y_new)
        final_predict = self.stacker.predict(x_new)
        predicted_values.loc[:, 'finalPredict'] = final_predict
        rmse_ensemble = np.sqrt(mean_squared_error(y_new, final_predict))
        return predicted_values, rmse_ensemble

    def save_models(self, departement):
        """

        after all job we will save the class with the models for
        deployement

        """
        joblib.dump(self, "../predictivesModels/Classes/"+departement+".pkl")


def convert_cat(dataset, cat_col, num_col):
    """

    this function will binarize a dataset given in parametrer and
    return the dataset with categorical columns binarise by one-hot
    encoding

    """
    encs = {}
    x_train_1 = dataset[cat_col]
    x_new = dataset[num_col]
    cat_col = x_train_1.columns
    for col in cat_col:
        data = dataset[[col]]
        enc = LabelBinarizer()
        enc.fit(data)
        # Fitting One Hot Encoding on train data
        temp = enc.transform(dataset[[col]])
        # Changing the encoded features into a data frame with new column names
        temp = pd.DataFrame(temp, columns=enc.classes_)
        # In side by side concatenation index values should be same
        # Setting the index values similar to the X_train data frame
        temp = temp.set_index(dataset.index)
        # adding the new One Hot Encoded varibales to the train data frame

        x_new = pd.merge(temp, x_new, right_index=True, left_index=True)
        #saving the encoder into a dict for others operations
        encs[col] = enc
    return x_new, encs


def final_job(dataframe):
    """"

    this method will handle all the task related to training models in
    each departement and in final they will return a dataset with
    all types of erros .
    """

    #first we iterate over the whole dataset to get each departement

    departement_names = ['droit', 'medecine', 'psycologie', 'sante', 'economie','technologie', 'theologie']
    results = {}
    predicted_resuts = {}
    for departement, datas in dataframe.groupby('FAC'):
        results[departement] = []
        predictive_model = PredictiveModelBuilding(dataset=datas, encoderFunction=convert_cat)
        predictive_model.scale(['DIPPERC', 'CGPA'])
        train_des, test_des = predictive_model.split()
        results[departement].append(predictive_model.dataset_bin.shape)
        print train_des
        print test_des
        predicted_values = predictive_model.train() #trainig the models
        rmse = {}
        for name, model in predictive_model.predictive_models.items():
            cgpa_mean = predictive_model.dataset_bin.CGPA.mean()
            rmse_train = predictive_model.evaluate(model=name, sur='train') #rmse of each model
            rmse[name] = [rmse_train, rmse_train*100/cgpa_mean]
            scores, score_std, score_mean = predictive_model.cross_evaluate(model=name)
            cv_score = [score_mean, score_mean*100/cgpa_mean, score_std]
            rmse[name].append(cv_score)
            print (model, scores)
            rmse_test = predictive_model.evaluate(model=name, sur='test') #rmse of each model
            rmse[name].append([rmse_test, rmse_test*100/cgpa_mean])
        final_predict, final_rmse = predictive_model.ensemble_methods(predicted_values)
        print final_predict.head(5)
        new_student = {'DIPPERC':0.60, 'SCHOOL_RIGHT':'itfm/bukavu', 'OPTION_RIGHT':'elec indust'}
        new_student_data = pd.DataFrame(new_student, columns=new_student.keys(), index=range(1))
        predicted_resuts[departement] = predictive_model.predict_new(new_student_data)
        results[departement].append(rmse)
        results[departement].append([final_rmse, final_rmse*100/cgpa_mean])
        predictive_model.save_models(departement)
    return results, predicted_resuts


def build_final_dataset(results):
    """

    this methods will help us to build the final dataset for our report

    """
    results_tab = pd.DataFrame(columns=[0, 1, 2, 3, 'CVSCORE Mean', u'CVSCORE Std', u'RMSE Train', u'RMSE Test'], index=range(0, 7))
    results_tab_2 = pd.DataFrame(
        columns=['STACK_RES', 'Dimensions', 'Faculte'],
        index=range(0, 35))
    results_tab_2.reset_index(inplace=True)
    results_tab.reset_index(inplace=True)
    final_dataframes = []
    next_index = 2 #index where we want to put the values in tab_2
    for name , val in results.items():
        results_data = pd.DataFrame.from_dict(val[1], orient='index')
        cv_score_mean = []
        cv_score_std = []
        for ind in results_data[2].index:
            cv_mean = (str("%.3f" % results_data[2][ind][0])) + "  : " + str("%.2f" % results_data[2][ind][1]) + '%'
            cv_score_std.append("%.4f" % results_data[2][ind][2])
            cv_score_mean.append(cv_mean)

        results_data['CVSCORE Mean'] = cv_score_mean
        results_data['CVSCORE Std'] = cv_score_std
        rmse_score_mean = []

        for ind in results_data[[0, 1]].index:
            rmse_mean = (str("%.2f" % results_data [0][ind])) + " : " + str("%.2f" % results_data [1][ind]) + '%'
            rmse_score_mean.append(rmse_mean)
        results_data['RMSE Train'] = rmse_score_mean
        rmse_score_mean_test = []

        for ind in results_data[3].index:
            rmse_mean = (str("%.2f" % results_data [3][ind][0])) + " : " + str("%.3f" % results_data [3][ind][1]) + '%'
            rmse_score_mean_test.append(rmse_mean)
        results_data['RMSE Test'] = rmse_score_mean_test
        final_score = (str("%.3f" % results.get(name)[2][0])) + " : " + str("%.3f" % results.get(name)[2][1]) + '%'

        results_tab_2.STACK_RES[next_index] = final_score
        results_tab_2.Dimensions[next_index] = str(results.get(name)[0])
        results_tab_2.Faculte[next_index] = name
        final_dataframes.append(results_data[[u'CVSCORE Mean', u'CVSCORE Std', u'RMSE Train', u'RMSE Test']])
        next_index += 5
    results_data = pd.concat(final_dataframes)
    results_data.reset_index(inplace=True)
    results_data.rename(columns={'index':'MODEL'}, inplace=True)
    results_data.reset_index(inplace=True)
    final = pd.merge(results_tab_2, results_data, on='index')
    return final
