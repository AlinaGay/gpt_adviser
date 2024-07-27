from flask import Flask, jsonify, render_template, request
from flasgger import Swagger
from openai import OpenAI
import logging

client = OpenAI()

def create_app():
    app = Flask(__name__)

    swagger = Swagger(app)

    logging.basicConfig(
        filename='app.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/answer", methods=["POST"])
    def answer():
        """
        This endpoint receives a message and returns a streamed response from OpenAI's API.
        ---
        tags:
          - ChatGPT Adviser API
        parameters:
          - name: body
            in: body
            required: true
            schema:
              type: object
              properties:
                message:
                  type: string
                  description: The message to send to the ChatGPT Adviser API.
                  example: "Hello, how are you?"
        responses:
          200:
            description: A streamed response from the ChatGPT API
            content:
              text/plain:
                schema:
                  type: string
          400:
            description: Invalid input
        """
        data = request.get_json()
        message = data.get("message")

        app.logger.info('Received request: %s', data)
        app.logger.info('User message: %s', message)

        def generate():
            try:
                app.logger.info('Calling ChatGPT Adviser API with message: %s', message)

                stream = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": message}],
                    stream=True
                )

                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        yield(chunk.choices[0].delta.content)
                        app.logger.info('ChatGPT Adviser API response chunk: %s', chunk.choices[0].delta.content)

            except Exception as e:
                app.logger.error('Error while calling ChatGPT Adviser API: %s', e)
                yield 'Error occurred while processing your request.'

        return app.response_class(generate(), content_type='text/plain')

    return app
