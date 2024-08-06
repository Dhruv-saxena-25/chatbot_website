from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import os
from chat.retrieval_generation import generation
from chat.data_ingestion import data_ingestion

app = Flask(__name__)

load_dotenv()

vstore=data_ingestion("done")
chain=generation(vstore)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route('/chatbot', methods=["GET", "POST"])
def gitRepo():

    if request.method == 'POST':
        user_input = request.form['question']
        ut(user_input)
        os.system("python store_index.py")

    return jsonify({"response": str(user_input) })


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    if input == "clear":
        os.system("rm -rf repo")
    result=chain({"query": input})
    print("Response : ", result["result"])
    return str(result["result"])


if __name__ == '__main__':
    app.run(port=8080, debug= True)