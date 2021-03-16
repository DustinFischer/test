import json
from unittest.mock import patch

from flaskr.models import Category, Question, db
from .base import BaseTestClass


class TriviaApiTestCase(BaseTestClass):

    def setUp(self):
        super().setUp()

        # Add some categories
        self.science = Category('Science')
        self.geography = Category('Geography')
        db.session.add(self.science)
        db.session.add(self.geography)
        db.session.commit()

        # Add some questions
        self.science_question = Question('What is science?', 'Nobody knows', self.science.id, 5)
        self.geog_question = Question('Is geography real?', 'Probably not', self.geography.id, 5)
        self.science_question.insert()
        self.geog_question.insert()

    def test_question_list(self):
        """Test that hitting the question list GET endpoint returns a list of question(s), as well as categories"""
        third_question = Question('Why is science?', 'Only Bill Nye knows', self.science.id, 5)
        third_question.insert()

        # Test list with pagination only returns 2 result
        resp = self.client.get('/api/questions')
        assert resp.status_code == 200

        data = json.loads(resp.data)
        assert 'categories' in data
        assert 'questions' in data
        assert 'total_questions' in data

        assert data == {
            'categories': {
                '1': 'Science',
                '2': 'Geography'
            },
            'questions': [
                {
                    'answer': 'Nobody knows',
                    'category': 1,
                    'difficulty': 5,
                    'id': 1,
                    'question': 'What is science?'
                },
                {
                    'answer': 'Probably not',
                    'category': 2,
                    'difficulty': 5,
                    'id': 2, 'question':
                    'Is geography real?'
                }
            ],
            'total_questions': 3
        }

    def test_question_by_category_404(self):
        """Test that a 404 is returned when a category id is not found"""
        resp = self.client.get(f'/api/categories/5000/questions')
        assert resp.status_code == 404

        assert json.loads(resp.data) == {
            'error': '404: Not Found',
            'message': 'Category matching the provided ID was not found'
        }

    def test_question_by_category(self):
        """
        Test that only questions for a given category will be returned when hitting the GET category questions endpoint.
        """
        assert Category.query.count() == 2
        cat = self.science
        resp = self.client.get(f'/api/categories/{cat.id}/questions')
        assert resp.status_code == 200

        data = json.loads(resp.data)

        assert 'current_category' in data
        assert data['current_category'] == cat.id

        assert 'questions' in data
        assert data['questions'][0]['category'] == cat.id

        # Check response shape
        assert data == {
            'current_category': 1,
            'questions': [
                {
                    'answer': 'Nobody knows',
                    'category': 1,
                    'difficulty': 5,
                    'id': 1,
                    'question': 'What is science?'
                }
            ],
            'total_questions': 1
        }

    def test_category_list(self):
        """Test that hitting the categories list GET endpoint returns a dictionary of supported categories"""
        resp = self.client.get('/api/categories')
        assert resp.status_code == 200

        data = json.loads(resp.data)
        assert data == {
            'categories': {
                '1': 'Science',
                '2': 'Geography'
            }
        }

    def test_create_question_fields(self):
        """Test field validations on question create POST endpoint"""
        url = '/api/questions'

        # Test missing fields
        data = {}
        resp = self.client.post(url, json=data)
        assert resp.status_code == 400
        assert json.loads(resp.data) == {
            'error': '400: Bad Request',
            'message': [
                {'question': 'Field is required'},
                {'answer': 'Field is required'},
                {'difficulty': 'Field is required'},
                {'category': 'Field is required'}
            ]
        }

        data = {
            'question': 'Why is science?',
            'answer': 'Only Bill Nye knows',
            'category': 5000,
            'difficulty': 0
        }

        # Test difficulty and cateory validation
        resp = self.client.post(url, json=data)
        assert resp.status_code == 400
        assert json.loads(resp.data) == {
            'error': '400: Bad Request',
            'message': [
                {'difficulty': 'Difficulty must be an integer between 1 and 5'},
                {'category': 'Category is not supported'}
            ]
        }

    @patch('flaskr.api.views.Question.insert')
    def test_create_question_422(self, mock_insert):
        """Test that a 422 error is returned when there is an error raised while processing question creation"""
        # Force raise an exeception while creating question in DB
        mock_insert.side_effect = Exception

        assert Question.query.count() == 2

        data = {
            'question': 'Why is science?',
            'answer': 'Only Bill Nye knows',
            'category': self.science.id,
            'difficulty': 3
        }

        resp = self.client.post('/api/questions', json=data)
        assert resp.status_code == 422
        assert json.loads(resp.data) == {
            'error': '422: Unprocessable Entity',
            'message': 'The request was well-formed but was unable to be followed due to semantic errors.'
        }

        # Ensure changes dont persist
        assert Question.query.count() == 2

    def test_create(self):
        """Test successful creation of a question"""
        assert Question.query.count() == 2

        data = {
            'question': 'Why is science?',
            'answer': 'Only Bill Nye knows',
            'category': self.science.id,
            'difficulty': 3
        }
        resp = self.client.post('/api/questions', json=data)
        assert resp.status_code == 200
        resp_data = json.loads(resp.data)
        assert resp_data == {
            'answer': 'Only Bill Nye knows',
            'category': 1,
            'difficulty': 3,
            'id': 3,
            'question': 'Why is science?'
        }

        # Ensure changes persist in DB
        assert Question.query.count() == 3
        question = Question.query.get(resp_data['id'])
        assert question is not None
        assert question.format() == resp_data

    def test_delete_question_404(self):
        """Test the trying to delete a non-existent question id returns a 404"""
        resp = self.client.delete('/api/questions/5000')
        assert resp.status_code == 404
        assert json.loads(resp.data) == {
            'error': '404: Not Found',
            'message': 'Question matching the provided ID was not found for delete'
        }

    @patch('flaskr.api.views.Question.delete')
    def test_delete_question_500(self, mock_delete):
        """Test that a 500 error is returned when there is an error raised while processing question deletion"""
        # Force raise an exeception while deleting question in DB
        mock_delete.side_effect = Exception

        assert Question.query.count() == 2

        resp = self.client.delete(f'/api/questions/{self.geog_question.id}')
        assert resp.status_code == 500
        assert json.loads(resp.data) == {
            'error': '500: Internal Server Error',
            'message': 'The server encountered an internal error and was unable to complete your request. '
                       'Either the server is overloaded or there is an error in the application.'
        }

        # Ensure delete does not persist in DB
        assert Question.query.count() == 2

    def test_delete_question(self):
        """Test question deletion response and persists in the database"""
        assert Question.query.count() == 2

        resp = self.client.delete(f'/api/questions/{self.geog_question.id}')
        assert resp.status_code == 204

        # Ensure changes persist in DB
        assert Question.query.count() == 1
        assert Question.query.get(self.geog_question.id) is None

    def test_search(self):
        """
        Test that question search can search by:
            - partial category match
            - partial question match
            - partial answer match
            - Specify a category search under
        """
        url = '/api/questions/search'

        search = {
            'searchTerm': 'sci'
        }

        # test category contains
        resp = self.client.post(url, json=search)
        assert resp.status_code == 200
        assert json.loads(resp.data) == {
            'questions': [
                {'answer': 'Nobody knows', 'category': 1, 'difficulty': 5, 'id': 1, 'question': 'What is science?'}
            ],
            'total_questions': 1
        }

        # Test question contains
        search['searchTerm'] = 'what is'
        resp = self.client.post(url, json=search)
        assert resp.status_code == 200
        assert json.loads(resp.data) == {
            'questions': [
                {'answer': 'Nobody knows', 'category': 1, 'difficulty': 5, 'id': 1, 'question': 'What is science?'}
            ],
            'total_questions': 1
        }

        # Test answer contains
        search['searchTerm'] = 'nobody'
        resp = self.client.post(url, json=search)
        assert resp.status_code == 200

        assert json.loads(resp.data) == {
            'questions': [
                {'answer': 'Nobody knows', 'category': 1, 'difficulty': 5, 'id': 1, 'question': 'What is science?'}
            ],
            'total_questions': 1
        }

        # test within category
        new_question = Question('Why is science?', 'Only Bill Nye knows', self.science.id, 5)
        new_question.insert()
        search['categoryId'] = self.science.id
        search['searchTerm'] = 'knows'

        resp = self.client.post(url, json=search)
        assert resp.status_code == 200
        assert json.loads(resp.data) == {
            'questions': [
                {'answer': 'Nobody knows', 'category': 1, 'difficulty': 5, 'id': 1, 'question': 'What is science?'},
                {'answer': 'Only Bill Nye knows', 'category': 1, 'difficulty': 5, 'id': 3, 'question': 'Why is science?'}
            ],
            'total_questions': 2
        }

    def test_quiz_question_categorized(self):
        """Test get random quiz question from specific category"""
        url = '/api/quizzes'
        previous_questions = []

        data = {
            'previous_questions': previous_questions,
            'quiz_category': self.science.id
        }

        # There is only 1 possible question in the science category
        resp = self.client.post(url, json=data)
        assert resp.status_code == 200
        resp_data = json.loads(resp.data)

        assert resp_data == {
            'question': {
                'answer': 'Nobody knows',
                'category': 1,
                'difficulty': 5,
                'id': 1,
                'question': 'What is science?'
            }
        }

        # Get depleted  questions
        previous_questions.append(resp_data['question']['id'])
        data['previous_questions'] = previous_questions

        resp = self.client.post(url, json=data)
        assert resp.status_code == 200

        resp_data = json.loads(resp.data)
        assert resp_data['question'] is None

    def test_quiz_question_uncategorized(self):
        """Test get random quiz question from any category"""
        url = '/api/quizzes'
        previous_questions = []
        data = {'previous_questions': previous_questions}

        resp = self.client.post(url, json=data)
        assert resp.status_code == 200
        resp_data = json.loads(resp.data)

        # Check response for question that was returned
        assert 'question' in resp_data
        assert 'id' in resp_data['question']
        question1 = Question.query.get(resp_data['question']['id'])
        assert question1 is not None
        assert resp_data['question'] == question1.format()

        # Get next question
        previous_questions.append(question1.id)
        data['previous_questions'] = previous_questions

        resp = self.client.post(url, json=data)
        assert resp.status_code == 200

        resp_data = json.loads(resp.data)
        question2 = Question.query.get(resp_data['question']['id'])
        assert question2 is not None
        assert question2.id not in previous_questions

        # Get depleted questions
        previous_questions.append(question2.id)
        data['previous_questions'] = previous_questions

        resp = self.client.post(url, json=data)
        assert resp.status_code == 200

        resp_data = json.loads(resp.data)
        assert resp_data['question'] is None
