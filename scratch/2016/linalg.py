
class mtrx:
	def __init__(self,name,lst):
		self.data = np.array(lst)
		self.name = name
		self.show()
	def show(self):
		print(self.name)
		print(self.data)
	def multiply(self,B,result_name):
		print('__________________')
		self.show()
		print('\ttimes')
		B.show()
		print '\tequals'
		C = mtrx(result_name,self.data.dot(B.data))
		print('__________________')
		return C
	def plus(self,B,result_name):
		print('__________________')
		self.show()
		print('\tplus')
		B.show()
		print '\tequals'
		C = mtrx(result_name,self.data + B.data)
		print('__________________')
		return C

I = mtrx('I',[[1,0,0],[0,1,0],[0,0,1]])
A = mtrx('A',[[2,1,1],[4,-6,0],[-2,7,2]])
E_ = mtrx('E_',[[0,0,0],[-2,0,0],[0,0,0]])
E_A = E_.multiply(A,'E_A')
EA = E_A.plus(A,'EA')
F_ = mtrx('F_',[[0,0,0],[0,0,0],[1,0,0]])
F_EA = F_.multiply(EA,'F_EA')
FEA = F_EA.plus(EA,'FEA')
G_ = mtrx('G_',[[0,0,0],[0,0,0],[0,1,0]])
G_FEA = G_.multiply(FEA,'G_FEA')
GFEA = G_FEA.plus(FEA,'GFEA')

E = E_.plus(I,'E')
F = F_.plus(I,'F')
G = G_.plus(I,'G')

GFE = G.multiply(F.multiply(E,'FE'),'GFE')

U = GFE.multiply(A,'U')

b = mtrx('b',[[5],[-2],[9]])

c = GFE.multiply(b,'c')
