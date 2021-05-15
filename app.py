from flask import Flask, jsonify, request
from model import classify, response
app = Flask(__name__)

@app.route('/question', methods=['POST'])
def getAnswer():
    question = request.get_json()['question']#not sure, maybe this will be a json later on but its not important now

#TODO now implement the code that uses the question and return it later on
    print(question)
    answer = response(question)
    if answer == "":
        answer = "Sorry no idea what you're talking about, bruh"
    return jsonify({'most fitting answer ' : answer})


if __name__ == '__main__':
    app.run(debug=True)
