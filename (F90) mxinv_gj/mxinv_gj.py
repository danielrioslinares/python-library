
"""
mxinv_gj
v0.1.0

	Matrix inversion, returns the inverse of a square matrix with the full
	pivoting Gauss-Jordan elimination.

Copyright (C) 2018  Daniel Ríos Linares

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

# Module on FORTRAN 90
import mxinv_gj_f90

# <function mxinv_gj_f90>
# 	@argument <list C> : NxN matrix to do the inversion
#
# 	@returns <list A> : NxN matrix inverse of <list C>
#
# 	@description : invert the input matrix with Gauss-Jordan algorithm by full
#		pivoting of a secondary matrix B
#
#	@example :
#		A = [[1,0],[0,1]]
#		Ainverted = mxinv_gj(A)
#
#	@name : mxinv_gj
#		    | |   |
#		    | |   Gauss-Jordan pivoting method
#		    | Matrix inversion
#		    Matrix
#
# 	@author : Daniel Ríos Linares
#
#	@version : 0.1.0
#
# 	@references :
# 		1) William H. Press, Saul A. TeuKolsky, W.T. Vetterling & B.P. Flannery
#          Numerical recipes in C - The art of Scientific Computing 2nd Edition
# 		   2002, chapter 2, Gauss-Jordan Elimination, pages 36-43
def mxinv_gj(C):
	N = len(C)
	M = len(C[0])
	if N != M:
		raise RivpyMatrixcalcError("Matrix N x M is not invertable, N = " + str(N) + ", M = " + str(M))
	A = mxinv_gj_f90.mxinv_gj(C,N)
	if str(A[0][0]) == 'nan':
		raise RivpyMatrixcalcError("Singular matrix")
	return A

''' [ Exception treatment ] '''

class RivpyMatrixcalcError(Exception):

	def __init__(self, msg = None):
		if msg == None: msg = "Unknown error encountered"
		super(RivpyMatrixcalcError,self).__init__(msg)

# End of file : mxinv_gj.py
