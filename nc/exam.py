import app
import model


from flask import Blueprint, render_template, current_app , request , session, redirect, url_for


exam = Blueprint('exam' , __name__ , url_prefix='/exames')




@exam.route('/', methods = ['GET','POST'])
def index():
	"""
	if 'username' not in session:
		return redirect(url_for('admin.login'))

	"""

	#data = model.read_tasks(session['userid'])
	
	data = model.get_all_contest()
	
	return render_template('exam/index.html' , contests = data )


@exam.route('/ver/<id>', methods = ['GET','POST'])
def view(id):
	"""
	if 'username' not in session:
		return redirect(url_for('admin.login'))

	"""

	exam = model.get_exam_by_id(id)

	questions = model.get_questions_view(id)
	tags = []
	for x in questions:
		if x.tag in tags:
			pass
		else:
			tags.append(x.tag)
	


	return render_template('exam/view.html' , exam=exam , questions = questions , tags = tags)




@exam.route('/realizar_exame/<id>', methods = ['GET','POST'])
def releaze(id):

	if 'username' not in session:
		return redirect(url_for('admin.login'))

	exam = model.get_exam_by_id(id)
	user = session['userid']
	questao = model.get_question_realize(user, exam.id)

	return render_template('exam/releaze.html' , exam=exam , questao=questao)


"""
#arrumar as variaveis, ta bagunçado
@exam.route('/seguinte/<question_id>/<exam_id>', methods = ['GET','POST'])
def next(question_id , exam_id):

	if 'username' not in session:
		return redirect(url_for('admin.login'))

	exam = model.get_exam_by_id(exam_id)
	user = session['userid']
	question_id = question_id


	questao = model.get_question_realize_next(user, exam.id , question_id)


	return render_template('exam/releaze.html' , exam=exam , questao=questao)

"""

@exam.route('/editar/<id>', methods=['GET'])
def edit(id):
    
	questions = model.get_all_questions_null(id)
	
	return render_template('exam/edit.html' , questions=questions)



@exam.route('/criar/<id>', methods=['GET' , 'POST'])
def create(id):
    
	contest = model.get_id_contest(id)
	
	if request.method == 'POST':
		name = request.form['name']
		year = request.form['year']
		description = request.form['description']
		types = request.form['types']
		contest_id = contest.id

		data = model.create_exam(contest_id, name, year, description, types)
		return redirect(url_for('contest.view_contest' , id = contest.id))



	return render_template('exam/create.html', contest = contest)


def configure(app):
	app.register_blueprint(exam)