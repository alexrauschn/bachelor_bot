from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/question', methods=['POST'])
def getAnswer():
    question = request.form['question']#not sure, maybe this will be a json later on but its not important now

#TODO now implement the code that uses the question and return it later on

    answer = "Here you have to put the answer string!"
    return jsonify({'most fitting answer ': answer})


if __name__ == '__main__':
    app.run(debug=True)
