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
	
@question.route('/realizar_questione/<id>', methods = ['GET','POST'])
def releaze(id):
	"""
	if 'username' not in session:
		return redirect(url_for('admin.login'))

	"""

	#data = model.read_tasks(session['userid'])
	question = model.get_question_by_id(id)

	return render_template('question/releaze.html' , question=question)

@question.route('/editar/<id>', methods=['GET'])
def edit(id):
    
	questions = model.get_all_questions_null(id)
	
	return render_template('question/edit.html' , questions=questions)



@question.route('/criar/<id>', methods=['GET' , 'POST'])
def create(id):
    
	contest = model.get_id_contest(id)
	if request.method == 'POST':
		name = request.form['name']
		year = request.form['year']
		description = request.form['description']
		types = request.form['types']
		contest_id = contest.id

		data = model.create_question(contest_id, name, year, description, types)
		return redirect(url_for('contest.view_contest' , id = contest.id))



	return render_template('question/create.html', contest = contest)


def configure(app):
	app.register_blueprint(question)