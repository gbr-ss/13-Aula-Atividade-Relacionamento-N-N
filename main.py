from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class Serie(Base):
    __tablename__ = "serie"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    nota = Column(Float, nullable=False)
    ano = Column(Float, nullable=False)
    genero = Column(String(100), nullable=True)

    episodios = relationship("Episodio", back_populates="serie")

    def __repr__(self):
        return f"Serie: ID = {self.id} - Nome = {self.nome} - Nota = {self.nota} - Ano = {self.ano} - Genero = {self.genero}"
    

class Episodio(Base):
    __tablename__ = "episodio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(100), nullable=False)
    temp_ep = Column(Float, nullable=False)
    descricao = Column(String(50), nullable=True)
    faixa_etaria = Column(Float,nullable=True)

    serie_id = Column(Integer,ForeignKey("serie.id"))

    serie = relationship("Serie", back_populates="episodios")

    def __repr__(self):
        return f"Serie: ID = {self.id} - Titulo = {self.titulo} - Tempo de episodio = {self.temp_ep} - Descrição = {self.descricao} - Faixa Etaria = {self.faixa_etaria}"

engine = create_engine("sqlite:///Entreterimento.db", echo=False)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)

def cadastrar_serie():
    nome_serie = input("digite o nome da serie: ").strip().capitalize()
    nota_serie = int(input("Digite a nota da serie: "))
    ano_serie = int(input("Digite a ano da serie: "))
    genero_serie = input("Digite o genero da serie: ")

    with Session() as session:
        try:
            serie = Serie(nome=nome_serie, nota=nota_serie, ano = ano_serie, genero = genero_serie )
            session.add(serie)
            session.commit()
            print("Serie Cadastrada com sucesso!✔😎")
        except Exception as erro:
            session.rollback()
            print(f"ocorreu um erro {erro}")

def cadastrar_episodio():
    nome_ep = input("Digite o nome do episodio: ").strip().capitalize()
    temp_ep = int(input(f"Digite o tempo do {nome_ep}: "))
    descricao_ep = input(f"Digite a descrição  do {nome_ep}: ").capitalize()
    faixa_etaria_ep = input(f"Digite a faixa etaria do {nome_ep}: ").capitalize()

    buscar_serie = input(f"digite o nome da serie do ep {nome_ep}:").strip().capitalize()
     
    with Session() as session:
        try:
            serie =session.query(Serie).filter_by(nome =buscar_serie).first()
            if serie ==None:
                print("nao encontrei nenhuma serie com esse nome.")
                return
            else:
                episodio = Episodio(titulo=nome_ep, temp_ep=temp_ep, descricao = descricao_ep, faixa_etaria = faixa_etaria_ep,serie_id=serie.id)
                session.add(episodio)
                session.commit()
                print(f"episodio cadastrado com sucesso!")
        except Exception as erro:        
            session.rollback()
            print(f"Ocorreu um erro {erro}")
            
def listar_Serie():
    with Session() as session:
        try:
            serie = session.query(Serie).all()
            for d in serie:
                print(f"\n{d}")
                for episodio in d.episodios:
                    print(episodio)
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")    

def serie_especifico(id_episodio):
    with Session() as session:
        try:
            episodio = session.query(Episodio).filter(Episodio.id == id_episodio).first()
            if not episodio:
                print("Episodio não encontrado.")
                return
            print("Episodio encontrado:", episodio)
            serie = episodio.serie
            print("Série do episódio:")
            print(serie.nome)
        except Exception as erro:
            session.rollback()
            print(f"Ocorreu um erro {erro}")