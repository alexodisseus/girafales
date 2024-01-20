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
	adresses:List['Address']=Relationship()
	accounts:List['Account']=Relationship()
	quotas:List['Quota']=Relationship()


class Address(SQLModel, table=True):
	"""docstring for Address"""
	id: Optional[int] = Field(default=None, primary_key=True)
	street:str
	number:str 
	city:str
	state:str
	cep:str
	user_id: int = Field(foreign_key='user.id')


class Account(SQLModel, table=True):
	"""docstring for Account"""
	id: Optional[int] = Field(default=None, primary_key=True)
	bank:str
	agency:str
	number_account:str
	name_bank:str
	user_id: int = Field(foreign_key='user.id')


class Quota(SQLModel, table=True):
	"""docstring for Quota"""
	id: Optional[int] = Field(default=None, primary_key=True)
	code:str
	status:str
	date:str
	old:str
	grouping:str #para agrupar tipo 'z a b' 

	user_id: int = Field(foreign_key='user.id')


class Closure(SQLModel, table=True):
	"""docstring for Closure"""
	id: Optional[int] = Field(default=None, primary_key=True)
	value:str
	date:str
	status:str
	type:str

class ReportPayment(SQLModel, table=True):
	"""docstring for repor payment"""
	id: Optional[int] = Field(default=None, primary_key=True)
	value:str
	date:str
	status:str
	amount:str

	user_id: int = Field(foreign_key='user.id')
	closure_id: int = Field(foreign_key='closure.id')

class Titulo(SQLModel, table=True):
	"""docstring for titulos, exportar para quotes"""
	
	id: Optional[int] = Field(default=None, primary_key=True)
	numero:str
	situacao:str
	cotista:str
	cotas:str
	data_aquis:str
	mes_transf:str
	ano_transf:str
	cotista2:str


class RuleTribute(SQLModel, table=True):
	"""docstring for titulos, exportar para quotes"""
	id: Optional[int] = Field(default=None, primary_key=True)
	status:str
	isento:str
	faixa1:str
	faixa2:str
	faixa3:str
	maximo:str
	date:str








engine = create_engine('sqlite:///db.db')

SQLModel.metadata.create_all(engine)





def create_shareholder(
	name:str, 
	email: str, 
	cpf: str, 
	birth: str, 
	telephone: str, 
	cell: str, 
	
	):
	with Session(engine) as session:
		session.add(User(name=name, email=email, cpf=cpf, birth=birth, telephone=telephone, cell=cell, status = "ativo" , code = "123"))
		session.commit()



def update_shareholder(
	name:str, 
	email: str, 
	cpf: str, 
	birth: str, 
	telephone: str, 
	cell: str,
	street:str,
	number:str,
	city:str,
	state:str,
	cep:str,
	banco:str,
	agencia:str,
	conta:str,
	id,
	
	):
	with Session(engine) as session:
		
		user = session.get(User, id)
		if name:
			user.name = name
		if email:
			user.email = email
		if cpf:
			user.cpf = cpf
		if birth:
			user.birth = birth
		if telephone:
			user.telephone = telephone
		if cell:
			user.cell = cell
		
		address = session.get(Address, user.id)
		if street:
			address.street=street
		if number:
			address.number=number
		if cep:
			address.cep=cep
		if city:
			address.city=city
		if state:
			address.state=state
		

		account = session.get(Account, user.id)
		if banco:
			account.bank = banco
		if agencia:
			account.agency = agencia
		if conta:
			account.number_account = conta

		session.commit()
		


def list_users_shareholder(filters:str, offset:str, per_page:str ):
	with Session(engine) as session:
		query = select(User)
		if filters:
			query = query.where( or_(User.name.contains(filters),User.cpf.contains(filters) ,User.code.contains(filters) ) )
		
		
		

		query = query.offset(offset).limit(per_page)

		data = session.exec(query).all()
		print(data)
		return data

def list_quote(filters:str, offset:str, per_page:str ):
	with Session(engine) as session:
		query = select(Quota)
		if filters:
			query = query.where( or_(Quota.code.contains(filters),Quota.old.contains(filters)) )
		
		query = query.offset(offset).limit(per_page)

				
		data = session.exec(query).all()
		return data




def list_quote_all(filters:str, offset:str, per_page:str ):
	with Session(engine) as session:
		query = select(Quota)
		if filters:
			query = query.where( or_(Quota.code.contains(filters),Quota.old.contains(filters)) )
		
		query = query.offset(offset).limit(per_page)

				
		data = session.exec(query).all()
		return data

def count_users_shareholder(filters:str, offset:str, per_page:str ):
	with Session(engine) as session:
		query = select(User)
		if filters:
			query = query.where( or_(User.name.contains(filters),User.cpf.contains(filters),User.code.contains(filters)) )
		
		data = session.exec(query).all()
		return len(data)
		
		
		
		
def count_quote(filters:str, offset:str, per_page:str ):
	with Session(engine) as session:
		query = select(Quota)
		if filters:
			query = query.where( or_(Quota.code.contains(filters),Quota.old.contains(filters)) )
		
		data = session.exec(query).all()
		return len(data)

def view_user_shareholder(id:str):
	with Session(engine) as session:
		query = select(User,Address,Account).join(Address).join(Account)
		query = query.where(User.id == id )

		data = session.exec(query).first()
		
		return data


def view_user_shareholder_quote(id:str):
	with Session(engine) as session:
		user = session.get(User, id)
		
		
		title = user.quotas
		
		contagem = [x.grouping for x in title]
		q = sum([int(post) for post in contagem])
		return [title,user , q]
		

"""
def view_user_shareholder_quote2(id:str):
	with Session(engine) as session:
		user = session.get(User, id)
		
		query = select(Titulo).where(Titulo.cotista== user.code , Titulo.situacao == "A")
		title = session.exec(query).all()

		contagem = [x.cotas for x in title]
		q = sum([int(post) for post in contagem])
		return [title,user , q]
		

"""



def list_report(filters:str, offset:str, per_page:str ):
	with Session(engine) as session:
		query = select(Quota)
		if filters:
			query = query.where( or_(Quota.code.contains(filters),Quota.old.contains(filters)) )
		
		query = query.offset(offset).limit(per_page)

				
		data = session.exec(query).all()
		return data

def list_report_resume_id(id):
	with Session(engine) as session:
		
		query= select(
			Account.bank,
			ReportPayment.value,
			func.sum(ReportPayment.amount),
			func.count(ReportPayment.amount),
			Account.name_bank,

			).join(User, ReportPayment.user_id == User.id).join(
			Account, User.id == Account.user_id).group_by(Account.bank)

		data = session.exec(query).all()
		return data

def list_report_comum(id , bank = None ):
	with Session(engine) as session:
		
		query= select(
			ReportPayment,
			User,
			Account
			).join(
			User, ReportPayment.user_id == User.id
			).join(
			Account, User.id == Account.user_id
			).where(
			ReportPayment.closure_id == id,
			Account.bank == bank if bank else ReportPayment.closure_id == id,
			ReportPayment.amount > 5,

			).order_by(
			Account.bank.desc()
			)
		data = session.exec(query).all()
		return data

def list_report_full(id , bank = None ):
	with Session(engine) as session:
		
		query= select(
			ReportPayment,
			User,
			Account
			).join(
			User, ReportPayment.user_id == User.id
			).join(
			Account, User.id == Account.user_id
			).where(
			Account.bank == bank if bank else ReportPayment.closure_id,
			ReportPayment.status == 'pendente'
			).order_by(
			Account.bank.desc()
			).order_by(
			User.name
			)
		data = session.exec(query).all()
		return data
		
		
def get_closure(id):
	with Session(engine) as session:
		
		data = session.get(Closure , id)
		return data
		
def tribute_last():
	with Session(engine) as session:
		asd = session.get(RuleTribute, 1)
		return asd

def count_report(filters:str, offset:str, per_page:str ):
	with Session(engine) as session:
		query = select(Quota)
		if filters:
			query = query.where( or_(Quota.code.contains(filters),Quota.old.contains(filters)) )
		
		data = session.exec(query).all()
		return len(data)




def list_closure(filters:str, offset:str, per_page:str ):
	with Session(engine) as session:
		query = select(Closure)
		if filters:
			query = query.where( or_(Quota.code.contains(filters),Quota.old.contains(filters)) )
		
		query = query.offset(offset).limit(per_page)

				
		data = session.exec(query).all()
		return data


def count_closure(filters:str, offset:str, per_page:str ):
	with Session(engine) as session:
		query = select(Quota)
		if filters:
			query = query.where( or_(Quota.code.contains(filters),Quota.old.contains(filters)) )
		
		data = session.exec(query).all()
		return len(data)


def create_closure(
	date: str, 
	value:str, 
	
	):
	with Session(engine) as session:
		session.add(Closure(value=value, date=date, status = "pendente"))
		session.commit()


def list_closure_pending(id=None):
	with Session(engine) as session:
		query = select(Closure).where( Closure.status == "pendente" )
		if id:
		    query = query.where(
		        Closure.id == id)
		
				
		data = session.exec(query).all()
		return data



def create_report_pay_check(id):
	with Session(engine) as session:
		query = select(ReportPayment).where( ReportPayment.closure_id == id )
		data = session.exec(query).first()
		if data:
			return None
		else:
			return True

def list_payment_filters(page):
	with Session(engine) as session:
		"""
		query = select(
			ReportPayment
			)
		data =session.exec(query).all()
		"""
		offset = page
		per_page = 10
		query= select(
			ReportPayment,
			User,
			Account
			).join(
			User, ReportPayment.user_id == User.id
			).join(
			Account, User.id == Account.user_id
			).where(
			ReportPayment.status == 'pendente'
			).order_by(
			Account.bank.desc()
			).order_by(
			User.name
			).offset(offset).limit(per_page)

		data = session.exec(query).all()


		return data


def create_report_pay_auto(id):
	with Session(engine) as session:
		#buscar todos os titulos e gravar no pagamento como pendente

		query = select(
			User,
			func.sum(Quota.grouping),
			
			).join(
			Quota
			).group_by(User.name).having(func.sum(Quota.grouping) > 0)
		data =session.exec(query).all()

		return data




def save_report(data, fechamento):
	with Session(engine) as session:
		"""
		print(fechamento)
		print(data[0])
		print(data[0][1])
		"""
		
		for x in data:
		    a = ReportPayment()
		    a.value=fechamento[0].value
		    a.date=fechamento[0].date
		    a.status="pendente"
		    a.amount=x[1]
		    a.user_id=x[0].id
		    a.closure_id=fechamento[0].id
		    
		    print(a)
		    print(x)
		    
		    
		    session.add(a)
		
		session.commit()
		print("terminado")
		    
		


def populqte():
    with Session(engine) as session:
        query = select(User)
        data = session.exec(query).all()
        return data

def titi(code):
    with Session(engine) as session:
        query = select(Titulo).where(
            Titulo.cotista==code,
            Titulo.situacao=="A")
        data = session.exec(query).all()
        return data


def save(data):
    with Session(engine) as session:
        session.add(data)
        session.commit()
        

"""
from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlalchemy import create_engine as sa_create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from flask import Flask, render_template, request

# Defina o modelo SQLModel
class Post(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    content: str

# Crie uma instância do mecanismo SQLAlchemy e uma sessão
engine = sa_create_engine('sqlite:///example.db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = Flask(__name__)

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)  # Obtenha o número da página da consulta de URL
    per_page = 5  # Número de itens por página
    offset = (page - 1) * per_page

    with Session(engine) as session:
        stmt = select(Post).offset(offset).limit(per_page)
        posts = session.exec(stmt).all()

    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)

"""





"""

def read_norm_list(description:str=None , tags:str=None, page:str = None):
	with Session(engine) as session:	
		query= select(
			Norm_iten_sub,
			Norm_iten.title,
			Norm_iten.iten,
			).join(Norm_iten)

		if description:
			query = query.where( Norm_iten_sub.description.contains(description))
		if tags and tags != []:
			
			query = query.where( or_(Norm_iten_sub.tag == x for x in tags))
		
		if page:
			index = 10
			query = query.offset(page).limit(index)

		else:
			index = 10
			query = query.limit(index)

			

		data = session.exec(query).all()
"""












"""
Tabelas

Person
Para administração do sistema
Em diferentes níveis de acesso e edição

Id
Nome
Matrícula ou código
Senha
Tipo -> comum ou master


Todo -> tarefas
Serve para listar as ações no sistema 
Id 
Nome
Observação
Natureza -> adição de valor, devolver valor
Valor
Person-> id.person
Data
Status -> ok, pendente, autorizado, apagado





User

Id
Nome
Nascimento 
Telefone
Celular
Status -> ativo, inativo 

Endereço -> externo
Conta -> externo




Cotas
Serve para listar todas as cotas

Id
Código
Data
User -> id.user
Agrupamento - none, tipoa, tipob, tipoz




Regras
Calcular allicotas
Corte
Porcentagem
Data aplicação
"""