from flask import Flask
from flask import request
from flask import render_template
from jinja2 import FileSystemLoader   
from jinja2.environment import Environment

app = Flask(__name__)

@app.route('/')
def my_form():

    return render_template('six_similar.html', YTID1='dZTwJ31kEHo')

@app.route('/', methods=['POST'])
def my_form_post():     
    if request.form['submit'] == 'receive_text':
        print ("button pushed")
        text = request.form['text']
        print (text)        
    return ('', 204)

if __name__ == '__main__':
    app.run()