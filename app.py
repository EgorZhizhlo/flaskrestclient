import aiohttp
from flask import Flask, redirect, url_for, render_template, session, request
import datetime
from werkzeug.security import generate_password_hash

serverURL = "http://127.0.0.2:8000"
o_key = "CgFuhy@g9XBc-6NEqTZ2ESUUc-6Z*SppVR#Nua"
app = Flask(__name__)
app.secret_key = '6NECgFuhy@ESUUc-6Z*Sp2ESU#Nua-Z*S6NEqphS6y@g'
app.config['SESSION_TYPE'] = 'filesystem'
app.permanent_session_lifetime = datetime.timedelta(days=365)
"""NOTES: Сделать выпадающее меню при нажатии на email. Добавить время создания поста.
CgFuhy@g9XBc"""


@app.route('/', methods=['GET', 'POST'])
async def home():
    async with aiohttp.ClientSession(serverURL) as s:
        async with s.get("/", json=({
            'operation_key': generate_password_hash(o_key),
        })) as rsp, s.get("/login/checkstatus/", json=({
            'operation_key': generate_password_hash(o_key),
            'user': {
                'email': session.get('email') if session.get('email') is not None else "_"
            }
        })) as rsp2:
            rsp, rsp2 = eval(await rsp.text()), eval(await rsp2.text())
            return render_template('main.html', page=request.args.get('page', 1, type=int),
                                   posts=rsp,
                                   email=session.get('email'),
                                   username=session.get('username'),
                                   admin=rsp2['data'] if rsp2['data'] is not None else 0
                                   )


@app.route('/about/', methods=['GET'])
async def about():
    async with aiohttp.ClientSession(serverURL) as s:
        async with s.get("/about/", json=({
            'operation_key': generate_password_hash(o_key),
        })) as rsp, s.get("/login/checkstatus/", json=({
            'operation_key': generate_password_hash(o_key),
            'user': {
                'email': session.get('email') if session.get('email') is not None else "_"
            }
        })) as rsp2:
            rsp, rsp2 = eval(await rsp.text()), eval(await rsp2.text())
            return render_template('about.html', info=rsp, email=session.get('email'),
                                   username=session.get('username'),
                                   admin=rsp2['data'] if rsp2['data'] is not None else 0)


@app.route('/aboutpost/<int:post_id>/', methods=['GET'])
async def about_post(post_id):
    async with aiohttp.ClientSession(serverURL) as s:
        async with s.get(f"/aboutpost/{post_id}/", json=({
            'operation_key': generate_password_hash(o_key),
        })) as rsp, s.get("/login/checkstatus/", json=({
            'operation_key': generate_password_hash(o_key),
            'user': {
                'email': session.get('email') if session.get('email') is not None else "_"
            }
        })) as rsp2:
            rsp, rsp2 = eval(await rsp.text()), eval(await rsp2.text())
            return render_template('aboutpost.html', post=rsp, email=session.get('email'),
                                   username=session.get('username'),
                                   admin=rsp2['data'] if rsp2['data'] is not None else 0)


@app.route('/login/', methods=['GET', 'POST'])
async def login():
    email = request.form.get('email')
    password = request.form.get('password')
    async with aiohttp.ClientSession(serverURL) as s:
        async with s.post("/login/", json=({
            'operation_key': generate_password_hash(o_key),
            'user': {
                'email': email,
                'password': password
            }
        })) as rsp, s.get("/login/checkstatus/", json=({
            'operation_key': generate_password_hash(o_key),
            'user': {
                'email': session.get('email') if session.get('email') is not None else "_"
            }
        })) as rsp2:
            rsp, rsp2 = eval(await rsp.text()), eval(await rsp2.text())
            if rsp and 'data' in rsp and 'email' in rsp and 'username' in rsp:
                session['email'] = rsp['email']
                session['username'] = rsp['username']
                return render_template("message.html", message=rsp['data'],
                                       email=rsp['email'], username=rsp['username'],
                                       admin=rsp2['data'] if rsp2['data'] is not None else 0)
            return render_template("message.html", message=rsp['data'], username=None, admin=0)


@app.route('/registration/', methods=['GET', 'POST'])
async def registration():
    new_username = request.form.get('username')
    new_email = request.form.get('email')
    new_password = request.form.get('password')
    new_password_rep = request.form.get('password_rep')
    async with aiohttp.ClientSession(serverURL) as s:
        async with s.post("/registration/", json=({
            'operation_key': generate_password_hash(o_key),
            'user': {
                'username': new_username,
                'email': new_email,
                'password': new_password,
                'password_rep': new_password_rep
            }
        })) as rsp, s.get("/login/checkstatus/", json=({
            'operation_key': generate_password_hash(o_key),
            'user': {
                'email': session.get('email') if session.get('email') is not None else "_"
            }
        })) as rsp2:
            rsp, rsp2 = eval(await rsp.text()), eval(await rsp2.text())
            if rsp and 'data' in rsp and 'id' in rsp:
                if rsp['id'] == 1:
                    session['email'] = rsp['email']
                    session['username'] = rsp['username']
                return render_template("message.html", message=rsp['data'],
                                       email=rsp['email'], username=rsp['username'],
                                       admin=rsp2['data'] if rsp2['data'] is not None else 0)
            return render_template("message.html", message=rsp['data'],
                                   email=None, username=None, admin=0)


@app.route('/logout/')
async def delete_visits():
    session.pop('email', None)
    session.pop('username', None)
    return redirect(url_for('home'))


@app.route('/createpost/', methods=['GET'])
async def create_post():
    async with aiohttp.ClientSession(serverURL) as s:
        async with s.get("/login/checkstatus/", json=({
            'operation_key': generate_password_hash(o_key),
            'user': {
                'email': session.get('email') if session.get('email') is not None else "_"
            }
        })) as rsp:
            rsp = eval(await rsp.text())
            return render_template("createpost.html", email=session.get('email'),
                                   username=session.get('username'),
                                   admin=rsp['data'] if rsp['data'] is not None else 0
                                   )


@app.route('/createpost/postrequest', methods=['GET', 'POST'])
async def create_post_postr():
    title = request.form.get('title')
    text = request.form.get('text')
    async with aiohttp.ClientSession(serverURL) as s:
        async with s.post("/createpost/", json=({
            'operation_key': generate_password_hash(o_key),
            'email': session.get('email'),
            'post': {
                "title": title,
                "author": session.get('username'),
                "text": text
            }
        })) as rsp, s.get("/login/checkstatus/", json=({
            'operation_key': generate_password_hash(o_key),
            'user': {
                'email': session.get('email') if session.get('email') is not None else ""
            }
        })) as rsp2:
            rsp, rsp2 = eval(await rsp.text()), eval(await rsp2.text())
            if rsp and 'data' in rsp and session.get('email') and session.get('username'):
                return render_template("message.html", message=rsp['data'],
                                       email=session['email'], username=session['username'],
                                       admin=rsp2['data'] if rsp2['data'] is not None else 0)
    return render_template("message.html", message=rsp['data'],
                           email=None, username=None, admin=0)


@app.route('/search/', methods=['GET', 'POST'])
async def search():
    search = '%{}%'.format(request.args.get('search'))
    async with aiohttp.ClientSession(serverURL) as s:
        async with s.post("/search/", json=({
            'operation_key': generate_password_hash(o_key),
            'search': search
        })) as rsp, s.get("/login/checkstatus/", json=({
            'operation_key': generate_password_hash(o_key),
            'user': {
                'email': session.get('email') if session.get('email') is not None else ""
            }
        })) as rsp2:
            rsp, rsp2 = eval(await rsp.text()), eval(await rsp2.text())
            return render_template('main.html', page=request.args.get('page', 1, type=int),
                                   posts=rsp,
                                   email=session.get('email'),
                                   username=session.get('username'),
                                   admin=rsp2['data'] if rsp2['data'] is not None else 0)


@app.route('/adminpanel/', methods=['GET'])
async def adminpanel():
    async with aiohttp.ClientSession(serverURL) as s:
        async with s.get("/login/checkstatus/", json=({
            'operation_key': generate_password_hash(o_key),
            'user': {
                'email': session.get('email') if session.get('email') is not None else "_"
            }
        })) as rsp:
            rsp = eval(await rsp.text())
            return render_template('adminpanel.html', email=session.get('email'),
                                   username=session.get('username'),
                                   admin=rsp['data'] if rsp['data'] is not None else 0)


if __name__ == '__main__':
    app.run()
