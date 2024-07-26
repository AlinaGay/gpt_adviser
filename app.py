from flask import Flask, jsonify, render_template, request 
from openai import OpenAI
import logging

client = OpenAI()

def create_app():
    app = Flask(__name__)

    logging.basicConfig(
        filename='app.log', 
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/answer", methods=["GET", "POST"])
    def answer():
        data = request.get_json()
        message = data["message"]

        app.logger.info('Received request: %s', data)
        app.logger.info('User message: %s', message)

        def generate():
            try:
                app.logger.info('Calling ChatGPT API with message: %s', message)

            
                stream = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": message}],
                    stream=True
                ) 

                for chunk in stream:
                    if chunk.choices[0].delta.content is not None:
                        yield(chunk.choices[0].delta.content)
                        app.logger.info('ChatGPT response chunk: %s', chunk.choices[0].delta.content)

            except Exception as e:
                app.logger.error('Error while calling ChatGPT API: %s', e)
                yield 'Error occurred while processing your request.'        

        return generate(), {"Content-Type": "text/plain"}

    return app