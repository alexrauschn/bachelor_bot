from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from model import classify, response


app = Flask(__name__)
CORS(app)


@app.route('/question', methods=['POST'])
def getAnswer():
    question = request.get_json()['question']#not sure, maybe this will be a json later on but its not important now

#TODO now implement the code that uses the question and return it later on
    print(question)
    answer = response(question)
    link = answer[1]#'https://www.ris.bka.gv.at/Dokumente/BgblAuth/BGBLA_2021_II_214/BGBLA_2021_II_214.html'
    probability = 2

    json_answer = jsonify({'answer': answer[0], 'link': link, 'probability': probability})
    json_answer.headers.add("Access-Control-Allow-Origin", "*")
    return json_answer


if __name__ == '__main__':
    app.run(debug=True)
