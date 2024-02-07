from typing import Optional, List
from sqlmodel import SQLModel ,or_, Field, create_engine, Session, select, Relationship
from sqlalchemy import func


db = SQLModel()

def configure(app):
    app.db = db




class Person(SQLModel, table=True):
	"""docstring for Person  -  tabela para usuarios do sistema"""
	id: Optional[int] = Field(default=None, primary_key=True)
	name:str
	password:str
	registration:str
	types:str  # do usuario, master ou comum
	todos:List['Todo']=Relationship()


class Todo(SQLModel, table=True):
	"""
	docstring for Todo   -   tabela para as acoes do sistema,
	adicionar valor
	devolver valor 
	"""
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str
	observation: str
	nature:str
	value:str
	date:str
	status:str
	person_id: int = Field(foreign_key='person.id')
	

class User(SQLModel, table=True):
	"""docstring for User  -  tabela para cotistas"""
	id: Optional[int] = Field(default=None, primary_key=True)
	name:str
	cpf:str
	email:str
	birth:str
	telephone:str
	cell:str
	status:str
	code:str
	income_tax:str
	



# Definindo o modelo de pergunta

class Question(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	text: str
	answer: str
	types:str
	




engine = create_engine('sqlite:///db.db')

SQLModel.metadata.create_all(engine)



def create_questions_from_dict(questions_dict: dict) -> List[Question]:
    questions = []
    for statement, answer in questions_dict.items():
    	question = Question(text=statement, answer=answer , types = "asd")
    	with Session(engine) as session:
    		session.add(question)
    		session.commit()
    		session.refresh(question)
    		questions.append(question)
    return questions

def get_all_questions() -> List[Question]:
    with Session(engine) as session:
        return session.exec(select(Question)).all()


# Operações CRUD


def list_quote_all(filters:str, offset:str, per_page:str ):
	with Session(engine) as session:
		query = select(Quota)
		if filters:
			query = query.where( or_(Quota.code.contains(filters),Quota.old.contains(filters)) )
		
		query = query.offset(offset).limit(per_page)

				
		data = session.exec(query).all()
		return data


# Criar uma nova pergunta
def create_question(text: str, answer: str) -> Question:
    question = Question(text=text, answer=answer)
    with Session(engine) as session:
        session.add(question)
        session.commit()
        session.refresh(question)
    return question



# Obter uma pergunta pelo ID
def get_question_by_id(question_id: int) -> Question:
    with Session(engine) as session:
        return session.get(Question, question_id)


# Obter todas as perguntas
def get_all_questions() -> List[Question]:
    with Session(engine) as session:
        return session.exec(select(Question)).all()


# Atualizar uma pergunta existente
def update_question(question_id: int, text: str, answer: str) -> Question:
    with Session(engine) as session:
        question = session.get(Question, question_id)
        if question:
            question.text = text
            question.answer = answer
            session.commit()
            session.refresh(question)
            return question
        return None


# Excluir uma pergunta
def delete_question(question_id: int) -> None:
    with Session(engine) as session:
        question = session.get(Question, question_id)
        if question:
            session.delete(question)
            session.commit()


