from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Usuario 
from functools import wraps

app = Flask(__name__)
app.secret_key = "chave_secreta_do_projeto_pim"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///academico.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def login_required(role="qualquer"):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'authenticated' not in session:
                return redirect(url_for('index')) 
            if role != "qualquer" and session.get('role') != role:
                return "Acesso Negado!", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    if 'authenticated' in session:
        
        role = session.get('role')
        if role == 'aluno':
            return redirect(url_for('dashboard_aluno'))
        elif role == 'professor':
            return redirect(url_for('dashboard_professor'))
        elif role == 'diretor':
            return redirect(url_for('dashboard_diretor'))
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    perfil = request.form.get('perfil')

    if perfil == 'aluno':
        ra_aluno = request.form.get('ra')
        usuario = Usuario.query.filter_by(ra=ra_aluno, role='aluno').first()
        
        if usuario:
            session['authenticated'] = True
            session['user_id'] = usuario.id
            session['username'] = usuario.nome
            session['role'] = usuario.role
            return redirect(url_for('dashboard_aluno'))
        else:
        
            return "RA de aluno inválido ou não encontrado.", 401

    elif perfil in ['professor', 'diretor']:
        email = request.form.get('email')
        senha = request.form.get('password')
        usuario = Usuario.query.filter_by(email=email, role=perfil).first()
        
        if usuario and usuario.check_senha(senha):
            session['authenticated'] = True
            session['user_id'] = usuario.id
            session['username'] = usuario.nome
            session['role'] = usuario.role
            
            if perfil == 'professor':
                return redirect(url_for('dashboard_professor'))
            else:
                return redirect(url_for('dashboard_diretor'))
        else:
            return "Email ou senha inválidos.", 401
    
    return "Erro no processo de login.", 400

@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('index'))

@app.route('/login/aluno')
def login_aluno_page():

    return render_template('alunos/Alunos.html')

@app.route('/login/professor')
def login_professor_page():
   
    return render_template('professores/professor.html')

@app.route('/login/diretor')
def login_diretor_page():
   
    return render_template('Diretoria/login_diretor.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)