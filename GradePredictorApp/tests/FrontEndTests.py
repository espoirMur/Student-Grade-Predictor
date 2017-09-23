import unittest
import os
import json
from flask import abort, url_for, Flask
import unittest
from config import app_config
import predictiveModelBuilding
from app import create_app




class TestBase(unittest.TestCase):
    """this is the base case for ours tests"""

    def setUp(self):
        """this method will make all initialisation for ours tests"""
        if os.getenv('CIRCLECI'): #if we are in CIRCLECI environement
            self.app = create_app(config_name="CIRCLECI")
        else:
            self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.new_student = {'DIPPERC':0.60, 'SCHOOL_RIGHT':'itfm/bukavu', 'OPTION_RIGHT':'elec indust'}
        self.model_names = ['FM', 'FSTA', 'FD', 'FSDC', 'FSEG', 'FPSE', 'FT']


    def tearDown(self):

        """
        the method will remove all variables
        used for the tests
        """


class TestViews(TestBase):
    """
    this class will handle the testing of our front end page
    and view

    """
    def test_homepage_view(self):
        """
        Test that homepage is accessible without login
        """
        response = self.client().get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome to grade ', str(response.data))


    def test_form_view(self):
        """
        Test if form is accesible
        """
        response = self.client().get('/predictions/predict_form/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Remplisssez et Voyez', str(response.data))


    def test_results_view(self):
        """
        Test that the users can view the predicted results
        """
        response = self.client().post('predictions/predict/', data=json.dumps(self.new_student), content_type='application/json')
        for model in self.model_names:
            self.assertIn(model, str(response.data))


class TestErrorPages(TestBase):
    """this class will test if the user can acess error pages"""
    def test_403_forbidden(self):
        # create route to abort the request with the 403 Error
        @self.app.route('/403')
        def forbidden_error():
            abort(403)

        response = self.client().get('/403')
        self.assertEqual(response.status_code, 403)
        self.assertTrue("403 Error" in response.data)

    def test_404_not_found(self):
        response = self.client().get('/nothinghere')
        self.assertEqual(response.status_code, 404)
        self.assertTrue("404 Error" in response.data)

    def test_500_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/500')
        def internal_server_error():
            abort(500)

        response = self.client().get('/500')
        self.assertEqual(response.status_code, 500)
        self.assertTrue("500 Error" in response.data)

    def test_400_internal_server_error(self):
        # create route to abort the request with the 500 Error
        @self.app.route('/400')
        def internal_server_error():
            abort(400)
        response = self.client().get('/400')
        self.assertEqual(response.status_code, 400)
        self.assertTrue("400 Error" in response.data)
