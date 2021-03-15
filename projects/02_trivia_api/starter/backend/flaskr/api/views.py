import random

from flask import jsonify, request, abort, current_app

from flaskr.api import api
from flaskr.models import Question, Category, db_session


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
    }), 200


def validate_required_fields(required_fields):
    errors = []
    for field, val in required_fields.items():
        if val is None:
            errors.append({field: 'Field is required'})

    if errors:
        abort(400, errors)


@api.route('/questions', methods=['POST'])
def create_question():
    data = request.get_json()

    fields = {
        'question': data.get('question') or None,  # Force none if empty string
        'answer': data.get('answer') or None,  # Force none if empty string
        'difficulty': data.get('difficulty', None),
        'category': data.get('category', None),
    }

    # Check required fields are populated
    validate_required_fields(fields)

    # Validate specific fields
    errors = []
    if fields['difficulty'] <= 0 or fields['difficulty'] > 5:
        errors.append({'difficulty': 'Difficulty must be an integer between 1 and 5'})

    category = Category.query.get(int(fields['category']))
    if not category:
        errors.append({'category': 'Category is not supported'})

    if errors:
        abort(400, errors)

    # Create the question
    try:
        with db_session():
            question = Question(**fields)
            question.insert()
            return jsonify(question.format())
            # TODO: Test side effect return 422
    except:
        abort(422)


@api.route('/categories')
def categories():
    categories = Category.query.order_by(Category.type)

    return jsonify({
        'categories': {category.id: category.type for category in categories.all()}
    }), 200


@api.route('/categories/<int:cat_id>/questions')
def category_questions(cat_id):
    category = Category.query.filter_by(id=cat_id)\
        .first_or_404('Category matching the provided ID was not found')

    questions = Question.query
    category_questions = questions.filter(Question.category == cat_id)
    pag_questions = paginate_query(request, category_questions)

    return jsonify({
        'questions': [question.format() for question in pag_questions],
        'total_questions': category_questions.count(),  # TODO: Test count
        'current_category': category.id,
    }), 200


@api.route('/questions/<int:question_id>', methods=['DELETE'])
def delete_question(question_id):
    question = Question.query.filter_by(id=question_id)\
        .first_or_404('Question matching the provided ID was not found for delete')
    try:
        with db_session():
            question.delete()
    except:
        abort(500)

    return jsonify({}), 204


@api.route('/questions/search', methods=['POST'])
def search_questions():
    data = request.get_json()
    search_term = data.get('searchTerm', '')
    category_id = data.get('categoryId', None)

    questions_categories = Question.query.join(Category, Question.category == Category.id)

    if category_id:
        questions_categories = questions_categories.filter(Question.category == category_id)

    search = questions_categories.filter(
        Question.question.ilike(f'%{search_term}%') |  # question contains
        Question.answer.ilike(f'%{search_term}%') |  # answer contains
        Category.type.ilike(f'%{search_term}%')  # category contains
    )

    pag_search = paginate_query(request, search)

    return jsonify({
        'questions': [question.format() for question in pag_search],
        'total_questions': search.count(),  # TODO: Test count
    }), 200


@api.route('/quizzes', methods=['POST'])
def quiz_question():
    data = request.get_json()
    category_id = data.get('quiz_category')
    exclude_questions = data.get('previous_questions', [])

    # Filter by remaining questions and category
    questions = Question.query.filter(Question.id.notin_(exclude_questions))
    if category_id:
        questions = questions.filter_by(category=category_id)

    # Randomize
    total_questions = questions.count()
    rand_offset = random.randint(0, total_questions - 1) if total_questions else 0

    # Fetch question
    question = questions.offset(rand_offset).first()

    return jsonify({
        'question': question.format() if question else None
    }), 200


