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
	email:str
	password:str
	#exams:List['Exam']=Relationship()
	



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
	questions:List['Question_exam']=Relationship()



class Question(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	text: str
	associate: Optional[int] 
	types:str
	tag: Optional[str]
	alternatives:List['Alternative']=Relationship()


class Question_exam(SQLModel, table=True):
	id: Optional[int] = Field(default=None, primary_key=True)
	exam_id: int = Field(foreign_key='exam.id')
	question_id: int = Field(foreign_key='question.id')


class Alternative(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    alternative:str
    text:str
    question_id: int = Field(foreign_key='question.id')
    


class Attempt(SQLModel, table=True):

	id: Optional[int] = Field(default=None, primary_key=True)
	user_id: int = Field(foreign_key='user.id')
	exam_id: int = Field(foreign_key='exam.id')
	question_id: int = Field(foreign_key='question.id')
	answer:str
	number: str
	#exams:List['Exam']=Relationship()



engine = create_engine('sqlite:///db.db')

SQLModel.metadata.create_all(engine)

def read_user(email , password):
	with Session(engine) as session:
		query = select(User).where(User.email == email , User.password == password )
		data = session.exec(query).first()

		return data



def get_question_realize(user_id , exam_id):
	with Session(engine) as session:

		query = select(Question)
		#continue
		data = session.exec(query).first()


		question = session.get(Question, data.id)

		return question,question.alternatives





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





def create_question_id(exame_id, tag:str, types:str, text:str , alt_a = None, alt_b = None, alt_c= None, alt_d = None, alt_e = None):
	#exam_id = 
	question = Question(text = text, tag = tag , types = types , associate = None)
	with Session(engine) as session:
		session.add(question)
		session.commit()
		session.refresh(question)
		if alt_a:
			data = Alternative(text = alt_a, alternative = "a", question_id =question.id)
			session.add(data)
			session.commit()
		if alt_b:
			data = Alternative(text = alt_b, alternative = "b", question_id =question.id)
			session.add(data)
			session.commit()
		if alt_c:
			data = Alternative(text = alt_c, alternative ="c", question_id =question.id)
			session.add(data)
			session.commit()
		if alt_d:
			data = Alternative(text = alt_d, alternative = "d", question_id =question.id)
			session.add(data)
			session.commit()
		if alt_e:
			data = Alternative(text = alt_e, alternative = "e", question_id =question.id)
			session.add(data)
			session.commit()

		exame_question = Question_exam(exam_id = exame_id , question_id =question.id )
		session.add(exame_question)
		session.commit()

	return True


def get_questions_by_id_exam(id):
	with Session(engine) as session:
		query = select(Question).join(Question_exam)
		query = query.where( Question_exam.exam_id == id )

		data = session.exec(query).all()

		questions =[x.alternatives for x in data ]
		return questions , data

def get_questions_view(id):
	with Session(engine) as session:
		query = select(Question).join(Question_exam)
		query = query.where( Question_exam.exam_id == id )

		data = session.exec(query).all()

		return data

def get_questions_view2(id):
	with Session(engine) as session:
		query = select(Question).join(Question_exam)
		query = query.where( Question_exam.exam_id == id )

		data = session.exec(query).all()

		questions = []
		for x in data:
			question = session.get(Question, x.id)
			questions.append(question)
			questions.append(question.alternatives)

		
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



def get_id_exam(id:int):
	with Session(engine) as session:
		data = session.get(Exam , id)
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
def create_exam(contest_id: int, name: str, year: str, description: str, types: str) -> Exam:
    exam = Exam(contest_id=contest_id, name=name, year=year, description=description, types=types)
    with Session(engine) as session:

	    session.add(exam)
	    session.commit()
	    session.refresh(exam)
	    
	    if exam:
	    	return exam
    
    return None


def get_exam(db: Session, exam_id: int) -> Optional[Exam]:
    return db.get(Exam, exam_id)

def get_exam_contest(contest_id):

	with Session(engine) as session:
		contest = session.get(Contest, contest_id)
		exams = contest.exams
		return exams

def get_search_question(search):

	with Session(engine) as session:
		query = select(Question).where(Question.text.contains(search))
		data = session.exec(query).all()
		
		return data



def get_exam_by_id(id):
	with Session(engine) as session:
		#question =session.get( Question_exam)  
		exam = session.get(Exam, id)
		
		return exam


def get_all_questions_null(id):
	with Session(engine) as session:
		questions =session.get( Question , id)  
		
		
		return questions



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
