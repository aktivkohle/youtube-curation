from flask import Flask, request, render_template, flash, redirect, url_for
import os.path, sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from video_similar_to_doc import similar_to_doc
import config


def verify_text(t):
    wordcount = len(t.split(' '))
    if wordcount > 20 and wordcount < 10000:
        return True
    else:
        return False


app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route('/')
def my_form():
    logger.info('initial render template sending for empty text box.')
    return render_template('six_similar.html', showAll = False)

@app.route('/', methods=['POST'])
def my_form_post():   
    global showAll 
    showAll = False

    if request.form['submit'] == 'receive_text' and not verify_text(request.form['text']):
        print ('wrong text')
        textlength = len((request.form['text']).split(' '))
        if textlength < 21:
            flash('Not enough text! Please try again.')
        elif textlength > 1000:
            flash('Text too long! Please try again.')
        else:
            flash('Please try again!')
        return redirect(url_for('my_form'))

    elif request.form['submit'] == 'receive_text' and verify_text(request.form['text']):
        text = request.form['text']
        showAll = True
        print (text)
        similar_vids = similar_to_doc(text)
        # ids :
        YTID1 = similar_vids[0][1]
        YTID2 = similar_vids[1][1]
        YTID3 = similar_vids[2][1]
        YTID4 = similar_vids[3][1]
        YTID5 = similar_vids[4][1]
        YTID6 = similar_vids[5][1]
        # titles:
        YTTITLE1 = similar_vids[0][0]
        YTTITLE2 = similar_vids[1][0]
        YTTITLE3 = similar_vids[2][0]
        YTTITLE4 = similar_vids[3][0]
        YTTITLE5 = similar_vids[4][0]
        YTTITLE6 = similar_vids[5][0]
        print (similar_vids)
        return render_template(
            'six_similar.html', YTID1=YTID1, YTID2=YTID2, YTID3=YTID3, YTID4=YTID4, YTID5=YTID5, YTID6=YTID6,
             YTTITLE1=YTTITLE1, YTTITLE2=YTTITLE2, YTTITLE3=YTTITLE3, YTTITLE4=YTTITLE4, YTTITLE5=YTTITLE5,
              YTTITLE6=YTTITLE6, showAll = showAll)

if __name__ == '__main__':
    app.run()