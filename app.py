from flask import Flask, render_template, request, redirect, url_for, session
from models import db, Usuario, Materia, Inscricao, Atividade, Entrega, Presenca, Turma
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = "chave_secreta_pim"
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

@app.route('/dashboard/professor')
@login_required(role='professor')
def dashboard_professor():
    
    professor = Usuario.query.get(session['user_id'])
    
    materias = Materia.query.filter_by(professor_id=professor.id).all()
    
    return render_template('professores/dashboard_professor.html', professor=professor, materias=materias)

@app.route('/professor/materia/<int:materia_id>')
@login_required(role='professor')
def materia_detalhes_professor(materia_id):
    materia = Materia.query.get_or_404(materia_id)
    
 
    if materia.professor_id != session['user_id']:
        return "Acesso Negado!", 403
        
 
    inscricoes = Inscricao.query.filter_by(materia_id=materia.id).all()
    alunos = [inscricao.aluno for inscricao in inscricoes]
    
  
    atividades = Atividade.query.filter_by(materia_id=materia.id).order_by(Atividade.data_entrega.desc()).all()

    return render_template('professores/materia_detalhes_prof.html', materia=materia, alunos=alunos, atividades=atividades)


@app.route('/professor/materia/<int:materia_id>/criar_atividade', methods=['GET', 'POST'])
@login_required(role='professor')
def criar_atividade(materia_id):
    materia = Materia.query.get_or_404(materia_id)

    if materia.professor_id != session['user_id']:
        return "Acesso Negado!", 403

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        data_entrega_str = request.form.get('data_entrega')
        

        data_entrega = datetime.strptime(data_entrega_str, '%Y-%m-%d')

        nova_atividade = Atividade(
            titulo=titulo,
            descricao=descricao,
            data_entrega=data_entrega,
            materia_id=materia.id
        )
        db.session.add(nova_atividade)
        db.session.commit()
        
        return redirect(url_for('materia_detalhes_professor', materia_id=materia.id))

    return render_template('professores/criar_atividade.html', materia=materia)

@app.route('/login/professor')
def login_professor_page():
    return render_template('professores/professor.html')

@app.route('/dashboard/diretor')
@login_required(role='diretor')
def dashboard_diretor():

    num_alunos = Usuario.query.filter_by(role='aluno').count()
    num_professores = Usuario.query.filter_by(role='professor').count()
    num_materias = Materia.query.count()
    
    return render_template(
        'Diretoria/dashboard_diretor.html',
        num_alunos=num_alunos,
        num_professores=num_professores,
        num_materias=num_materias
    )

@app.route('/login', methods=['POST'])
def login():
    print("=== TENTATIVA DE LOGIN ===")
    print(f"Dados recebidos: {dict(request.form)}")
    
    
    if 'ra' in request.form and request.form.get('ra'):
        
        ra = request.form.get('ra')
        password = request.form.get('password')
        print(f"Tentando login como ALUNO - RA: {ra}")
        
        usuario = Usuario.query.filter_by(ra=ra, role='aluno').first()
        print(f"Aluno encontrado: {usuario}")
        
    elif 'email' in request.form and request.form.get('email'):
       
        email = request.form.get('email')
        password = request.form.get('password')
        print(f"Tentando login com EMAIL: {email}")
        
        usuario = Usuario.query.filter_by(email=email).first()
        print(f"Usuário encontrado: {usuario}")
        
        if usuario and usuario.role not in ['professor', 'diretor']:
            print("Usuário encontrado mas não é professor/diretor")
            usuario = None
    else:
        usuario = None

    if usuario and usuario.check_senha(password):
        print("✅ SENHA CORRETA - LOGIN BEM-SUCEDIDO!")
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
    
    print(" LOGIN FALHOU!")
    return '<h1>Usuário ou senha inválidos.</h1><a href="/">Voltar</a>'

@app.route('/diretor/professores')
@login_required(role='diretor')
def gerenciar_professores():
    professores = Usuario.query.filter_by(role='professor').all()
    return render_template('Diretoria/gerenciar_professores.html', professores=professores)

@app.route('/diretor/cadastrar_professor', methods=['GET', 'POST'])
@login_required(role='diretor')
def cadastrar_professor():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if Usuario.query.filter_by(email=email).first():
            return "Erro: Este e-mail já está cadastrado.", 400

        novo_professor = Usuario(
            nome=nome,
            email=email,
            role='professor'
        )
        novo_professor.set_senha(senha)
        
        db.session.add(novo_professor)
        db.session.commit()
        
        return redirect(url_for('gerenciar_professores'))

    return render_template('Diretoria/Cadastro_Professores.html')

@app.route('/diretor/turmas')
@login_required(role='diretor')
def gerenciar_turmas():
    turmas = Turma.query.all()
    return render_template('Diretoria/gerenciar_turmas.html', turmas=turmas)

@app.route('/diretor/cadastrar_turma', methods=['GET', 'POST'])
@login_required(role='diretor')
def cadastrar_turma():
    if request.method == 'POST':
        nome = request.form.get('nome')

        if Turma.query.filter_by(nome=nome).first():
            
            return "Erro: Já existe uma turma com este nome.", 400

        nova_turma = Turma(nome=nome)
        db.session.add(nova_turma)
        db.session.commit()
        
        return redirect(url_for('gerenciar_turmas'))

    return render_template('Diretoria/Cadastro_Turmas.html')

@app.route('/diretor/alunos')
@login_required(role='diretor')
def gerenciar_alunos():
    alunos = Usuario.query.filter_by(role='aluno').all()
    return render_template('Diretoria/gerenciar_alunos.html', alunos=alunos)

@app.route('/diretor/cadastrar_aluno', methods=['GET', 'POST'])
@login_required(role='diretor')
def cadastrar_aluno():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        ra = request.form.get('ra')
        senha = request.form.get('senha')

        if Usuario.query.filter_by(email=email).first() or Usuario.query.filter_by(ra=ra).first():
            return "Erro: Email ou RA já cadastrado.", 400

        novo_aluno = Usuario(
            nome=nome,
            email=email,
            ra=ra,
            role='aluno'
        )
        novo_aluno.set_senha(senha)
        db.session.add(novo_aluno)
        db.session.commit()
        
        return redirect(url_for('gerenciar_alunos'))

    return render_template('Diretoria/Cadastro_Alunos.html')


@app.route('/diretor/materias')
@login_required(role='diretor')
def gerenciar_materias():
    materias = Materia.query.all()
    professores = Usuario.query.filter_by(role='professor').all()
    return render_template('Diretoria/gerenciar_materias.html', materias=materias, professores=professores)


@app.route('/diretor/cadastrar_materia', methods=['POST'])
@login_required(role='diretor')
def cadastrar_materia():
    nome = request.form.get('nome')
    professor_id = request.form.get('professor_id')

    if Materia.query.filter_by(nome=nome).first():
        return "Erro: Já existe uma matéria com este nome.", 400
    
    nova_materia = Materia(nome=nome, professor_id=professor_id)
    db.session.add(nova_materia)
    db.session.commit()

    return redirect(url_for('gerenciar_materias'))

@app.route('/logout')
def logout():
    session.clear() 
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)