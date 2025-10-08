from app import app, db, Usuario, Materia, Inscricao, Atividade, Presenca
from datetime import datetime, date

usuarios_padrao = [
    {
        "nome": "Aluno Padrão",
        "email": "aluno@exemplo.com",
        "ra": "1234567",
        "senha": "aluno123",
        "role": "aluno"
    },
    {
        "nome": "Professor Padrão",
        "email": "professor@exemplo.com",
        "ra": None,
        "senha": "prof123",
        "role": "professor"
    },
    {
        "nome": "Diretor Padrão",
        "email": "diretor@exemplo.com",
        "ra": None,
        "senha": "diretor123",
        "role": "diretor"
    }
]

def popular_banco():
    with app.app_context():
        
        print("Recriando o banco de dados...")
        db.drop_all()
        db.create_all()
        
        print("\nCriando usuários padrão...")
        for dados in usuarios_padrao:
       
            if dados['role'] == 'aluno':
                usuario_existente = Usuario.query.filter_by(ra=dados["ra"]).first()
            else:
                usuario_existente = Usuario.query.filter_by(email=dados["email"]).first()
            
            if not usuario_existente:
                novo_usuario = Usuario(
                    nome=dados["nome"],
                    email=dados["email"],
                    ra=dados["ra"],
                    role=dados["role"]
                )
                novo_usuario.set_senha(dados["senha"])
                db.session.add(novo_usuario)
                print(f"- Usuário '{dados['nome']}' criado.")
        

        db.session.commit()
        print("Usuários salvos!")

        print("\nCriando matérias e atribuindo professores...")
        prof = Usuario.query.filter_by(email="professor@exemplo.com").first()
        if prof:
            materia_eng_software = Materia(
                nome="Engenharia de Software",
                professor_id=prof.id
            )
            db.session.add(materia_eng_software)
            db.session.commit()
            print("- Matéria 'Engenharia de Software' criada e atribuída ao Professor Padrão.")


        print("\nInscrevendo aluno em matérias...")
        aluno = Usuario.query.filter_by(ra="1234567").first()
        materia = Materia.query.filter_by(nome="Engenharia de Software").first()
        if aluno and materia:
            nova_inscricao = Inscricao(aluno_id=aluno.id, materia_id=materia.id)
            db.session.add(nova_inscricao)
            db.session.commit()
            print("- Aluno Padrão inscrito em 'Engenharia de Software'.")

    
        print("\nCriando atividades...")
        if materia:
            atividade1 = Atividade(
                titulo="Trabalho 1: Levantamento de Requisitos",
                descricao="Elaborar um documento de requisitos para um sistema de biblioteca.",
                data_entrega=datetime(2025, 10, 20),
                materia_id=materia.id
            )
            db.session.add(atividade1)
            db.session.commit()
            print("- Atividade 'Trabalho 1' criada.")
            
        print("\nRegistrando presenças...")
        if aluno and materia:
            presenca1 = Presenca(data=date(2025, 10, 6), presente=True, aluno_id=aluno.id, materia_id=materia.id)
            presenca2 = Presenca(data=date(2025, 10, 7), presente=False, aluno_id=aluno.id, materia_id=materia.id)
            db.session.add_all([presenca1, presenca2])
            db.session.commit()
            print("- Presenças dos dias 06/10 e 07/10 registradas.")

        print("\nProcesso de popular o banco de dados concluído!")

if __name__ == '__main__':
    popular_banco()