import fileinput
import re
import math
import sys
import copy

global dic_assign 
dic_assign = {}

class Ngon():
	def __init__(self,x_,y_,r_,n_):
		self.x = eval_(x_)
		self.y = eval_(y_)
		self.r = eval_(r_)
		self.n = eval_(n_)
	def draw_ngon(self):
		pic = []
		pic.append([self.x+self.r,self.y,'moveto'])
		pi = 3.141592653589397238
		theta = (360/int(self.n))*pi/180
		x0 = self.r
		y0 = 0
		for i in range(int(self.n)):
			x1 =math.cos(theta)*(x0)-math.sin(theta)*(y0)
			y1 =math.sin(theta)*(x0)+math.cos(theta)*(y0)
			pic.append([x1+self.x,y1+self.y,'lineto'])
			x0 = x1
			y0 = y1
		#print('uiiid')
		return pic
	def line(self):
		res = [0,0]
		res[0] = [self.x,self.y,'moveto']
		res[1] = [self.r,self.n,'lineto']
		return res
	def rect(self):
		
		res = [0,0,0,0,0]
		res[0] = [self.x,self.y,'moveto']
		res[1] = [self.x+self.r,self.y,'lineto']
		res[2] = [self.x+self.r,self.y+self.n,'lineto']
		res[3] = [self.x,self.y+self.n,'lineto']
		res[4] = [self.x,self.y,'lineto']
		return res

	def sector(self,E):
		#(sector 0 0 100 30 60)
		E = eval_(E)
		if self.n<0:
			self.n = 360+self.n
		if E<0:
			E = 360+E
		theta = math.radians(self.n)
		x =math.cos(theta)*(self.r)-math.sin(theta)*(0)
		y =math.sin(theta)*(self.r)+math.cos(theta)*(0)
		res = [0,0,0,0]
		res[0] = [self.x,self.y,'moveto']
		res[1] = [x+self.x,y+self.y,'lineto']
		res[2] = [self.x,self.y,self.r,self.n,E,'arc']
		res[3] = [self.x,self.y,'lineto']
		return res
#***************************************************************************
class transform():
	def __init__(self,pic,x_,y_):
		self.pic = pic
		self.x = eval_(x_)
		self.y = eval_(y_)	
	def translate(self):
		#print(self.pic,'sjjjjjjjjjj')
		#print(self.x,'skskskksksksk')
		#print(self.pic[0][0],'lqlqlqlqllqlq')
	#pic=[[-50, 0, 'moveto'], [10, 0, 'lineto'],[filled]]
	#[[7.0, -1.9999999999999996, 'moveto'], [13.0, -3.999999999999999, 'lineto'], ['stroke']]
		for i in range(len(self.pic)-1):
			self.pic[i][0]=self.pic[i][0]+self.x
			self.pic[i][1]=self.pic[i][1]+self.y
		return self.pic
	def rotate(self):
	#change into radian
		
		theta = math.radians(self.x)
		#[[100,0,'lineto']]
		
		for i in range(len(self.pic)-1):
			x =math.cos(theta)*(self.pic[i][0])-math.sin(theta)*(self.pic[i][1])
			y =math.sin(theta)*(self.pic[i][0])+math.cos(theta)*(self.pic[i][1])
			self.pic[i][0] = x
			self.pic[i][1] = y
			if self.pic[i][-1]=='arc':
				self.pic[i][3] +=self.x
				self.pic[i][4] +=self.x
				self.pic[i][3] = self.pic[i][3]%360
				self.pic[i][4] = self.pic[i][4]%360
		return self.pic
	def scale(self):
		s = self.x
		for i in range(len(self.pic)-1):
			self.pic[i][0]=self.pic[i][0]*s
			self.pic[i][1]=self.pic[i][1]*s
			if self.pic[i][-1]=='arc':
				self.pic[i][2]=self.pic[i][2]*s
		return self.pic
	def generate(self,char):
		if char == 'translate':
			self.pic = self.translate()
		elif char == 'rotate':
			self.pic = self.rotate()
		elif char == 'scale':
			self.pic = self.scale()
		return self.pic
#******************************************************************************************************************
#1 .draw_picture 
#2 .group
#3 .for 
#4 .tansform
#5 .operator
#6 .:=
#7 .color linewidth
# stack = [[['translate', ['group', ['line', 'x', '3', '15', '9'], ['line', 'x', '7', '6', '13']], '11.5', '9'], ['line', 'x', '3', '15', '9'], ['line', 'x', '7', '6', '13']]]

def eval_(nu):
	try:
		no = eval(nu)
	except NameError:
		no = dic_assign[nu]
	except TypeError:
		no = nu
	return no

def caculate(st):
	#st = ['+', '-7', '3'] or ['cos', '-5']# only one level
	name = st[0]
	if len(st)==3:
		n1 = eval_(st[1])
		n2 = eval_(st[2])
	else:
		n1 = eval_(st[1])
	if name == '+':
		return str(n1+n2)
	elif name == '*':
		return str(n1*n2)
	elif name == '/':
		return str(n1/n2)
	elif name == '-':
		return str(n1-n2)
	elif name == 'sin':
		return str(math.sin(math.radians(n1)))
	elif name == 'cos':
		return str(math.cos(math.radians(n1)))

#*************************************************************************************************************************************************************************
def draw(inputs):
	#['line', '5', '3', 'y', '9'] one level
	atrr = inputs[0]
	atrr_1 = {'tri':(3,1),'filledtri':(3,0),'square':(4,1),'filledsquare':(4,0),'penta':(5,1),'filledpenta':(5,0),'hexa':(6,1),'filledhexa':(6,0)}
	atrr_2 = {'line':1,'rect':1,'filledrect':0,'ngon':1,'filledngon':0}
	atrr_3 = {'filledsector':0,'sector':1}
	if atrr in atrr_1:
		pict = Ngon(inputs[1],inputs[2],inputs[3],atrr_1[atrr][0])
		#[[30, 0, 'moveto'], [9.2, 28.5, 'lineto'], [-24.2, 17.6, 'lineto']]	
		return Pict(atrr,atrr_1[atrr][1],pict)		
	elif atrr in atrr_2:
		pict = Ngon(inputs[1],inputs[2],inputs[3],inputs[4])	
		return  Pict(atrr,atrr_2[atrr],pict)
	elif atrr in atrr_3:
		pict = Ngon(inputs[1],inputs[2],inputs[3],inputs[4])
		picture = pict.sector(inputs[5])
		return Pict('sector',atrr_3[atrr],picture)

def Pict(atrr,oj,picture):
	#['line', '5', '3', 'y', '9']
	#picture is a class_example
	if atrr =='rect':
		pict_init = picture.rect()
	elif atrr =='filledrect':
		pict_init = picture.rect()
	elif atrr =='line':
		pict_init = picture.line()
	elif atrr == 'sector':
		#pass
		pict_init = picture
	else:
		pict_init = picture.draw_ngon()
	if oj == 0:
		pict_init.append(['fill'])
	else:
		pict_init.append(['stroke'])
	return pict_init

def groups(inputs):
	#[['line', '5', '3', '15', '9'],['line', '2', '7', '4', '13']]
	pics = []
	for i in range(len(inputs)):
		pics.append(draw(inputs[i]))
	return pics

#*********************************************************************************************************************************************************************
def Tran(inputs):
	#kvl = [[18, 56, 'moveto'], [6, 13, 'lineto'], ['stroke']] 
	char = inputs[0] 
	if char == 'translate':
		x1 = inputs[2]
		y1 = inputs[3]
	else:
		x1 = inputs[2]
		y1 = -1
	return treat(inputs[1],x1,y1,char)

def treat(kvl,x1,y1,char):
	if isinstance(kvl[0][0],list)!=True:
		transf = transform(kvl,x1,y1)
		kcl = transf.generate(char)
		#print(kcl,'zzzzzzzzzzzz')
		return kcl
	elif isinstance(kvl[0][0],list)==True:
		#print(kvl[0],'zzzhhhhhhhhhhzzzzzzzzz')
		jan = []
		for pp in kvl:
			jan.append(treat(pp,x1,y1,char))
		return jan
#********************************************************************************************************************

def Parser(tree):
	#only solving one level command (....)
	#not (....)(....)
	#
	result = copy.deepcopy(tree)
	store = []
	for j in range(len(result)):
		order = result[j]
		if isinstance(order,list)==True:
			#order = ['line', '5', '20', '15', '9']
			result[j] = Parser(order)
			store.append(result[j])
			#print(tree[j])
		elif isinstance(order,str)==True:
			store.append(order)
	if all_dic[store[0]]== 'operator':
		return caculate(store)
	elif all_dic[store[0]]== 'draw':
		return draw(store)
	elif all_dic[store[0]]== 'group':
		return store[1:]
	elif all_dic[store[0]]== 'tran':
		return Tran(store)
	#[[[17.5, 12, 'moveto'], [26.5, 18, 'lineto'], ['stroke']], [[35.5, 20, 'moveto'], [17.5, 22, 'lineto'], ['stroke']]]
	elif all_dic[store[0]]==':=':
		dic_assign[store[1]]=eval_(store[2])
		#store = [':=', 'x', '0.5000000000000001']
	elif all_dic[store[0]]=='linewidth':
		#['linewidth', 'X']
		val = eval_(store[1])
		return [val,'setlinewidth']
	elif all_dic[store[0]]=='color':
		val = []
		for nui in store[1:]:
			val.append(eval_(nui))
		val.append('setrgbcolor')
		return val
		#tree = ['for', 'y', '1', '2', ['translate', ['group', ['line', '5', '3', 'y', '9'], ['line', '2', '7', '4', '13']], '110', 'y'], ['rotate', ['filledrect', '2', '7', '4', '13'], ['*', '15', '4']]]

def control(tr):
	#tree = ['for', 'y', '1', '2',E1,E2]
	lent = len(tr)
	if eval_(tr[2])>eval_(tr[3]):
		dic_assign[tr[1]]= eval_(tr[2])
		return None
	elif lent == 4:
		dic_assign[tr[1]]= eval_(tr[3])
		return None
	else:
		diu = []
		for u in range(eval_(tr[2]),eval_(tr[3])+1):
			dic_assign[tr[1]]= u
			for op in range(4,len(tr)):
				if tr[op][0]=='for':
					diu.append(control(tr[op]))
				else:
					diu.append(Parser(tr[op]))
			dic_assign[tr[1]]= u
	return diu
string11 = '(rotate (group (translate (sector 20 30 100 30 60) (* 100 0.1) 20)(line 18 7 6 13)) (* 20 3))'
string0 = '(for y 1 4  (translate (line 5 3 5 9) (* 100 y) y) )(translate (filledrect 2 7 4 13) ( * 15 4) 11)(:= X 1) (linewidth X)(color 0 0 0.5)'
string10 = '( for x 1 5 (line 4 5 6 7))(linewidth x)'
string9 = '(   :=   x (  cos (+    -7 3)   	 ))(translate (group (line x 3 15 9)(line x 7 6 13)) 110 90)(   :=   x (  cos (+    20 40)   	 ))(line x 3 15 9)(:= X 1) (linewidth X)(color 0 0 0.5)'
string8 = '(translate (group (line 6 3 15 9)(line 24 (+ 5 6) 6 13)(group (filledrect 2 7 4 13)(line 18 (* 7 8) 6 13))) 11.5 9)'
string7 = '( for x 1 5(:= x 0))(linewidth x)'
string5 = '(for y -1 4  (translate (line 5 3 5 9) (* 100 y) y) )'
string4 = '(   :=   x (  cos (+    20 40)   	 ))(translate (group (line x 3 15 9)(line 4 x 6 13)) 11.5 9)(line x 3 15 9)(line x 7 6 13)'
string = '(:= y 4)(   :=   x y)(line 3 4 x y)'
string2 = '(line (* 4 20) 20 15 9)(line 7 7 6 13)'
string6 = '(rotate (sector 20 30 100 30 60) (* 20 3))'
string12 = '(   :=   x (  cos (+    -7 3)   	 ))(for   y 1 2 (translate (rotate (group (line 5 x y 9) (line 2 7 4 13)) -90) 11 y))'
string13 = '(translate (sector 20 30 100 30 60) (* 10 4) 35) '
string14 = '(rotate (sector 20 30 100 340 170) (* 15 4))'
string15 = '(group (line 6 3 15 9))'

atrr_dic_1 = {'tri':(3,1),'filledtri':(3,0),'square':(4,1),'filledsquare':(4,0),'penta':(5,1),'filledpenta':(5,0),'hexa':(6,1),'filledhexa':(6,0)}
atrr_dic_2 = {'line':1,'rect':1,'filledrect':0,'ngon':1,'filledngon':0}
all_dic = {'tri':'draw','filledtri':'draw','square':'draw','filledsquare':'draw','penta':'draw','filledpenta':'draw','hexa':'draw','filledhexa':'draw','line':'draw','rect':'draw','filledrect':'draw','ngon':'draw','filledngon':'draw','group':'group','+':'operator','*':'operator', '/':'operator', '-': 'operator','sin': 'operator','cos':'operator','translate':'tran','rotate':'tran','scale':'tran',':=':':=','color':'color','linewidth':'linewidth','for':'for','filledsector':'draw','sector':'draw'}
#classfiy {'+':'operator','*':'operator', '/':'operator', '-': 'operator','sin': 'operator','cos':'operator'}


def read():
	string = ''
	for line in fileinput.input():
		string = string+line
	sub = re.compile(r'\r|\t|' '')
	x__ = sub.sub('',string)
	x__ = x__.replace('\n',' ')
	return x__
#print(read())
def dispose(string_):
	stack = []
	stri = '('+string_+')'
	stri = stri.replace('(',' ( ')
	stri = stri.replace(')',' ) ')
	strli = re.split(r'\s+', stri)
	strli = strli[1:-1]
	for s in strli[::-1]:
		if s != '(':
			stack.append(s)
		else:
		
			pop = stack[-1]
			cha = []
			for s2 in stack[::-1]:
				if s2!=')':
					cha.append(s2)
					stack.pop()
				else:
					stack.pop()
					break
			stack.append(cha)
	return stack
#tree = [['translate', ['group', ['line', '5', '3', '1', '9'], ['line', '2', '7', '4', '13']], '110', '1']]
#print(Parser(stack[0][0]))
#all_cmd = [[for ...][tran ...][:= ...][]]
def out_all(all_cmd):
	output = []
	for mj in all_cmd:
		if mj[0]=='for':
			output.append(control(mj))
		else:	
			output.append(Parser(mj))
	return output


def out(t):
	for pri in t:
		if isinstance(pri,list)==True:
			out(pri)
		elif pri == None:
			pass
		else:
			xx = ''
			for i in t:
				xx+=str(i)+' '
			xx = xx.rstrip()
			print(xx)
			break
#print(read())
all_cmd = dispose(read())[0]
#all_cmd = dispose(string10)[0]
#print(all_cmd)
print('%!PS-Adobe-3.0 EPSF-3.0')
print("%%BoundingBox: 0 0 1239 1752")
out(out_all(all_cmd))
