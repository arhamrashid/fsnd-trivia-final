import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from flaskr import create_app
from models import Question, Category

# Getting values from .env file
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
database_name = os.getenv('TEST_DB_NAME')


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

    def setup_db(app):
        db = SQLAlchemy()
        database_path = 'postgresql://{}:{}@{}:{}/{}'.format(
            user, password, 'localhost', 5432, database_name)
        app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        db.app = app
        db.init_app(app)
        db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO: Done
    Write at least one test for each test for successful operation
    and for expected errors.
    """
    # Get paginated list of questions

    def test_get_paginated_questions(self):
        result = self.client().get('/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        #
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['questions'])

    # Getting a page which does not exists
    def test_404_out_of_range_questions(self):
        result = self.client().get('/questions?page=100')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_search_question(self):
        search_term = {'searchTerm': 'who'}

        result = self.client().post('/questions/search', json=search_term)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_question_not_found(self):
        search_term = {'searchTerm': 'some-random-string-balabla-dkfjdkj'}

        result = self.client().post('/questions/search', json=search_term)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'not found')

    def test_add_question(self):
        question = {
            'question': 'A new question?',
            'answer': 'Answer',
            'difficulty': 3,
            'category': 2
        }

        result = self.client().post('/questions', json=question)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_get_categories(self):
        result = self.client().get('/categories')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(result.status_code, 200)
        self.assertTrue(len(data['categories']))

    def test_404_category_not_found(self):
        result = self.client().get('/categories/100')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_deleting_question(self):
        question_json = {
            'question': 'A test question?',
            'answer': 'Answer',
            'difficulty': 2,
            'category': 2
        }
        question = Question(question='test question?',
                            answer='Answer', difficulty=2, category=2)

        question.insert()
        question_id = question.id

        result = self.client().delete(f'/questions/{question_id}')
        data = json.loads(result.data)

        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNone(question)
        self.assertEqual(data['deleted'], str(question_id))

    def test_422_sent_deleting_non_existing_question(self):
        result = self.client().delete('/questions/1000')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_get_questions_of_selected_category(self):
        result = self.client().get('/categories/1/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    def test_404_get_questions_of_selected_category(self):
        result = self.client().get('/categories/a/questions')
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], "not found")

    def test_play_quiz(self):
        quiz_data = {'previous_questions': [],
                     'quiz_category': {'type': 'Entertainment', 'id': 5}}

        result = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertIsNotNone(data['question'])

    def test_404_play_quiz(self):
        quiz_data = {'previous_questions': []}
        result = self.client().post('/quizzes', json=quiz_data)
        data = json.loads(result.data)

        self.assertEqual(result.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
