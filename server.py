from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
# Imports
import fasttext
import flask
from flask import Flask, request, jsonify, send_from_directory, render_template
import json
import requests
import random
import argparse # MAA

app = flask.Flask(__name__)
model_name = 'model.bin'
train_file_name = 'train_data.txt'
response_file_name = 'story.json'
treshold = 0.45
def train( epochCount = 100, vectorSize = 5):
    print("Epoch Count: " , epochCount, " Vector Size: " , vectorSize)
    print('--- training started --- ' )
    model = fasttext.train_supervised(train_file_name,
                                    lr=0.05,    #learning rate
                                    dim = 5,  #size of word vectors (orj 100)
                                    ws = vectorSize,     #size of context window
                                    epoch = epochCount,  #number of epochs (5'ten 100'e yükseltildi)
                                    neg = 5)    #number of negatives samples
    model.save_model(model_name)
    print('--- training ended ---')
    return True
def predict(query):
    texts = [query]
    model = fasttext.load_model(model_name)
    predT = model.predict(texts, k=3)
    print("Predictions: ", predT)
    return predT

def utter(prediction):
    response_file = open(response_file_name,'r')
    response = json.loads(response_file.read())
    processedPred = []
    preds = prediction[0][0]
    scores = prediction[1][0]

    for i in range(len(preds)):
        predItem = {}
        predItem["predName"] = preds[i]
        predItem["score"] = scores[i]
        utter_list = response[preds[i]]
        #is best score bigger than treshold.
        if scores[i] > treshold:
            predItem["className"] = random.choice(utter_list)
        else :
            predItem["className"] = "NotFound"
            predItem["classActual"] = random.choice(utter_list)
        processedPred.append(predItem)

    utter_list = response[preds[i]]
    return processedPred

@app.route('/demo/predict/<query>',methods=['POST','GET'])
def ask(query):
    prediction = predict(query)
    utterance = utter(prediction)
    return json.dumps(utterance)

@app.route('/demo/batchTest/',methods=['POST','GET'])
def bathAsk():
    print("Batch Testing")
    bData = json.loads(request.get_json())
    score = 0
    all = 0
    for x in bData:
        cresult = ask (x["Query"])
        print("Result")
        res1 = json.loads(cresult)[0]
        print(res1)

        all += 1
        if res1["className"] == x["Recommended"]:
           print("Correct")
           score += 1
        else:
           print("False")
    batchScore = {}
    batchScore["success"] = score
    batchScore["all"] = all
    print(batchScore)
    fRes = {"status":"success", "batchScore": batchScore }
    return jsonify(fRes)
    #return json.dumps(batchScore)

@app.route('/demo/example',methods=['GET'])
def example():
    return  open("sampleTurkish.json").read()

@app.route('/demo',methods=['POST','GET'])
def demo():
    if request.method == 'POST':
        rData = json.loads(request.get_json()["textData"])
        vectorSize = json.loads(request.get_json()["vectorSize"])
        epochCount = json.loads(request.get_json()["epochCount"])
        QnAdata = rData["intents"]
        train_file = open(train_file_name,'w')
        response_file = open(response_file_name,'w')
        train_data = ''
        response_data = {}
        counter = 0
        for intent in QnAdata:
            questions = intent["patterns"]
            answers = [intent["tag"]]
            for question in questions:
                train_data += '__label__QnA'+str(counter)+' '+question+'\n'
            response_data['__label__QnA'+str(counter)] = answers
            counter += 1
        train_file.write(train_data)
        response_file.write(json.dumps(response_data))
        train_file.close()
        response_file.close()
        train(epochCount, vectorSize)
        return jsonify('{"status":"success"}')

    return '''
    <!doctype html>
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
            <script>
                function send(){
                    var textdata = $('#textArea').val()
                    var epocharea = $('#epocharea').val()
                    var vectorsizearea = $('#vectorsizearea').val()

                    var trainReq ={};
                    trainReq.epochCount = epocharea;
                    trainReq.vectorSize = vectorsizearea;
                    trainReq.textData = textdata;
                    console.log(trainReq);

                    console.log(  epocharea + ' '  + vectorsizearea)
                    $("#text").html('training agent..')
                    $.ajax({
                        type: 'POST',
                        url: '/demo',
                        data: JSON.stringify(trainReq),
                        success: function(resp) {$("#text").html('training completed.')},
                        error: function (jqXHR, exception){console.log('error')},
                        contentType: "application/json",
                        dataType: 'json'
                    })
                }
                function test(){
                    var testarea = $('#testarea').val()

                    console.log(testarea )
                    $.ajax({
                        type: 'GET',
                        url: '/demo/predict/'+testarea,
                        success: function(resp) {$("#testresult").html(resp)},
                        error: function (jqXHR, exception){console.log('error')}
                    })
                }
                function batchtest(){
                    var batchtext = $('#batcharea').val()
                    $("#batchresult").html('testing agent..')
                    console.log(batchtext )
                    $.ajax({
                        type: 'POST',
                        url: '/demo/batchTest/',
                        data: JSON.stringify(batchtext),
                        success: function(resp) {$("#batchresult").html('Done ' + JSON.stringify(resp))},
                        error: function (jqXHR, exception){console.log('error')},
                        contentType: "application/json",
                        dataType: 'json'
                    })
                }
            </script>
        </head>
        <body>
            <p> paste your FAQ here: <a href="/demo/example" target="new">see an example training data</a></p>
            <textarea id="textArea" rows="10"></textarea>
            <p> Epoch: <input type="text" id="epocharea" value="100" placeholder="100" /> Word Vector Size: <input type="text" id="vectorsizearea" value="5" /></p>
            <button onclick="send()">train</button>
            <p id="text"></p>

            <input type="text" id="testarea" placeholder="enter your query" />
            <button onclick="test()">test</button>
            <p id="testresult"></p>
            <p></p>
            <textarea id="batcharea" rows="10"></textarea>

            <button onclick="batchtest()">batch test</button>
            <p id="batchresult">Naber</p>
        </body>
        <style>
            textarea,input {
                width: 99.7%;
                resize: none;
                border: 1px solid;
            }
            button {
                margin-top: 10px;
            }
        </style>
    </html>
    '''

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default='80', type=int)
    args = parser.parse_args()
    try:
        app.run(host="0.0.0.0", port=args.port)
    except PermissionError as e:
        print ("You don't have enough priviledges to open a socket on port {}".format(args.port))
        print ("Try to change the port to a value higher than 1024, with argument --port")
        print (str(e))
