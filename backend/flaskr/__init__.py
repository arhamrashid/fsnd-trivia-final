import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random
from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.app_context().push()
    setup_db(app)
    # CORS
    CORS(app)
    # After_request decorator to set Access-Control-Allow

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Endpoint to handle GET requests
    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.type).all()

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': {category.id: category.type for category in categories}
        })

    # Pagination

    def paginate_questions(request, data):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in data]
        paginated_questions = questions[start:end]

        return paginated_questions

    # Endpoint to handle GET requests for questions

    @app.route('/questions')
    def get_questions():
        try:
            all_questions = Question.query.order_by(Question.id).all()
            paginated_questions = paginate_questions(request, all_questions)
            categories = Category.query.order_by(Category.type).all()

            if len(paginated_questions) == 0:
                abort(404)

            response = jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(all_questions),
                'categories': {category.id: category.type for category in categories},
                'current_category': None
            })
            return response

        except Exception as e:
            abort(404)

    # Endpoint to DELETE question using a question ID.

    @app.route("/questions/<question_id>", methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.filter(
            Question.id == question_id).one_or_none()
        if question_id is None:
            abort(404)

        try:
            question.delete()
            response = jsonify({
                'success': True,
                'deleted': question_id
            })

            return response
        except Exception as e:
            abort(422)

    # Endpoint to POST a new question,
    @app.route("/questions", methods=['POST'])
    def insert_question():
        body = request.get_json()

        question = body.get('question')
        answer = body.get('answer')
        difficulty = body.get('difficulty')
        category = body.get('category')

        try:
            new_question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category)

            new_question.insert()
            response = jsonify({
                'success': True,
                'created': new_question.id
            })
            return response

        except Exception as e:
            abort(422)

    # Search questions
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search = body.get('searchTerm')

        search_results = Question.query.filter(
            Question.question.ilike(f'%{search}%')).all()
        result_paginated = paginate_questions(request, search_results)

        if (len(result_paginated) == 0):
            abort(404)
        try:
            response = jsonify({
                'success': True,
                'questions': result_paginated,
                'total_questions': len(search_results),
                'current_category': None
            })

            return response
        except Exception as e:
            abort(422)

    # Endpoint to get questions based on category.

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter(
                Question.category == category_id).all()
            paginated_questions = paginate_questions(request, questions)
            return jsonify({
                'success': True,
                'questions': paginated_questions,
                'total_questions': len(questions),
                'current_category': category_id
            })
        except Exception as e:
            abort(404)

    # Play Quiz

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            category = body.get('quiz_category')
            prev_questions = body.get('previous_questions')

            if not category and prev_questions:
                abort(422)

            if category['type'] == 'click':
                available_questions = Question.query.filter(
                    Question.id.notin_((prev_questions))).all()
            else:
                available_questions = Question.query.filter_by(
                    category=category['id']).filter(
                    Question.id.notin_((prev_questions))).all()

            new_question = available_questions[random.randrange(
                0, len(available_questions))].format() if len(available_questions) > 0 else None

            return jsonify({
                'success': True,
                'question': new_question
            })
        except Exception as e:
            abort(422)

    # Error Handlers

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    return app
