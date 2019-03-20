from flask import *
from loginform import LoginForm
from adminform import AdminForm

from add_news import AddNewsForm
from db_connect import *

db = DB()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found 404'}), 404)

#WORK WITH LOGIN AND LOGOUT-------------------------------------------------

@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
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

   
@app.route('/success', methods=['GET', 'POST'])
def success():
    return render_template('succes.html', title='Заработало')

@app.route('/logout')
def logout():
    session.pop('username',0)
    session.pop('user_id',0)
    return redirect('/login')

#WORK WITH LOGIN AND LOGOUT-------------------------------------------------


#WORK WITH NEWS-------------------------------------------------------------
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
    return render_template('add_news.html', title='Добавление новости',
                           form=form, username=session['username'])

@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news1(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")


@app.route('/news',  methods=['GET'])
def get_news():
    news = NewsModel(db.get_connection()).get_all()
    return jsonify({'news': news})

@app.route('/news/<int:news_id>',  methods=['GET'])
def get_one_news(news_id):
    news = NewsModel(db.get_connection()).get(news_id)
    if not news:
        return jsonify({'error': 'Not found this news'})
    return jsonify({'news': news})

@app.route('/news', methods=['POST'])
def create_news():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in ['title', 'content', 'user_id']):
        return jsonify({'error': 'Bad request'})
    news = NewsModel(db.get_connection())
    news.insert(request.json['title'], request.json['content'],
                request.json['user_id'])
    return jsonify({'success': 'OK'})

@app.route('/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    news = NewsModel(db.get_connection())
    if not news.get(news_id):
        return jsonify({'error': 'Not found'})
    news.delete(news_id)
    return jsonify({'success': 'OK'})

#WORK WITH NEWS-------------------------------------------------------------


#OLD EXAMPLES---------------------------------------------------------------
@app.route('/news_old')
def news():
    with open("sp.json", "rt", encoding="utf8") as f:
        news_list = json.loads(f.read())
    print(news_list)
    return render_template('news.html', news=news_list)

@app.route('/admin')
def admin():
    return 'ok'


@app.route('/adminlog', methods=['GET', 'POST'])
def adminlog():
    form = AdminForm()
    if form.validate_on_submit():
        password = form.password.data
        if password == '789':
            return redirect("/admin")
        return redirect('/#')
    return render_template('admin.html', title='Вход для админа', form=form)

#OLD EXAMPLES---------------------------------------------------------------

if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')

