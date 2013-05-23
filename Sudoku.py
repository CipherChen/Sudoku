# -*- coding: utf-8 -*-
'''
This is a simple resolution of given Sudoku.
Some Sudoku would have multiple resolutions, but we'll just figure out one of them.
'''
'''
TODO:

'''

import random
import copy
import time

_Values = set(range(1, 10))

testcase3 = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

testcase = [[0, 0, 0, 3, 0, 5, 0, 0, 4],
		    [3, 1, 0, 4, 0, 0, 0, 2, 0], 
		    [9, 6, 4, 1, 7, 2, 0, 0, 0], 
		    [0, 0, 0, 5, 6, 1, 2, 3, 9], 
		    [0, 3, 6, 0, 0, 0, 4, 8, 0], 
		    [5, 2, 9, 8, 3, 4, 0, 0, 0], 
		    [0, 0, 0, 9, 1, 3, 6, 7, 2], 
		    [0, 7, 0, 0, 0, 8, 0, 9, 3], 
		    [2, 0, 0, 6, 0, 7, 0, 0, 0],
		   ]

testcase_r = [[7, 8, 2, 3, 9, 5, 1, 6, 4], 
			  [3, 1, 5, 4, 8, 6, 9, 2, 7], 
			  [9, 6, 4, 1, 7, 2, 3, 5, 8], 
			  [8, 4, 7, 5, 6, 1, 2, 3, 9], 
			  [1, 3, 6, 7, 2, 9, 4, 8, 5], 
			  [5, 2, 9, 8, 3, 4, 7, 1, 6], 
			  [4, 5, 8, 9, 1, 3, 6, 7, 2], 
			  [6, 7, 1, 2, 4, 8, 5, 9, 3], 
			  [2, 9, 3, 6, 5, 7, 8, 4, 1], 
			 ]

a = [[0, 0, 3, 0, 8, 0, 0, 9, 0], 
	 [8, 0, 0, 0, 0, 0, 6, 0, 1], 
	 [0, 0, 4, 0, 0, 9, 2, 0, 0], 
	 [0, 4, 0, 0, 6, 7, 9, 0, 0], 
	 [0, 0, 8, 3, 0, 2, 7, 0, 0], 
	 [0, 0, 7, 9, 5, 0, 0, 2, 0], 
	 [0, 0, 6, 5, 0, 0, 3, 0, 0],
	 [4, 0, 2, 0, 0, 0, 0, 0, 7], 
	 [0, 8, 0, 0, 7, 0, 4, 0, 0], 
	]

# At first, I was trying to define values of types"Given/Assumed"
# Then I realize that Backbrace would be better.
class Value(object):
	def __init__(self, value, type):
		self.value = value
		self.type = type
		
	def getRow(self):
		pass
	
	def getLine(self):
		pass
	
	def getsubRow(self):
		pass
	
	def getsubLine(self):
		pass


# For debug indentation
EmptyValue = 0
spac = [' ']

class Cuber(object):
	'''
	Base-class Cuber.
	lineno/rowno should start with 0.
	'''
	def __init__(self, values):
		self.values = values
		
	def getLine(self, lineno):
		return self.values[lineno]
	
	def getRow(self, rowno):
		return [line[rowno] for line in self.values]
	
	def getValue(self, pos):
		lineno, rowno = pos
		return self.values[lineno][rowno]
	
	def setValue(self, pos, value):
		global spac
		if value == EmptyValue:
			spac.pop()
		lineno, rowno = pos
		print ''.join(spac), pos, '->', value, 
		if value == EmptyValue:
			print '...'
		else:
			print
		self.values[lineno][rowno] = value
		if value != EmptyValue:
			spac.extend(' ')
	
	def lines(self):
		# Iterator over all lines
			return self.values
	
	def rows(self):
		# Iterator over all lines
		length = len(self.values)
		_rows = [None] * length
		for i in range(length):
			_rows[i] = self.getRow(i)
		return _rows
	
	def check(self):
		pass
	
	def __eq__(self, obj):
		return self.values == obj.values
	
	def __str__(self):
		_str = []
		for i in range(len(self.values)):
			_str.append('  ')
			for j in range(len(self.values[i])):
				_str.append('%d  ' % self.values[i][j])
			if i < len(self.values[j]) - 1:
				_str.append('\n\n')
		return ''.join(_str)

class Cuber3(Cuber):
	def __init__(self, values = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]):
		self.values = values

	def inCuber3(self, value):
		if value != 0:
			# We use '0' as an empty value
			for line in self.values:
				if value in line:
					return True
		return False
	
	def getPos(self, value):
		if value != 0:
			# We use '0' as an empty value
			for (i, v) in enumerate(self.values):
				for (j, x) in enumerate(v):
					if x == value:
						return (i, j)
		return None
	
	def setValueAndCheck(self, pos, value):
		if self.inCuber3(value):
			return False
		self.setValue(pos, value)
		return True
		

	def check(self):
		_alllines = []
		for line in values:
			if 0 in line:
				# There should be one more '0' element in some lines
				return False
			_alllines.append(line)
		for i in range(1, 10):
			if _alllines.count(i) != 1:
				return False
		return True
		
class Cuber9(Cuber):
	def __init__(self, values):
		self.values = values
	
	def getSubCubers(self):
		_SubCubers = {}
		i = 0
		while i < len(self.values):
			j = 0
			while j < len(self.values[i]):
				_SubCubers[(i/3, j/3)] = Cuber3([
												self.getLine(i)[j:j+3],
												self.getLine(i+1)[j:j+3],
												self.getLine(i+2)[j:j+3]
												])
				j += 3
			i += 3
		return _SubCubers
	
	def setValueAndCheck(self, pos, value):
		# A roll-back operation
		if value == EmptyValue:
			self.setValue(pos, value)
		else:
			lineno, rowno = pos
			if (value in self.getLine(lineno)) or (value in self.getRow(rowno)):
				return False
			self.setValue(pos, value)
		return True

	def getAllEmptyPos(self):
		'''Get all empty pos, return a pos list'''
		_leftEmpty = []
		for (l, line) in enumerate(self.values):
			for (r, v) in enumerate(line):
				if v == EmptyValue:
					_leftEmpty.append((l, r))
		return _leftEmpty
	
	def check(self):
		'''
		Check the whole Cuber9 to see if it' ok.
		'''
		_alllines = []
		for line in self.values:
			if EmptyValue in line:
				# There should be one more '0' element in some lines
				return False
			_alllines.extend(line)
		for i in range(1, 10):
			if _alllines.count(i) != 9:
				return False
		return True


def test():
	print cuber9
	for line in cuber9.lines():
		print line
	print 
	print cuber9
	for row in cuber9.rows():
		print row
	print
	print cuber9
	print cuber9.getAllEmptyPos()

_Values = set(range(0, 10))

# 回溯，问题不难，定义好每个对象的接口
# 两层循环，貌似不够？
def Boom(case):
	# print case
	leftEmpty = case.getAllEmptyPos()
	# print 'leftEmpty: ', leftEmpty
	# All space filled, so we give it a check.
	if not leftEmpty:
		print 'All filled, check now'
		if case.check():
			return case
	# Iterate over each pos
	for pos in leftEmpty:
		l, r = pos
		linel = case.getLine(l)
		subset = _Values - set(linel)
		
		if EmptyValue in subset:
			subset.remove(EmptyValue)

		# Iterate over each valid values
		for each in subset:
			if case.setValueAndCheck(pos, each):
				# subset.remove(each)
 				if Boom(case):
 					return case
 				else:
 					# Roll back
 					case.setValueAndCheck(pos, EmptyValue)
 					# subset.add(each)
		# !!! Since the whole subset doesn't fit this line, the upper level must be wrong.
 		return None

# x = Cuber9(copy.deepcopy(testcase_r))
# for i in range(0, 20):
# 	l = random.randrange(0, 9)
# 	r = random.randrange(0, 9)
# 	x.setValue((l, r), EmptyValue)

x = Cuber9(testcase)
print x
now = time.time()
Boom(x)
print 'Used: ', time.time() - now
print x == Cuber9(testcase_r)
print x.check()
print x

	

# cuber9 = Cuber9(testcase)
# Boom(cuber9)
# print cuber9
# print cuber9.check()
