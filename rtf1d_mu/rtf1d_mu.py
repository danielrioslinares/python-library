#!/usr/bin/env python

"""
rtf1d_mu
	@version : 0.1.0

	@author : Daniel Ríos Linares (c) 2017, hasbornasu@gmail.com
	@description : A program able to solve an equation f(x) = 0, you can use
	classic methods	like bisection, secant or regula-falsi, and others like Van
	Wijngaarden-Dekker-Brent.

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

# Import the rootfinding coded in FORTRAN and converted with F2PY
import rtf1d_mu_f90 as rootfinding_f90

# class RootFinding(function f, *function dfdx, *float tol, *int max_iters, *list args)
# 	@variable self.f : function to solve
# 	@variable self.dfdx : variation of the function f through independient (x)
# 	@variable self.tol : tolerance of error
# 	@variable self.max_iters : maximum number of iterations
# 	@variable self.args : required arguments for the function f and dfdx
#
# 	@description : solves the typical problem of f(x) = 0, using a variety of
# 		different numerical algorithms, is recommendable the brent when you do
# 		not want to calculate the derivate else you can use the newton method.
class RootFinding:

	def __init__(self, f, dfdx = None, tol = 1e-14, max_iters = 1000, args = []):
		self.f = f
		self.dfdx = dfdx if dfdx != None else self.dfdx_default
		self.args = args
		self.tol = tol
		self.max_iters = max_iters

	# fcn(x) : float function(float x)
	# 	@argument x : independient variable to evaluate
	#
	# 	@description : evaluation of the independient variable for self.f
	def fcn(self,x): return self.f(x,*self.args)

	# dfcndx(x) : float function(float x)
	# 	@argument x : independient variable to evaluate
	#
	# 	@description : evaluation of the independient variable for self.dfdx
	def dfcndx(self,x): return self.dfdx(x,*self.args)

	# dfdx_default(x) : float function(float x)
	# 	@argument x : independient variable to evaluate
	#
	# 	@description : when self.dfdx is not defined, automatically calculate
	# 		the numerical derivate
	def dfdx_default(self,x):
		h = 1e-12
		return (self.fcn(x+h) - self.fcn(x-h)) / (2*h)

	# bisection(a,b) : float function(float a, float b)
	# 	@argument a : lower bracketed independient value
	# 	@argument b : upper bracketed independient value
	#
	# 	@description : given a function self.f and an initial guess range from a
	# 		to b, a subroutine find the root of known function using bisection
	# 		the convergence is guaranteed.
	def bisection(self,a,b):
		if a > b:
			sol = rootfinding_f90.bisection(self.fcn,b,a,self.tol,self.max_iters)
		else:
			sol = rootfinding_f90.bisection(self.fcn,a,b,self.tol,self.max_iters)
		return sol

	# secant(a,b) : float function(float a, float b)
	# 	@argument a : lower bracketed independient value
	# 	@argument b : upper bracketed independient value
	#
	# 	@description : given a function self.f and an initial guess range from a
	# 		to b, a subroutine find the root of known function using secant,
	# 		the convergence is not guaranteed.
	def secant(self,a,b):
		sol = rootfinding_f90.secant(self.fcn,a,b,self.tol,self.max_iters)
		return sol

	# regulafalsi(a,b) : float function(float a, float b)
	# 	@argument a : lower bracketed independient value
	# 	@argument b : upper bracketed independient value
	#
	# 	@description : given a function self.f and an initial guess range from a
	# 		to b, a subroutine find the root of known function using regulafalsi
	# 		the convergence is not guaranteed.
	def regulafalsi(self,a,b):
		if a > b:
			sol = rootfinding_f90.regulafalsi(self.fcn,b,a,self.tol,self.max_iters)
		else:
			sol = rootfinding_f90.regulafalsi(self.fcn,a,b,self.tol,self.max_iters)
		return sol

	# ridders(a,b) : float function(float a, float b)
	# 	@argument a : lower bracketed independient value
	# 	@argument b : upper bracketed independient value
	#
	# 	@description : given a function self.f and an initial guess range from a
	# 		to b, a subroutine find the root of known function using ridders,
	# 		the convergence is not guaranteed.
	def ridders(self,a,b):
		sol = rootfinding_f90.regulafalsi(self.fcn,a,b,self.tol,self.max_iters)
		return sol

	# brent(a,b) : float function(float a, float b)
	# 	@argument a : lower bracketed independient value
	# 	@argument b : upper bracketed independient value
	#
	# 	@description : given a function self.f and an initial guess range from a
	# 		to b, a subroutine find the root of known function using brent,
	# 		the convergence is guaranteed and faster than other different of the
	# 		algorithms (excepting newton-raphson).
	def brent(self,a,b):
		sol = rootfinding_f90.brent(self.fcn,a,b,self.tol,self.max_iters)
		return sol

	# newtonraphson(x0) : float function(float a, float b)
	# 	@argument x0 : initial guess
	#
	# 	@description : given a function self.f and an initial guess x0, a
	# 		subroutine computes the succesion of values of x.
	def newtonraphson(self,x0):
		def f_and_dfdx(x,i): return self.fcn(x) if i == 0 else self.dfcndx(x)
		sol = rootfinding_f90.newtonraphson(f_and_dfdx,x0,self.tol,self.max_iters)
		return sol
