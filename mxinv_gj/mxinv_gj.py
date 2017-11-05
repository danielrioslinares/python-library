#!/usr/bin/env python

"""
mxinv_gj
	@version : 0.1.0

	@author : Daniel Ríos Linares (c) 2017, hasbornasu@gmail.com
	@description : A simple program to demonstrate Gauss-Jordan pivoting method
		of square matrix inversion

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

# <function mxinv_gj>
# 	@argument <list C> : N x N matrix to do the inversion
#
# 	@returns <list A> : N x N matrix inverse of <list C>
#
# 	@description : invert the input matrix with Gauss-Jordan algorithm by full
#		pivoting of a secondary matrix B
#
# 	@author : Daniel Ríos Linares
#
#	@name : mxinv_gj
#		    |     |
#		    |     Gauss-Jordan algorithm (pivoting)
#		    Matrix inversion
#
#	@version : 0.1.0 September 21, 2017
#
# 	@references :
# 		1) William H. Press, Saul A. TeuKolsky, W.T. Vetterling & B.P. Flannery
#          Numerical recipes in C - The art of Scientific Computing 2nd Edition
# 		   2002, chapter 2, Gauss-Jordan Elimination, pages 36-43
#
def mxinv_gj(C):

	N = len(C)
	M = len(C[0])
	if N != M:
		raise RivpyMatrixcalcError("Matrix N x M is not invertable, N = " + str(N) + ", M = " + str(M))

	A = [[C[i][j] for j in range(N)] for i in range(N)]
	B = [[0 if i != j else 1 for j in range(N)] for i in range(N)]

	for j in range(N):
		for i in range(j,N):
			if A[i][j] != 0:
				A[j],A[i] = A[i],A[j]
				B[j],B[i] = B[i],B[j]
			d = A[j][j]
			for k in range(N):
				try:
					A[j][k] /= d
					B[j][k] /= d
				except:
					raise RivpyMatrixcalcError("Singular matrix")
			for l in range(N):
				if l != j:
					d = -A[l][j]
					for k in range(N):
						A[l][k] += A[j][k]*d
						B[l][k] += B[j][k]*d
	return B
# End of <function mxinv_gj>

''' [ Exception treatment ] '''

class RivpyMatrixcalcError(Exception):

	def __init__(self, msg = None):
		if msg == None: msg = "Unknown error encountered"
		super(RivpyMatrixcalcError,self).__init__(msg)

# End of file : matrixcalc.py
