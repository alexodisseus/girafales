import app
import model


from flask import Blueprint, render_template, current_app , request , session, redirect, url_for


admin = Blueprint('admin' , __name__ , url_prefix='/')


#usado para administrar os usuarios do sistema
@admin.route('/', methods = ['GET','POST'])
def index():
	"""
	if 'username' not in session:
		return redirect(url_for('admin.login'))

	"""

	#data = model.read_tasks(session['userid'])
	
	return render_template('index.html' )
	#return render_template('login.html' )



"""
@admin.route('/login', methods = ['GET','POST'])
def login():
	if request.method == 'POST':

		name = request.form['name']
		password = request.form['password']
		data = model.read_user(name,password)

		if data:

			session['username'] = data.name
			session['userid'] = data.id
			
			return redirect(url_for('admin.index'))

		return render_template('login.html' )


	return render_template('login.html' )



@admin.route('/admis', methods = ['GET','POST'])
def admis():
	if 'username' not in session:
		return redirect(url_for('admin.login'))
	return render_template('login.html')


@admin.route('/view/<id>', methods = ['GET','POST'])
def view(id):
	if 'username' not in session:
		return redirect(url_for('admin.login'))

	data = model.read_tasks_view(id)
	
	#sai da sessao se o usuario estiver errado
	if data.person_id != session['userid']:
		session.pop('username', None)
		return redirect(url_for('admin.login'))

	return render_template('view.html' , data=data)


@admin.route('/create/', methods = ['GET','POST'])

def create():
	#if 'username' not in session:
		#return redirect(url_for('admin.login'))

	if request.method == 'POST':
		user = request.form['name']
		password = request.form['password']

		model.create_user(user,password)
		return redirect(url_for('admin.login'))

	return render_template('create.html')





@admin.route('/create_task/', methods = ['GET','POST'])
def create_task():

	if request.method == 'POST':
		title = request.form['title']
		status = request.form['status']

		model.create_tasks(title,status , session['userid'])
		return redirect(url_for('admin.index'))

	return render_template('create_task.html')


@admin.route('/logout', methods = ['GET','POST'])
def logout():

	session.pop('username', None)
	return redirect(url_for('admin.login'))
"""

def configure(app):
	app.register_blueprint(admin)