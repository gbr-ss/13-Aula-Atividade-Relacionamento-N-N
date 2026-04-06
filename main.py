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