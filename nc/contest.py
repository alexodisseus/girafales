import app
import model


from flask import Blueprint, render_template, current_app , request , session, redirect, url_for


contest = Blueprint('contest' , __name__ , url_prefix='/concursos')


#usado para administrar os usuarios do sistema
@contest.route('/', methods = ['GET','POST'])
def index():
	"""
	if 'username' not in session:
		return redirect(url_for('admin.login'))

	"""

	#data = model.read_tasks(session['userid'])
	
	data = model.get_all_contest()
	
	return render_template('contest/index.html' , contests = data )
	





@contest.route('/cadastrar_concurso', methods = ['GET','POST'])
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
		
		return redirect(url_for('contest.index'))
	
	return render_template('contest/create_contest.html' , data = asd )



@contest.route('/contest_view/<id>', methods=['GET'])
def view_contest(id):
    

	contest = model.get_id_contest(id)
	exams = model.get_exam_contest(contest.id)
	

	return render_template('contest/view_contest.html', contest=contest , exams=exams)


@contest.route('/exame_view/<id>', methods=['GET'])
def view_exam(id):
    
	exam = model.get_exam_by_id(id)
	
	return render_template('contest/view_exam.html' , exam=exam)

@contest.route('/exame_editar/<id>', methods=['GET'])
def edit_exam(id):
    
	questions = model.get_all_questions_null(id)
	
	return render_template('contest/edit_exam.html' , questions=questions)

@contest.route('/ajax', methods=['GET'])
def ajax_contest():
	asd = request.args.get('codigo')
	asd1 = request.args.get('page')
	busca = request.args.get('busca')
	print(asd)
	print(asd1)
	print(busca)
	print("asd")
	data = model.get_search_question(busca)
	
	return render_template('contest/ajax_contest.html',data=data)



@contest.route('/realizar_exame/<id>', methods=['GET'])

def go_exam(id):
   
	exam = model.get_exam_by_id(id)

	return render_template('contest/go_exam.html' , exam=exam)





@contest.route('/exame_criar/<id>', methods=['GET' , 'POST'])
def create_exam(id):
    
	contest = model.get_id_contest(id)
	if request.method == 'POST':
		name = request.form['name']
		year = request.form['year']
		description = request.form['description']
		types = request.form['types']
		contest_id = contest.id

		data = model.create_exam(contest_id, name, year, description, types)
		return redirect(url_for('contest.view_contest' , id = contest.id))



	return render_template('contest/create_exam.html', contest = contest)





@contest.route('/contest_edit/<id>', methods=['GET', 'POST'])
def edit_contest(id):
	contest = model.get_id_contest(id)

	if request.method == 'POST':
		contest.name = request.form['name']
		contest.types = request.form['types']
		asd = model.update_contest(id, contest.name, contest.types)
		if asd:
			return redirect(url_for('contest.index'))
	
	return render_template('contest/edit_contest.html', contest=contest)
    





def configure(app):
	app.register_blueprint(contest)