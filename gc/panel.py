import app
import model

import nltk
nltk.download('punkt')

from nltk.tokenize import sent_tokenize
from flask import Blueprint, render_template, current_app , request , session, redirect, url_for


panel = Blueprint('panel' , __name__ , url_prefix='/painel')


#usado para administrar os usuarios do sistema
@panel.route('/', methods = ['GET','POST'])
def index():
	"""
	if 'username' not in session:
		return redirect(url_for('admin.login'))

	"""

	#data = model.read_tasks(session['userid'])
	
	return render_template('panel/index.html' )
	#return render_template('login.html' )





@panel.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    
    text = request.form['text']
    sentences = sent_tokenize(text)
    # Gera perguntas de verdadeiro ou falso com base nas frases
    questions = []
    for idx, sentence in enumerate(sentences, start=1):
    	question = {'statement': sentence, 'answer': True}
    	questions.append(question)

    return render_template('panel/view.html', questions=questions)



def configure(app):
	app.register_blueprint(panel)