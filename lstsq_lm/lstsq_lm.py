#!/usr/bin/env python

"""
lstsq_lm
	@version : 0.1.0
	@author : Daniel Ríos Linares (c) 2016, riv@hotmail.es
	@description : A simple program to demonstrate the Levenberg-Marquardt least
		squares	algorithm for linear and nonlinear fits. The complete program
		has been obtained from Numerical Recipes in C, and the source code from
		its publications (sometimes translated directly from the source, but for
		the most part has been interpretated by me and modified). This package
		is the standalone version, you can sustitute the inv function (computes
		the inverse of a matrix) with other different.

	@license : GPL-3.0
		This program is free software: you can redistribute it and/or modify
		it under the terms of the GNU General Public License as published by
		the Free Software Foundation, either version 3 of the License, or
		(at your option) any later version.

		This program is distributed in the hope that it will be useful,
		but WITHOUT ANY WARRANTY; without even the implied warranty of
		MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
		GNU General Public License for more details.

		You should have received a copy of the GNU General Public License
		along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# Required for the Levenberg-Marquardt algorithm
from numpy.linalg import inv

# <class LeastSquares>
# 	@variable self.X : independient data, can be list<list> or only list
# 	@variable self.Y : dependient data, can be list<list> or only list
# 	@variable self.f : list/float function(list/float x, list P) to fit
# 	@variable self.P : list of initial guess for the parameters
# 	@variable self.w : float function(list/float x, list P) to weight the fit
# 	@variable self.dP : default dimensional parameter variation, same lenght of P
# 	@variable self.Plbl : labels of parameters, by default a,b,...,z,a1,b1,...
# 	@variable self.pr : print selection (if True, terminal output will be displayed)
# 	@variable self.dimX : dimension of X, if X is a list then will be 1, but if
# 		is a multidimensional fit, will be the dimension of list<list>
# 	@variable self.dimY : dimension of Y, if Y is a list then will be 1, but if
# 		is a multidimensional fit, will be the dimension of list<list>
# 	@variable self.N : number of output lines of data
# 	@variable self.M : number of parameters to fit
# 	@variable self.R : residuals of each data, its lenght is the product of
# 		self.N and self.dimY because each Y column is considered a points
# 	@variable self.J : jacobian of the data, you can override it by extending
# 		the class if you need a improvement in speed
#
# 	@description : a instantiation of this class will fit the data X,Y in the
# 		function f compensating the weight of function w with the iteration of P
# 		with dP. The Levenberg-Marquardt algorithm has been selected for this
# 		task, because is simple and very robust (class LevenbergMarquardt in
# 		this same file).
#
# 	@author : Daniel Ríos Linares
#
#	@version : 0.1.1
#		*updated from 0.1.0 August 19, 2017 : <method recalc_jac> improved
#
# 	@references :
# 		1) William H. Press, Saul A. TeuKolsky, W.T. Vetterling & B.P. Flannery
#          Numerical recipes in C - The art of Scientific Computing 2nd Edition
# 		   2002, chapter 2, Gauss-Jordan Elimination, pages 681-687
class LeastSquares:
	''' [ Static variables ] '''
	# Parameter label sequence
	lbl = 'abcdefghijklmnopqrstuvwxyz'

	''' [ Constructors ] '''
	# <function LeastSquares>
	# 	@argument X : independient data, can be list<list> or only list
	# 	@argument Y : dependient data, can be list<list> or only list
	# 	@argument *f : list/float function(list/float x, list P) to fit, if is
	# 		not defined, self.f_default is setted
	# 	@argument *P : list of initial guess for the parameters
	# 	@argument *w : float function(list/float x, list P) to weight the fit,
	# 		if isn't defined, self.w_default is setted (always return 1)
	# 	@argument *dP : default dimensional parameter variation same lenght of P
	# 	@argument *Plbl : labels of parameters, by default a,b,...,z,a1,b1,...
	# 	@argument *pr : print selection (if True, terminal output displayed)
	def __init__(self, X, Y, f=None, P=None, w=None, dP=None, Plbl=None, pr=False):

		# Non-optional input arguments: X and Y data and function f
		self.X = X
		self.Y = Y

		# Obtain the dimension of the X and Y data matrixes :
		try: self.dimX = len(X[0])
		except: self.dimX = 1
		try: self.dimY = len(Y[0])
		except: self.dimY = 1

		# Optional arguments : function to fit (f) and weight (w)
		self.w = w if (w != None) else self.w_default
		self.f = f if (f != None) else self.f_default

		# Optional arguments : parameter, variation and labels
		self.P = P if (P != None) else [1e-3 for p in range(self.detect_P())]
		self.dP = dP if (dP != None) else [1e-6 for p in self.P]
		self.Plbl = Plbl if (Plbl != None) else [self.detect_label(i) for i in range(len(self.P))]

		# Number of points of the grid
		self.N = len(X)

		# Number of parameters of the problem
		self.M = len(self.P)

		# Residuals vector
		self.R = [0 for i in range(self.N*self.dimY)]

		# Jacobian matrix
		self.J = [[0 for j in range(self.M)] for i in range(self.N*self.dimY)]

		# Print iterations?
		self.pr = True if pr == True else False

	''' [ Solve ] '''
	# <method solve>
	#	@returns <list P> : returns self.P after solution
	#
	#	@description : operates the main loop of the solver (LevenbergMarquardt)
	def solve(self):
		if self.pr:
			print("Initial parameters")
			for i in range(self.M): print(self.Plbl[i],'=',self.P[i])
		if self.pr:
			print("Processing...")
		solver = LevenbergMarquardt(self,self.M,self.N*self.dimY,self.pr)
		solver.solve()
		if self.pr:
			print("Finished!")
			print("Final parameters")
			for i in range(self.M): print(self.Plbl[i],'=',self.P[i])
		return self.P

	''' [ Internal functions ] '''
	# <method func>
	# 	@argument <int i> : int that consider the current index of X,Y data
	#
	#	@returns <list/float self.f.__call__> : reuturns the value of self.f
	#
	# 	@description : returns the value of the fit from the function self.f
	def func(self,i):
		# When there is only 1D at the output return it as usual
		if self.dimY == 1: return self.f(self.X[i],self.P)
		# If not, the call is from the residual computation, so the number of
		# points has been multiplied by self.dimY
		else:
			c = 0
			while i >= self.N:
				i -= self.N
				c += 1
			return self.f(self.X[i],self.P)[c]

	# <method f_default>
	# 	@argument <list/float x> : is the set of data from self.X[i]
	# 	@argument <list P> : is the list of parameters to compute
	#
	#	@returns <list/float self.Y.item> : returns an item of self.Y
	#
	# 	@description : this function is used to fit a linear regression to the
	# 		set of data X,Y (for every dimension combination), is automatically
	# 		selected when there is no other defined by the user as self.f
	def f_default(self,x,P):
		y = [0 for i in range(self.dimY)]
		if self.dimX != 1:
			# X = [[x11,x12,....,x1(dimX)],[x21,x22,....,x2(dimX)],...]
			if self.dimY != 1:
				# Y = [[y11,y12,...,y1(dimY)],[y21,y22,...,y2(dimY)],...]
				for j in range(self.dimY):
					for i in range(len(x)): y[j] += x[i]*P[i+len(x)*j]
					y[j] += P[len(x)+len(x)*j]
			else:
				# Y = [y1,y2,y3,...]
				y = 0
				for i in range(len(x)): y += x[i]*P[i]
				y += P[len(x)]
		else:
			# X = [x1,x2,...]
			if self.dimY == 1:
				# Y = [y1,y2,y3,...]
				y = x*P[0]+P[1]
			else:
				# Y = [[y11,y12,...,y1(dimY)],[y21,y22,...,y2(dimY)],...]
				for j in range(self.dimY): y[j] = x*P[0+2*j]+P[1+2*j]
		return y

	# <method weight>
	# 	@argument <int i> : int of the index for the X,Y set of data
	#
	#	@returns <float self.w.__call__> : weight of the x,y set
	#
	# 	@description : used by the class in order to ponderate a situation of
	# 		the problem to the requirements of the user
	def weight(self,i):
		if self.dimY == 1:
			return self.w(self.X[i],self.P)
		else:
			c = 0
			while i >= self.N:
				i -= self.N
				c += 1
			return self.w(self.X[i],self.P)

	# <method w_default>
	# 	@argument <list/float x> : is the set of data from self.X[i]
	# 	@argument <list P> : is the list of parameters to compute
	#
	#	@returns <float 1.0> : default weighting 1
	#
	# 	@description : this function is used to fit a linear regression to the
	# 		set of data X,Y, is automatically selected as self.w when there is
	# 		no other defined by the user, always return 1 when is no ponderation
	def w_default(self,x,P): return 1.0

	# <method data>
	# 	@argument i : int that is the value of the
	#
	#	@returns <list/float x, list/float y> : set of data returned
	#
	# 	@description : it returns a X,Y data considering the overflow of the i
	# 		into the data as a detection of a residual taking
	def data(self,i):
		if self.dimY == 1:
			return self.X[i],self.Y[i]
		else:
			c = 0
			while i >= self.N:
				i -= self.N
				c += 1
			return self.X[i],self.Y[i][c]

	# <method merit>
	#	@returns <float chi_squared> : returns the current chi_squared
	#
	# 	@description : returns the chi squared (sum of difference squares
	# 		between the data and the fit) of the current state
	def merit(self):
		chi_squared = 0
		self.recalc_residuals()
		for r in self.R:
			chi_squared += r**2
		return chi_squared

	''' [ Internal computation ] '''
	# <method increase_P>
	# 	@argument dP : list of parameter increase
	#
	# 	@description : modifies the self.P parameter list by increasing with
	# 		argument dP
	def increase_P(self,dp):
		for j in range(self.M):
			self.P[j] += dp[j]
		self.recalc_residuals()

	# <method recalc_residuals>
	# 	@description : recalculation of the residuals
	def recalc_residuals(self):
		for i in range(self.N*self.dimY):
			_,y = self.data(i)
			w = self.weight(i)
			self.R[i] = (self.func(i)-y)*w if w != 0 else 0

	# <method recalc_jac>
	# 	@description : recomputes all indexes of the jacobian
	def recalc_jac(self):
		for j in range(self.M):
			# 1) Erase dp (reinitialization)
			dp = [0 for k in range(self.M)]

			# 2) Calculate chi(p+dp)
			dp[j] = self.dP[j]
			self.increase_P(dp)
			chi_p = [self.R[i] for i in range(len(self.R))]

			# 3) Calculate chi(p-dp) = chi(p+dp-2*dp)
			dp[j] = -2*self.dP[j]
			self.increase_P(dp)
			chi_m = [self.R[i] for i in range(len(self.R))]

			# 4) Central PD indexes on J will be (chi(p+dp)-chi(p-dp))/2h
			for i in range(self.N*self.dimY):
				self.J[i][j] = (chi_p[i]-chi_m[i])/(2*self.dP[j])

			# 5) With J calculated, return to the original p
			dp[j] = self.dP[j]
			self.increase_P(dp)

	''' [ Detection ] '''
	# <method detect_P>
	#	@returns <int p> : number of parameters auto-detected
	#
	# 	@description : with X and f defined is able to know the P lenght by
	# 		trying the function self.f until there is no error, as a crazy limit
	# 		it has a 100000 parameters as a bad self.f definition
	def detect_P(self):
		p = 1
		while p < 100000:
			try: self.f( self.X[0] , [0 for i in range(p)] ); break
			except: pass
			p += 1
		return int(p)

	# <method detect_label>
	#	@returns <str lbl> : label auto-generated
	#
	# 	@description : obtains a list of auto-generated labels for parameters P
	def detect_label(self,i):
		c = 0
		while i >= len(self.lbl):
			i -= len(self.lbl)
			c += 1
		lbl = self.lbl[i]
		if c != 0: lbl += str(c)
		return lbl

	''' [ Setters & getters ] '''
	# <method get_residual>
	# 	@argument <int i> : int index of the residual
	#
	#	@return <float self.R.item> : item of the current residuals self.R list
	#
	# 	@description : returns the value of the residual in i index
	def get_residual(self,i): return self.R[i]

	# <method get_jacobian>
	# 	@argument <int i> : int row of the jacobian
	# 	@argument <int j> : int column of the jacobian
	#
	#	@returns <float self.J.item> : item of the current jacobian self.J list
	#
	# 	@description : returns the value of the jacobian in i,j
	def get_jacobian(self,i,j): return self.J[i][j]

	# <method get_P>
	#	@return <list self.P> : current parameters self.P
	#
	# 	@description : returns a list of parameters (normally used after the
	# 		self.solve() in order to get the fitting)
	def get_P(self): return self.P

	# <method merit>
	#	@returns <float chi_squared> : value of chi_squared
	#
	# 	@description : returns the chi squared (sum of difference squares
	# 		between the data and the fit) of the current state
	def get_chiSquared(self):
		chi_squared = 0
		for i in range(self.N*self.dimY):
			_,y = self.data(i)
			chi_squared += (self.func(i)-y)**2
		return chi_squared

# End of <class LeastSquares>


# <class LevenbergMarquardt>
# 	@variable <LeastSquares.object self.host> : is the host of the parameters
#		and merit figure, is always an instantiation of LeastSquares
# 	@variable <int self.N> : number of output lines of data (not the same as the
#		host)
# 	@variable <int self.M> : number of parameters to fit
# 	@variable <bool *self.pr> : print selectable
# 	@variable <static int self.max_iterations> : maximum number of iterations
#		that the algorithm can execute
# 	@variable <static float lamb_dmp> : damping multiplier/divider of the
#		Levenberg-Marquardt algorithm
# 	@variable <static float lamb_max> : max non-dimensional damping allowed
#	@variable <static float lamb_min> : min non-dimensional damping allowed
#	@variable <static float lamb_tol> : when the merit figure of the host only
#		improves in this magnitude, the loop stops.
#
# 	@description : computes the Levenberg-Marquardt algorithm with self.host as
# 		a object with the methods get_jacobian, recalc_jac, get_residual,
# 		recalc_residuals, merit, increase_P. Each 10 iterations, the first one
# 		and the last one are printed in the console to display the process.
#
# 	@author : Daniel Ríos Linares
#
#	@version : 1.0
#
# 	@references :
# 		1) William H. Press, Saul A. TeuKolsky, W.T. Vetterling & B.P. Flannery
#          Numerical recipes in C - The art of Scientific Computing 2nd Edition
# 		   2002, chapter 2, Gauss-Jordan Elimination, pages 681-687
class LevenbergMarquardt:
	''' [ Static variables ] '''
	max_iterations = 250 # maximum number of iterations
	lamb_dmp = 10 # damping recommended in Numerical Recipes in C
	lamb_max = 1.000e+010 # maximum non-dimensional lambda
	lamb_tol = 1.000e-010 # maximum non-dimensional lambda

	''' [ Constructors ] '''
	# <method LevenbergMarquardt>
	# 	@argument <LeastSquares self.host> : is the host of the parameters and
	#		the merit figure, is always an instantiation of LeastSquares
	# 	@argument <int self.N> : number of output lines of data (not the same
	#		as the host)
	# 	@argument <int self.M> : number of parameters to fit
	# 	@argument <boolean *self.pr> : print selectable
	def __init__(self,host,M,N, pr = True):
		# Host and number of parameters/points
		self.host = host
		self.M = M
		self.N = N
		self.pr = pr

	''' [ Solve ] '''
	# solve() : void function(void)
	#	@description : executes the solver
	def solve(self):
		# Class variables shortcut
		M = self.M
		N = self.N
		host = self.host

		# 1) Gradient definitions
		alph = [[0 for j in range(M)] for j in range(M)]
		inv_alph = [[0 for j in range(M)] for j in range(M)]
		beta = [0 for j in range(M)]
		delt = [0 for j in range(M)]

		# 2) Initialization
		lamb = 1e-3
		count = 0

		# 3) Levenberg-Marquardt loop initialization
		while count < self.max_iterations:
			host.recalc_residuals()
			chiSquared = host.merit()
			chiSquared_last = chiSquared
			host.recalc_jac()

			if count % 10 == 0 and self.pr:
				print("  iteration " + str(count) + ", sum of squares = " + str(host.get_chiSquared()))

			for j in range(M):
				beta[j] = -sum([host.get_residual(i)*host.get_jacobian(i,j) for i in range(N)])

			for j2 in range(M):
				for j in range(M):
					alph[j][j2] = sum([host.get_jacobian(i,j)*host.get_jacobian(i,j2) for i in range(N)])

			merit_rel = float('inf')

			# 4) Levenberg-Marquardt loop
			while lamb < self.lamb_max and merit_rel > self.lamb_tol:
				# 4a) Solve the linear system alph*delt = beta inverting alph
				for j in range(M): alph[j][j] *= (1+lamb)

				inv_alph = inv(alph)

				for j in range(M): delt[j] = sum([inv_alph[j2][j]*beta[j2] for j2 in range(M)])

				host.increase_P(delt)
				chiSquared = host.merit()

				merit_rel = (chiSquared-chiSquared_last)

				# 4b) If merit_rel increases we are not doing well
				if merit_rel <= 0:
					lamb /= self.lamb_dmp
					break
				# 4c) Then the iteration is doing well
				else:
					lamb *= self.lamb_dmp

				host.increase_P([-d for d in delt])
				chiSquared = host.merit()

			# 5) When the merit can't reduce more break the loop!
			if merit_rel > -self.lamb_tol: break

			count += 1
		if self.pr: print("  iteration " + str(count) + ", sum of squares = " + str(host.get_chiSquared()))
# End of <class LevenbergMarquardt>

# End of file : fitting.py
