from flask import Flask, render_template, request, redirect, url_for, session # type: ignore
from models import db, Usuario, Materia, Inscricao, Atividade, Entrega, Presenca
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from functools import wraps

app = Flask(__name__)
app.secret_key = "chave_secrety_pim"
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
                return "Acesso Negado! Você não tem permissão para acessar esta página.", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/aluno')
def login_aluno_page():
    return render_template('alunos/Alunos.html')

@app.route('/dashboard/aluno')
@login_required(role='aluno')
def dashboard_aluno():

    aluno = Usuario.query.get(session['user_id'])
    
    inscricoes = aluno.inscricoes
    materias = [inscricao.materia for inscricao in inscricoes]
    
    return render_template('alunos/dashboard_aluno.html', aluno=aluno, materias=materias)

@app.route('/materia/<int:materia_id>')
@login_required(role='aluno')
def materia_detalhes(materia_id):
    aluno_id = session['user_id']
    materia = Materia.query.get_or_404(materia_id)
    
    atividades = Atividade.query.filter_by(materia_id=materia.id).all()
    
    entregas = Entrega.query.filter(
        Entrega.aluno_id == aluno_id,
        Entrega.atividade_id.in_([a.id for a in atividades])
    ).all()
    notas_entregas = {entrega.atividade_id: entrega.nota for entrega in entregas}

    presencas = Presenca.query.filter_by(aluno_id=aluno_id, materia_id=materia.id).order_by(Presenca.data.desc()).all()

    return render_template(
        'alunos/materia_detalhes.html', 
        materia=materia, 
        atividades=atividades,
        notas_entregas=notas_entregas,
        presencas=presencas
    )

@app.route('/atividade/<int:atividade_id>', methods=['GET', 'POST'])
@login_required(role='aluno')
def responder_atividade(atividade_id):
    aluno_id = session['user_id']
    atividade = Atividade.query.get_or_404(atividade_id)
    
    entrega_existente = Entrega.query.filter_by(
        aluno_id=aluno_id, 
        atividade_id=atividade.id
    ).first()

    if request.method == 'POST':

        if not entrega_existente:
            conteudo_resposta = request.form.get('resposta')
            nova_entrega = Entrega(
                conteudo=conteudo_resposta,
                aluno_id=aluno_id,
                atividade_id=atividade.id
            )
            db.session.add(nova_entrega)
            db.session.commit()

            return redirect(url_for('materia_detalhes', materia_id=atividade.materia_id))


    return render_template(
        'alunos/responder_atividade.html', 
        atividade=atividade, 
        entrega=entrega_existente
    )

@app.route('/login/professor')
def login_professor_page():
    return render_template('professores/professor.html')

@app.route('/login/diretor')
def login_diretor_page():
    return render_template('Diretoria/login_diretor.html')

@app.route('/login', methods=['POST'])
def login():
    
    role = request.form.get('role')
    password = request.form.get('password')
    usuario = None

    if role == 'aluno':
        ra = request.form.get('ra')
        usuario = Usuario.query.filter_by(ra=ra, role='aluno').first()
    elif role in ['professor', 'diretor']:
        email = request.form.get('email')
        usuario = Usuario.query.filter_by(email=email, role=role).first()

    if usuario and usuario.check_senha(password):
        
        session['authenticated'] = True
        session['user_id'] = usuario.id
        session['username'] = usuario.nome
        session['role'] = usuario.role

        if usuario.role == 'aluno':
            return redirect(url_for('dashboard_aluno'))
        elif usuario.role == 'professor':
            return redirect(url_for('dashboard_professor'))
        elif usuario.role == 'diretor':
            return redirect(url_for('dashboard_diretor'))
    
    return '<h1>Usuário ou senha inválidos.</h1><a href="/">Voltar</a>'


@app.route('/dashboard/professor')
@login_required(role='professor')
def dashboard_professor():
    return f"<h1>Bem-vindo à sua área, Professor {session['username']}!</h1><a href='/logout'>Sair</a>"

@app.route('/dashboard/diretor')
@login_required(role='diretor')
def dashboard_diretor():
    return f"<h1>Bem-vindo à sua área, Diretor {session['username']}!</h1><a href='/logout'>Sair</a>"

@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)