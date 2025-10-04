from app import app, db, Usuario

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
     
        db.create_all()
        
        print("Verificando e criando usuários padrão...")
        
        for dados in usuarios_padrao:
          
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
                print(f"- Usuário '{dados['nome']}' criado com sucesso.")
            else:
                print(f"- Usuário '{dados['nome']}' já existe. Nenhuma ação foi tomada.")
        
        db.session.commit()
        print("\nProcesso de verificação concluído!")

if __name__ == '__main__':
    popular_banco()