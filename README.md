# Trivia App Documentation

## Introduction and getting started
Udacity was intrested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, and this API is built out to handle the backend requests for: 

1. Displaying paginated questions - both all questions and by category.
2. Add or Delete questions.
4. Search for questions based on a text query string.
5. Play the quiz game.

### Installing backend dependancies

To start the backend server, we need to setup a Virtual Environment using virtualenv. After activating Virtual Environment, install the dependencies from 'Requirements.txt' using the following command.

`pip install -r requirements.txt`

After installation of the required dependancies, start the Flask App using following commands.

### For Windows CMD:
`set FLASK_APP=flaskr`<br/>
`set FLASK_ENV=development`<br/>
`flask run`<br/>

The application will be running on [localhost:5000](http://localhost:5000/).

## API Endpoints
`GET /categories`<br/>
example: curl localhost:5000/categories<br/>
It will return the question categories in the following format.
```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  }
}
```

`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: `page` - integer <br/>
Sample:`curl http://localhost:5000/page=1`

- Returns: An object with 10 questions, total questions, object including all categories, and current category 

```json
{
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of Pakistan",
      "answer": "Islamabad",
      "difficulty": 5,
      "category": 2
    }
  ],
  "totalQuestions": 25,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategory": "History"
}
```

`GET '/categories/${id}/questions'`

- Returns questions for a cateogry specified by id request 
- Request Arguments: `id` - integer <br/>
Sample: `curl http://localhost:5000/categories/3/questions`
- Returns: An object with questions for the specified category, total questions, and current category string

```json
{
  "questions": [
    {
      "id": 1,
      "question": "What is the capital of Pakistan",
      "answer": "Islamabad",
      "difficulty": 5,
      "category": 4
    }
  ],
  "totalQuestions": 100,
  "currentCategory": "History"
}
```

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: `id` - integer

Sample:`curl -X DELETE http://localhost:5000/questions/16`

```json
{
  "success": true
}
```
`POST '/quizzes'`

- Sends a post request to get the next question <br/>
Sample: `curl http://localhost:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"type":"Geography","id":"3"}, "previous_questions"}'`
- Request Body:

```json
{
    "previous_questions": [1, 4, 20, 15]
    "quiz_category": "current category"
 }
```
- Returns: a new question object

```json
{
    "question": {
    "id": 1,
    "question": "Question",
    "answer": "Answer",
    "difficulty": 4,
    "category": 2
  }
}
```

`POST '/questions'`

- Sends a post request to add a new question <br/>

Sample: `curl localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Question?", "answer": "Answer","category" :"2", "difficulty":"4"}'`

- Request Body:

```json
{
  "question": "Question?",
  "answer": "Answer",
  "difficulty": 4,
  "category": 2
}
```

- Returns:
```json
{
    "created": 39,
    "success": true
}
```
`POST '/questions'`

- Send a post request to search for questions based on search term <br/>
Sample: `curl http://localhost:5000/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"capital"}'`
- Request Body:

```json
{
  "searchTerm": "The search term"
}
```

- Returns: JSON response with a list of questions matching search term, total questions, and category. 

```json
{
  "questions": [
    {
      "id": 1,
      "question": "Question?",
      "answer": "Answer",
      "difficulty": 4,
      "category": 4
    }
  ],
  "totalQuestions": 26,
  "currentCategory": "Entertainment"
}
```

## Error Handling
API returns the errors in JSON objects in the following format:

```json
{
  "success": false,
  "error"  : 400,
  "message" : "bad request"
}
```

 ## The API will return following three errors when a request fail:
    400: Bad Request
    404: Not Found
    422: Not Processable


