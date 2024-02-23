import app
import model


from flask import Blueprint, render_template, current_app , request , session, redirect, url_for


question = Blueprint('question' , __name__ , url_prefix='/questoes')




@question.route('/', methods = ['GET','POST'])
def index():
	"""
	if 'username' not in session:
		return redirect(url_for('admin.login'))

	"""

	#data = model.read_tasks(session['userid'])
	
	data = model.get_all_contest()
	
	return render_template('question/index.html' , contests = data )


@question.route('/ver/<id>', methods = ['GET','POST'])
def view(id):
	"""
	if 'username' not in session:
		return redirect(url_for('admin.login'))

	"""

	#data = model.read_tasks(session['userid'])
	question = model.get_question_by_id(id)
	
	return render_template('question/view.html' , question=question)
	

@question.route('/editar/<id>', methods=['GET'])
def edit(id):
    
	questions = model.get_all_questions_null(id)
	
	return render_template('question/edit.html' , questions=questions)


@question.route('/criar/<id>', methods=['GET' , 'POST'])
def create(id):
    
	exam = model.get_id_exam(id)

	if request.method == 'POST':
		exam_id = request.form['exam_id']
		
		tema = request.form['tema']
		tipo = request.form['tipo']
		questao = request.form['questao']
		alternativa_a = request.form['alternativa_a']
		alternativa_b = request.form['alternativa_b']
		alternativa_c = request.form['alternativa_c']
		alternativa_d = request.form['alternativa_d']
		alternativa_e = request.form['alternativa_e']

		
		

		data = model.create_question_id( exam_id, tema, tipo, questao, alternativa_a , alternativa_b, alternativa_c, alternativa_d, alternativa_e)
		return redirect(url_for('exam.view' , id = exam_id))



	return render_template('question/create.html', exam = exam)


def configure(app):
	app.register_blueprint(question)