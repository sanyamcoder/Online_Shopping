#!/usr/bin/env python
# coding: utf-8

# 

# In[4]:


#Imports
import nltk
from nltk.stem.lancaster import LancasterStemmer

import numpy as np
import tflearn
import tensorflow as tf
from tensorflow.python.framework import ops

import random
import json
import pickle

from flask import Flask, redirect, url_for, request, render_template

stemmer = LancasterStemmer()
ignore = ['?','.','&','!']  
login_status = False

#Loading Data
with open("intents.json") as file:
    data = json.load(file)
  
try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
        
except:
     #Initializing empty lists
    words = []
    labels = []
    docs_x = []
    docs_y = []

    #Looping through our data
    for intent in data['intents']:
        for pattern in intent['patterns']:
            pattern = pattern.lower()
            #Creating a list of words
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent['tag'])
    
        if intent['tag'] not in labels:
            labels.append(intent['tag'])
  
    words = [stemmer.stem(w.lower()) for w in words if w not in ignore]
    words = sorted(list(set(words)))
    labels = sorted(labels)

    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]
    for x,doc in enumerate(docs_x):
        bag = []
        wrds = [stemmer.stem(w) for w in doc]
        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)
        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1
        training.append(bag)
        output.append(output_row)
    
    #Converting training data into NumPy arrays
    training = np.array(training)
    output = np.array(output)

    #Saving data to disk
    with open("data.pickle","wb") as f:
        pickle.dump((words, labels, training, output),f)
 
try:
    model.load('./my_model/model.tflearn')
except Exception:
    ops.reset_default_graph()

    net = tflearn.input_data(shape = [None, len(training[0])])
    net = tflearn.fully_connected(net,8)
    net = tflearn.fully_connected(net,8)
    net = tflearn.fully_connected(net,len(output[0]), activation = "softmax")
    net = tflearn.regression(net)

    model = tflearn.DNN(net)
    
    model.fit(training, output, n_epoch = 200, batch_size = 8, show_metric = True)
    model.save("my_model/model.tflearn")
    

def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1
            
    return np.array(bag)
'''def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        results = model.predict([bag_of_words(inp, words)])
        results_index = np.argmax(results)
        tag = labels[results_index]

        for tg in data["intents"]:
            if tg['tag'] == tag:
                responses = tg['responses']

        print(random.choice(responses))

#chat()
'''


# In[8]:


app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('first_page.html')
    

@app.route('/',methods=['POST','GET'])
def home_page_processing():
    if request.method == "POST":
        user = (request.form.get('user_name'))
        pswd = (request.form.get('password'))
        
        if user == pswd:
            login_status = True
            return render_template('second_page.html',title ='Successful')
        else:
            login_status = False
            return render_template('second_page.html',title ='Failed')
    else:
        return render_template('second_page.html',title ='Error')
    
        
@app.route('/dashboard',methods=['POST','GET'])
def second_screen():
    return render_template('dashboard.html')

@app.route('/chatbot',methods=['POST','GET'])
def chatbot_input():
    return render_template('chatbot.html')


@app.route('/response',methods=['POST','GET'])
def get_bot_response():
    seat_count = 10
    message = request.args.get('msg')
    if message:
        message = message.lower()
        results = model.predict([bag_of_words(message,words)])
        
        if message == "quit":
            return redirect(url_for('second_screen'))
        
        result_index = np.argmax(results)
        tag = labels[result_index]
        if np.amax(results) > 0.5:
            if tag == "book_table":
                seat_count -= 1
                response = "Your table has been booked successfully. Remaining tables: " + str(seat_count)    
            elif tag == "available_tables":
                response = "There are " + str(seat_count) + " tables available at the moment."
            elif tag == "navigate_dashboard":
                if login_status == True:
                    response = "Redirecting to dashboard."
                else:
                    response = "Login to system."
            else:
                for tg in data['intents']:
                    if tg['tag'] == tag:
                        responses = tg['responses']
                response = random.choice(responses)
        else:
            response = "I didn't quite get that, please try again."
        return str(response)
    return "Missing Data!"

if __name__ == '__main__':
    app.run()


# In[ ]:




