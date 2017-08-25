
import os
import sys
sys.path.insert(0,"codes/")
import json
import unittest
from predictiveModelBuilding import PredictiveModelBuilding
from app import create_app
from testfixtures import TempDirectory
from sklearn.externals import joblib



class GradePredictorTestCase(unittest.TestCase):
    """

    this class represent all the test cases we will use to test
    our API

    """

    def setUp(self):
        """this method will make all initialisation for ours tests"""

        if os.getenv('CIRCLECI'): #if we are in CIRCLECI environement
            self.app = create_app(config_name="CIRCLECI")
        else:
            self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.directory = TempDirectory(
            path='../predictivesModels/',
            create=False)        #initialisation of temporary directory
        self.predictives_models = []

    def test_model_exist(self):
        """

        the following testcase will vertify if predictives models
        exist in the floder classes

        """
        self.directory.compare(sorted([
            'medecine.pkl',
            'technologie.pkl',
            'droit.pkl',
            'sante.pkl',
            'economie.pkl',
            'psycologie.pkl',
            'theologie.pkl'
            ], reverse=True), path='Classes/')


    def test_step_one(self):
        """

        test that the app can read the model from saved floders
        here we will try to read all the modeles
        and check if there are instances of preictives models class

        """
        path = '../predictivesModels/Classes/'
        for filename in os.listdir(path):
            print '-------------before load--------------'
            model = joblib.load(path+filename)
            self.predictives_models.append(model)
            print '-------------after load--------------'
            self.assertIsInstance(model, PredictiveModelBuilding)

    def step_two(self):
        """

        this method will test if the app can predict good values
        of students grades by goods values I mean grades betweens 30-100
        percents .

        """
        #check if the model can handle unknow schools
        new_student_data = {'DIPPERC':0.60, 'SCHOOL_RIGHT':'itfm/bukavu', 'OPTION_RIGHT':'elec indust', 'CGPA':0}
        for dept in self.predictives_models:
            predicted_grades = dept.predict_new(new_student_data)
            final_grade = predicted_grades['finalOutput']
            self.assertTrue(final_grade in range(30, 100))

    def _steps(self):
        for name in sorted(dir(self)): #attributes of a object
            if name.startswith("step"):
                yield name, getattr(self, name)

    def test_steps(self):
        """for now I don't know who this works"""
        for name, step in self._steps():
            try:
                step()
            except Exception as exception:
                self.fail("{} {} failed ({}: {})".format(step, name, type(exception), exception))

    def tearDown(self):
        """the method will remove all variables used for the tests"""
        pass

if __name__ == "__main__":
    unittest.main()
