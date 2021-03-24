import pyrebase
from product_search import product_dict, get_products
from flask import Flask, render_template, request, redirect, url_for, session
 

app = Flask(__name__)
app.config['SECRET_KEY'] = '\x8f{1O\x00\x0b\x17\xda\xfd\xf1\x8d\xf4\xe5A\xbb\xa2(|\xfb\x93q\xcf\x0fb'
user_table_name = ''

config = {
	"apiKey": "AIzaSyAfOSyvRVi3pGCpCWagT0s_L9kc3hpcyB8",
    "authDomain": "online-shopping-f8fdd.firebaseapp.com",
    "databaseURL": "https://online-shopping-f8fdd-default-rtdb.firebaseio.com",
    "projectId": "online-shopping-f8fdd",
    "storageBucket": "online-shopping-f8fdd.appspot.com",
    "messagingSenderId": "471497295887",
    "appId": "1:471497295887:web:6be64e226ce52af41d3b7a",
    "measurementId": "G-QQYT7K4DSM"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()


def format_email_firebase(email):
	char = ['.','$','[',']','#','/']
	for c in char:
		if c in email:
			user_table_name = email.replace(c, '-')
	return user_table_name



@app.route('/', methods=['GET','POST'])
@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		email = request.form['Email']
		password = request.form['Password']

		try:
			auth.sign_in_with_email_and_password(email, password)
			session['id'] = 'admin'
			return redirect(url_for('account'))
		except:
			error_msg = 'Invalid Username or Password'
			return render_template('login.html', err=error_msg)
	else:
		session['id'] = 'None'
		return render_template('login.html')


@app.route('/register', methods=['GET','POST'])
def register():
	if request.method == 'POST':
		email = request.form['Email']
		password = request.form['Password']

		try:
			auth.create_user_with_email_and_password(email, password)
			user_table_name = format_email_firebase(email)		
			db.child(user_table_name).set({'Wishlist':''})
			return redirect(url_for('account'))

		except Exception as e:
			print(e)
			error_msg = 'There is already an account registered to this Email Id'
			return render_template('register.html', err=error_msg)
	else:
		session['id'] = 'None'
		return render_template('register.html')

@app.route('/dashboard', methods=['GET','POST'])
def account():
	if session['id'] == 'admin':
		if request.method == 'POST':
			product_name = request.form['q']
			get_products(product_name)
			session['results'] = product_dict
			return redirect(url_for('result'))

		return render_template('dashboard.html')

	else:
		return redirect(url_for('login'))


@app.route('/result')
def result():
	if session['id'] == 'admin':
		return render_template('results.html', product_dict = session['results'])
	return redirect(url_for('login'))


@app.route('/wishlist', methods=['GET','POST'])
def wishlist():
	if request.method == 'POST':
			product = request.form['product']
			db.child(user_table_name).set({'Wishlist':product})
	else:
		return render_template('wishlist.html')



if __name__ == '__main__':
    app.run(debug=True)