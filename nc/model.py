from typing import Optional, List

from sqlmodel import SQLModel ,or_, Field, create_engine, Session, select, Relationship
from sqlalchemy.sql.expression import delete as sql_delete
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






# Definição das classes de modelo





















class Contest(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str
	types: Optional[str]
	exams:List['Exam']=Relationship()



class Exam(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	name: str
	year: str
	description: str
	types:str #para indicar se é a prova do concurso ou uma prova montada
	contest_id: int = Field(foreign_key='contest.id')




class Question(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	text: str
	answer: str
	types:str
	tag: Optional[str]


class Question_exam(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	exam_id: int = Field(foreign_key='exam.id')
	question_id: int = Field(foreign_key='question.id')
	


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

def get_all_contest():
	with Session(engine) as session:
		query = select(Contest)
		data = session.exec(query).all()
		return data

def get_id_contest(id:int):
	with Session(engine) as session:
		
		data = session.get(Contest , id)
		return data

def update_contest(contest_id: int, name: str, types: str) -> Contest:
    with Session(engine) as session:
        contest = session.get(Contest, contest_id)
        if contest:
            contest.name = name
            contest.types = types
            session.commit()
            session.refresh(contest)
            return contest
        return None


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



# Operações CRUD para Contest
def create_contest(name: str, types: str) -> Contest:
    with Session(engine) as session:
	    contest = Contest(name=name, types=types)
	    session.add(contest)
	    session.commit()
	    session.refresh(contest)
	    return contest



def get_contest(db: Session, contest_id: int) -> Optional[Contest]:
    return db.get(Contest, contest_id)





def delete_contest(db: Session, contest_id: int):
    db.execute(delete(Contest).where(Contest.id == contest_id))
    db.commit()


# Operações CRUD para Exam
def create_exam(db: Session, contest_id: int, name: str, year: str, description: str, types: str) -> Exam:
    exam = Exam(contest_id=contest_id, name=name, year=year, description=description, types=types)
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam


def get_exam(db: Session, exam_id: int) -> Optional[Exam]:
    return db.get(Exam, exam_id)


def update_exam(db: Session, exam_id: int, name: str, year: str, description: str, types: str) -> Optional[Exam]:
    exam = get_exam(db, exam_id)
    if exam:
        exam.name = name
        exam.year = year
        exam.description = description
        exam.types = types
        db.commit()
        db.refresh(exam)
    return exam


def delete_exam(db: Session, exam_id: int):
    db.execute(delete(Exam).where(Exam.id == exam_id))
    db.commit()


# Operações CRUD para Question
def create_question(db: Session, text: str, answer: str, types: str, tag: str) -> Question:
    question = Question(text=text, answer=answer, types=types, tag=tag)
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


def get_question(db: Session, question_id: int) -> Optional[Question]:
    return db.get(Question, question_id)


def update_question(db: Session, question_id: int, text: str, answer: str, types: str, tag: str) -> Optional[Question]:
    question = get_question(db, question_id)
    if question:
        question.text = text
        question.answer = answer
        question.types = types
        question.tag = tag
        db.commit()
        db.refresh(question)
    return question


def delete_question(db: Session, question_id: int):
    db.execute(delete(Question).where(Question.id == question_id))
    db.commit()
