# Full Stack Trivia API Backend
This project is is an API backend interface for retrieving and creating categorized trivia questions. 
As part of the Udacity Fullstack Nanodegree, the API constitutes the backend component of a Trivia web app project. 
This API allows users to view existing questions and categories supported in the database, 
create new questions within those categories in the database,
and retrieve randomized and categorized questions, with the capability to exclude questions which have already been 
returned.

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/).

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < data/trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

Note: Configurable environment variables may be stored in a `.env` file in the root directory. 
An example file has been included, and you may replace the variables and/or values as you see fit.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 


## Api Reference

### Getting started

- API Base URL: `http://localhost:5000/api`. At present this project can only be run locally. 
Once the local server is running you can visit this URL which will provide a list of the available endpoints and their methods.

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "error": "404: Not Found",
    "description": "The specified resource could not be located"
}
```
The API will return four error types when requests fail:
- 400: Bad Request
- 404: Not Found
- 422: Unprocessable Entity
- 500: Server Error



### Endpoints

##### GET /categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
- Sample: `curl http://localhost:5000/api/categories`
```
{
    '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports"
}
```

##### GET /categories/{category_id}/questions
- Fetches all questions which belong to a specified category
- Request Arguments: category_id - Category ID
- Returns: An object with a paginated list questions and related data for this category
    - Questions are paginated by 10 items (configurable)
- Sample: `curl http://localhost:5000/api/categories/6/questions?page=1`
```
{
  "current_category": 6,
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "total_questions": 2
}
```

##### GET /questions
- Fetches a list of all questions in the database
- Request Arguments: None
- Returns: An object containing a paginated list of all questions. 
Also includes a dictionary of all categories, and total number of avaliable questions.
    - Questions are paginated by 10 items (configurable)
- Sample: `curl http://localhost:5000/question?page=1`
```
{
    "categories" : {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    },
    "questions": {
        {
          "answer": "Apollo 13",
          "category": 5,
          "difficulty": 4,
          "id": 2,
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
          "answer": "Tom Cruise",
          "category": 5,
          "difficulty": 4,
          "id": 4,
          "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
          "answer": "Maya Angelou",
          "category": 4,
          "difficulty": 2,
          "id": 5,
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
            ... 7 more
    },
    "total_questions": 19  
}
```

##### POST /questions
- Create a question which belongs to a specified category
- Request Arguments: None
- Returns: A serialized object of the created question (HTTP_201)
- Params:
    - difficulty: integer between 1 - 5
- Sample: `curl localhost:5000/api/questions 
            -X POST 
            -H "Content-Type: application/json" 
            -d '{"question": "How are you?", "answer": "Fine", "category": 1, "difficulty": 5}'`
```
{
  "answer": "Fine",
  "category": 1,
  "difficulty": 5,
  "id": 24,
  "question": "How are you?"
}
```

#### DELETE /questions/{question_id}
- Deletes a question from the database
- Request Arguments: question_id - Question ID
- Returns: An empty object (HTTP_204)
- Sample: `curl -X DELETE http://localhost:5000/api/questions/20`
```
```

#### POST /questions/search?page=1
- Search for a question containing a search term
- Request Arguments: None
- Params:
    - searchTerm:    
        - similar to question
        - similar to answer
        - all of the above for a specified category
        - similar to a category name
    - categoryId [optional]: Category ID to search within only the specified category
- Returns: An object containing a list of paginated questions and the total number of questions returned for the search
- Sample: `curl localhost:5000/api/questions/search 
            -X POST 
            -H "Content-Type: application/json" 
            -d '{"searchTerm":"Blood", "categoryId": "1"}'`
```
{
  "questions": [
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "total_questions": 1
}
```

#### POST /quizzes
- Retrieves a random question based on a selected category, allowing for the exclusion of previously seen questions
- Request Arguments: None
- Params:
    - quiz_category: Category ID (0 or empty for ALL categories)
    - previous_questions: List of previously seen question IDs (to exclude from random selection)
- Returns: An object containing a question object
- Sample: `curl localhost:5000/api/quizzes 
            -X POST 
            -H "Content-Type: application/json" 
            -d '{"quiz_category": 1, "previous_questions": [22]}'`
```
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  }
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
pytest tests/
```
