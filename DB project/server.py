from flask import *
from loginform import LoginForm
from adminform import AdminForm
from add_news import AddNewsForm
from db_connect import *

db = DB()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'whatisit'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found 404'}), 404)


 @app.route('/')
def start():
    if 'username' in session:
        return redirect('/index')
    return render_template('start.html')
   

#-----------------USER-AREA--------------------------------------
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/')
    news = NewsModel(db.get_connection()).get_all(session['user_id'])
    return render_template('index.html', username=session['username'],
                           news=news)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = form.username.data
        password = form.password.data
        user_model = UserModel(db.get_connection())
        user_model.init_table()
        if form.sign_up.data:
            user_model.insert(user_name, password)
        exists = user_model.exists(user_name, password)
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
        return redirect("/index")
    return render_template('login.html', title='Авторизация', form=form)

   
@app.route('/logout')
def logout():
    session.pop('username',0)
    session.pop('user_id',0)
    return redirect('/')


#--------------THOUGHTS-AREA----------------------
@app.route('/add_news', methods=['GET', 'POST'])
def add_news():
    if 'username' not in session:
        return redirect('/login')
    form = AddNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        nm = NewsModel(db.get_connection())
        nm.insert(title,content,session['user_id'])
        return redirect("/index")
    return render_template('add_news.html', title='Добавление мысли',
                           form=form, username=session['username'])


@app.route('/news/<int:news_id>',  methods=['GET'])
def get_one_news(news_id):
    news = NewsModel(db.get_connection()).get(news_id)
    if not news:
        return jsonify({'error': 'Not found this news'})
    return jsonify({'news': news})


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news1(news_id):
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect('/')


#----------------ADMIN-AREA--------------------------------
@app.route('/delete_user/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    nm = UserModel(db.get_connection())
    nm.delete(user_id)
    return redirect('/')


@app.route('/del_th', methods=['GET'])
def del_th():
    news = NewsModel(db.get_connection()).get_all()
    return render_template('del_th.html', news=news)


@app.route('/thoughts',  methods=['GET'])
def get_news():
    news = NewsModel(db.get_connection()).get_all()
    return render_template('news.html', news=news)


@app.route('/users',  methods=['GET'])
def get_users():
    users = UserModel(db.get_connection()).get_all()
    return render_template('users.html', users=users) 


@app.route('/del_user',  methods=['GET'])
def del_users():
    users = UserModel(db.get_connection()).get_all()
    return render_template('del_user.html', users=users) 


@app.route('/admin')
def admin():
    return render_template('adminmain.html')


@app.route('/adminlog', methods=['GET', 'POST'])
def adminlog():
    form = AdminForm()
    if form.validate_on_submit():
        password = form.password.data
        if password == '789':
            session.pop('username',0)
            session.pop('user_id',0)
            return redirect("/admin")
        return redirect('/')
    return render_template('admin.html', title='Вход для администратора', form=form)


#---------------MAIN------------------
if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

