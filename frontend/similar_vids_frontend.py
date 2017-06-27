from flask import Flask
from flask import request
from flask import render_template
from jinja2 import FileSystemLoader   
from jinja2.environment import Environment
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from video_similar_to_doc import similar_to_doc

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('six_similar.html', showAll = False)

@app.route('/', methods=['POST'])
def my_form_post():   
    global showAll  
    if request.form['submit'] == 'receive_text':
        print ("button pushed")
        text = request.form['text']
        print (text)
        similar_vids = similar_to_doc(text)
        showAll = True   
        YTID1 = similar_vids[0][1]
        YTID2 = similar_vids[1][1]
        YTID3 = similar_vids[2][1]
        YTID4 = similar_vids[3][1]
        YTID5 = similar_vids[4][1]
        YTID6 = similar_vids[5][1]
        print (similar_vids)        
    return render_template(
        'six_similar.html', YTID1=YTID1, YTID2=YTID2, YTID3=YTID3, YTID4=YTID4, YTID6=YTID6, showAll = True)           

    #return ('', 204)

if __name__ == '__main__':
    app.run()