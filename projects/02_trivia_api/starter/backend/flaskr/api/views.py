from flask import jsonify, request, abort, current_app

from flaskr.api import api
from flaskr.models import Question, Category


@api.route('/')
def api_index():
    return jsonify({
        'success': True,
        'endpoints': []
    })


def paginate_query(req, query):
    """Paginate a SQLAlcehmy query"""
    page = req.args.get('page', 1, type=int)
    return query.paginate(page, current_app.config['POSTS_PER_PAGE']).items


@api.route('/questions')
def questions():
    questions = Question.query
    pag_query = questions.order_by(Question.id)
    pag_questions = paginate_query(request, pag_query)
    categories = Category.query.order_by(Category.type)

    return jsonify({
        'questions': [question.format() for question in pag_questions],
        'total_questions': questions.count(),
        'categories': {category.id: category.type for category in categories.all()},
    })


@api.route('/categories/<int:cat_id>/questions')
def questions_by_category(cat_id):
    category = Category.query.filter_by(id=cat_id).first_or_404()

    questions = Question.query
    # Join on (db unenforced) Foreign Key relation
    category_questions = questions.join(Category, Question.category==Category.id).filter(Question.category == cat_id)
    pag_questions = paginate_query(request, category_questions)

    return jsonify({
        'questions': [question.format() for question in pag_questions],
        'total_questions': category_questions.count(),  # TODO: Test count
        'current_category': category.id,
    })
