import app
import model
import re

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

    
    header, numbered_questions = extract_header_and_questions(text)
    headers = []
    headers.append(header)

    return render_template('panel/view.html', questions=numbered_questions , headers = headers)




@panel.route('/quiz_create', methods=['POST'])
def quiz_create():
    
    questions ="asd"
    todos_os_parametros = request.form.to_dict()
    #ver como pegar o id do anterior e os parametros do outro

    return render_template('quiz/view.html', questions=todos_os_parametros)

@panel.route('/steam', methods=['GET'])
def steam():
    
    questions ="asd"
    

    return render_template('panel/steam.html')






def extract_header_and_questions(text):
    """
    # Tokenização em frases
    sentences = sent_tokenize(text)

    # Cabeçalho é a primeira frase
    header = sentences[0]

    # Filtrar frases que parecem ser questões numeradas
    question_pattern = re.compile(r'^\d+\s')
    numbered_questions = [sentence for sentence in sentences[1:] if question_pattern.match(sentence)]
    """
    sentences = sent_tokenize(text)

    # Cabeçalho é a primeira frase
    header = sentences[0]

    # Filtrar frases que parecem ser questões numeradas
    question_pattern = re.compile(r'^\d+\s')
    numbered_questions = []
    current_question = ""

    for sentence in sentences[1:]:
        if question_pattern.match(sentence):
            # Se encontrou uma nova questão numerada, adiciona a anterior à lista
            if current_question:
                numbered_questions.append(current_question.strip())
            # Inicia uma nova questão
            current_question = sentence
        else:
            # Continua a construção da questão atual
            current_question += " " + sentence

    # Adiciona a última questão à lista
    if current_question:
        numbered_questions.append(current_question.strip())

    return header, numbered_questions



    return header, numbered_questions




def configure(app):
	app.register_blueprint(panel)