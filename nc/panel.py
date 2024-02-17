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
    asd  = request.args.get('id')

    return render_template('panel/index.html'  , id = asd)

    #return render_template('login.html' )



@panel.route('/generate_quiz', methods=['POST'])
def generate_quiz():
    asd  = request.args.get('id')
    
    text = request.form['text']
    
    header, numbered_questions = extract_header_and_questions(text)
    headers = []
    headers.append(header)

    return render_template('panel/view.html', questions=numbered_questions , headers = headers , id = asd)



@panel.route('/quiz_create', methods=['POST'])
def quiz_create():
    asd  = request.args.get('id')
    
    todos_os_parametros = request.form.to_dict()
    created_questions = model.create_questions_from_dict(todos_os_parametros)
    
    if created_questions:
        return redirect(url_for('quiz.view_exam' , id = asd))
    
    return redirect(url_for('panel.generate_quiz' , id = asd))





def extract_header_and_questions(text):
    sentences = sent_tokenize(text)

    header = sentences[0]

    question_pattern = re.compile(r'^\d+\s')
    numbered_questions = []
    current_question = ""

    for sentence in sentences[1:]:
        if question_pattern.match(sentence):
            if current_question:
                numbered_questions.append(current_question.strip())
            current_question = sentence
        else:
            current_question += " " + sentence

    if current_question:
        numbered_questions.append(current_question.strip())

    return header, numbered_questions



def configure(app):
	app.register_blueprint(panel)




"""
# Exemplo de uso
if __name__ == "__main__":
    # Criando uma pergunta
    question1 = create_question(text="Qual é a capital do Brasil?", answer="Brasília")


    # Obtendo todas as perguntas
    all_questions = get_all_questions()
    print("Todas as perguntas:", all_questions)


    # Atualizando uma pergunta
    update_question(question1.id, text="Qual é a capital da França?", answer="Paris")
    updated_question = get_question_by_id(question1.id)
    print("Pergunta atualizada:", updated_question)


    # Excluindo uma pergunta
    delete_question(question1.id)
    remaining_questions = get_all_questions()
    print("Perguntas restantes:", remaining_questions)
"""






