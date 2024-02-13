import app
import model


from flask import Blueprint, render_template, current_app , request , session, redirect, url_for


quiz = Blueprint('quiz' , __name__ , url_prefix='/quiz')


#usado para administrar os usuarios do sistema
@quiz.route('/', methods = ['GET','POST'])
def index():
	"""
	if 'username' not in session:
		return redirect(url_for('admin.login'))

	"""

	#data = model.read_tasks(session['userid'])
	
	data = model.get_all_contest()
	
	return render_template('quiz/index.html' , contests = data )
	





@quiz.route('/cadastrar_concurso', methods = ['GET','POST'])
def create_contest():
	"""
	if 'username' not in session:
		return redirect(url_for('admin.login'))

	"""

	asd = model.get_all_questions()

	if request.method == 'POST':
		name = request.form['name']
		types = request.form['types']
		model.create_contest(name,types)
		
		return redirect(url_for('quiz.index'))
	
	return render_template('quiz/create_contest.html' , data = asd )



@quiz.route('/quiz_view/<id>', methods=['GET'])
def view_contest(id):
    

	contest = model.get_id_contest(id)
	exams = model.get_exam_contest(contest.id)
	print(exams)

	return render_template('quiz/view_contest.html', contest=contest , exams=exams)




@quiz.route('/exame_criar/<id>', methods=['GET' , 'POST'])
def create_exam(id):
    
	contest = model.get_id_contest(id)
	if request.method == 'POST':
		name = request.form['name']
		year = request.form['year']
		description = request.form['description']
		types = request.form['types']
		contest_id = contest.id

		data = model.create_exam(contest_id, name, year, description, types)
		return redirect(url_for('quiz.view_contest' , id = contest.id))



	return render_template('quiz/create_exam.html', contest = contest)





@quiz.route('/quiz_edit/<id>', methods=['GET', 'POST'])
def edit_contest(id):
	contest = model.get_id_contest(id)

	if request.method == 'POST':
		contest.name = request.form['name']
		contest.types = request.form['types']
		asd = model.update_contest(id, contest.name, contest.types)
		if asd:
			return redirect(url_for('quiz.index'))
	
	return render_template('quiz/edit_contest.html', contest=contest)
    





def configure(app):
	app.register_blueprint(quiz)