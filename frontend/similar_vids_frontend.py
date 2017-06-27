from flask import Flask
from flask import request
from flask import render_template
from jinja2 import FileSystemLoader   
from jinja2.environment import Environment

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('six_similar.html', YTID1='dZTwJ31kEHo', showAll = False)

@app.route('/', methods=['POST'])
def my_form_post():   
    global showAll  
    if request.form['submit'] == 'receive_text':
        print ("button pushed")
        text = request.form['text']
        print (text)
        showAll = True     
    return render_template('six_similar.html', YTID1='dZTwJ31kEHo', showAll = True)           

    #return ('', 204)

if __name__ == '__main__':
    app.run()