# GPT Adviser

## Overview

GPT Adviser is a Flask-based web application that leverages OpenAI's GPT-4 API to provide intelligent responses based on user input. The application allows users to interact with GPT-4 via a simple web interface and view the generated responses. It also includes Swagger documentation for easy API exploration.

## Features

Interactive Web Interface: Users can input messages and receive responses from GPT-4.
Streaming Responses: Real-time streaming of responses from the GPT-4 API.
Swagger Documentation: Automatically generated API documentation using Flasgger for easy exploration of the available endpoints.
* Prerequisites
* Python 3.7 or higher
* OpenAI API key

## Prerequisites

* Python 3.7 or higher
* OpenAI API key

## Installation

1. Clone the Repository
```python
git clone https://github.com/AlinaGay/gpt_adviser.git
cd gpt_adviser
```
2. Create and Activate a Virtual Environment
```python
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```
3. Install Dependencies
```python
pip install -r requirements.txt
```
4. Set Up Environment Variables

Create a .env file in the root directory of the project and add your OpenAI API key:
```python
OPENAI_API_KEY=your_openai_api_key
```
Ensure you replace your_openai_api_key with your actual OpenAI API key.

## Running the Application

1. Run the Flask Application
```python
python run.py
```
2. Access the Application

Open your web browser and navigate to:

* Web Interface: `http://localhost:5000/`
* Swagger Documentation: `http://localhost:5000/apidocs`

## API Endpoints
## POST /api/answer

Description: Sends a message to the GPT-4 API and streams the response.

Request Body:
```python
{
  "message": "Your message here"
}
```
Responses:

* 200 OK: Returns a streamed response from the GPT-4 API.
* 400 Bad Request: If the input data is invalid.

Example Request:
```python
curl -X POST http://localhost:5000/api/answer \
-H "Content-Type: application/json" \
-d '{"message": "Hello, how are you?"}'
```

##  Testing

To run tests, you should add a test suite to your project. You can use libraries like pytest for this purpose.
```python
pip install pytest
python -m unittest test_app.py
```
