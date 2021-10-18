from flask import Blueprint, render_template, request, jsonify, url_for, session, g
from zolzima import db
from zolzima.models import Subject, Todo, Timer, User

from zolzima.forms import TodoForm

from werkzeug.utils import redirect

import operator

import json

def sum(n): #가장 최근의 같은 유저 타이머를 찾아주는 함수
  for i in range(n,1,-1):
    if Timer.query.get(i).user:
      if Timer.query.get(i).user.username == g.user.username: 
        return Timer.query.get(i).time
    else:
      continue
    if(i == 1):
      return 0

def ranktime(n, k):
  for i in range(n,1,-1):
    if Timer.query.get(i).user:
      if Timer.query.get(i).user.username == k: 
        return Timer.query.get(i).time
    else:
      continue
    if(i == 1):
      return 0
      
bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def timer():
	return render_template("timer.html")

@bp.route('/journal', methods=['GET', 'POST'])
def journal():
  
  todo_list = Subject.query.order_by(Subject.create_date.desc())
  
  return render_template('journal.html', todo_list = todo_list)

@bp.route('/rank')
def rank():
	return render_template('rank.html')

@bp.route('/test')
def test():
	return render_template('test.html')
	
#@bp.route('/tst', methods=['GET', 'POST'])
#def tst():
#data = request.get_json()
#data = int(data)
#count = Timer.query.count()
#sum = sum(count)	
#time = Timer(time = data + sum)
#db.session.add(time)
#db.session.commit()
#return jsonify(result = "success", result2 = Timer.query.get(count+1))
    
@bp.route('/study', methods=['GET', 'POST'])
def study(): #g.user 인경우 실행이 필요함.
	data = request.get_json()
	data = int(data)
	count = Timer.query.count()
	if g.user:
		Alltime = sum(count)
		if Alltime is None:
			Alltime = 0
		time = Timer(time = data + Alltime, user=g.user)
		db.session.add(time)
		db.session.commit()
		recentTime = Timer.query.get(count+1).time
		return str(recentTime)
	else:
		return


@bp.route('/detail/<int:todo_id>/')
def detail(todo_id):
	form = TodoForm()
	todo = Todo.query.get_or_404(todo_id) #이거 하면은 찾을수 없는 경우에 404가 된다!
	return render_template('detail.html', todo = todo, form = form)

@bp.route('/current', methods=['GET'])
def t():
	count = Timer.query.count()
	if g.user:
		current=sum(count)
		if current is None:
			current = 0
		return str(current)
	else: 
		return
   
@bp.route('/ginon')
def ginon():
	return render_template('ginon.html')
 
 
@bp.route('/rankdata', methods=['GET']) # return 은 됨 
def rankdata():
	count = Timer.query.count()
	usercount = User.query.count()
	Userlist = []
	UserTime = []
	for i in range(1,usercount+1):
		Userlist.append(User.query.get(i).username)
	CurrentTime = {}
	for i in Userlist:
		UserTime.append(ranktime(count, i))
		CurrentTime[i] = ranktime(count, i)
	CurrentTime=sorted(CurrentTime.items() ,key = operator.itemgetter(1), reverse = True)
  #json_val = json.dumps(CurrentTime)
	return str(CurrentTime)  	
 
 
 
#if j == 10:
#break
#Currenttime = sorted(CurrentTime.items(), key=operator.itemgetter(1), reverse = True)[:10] #딕셔너리 정렬
#Currenttime = str(Currenttime)
#if Currenttime == None:
#return "생성된 유저가 없습니다."
	#string_Usertime = [str(i) for i in UserTime]
	#string_Usertime = ''.join(string_Usertime)
	#string_Usertime = str(string_Usertime) 
	#return string_Usertime
    
