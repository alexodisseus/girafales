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


@question.route('/ver/<question_id>/<exam_id>', methods = ['GET','POST'])
def view(question_id, exam_id):
	
	if 'username' not in session:
		return redirect(url_for('admin.login'))
	
	user = session['userid']

	exam = model.get_exam_by_id(exam_id)
	questao = model.get_question_realize(user, exam.id , question_id)

	return render_template('question/view.html' , exam=exam , questao=questao)
	

@question.route('/resposta/<question_id>/<exam_id>', methods = ['GET','POST'])
def response(question_id, exam_id):
	
	if 'username' not in session:
		return redirect(url_for('admin.login'))
	
	if request.method == 'POST':
		titulo = request.form['titulo']
		explicacao = request.form['explicacao']
		link = request.form['link']
		resposta = request.form['resposta']

		
		
		
		asd = model.create_response(session['userid'] , exam_id , question_id,resposta , explicacao , link , titulo)
		


	user = session['userid']
	exam = model.get_exam_by_id(exam_id)

	questao = model.get_question_realize(user, exam.id , question_id)
	responses = model.get_response_by_question(question_id)

	return render_template('question/response.html' , exam=exam , questao=questao , responses = responses)



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