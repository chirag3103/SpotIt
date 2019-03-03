import os
from flask import Flask, request, jsonify, Response, render_template, send_from_directory
from flask_httpauth import HTTPBasicAuth
from src.Question import Question
from src.Google_datastore import Datastore

app = Flask(__name__)
auth = HTTPBasicAuth()
question_obj = Question(os.path.join(os.path.dirname(__file__), 'resources/questions.json'))

USER_DATA = {
    "admin": "spotit$"
}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/<path:filename>')
def ui_pages(filename='index.html'):
    return render_template(filename)


@app.route('/images/<path:filename>', methods=['GET'])
def serve_static_image(filename):
    """
    To serve question images for the UI
    :param filename: Image filename
    :return:
    """
    curr_dir = os.getcwd()
    return send_from_directory(os.path.join(curr_dir, 'resources/images'), filename)


@app.route('/audio/<path:filename>', methods=['GET'])
def serve_static_audio(filename):
    """
    To serve audio for the UI
    :param filename: Audio filename
    :return:
    """
    curr_dir = os.getcwd()
    return send_from_directory(os.path.join(curr_dir, 'resources/audio'), filename)


@app.route('/api/questions', methods=['GET'])
def get_questions():
    count = request.args.get('count', 10)
    questions = question_obj.random_questions(count)
    return jsonify({"questions": questions})


@app.route('/api/speech_text', methods=['POST'])
def validate_speech():
    answer = request.args.get('answer')
    speech = request.files['answer.mp3']
    result = question_obj.speech_answer(speech, answer)
    return jsonify({"result": result})


@app.route('/api/create_questions')
@auth.login_required
def create_questions():
    # Create questions and audio from images
    ds = Datastore()
    Question.create_questions(ds)
    return Response()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
