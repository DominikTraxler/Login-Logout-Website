from flask import Flask, render_template, request, session, redirect
import sys
import os
import SQL_Login
import SQL_Register_SQLight
import SQL_Post

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

# For inserting given data into SQL table
def SQL_INSERT(data):
    SQL_Register_SQLight.InsertAccountData(data[0], data[1], data[2])
    #for variable in data:
    #    sys.argv.append(variable)
    #exec(open(os.path.dirname(os.path.abspath(__file__)) + "/SQL_Register_SQLight.py").read())
    #sys.argv = [sys.argv[0]]

# For Checking if given Data is compatible with tables data
def SQL_CHECK(data):
    result = SQL_Login.CheckIfValid(data[0],data[1])
    return result
    #print("Data: ", data[0],data[1])
    #for variable in data:
    #    sys.argv.append(variable)
    #exec(open(os.path.dirname(os.path.abspath(__file__)) + "/SQL Login.py").read())


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if(request.form['submit_button'] == 'logout'):
            #print("2.: " + session['username'])
            session.pop('username', default=None)
            return render_template('index.html')

    if 'username' in session:
        #print("1.: " + session['username'])
        if(SQL_Post.GetPostData_All() == ""):
            return render_template('index.html', nopost='nopost')
        else:
            PostInfo = SQL_Post.GetPostData_All()
            try:
                print(PostInfo[0][0])
            except IndexError:
                print("NOOOOPOST")
                return render_template('index.html', username=session['username'], nopost="nopost")
            postnames = PostInfo[0]
            posttexts = PostInfo[1]
            postauthors = PostInfo[2]
            return render_template('index.html', username=session['username'], postnames = postnames, posttexts = posttexts, postauthors = postauthors)

    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        if(request.form['submit_button'] == 'logout'):
            session.pop('username', default=None)
            return render_template('index.html')
    if 'username' in session:
        print(SQL_Post.GetPostData_User(session['username']))
        if(SQL_Post.GetPostData_User(session['username']) == ""):
            return render_template('profile.html', nopost='nopost')
        else:
            return render_template('profile.html', username=session['username'], postnames = SQL_Post.GetPostData_User(session['username'])[0], posttexts = SQL_Post.GetPostData_User(session['username'])[1])
    return render_template('error.html')

@app.route('/post', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        #print(request.form.get('submit_button'))
        if(request.form.get('submit_button') == 'logout'):
            #print("2.: " + session['username'])
            session.pop('username', default=None)
            return render_template('index.html')
        else:
            heading = request.form['Heading']
            text = request.form['post_text']

            SQL_Post.InsertPostData(heading,text,session['username'])
            return render_template('success_post.html', heading=heading)

    if 'username' in session:
        #print("Error with login")
        return render_template('post.html', username=session['username'])
    else:
        return render_template('error.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        Data = [username, password]
        result = SQL_CHECK(Data)
        #Check if User is Registered, not Registered or has the right password
        if(result) == 'Registered':
            session['username'] = username
            return render_template('success_login.html', username=username)
        elif(result == 'Not Registered'):
            return render_template('login.html', notRegistered='not Registered')
        elif(result == 'Wrong Password'):
            return render_template('login.html', wrongPassword='wrong Password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        yob = request.form['yob']

        #checking if username already in database
        if(SQL_Register_SQLight.CheckUsername(username) == "Registered"):
            return render_template('register.html', Registered="Registered")
        else:
            Data = [username, password, yob]
            SQL_INSERT(Data)
            session['username'] = username
            return render_template('success_register.html', username=username)
    return render_template('register.html')



if __name__ == '__main__':
    app.run(debug=True, port=8001)