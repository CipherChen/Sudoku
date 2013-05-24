# -*- coding: utf-8 -*-
'''
This is a simple resolution of given Sudoku.
Some Sudoku would have multiple resolutions, but we'll just figure out one of them.

You may be interested in the process how this program solve these, then make sure that the variable DEBUG == True.
'''

'''
TODO:
 - [Done] Check the 3*3 cuber.
 - Do more complete check() in Cuber9.check()
 - Consider the line/row/Cuber3 which only has one EmptyValue first.
 - Consider the line/row/Cuber3 which the last filled pos is in. 
 - Consider cases which have more than one solution. 
'''

import random
import copy
import time

# For DEBUG
DEBUG = False
EmptyValue = 0
spac = [' ']

class Cuber(object):
	'''
	Base-class Cuber.
	lineno/rowno should start with 0.
	'''
	def __init__(self, values):
		# THe inner data stands for the puzzle.
		self.values = values
		
	def getLine(self, lineno):
		return self.values[lineno]
	
	def getRow(self, rowno):
		return [line[rowno] for line in self.values]
	
	def getValue(self, pos):
		lineno, rowno = pos
		return self.values[lineno][rowno]
	
	def setValue(self, pos, value):
		lineno, rowno = pos
		
		if DEBUG:
			global spac
			if value == EmptyValue:
				spac.pop()
		
			print ''.join(spac), pos, '->', value, 
		
			# Roll back
			if value == EmptyValue:
				print '...'
			else:
				print

		self.values[lineno][rowno] = value
		
		if DEBUG:
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
	
	def getPosSubCuber(self, pos):
		i, j = pos
		return self.getSubCubers()[(i/3, j/3)]
		
	
	def setValueAndCheck(self, pos, value):
		# A roll-back operation
		if value == EmptyValue:
			self.setValue(pos, value)
		else:
			lineno, rowno = pos
			if (value in self.getLine(lineno)) \
			or (value in self.getRow(rowno)) \
			or self.getPosSubCuber(pos).inCuber3(value):
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
		Do something more.
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

# Used to get the subset of each line/row/Cuber3
_Values = set(range(0, 10))

def Boom(case):
	'''
	The main algorithm of this program.
	I use recursion function to implement the backtrace.
	When it finds that the current assumed value has conflict with others,
	go back to the last assumed pos to try another possible value.
	'''
	leftEmpty = case.getAllEmptyPos()
	
	# All empty places filled, so we give it a check.
	if not leftEmpty:
		if case.check():
			return case
	
	# Iterate over each empty pos
	for pos in leftEmpty:
		l, r = pos
		linel = case.getLine(l)
		subset = _Values - set(linel)
		
		if EmptyValue in subset:
			subset.remove(EmptyValue)

		# Iterate over each valid values
		for each in subset:
			if case.setValueAndCheck(pos, each):
				# Fill in one value, so pass it to next level.
 				if Boom(case):
 					return case
 				else:
 					# Roll back
 					case.setValueAndCheck(pos, EmptyValue)
		# !!! Since the whole subset doesn't fit this line, the upper level must be wrong.
 		return None



def main():
	
	_testcases = (
				      # Easy
                      ([[0, 0, 0, 3, 0, 5, 0, 0, 4],
                        [3, 1, 0, 4, 0, 0, 0, 2, 0], 
                        [9, 6, 4, 1, 7, 2, 0, 0, 0], 
                        [0, 0, 0, 5, 6, 1, 2, 3, 9], 
                        [0, 3, 6, 0, 0, 0, 4, 8, 0], 
                        [5, 2, 9, 8, 3, 4, 0, 0, 0], 
                        [0, 0, 0, 9, 1, 3, 6, 7, 2], 
                        [0, 7, 0, 0, 0, 8, 0, 9, 3], 
                        [2, 0, 0, 6, 0, 7, 0, 0, 0],
                       ], 
                       [[7, 8, 2, 3, 9, 5, 1, 6, 4], 
                        [3, 1, 5, 4, 8, 6, 9, 2, 7], 
                        [9, 6, 4, 1, 7, 2, 3, 5, 8], 
                        [8, 4, 7, 5, 6, 1, 2, 3, 9], 
                        [1, 3, 6, 7, 2, 9, 4, 8, 5], 
                        [5, 2, 9, 8, 3, 4, 7, 1, 6], 
                        [4, 5, 8, 9, 1, 3, 6, 7, 2], 
                        [6, 7, 1, 2, 4, 8, 5, 9, 3], 
                        [2, 9, 3, 6, 5, 7, 8, 4, 1], 
                       ]), 

		              # Hard
                      ([[0, 0, 3, 0, 8, 0, 0, 9, 0], 
                        [8, 0, 0, 0, 0, 0, 6, 0, 1], 
                        [0, 0, 4, 0, 0, 9, 2, 0, 0], 
                        [0, 4, 0, 0, 6, 7, 9, 0, 0], 
                        [0, 0, 8, 3, 0, 2, 7, 0, 0], 
                        [0, 0, 7, 9, 5, 0, 0, 2, 0], 
                        [0, 0, 6, 5, 0, 0, 3, 0, 0],
                        [4, 0, 2, 0, 0, 0, 0, 0, 7], 
                        [0, 8, 0, 0, 7, 0, 4, 0, 0], 
                        ], 
                       [[1, 2, 3, 7, 8, 6, 5, 9, 4], 
                        [8, 7, 9, 4, 2, 5, 6, 3, 1], 
                        [6, 5, 4, 1, 3, 9, 2, 7, 8], 
                        [2, 4, 5, 8, 6, 7, 9, 1, 3], 
                        [9, 6, 8, 3, 1, 2, 7, 4, 5], 
                        [3, 1, 7, 9, 5, 4, 8, 2, 6], 
                        [7, 9, 6, 5, 4, 1, 3, 8, 2], 
                        [4, 3, 2, 6, 9, 8, 1, 5, 7], 
                        [5, 8, 1, 2, 7, 3, 4, 6, 9], 
                      ]), 

                      # Diabolical
                      ([[8, 0, 7, 0, 0, 0, 0, 0, 0], 
                        [3, 0, 0, 5, 0, 0, 0, 0, 0], 
                        [0, 0, 9, 0, 8, 0, 0, 5, 0], 
                        [1, 0, 0, 0, 5, 4, 9, 0, 6], 
                        [0, 0, 4, 0, 1, 0, 3, 0, 0], 
                        [9, 0, 3, 6, 2, 0, 0, 0, 1], 
                        [0, 9, 0, 0, 6, 0, 2, 0, 0], 
                        [0, 0, 0, 0, 0, 8, 0, 0, 9], 
                        [0, 0, 0, 0, 0, 0, 6, 0, 8], 
                       ], 
                       [[8, 5, 7, 9, 4, 3, 1, 6, 2], 
                        [3, 1, 6, 5, 7, 2, 8, 9, 4], 
                        [2, 4, 9, 1, 8, 6, 7, 5, 3], 
                        [1, 7, 2, 3, 5, 4, 9, 8, 6], 
                        [5, 6, 4, 8, 1, 9, 3, 2, 7], 
                        [9, 8, 3, 6, 2, 7, 5, 4, 1], 
                        [7, 9, 8, 4, 6, 1, 2, 3, 5], 
                        [6, 2, 5, 7, 3, 8, 4, 1, 9], 
                        [4, 3, 1, 2, 9, 5, 6, 7, 8], 
                       ]), 
                     )
	
	# x = Cuber9(copy.deepcopy(testcase_r))
	# for i in range(0, 20):
	# 	l = random.randrange(0, 9)
	# 	r = random.randrange(0, 9)
	# 	x.setValue((l, r), EmptyValue)
	
	for (p, s) in _testcases:
		print '*' * 80
		if DEBUG:
			global spac 
			spac = [' ']
		case = Cuber9(p)
		case_solution = Cuber9(s)
		
		start = time.time()
		Boom(case)
		end = time.time()
		
		if case == case_solution:
			print 'Case: '
			print case
			print 'Solution: '
			print case_solution
			print 'Congratulations, seconds elapsed: ', end - start
		else:
			print 'Case FAILED: '
			print case

if __name__ == '__main__':
	main()
