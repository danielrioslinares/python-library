#!/usr/bin/env python

"""
intsm_ue
	@version : 0.1.0

	@author : Daniel Ríos Linares (c) 2018, hasbornasu@gmail.com

	@description : A simple program to demonstrate the classical Simpson 1D
	 	integration of a set of data X,Y with a non-uniform mesh (uneven)

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

# Import the integration coded in FORTRAN and converted with F2PY
import intsm_ue_f90

# <function intsm_ue(X, Y)>
# 	@argument <list X> : 1D list with all the input independient variable
# 	@argument <list Y> : 1D list with all the f(X) of dependient variable
#
#	@returns <float inte> : integration of f(x) along X
#
# 	@description : implementation of the Simpson integration for a non-uniform
#		1D mesh, if you want to integrate an uniform mesh is better to use the
#		<function int1duu_simpson>
#
#	@example: integration of f(x) = x^2 in the interval x = [0,1]
#		X = [i/100 for i in range(101)]
#		Y = [x**2 for x in X]
#		result = intsm_ue(X,Y)
#
#	@name : intsm_ue
#		    |  |  |
#		    |  |  non-uniform grid
#		    |  Integration method (Simpson)
#		    Integration
#
# 	@author : Daniel Ríos Linares
#
#	@version : 0.1.0 January 25, 2018
#
# 	@references :
#		@TODO all the mathematical treatment made by myself
#
def intsm_ue(X, Y): return intsm_ue_f90.intsm_ue(X,Y,len(X))
