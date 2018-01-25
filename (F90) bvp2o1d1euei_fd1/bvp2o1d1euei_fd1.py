#!/usr/bin/env python

"""
bvp2o1d1euei_fd1
	@version : 0.1.0

	@author : Daniel Ríos Linares (c) 2018, hasbornasu@gmail.com

	@description : A simple BVP (Boundary Value Problem) solver for second order
		differential equations of the form y'' = f(y,x) (no y' term).

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

# Import bvp2o1d1euei_fd1_f90 module with Fortran compilation
import bvp2o1d1euei_fd1_f90

# <function bvp2o1d1euei_fd1(f, X, Y, tol, max_iters)>
#	@argument <function f> : y'' = f(y)
# 	@argument <list X> : 1D list with all the input independient variable
# 	@argument <list Y> : 1D list with the initial guess of dependient variable
# 	@argument <float tol> : output tolerance (when the maximum of the output
#		increase is lower than tol, stops the loop)
# 	@argument <int max_iters> : maximum number of iterations allowed
#
# 	@description : solves the 1D boundaries values problem (BVP), no y' term:
#   	y''(x) = f(y,x) }
# 		     y(xi) = yi }
# 	         y(xf) = yf }
# 		numerically by the method of finite differences with every X (non
#		uniform grid of points required)
#
#	@example :
#		def f(y,x): return y+x
#		y0 = 0
#		yf = 3
#		Y = bvp2o1d1euei_fd1(f,X,y0,yf)
#
#	@name : bvp2o1d1euei_fd1
#		    |  | | | | | | |
#		    |  | | | | | | version 1, means y''(x) = f(y,x)
#		    |  | | | | | Finite differences
#		    |  | | | | iterative method
#		    |  | | | non-uniform grid
#		    |  | | 1 equation (not a system)
#		    |  | 1 dimension y(x)
#		    |  2nd order ODE
#		    Boundary Value Problem
#
# 	@author : Daniel Ríos Linares
#
#	@version : 0.1.0
#
# 	@references :
# 		1) William H. Press, Saul A. TeuKolsky, W.T. Vetterling & B.P. Flannery
#          Numerical recipes in C - The art of Scientific Computing 2nd Edition
# 		   2002, chapter 17, Two point Boundary Value Problems, pages 762-772
#
def bvp2o1d1euei_fd1(f, X, y0, yf, tol=1e-12, max_iters=10000):
	N = len(X)
	Y = [y0 + (yf-y0)/(len(X)-1)*i for i in range(len(X))]
	Z = bvp2o1d1euei_fd1_f90.bvp2o1d1euei_fd1(f,X,Y,tol,max_iters,N)
	return Z
