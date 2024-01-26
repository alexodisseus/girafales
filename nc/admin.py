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



@admin.route('/login', methods = ['GET','POST'])
def login():
	if request.method == 'POST':

		email = request.form['emai']
		password = request.form['password']
		data = model.read_user(email,password)

		if data:

			session['username'] = data.name
			session['userid'] = data.id
			return redirect(url_for('contest.index'))


	return render_template('login.html' )


def configure(app):
	app.register_blueprint(admin)