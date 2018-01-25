#!/usr/bin/env python

"""
bvp2o1d1euec_diffusion
	@version : 0.1.0

	@author : Daniel Ríos Linares (c) 2018, hasbornasu@gmail.com

	@description : A simple BVP (Boundary Value Problem) solver for second order
		differential equations - d/dx ( D(x) * dy/dx ) + K(x) y(x) = q(x),
		diffusion equation

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

# <function bvp2o1d1euec_diffusion(fD, dfDdx, fK, fq, X, y0, yf)>
# 	@argument <function fD> : diffusion coefficient in function of x
# 	@argument <function dfDdx> : diffusion coefficient derivate in function of x
# 	@argument <function fK> : coefficient with the dependient variable y
# 	@argument <function fq> : independient variable x function
# 	@argument <list X> : 1D list with all the input independient variable
# 	@argument <float y0> : left boundary value y(xi) = y0
# 	@argument <float yf> : right boundary value y(xf) = yf
#
# 	@description : solves the 1D diffusion boundaries values problem (BVP):
#   	- d/dx ( D(x) * dy/dx ) + K(x) y(x) = q(x) }
# 		                                y(xi) = yi }
# 		                                y(xf) = yf }
# 		numerically by the method of tridiagonal matrix casting of A·y = q, it's
#		not required an uniform X grid
#
#	@example : solves -y'' + y' = 1, y(1) = 0, y(7) = 1
#		def fD(x): return 1
#		def dfDdx(x): return 0
#		def fK(x): return 1
#		def fq(x): return 1
#		X = [1,2,3,4,5,6,7]
#		y0,yf = 0,1
#		Y = bvp2o1d1euec_diffusion(fD,dfDdx,fK,fq,X,y0,yf)
#
#	@name : bvp2o1d1euec_diffusion
#		    |  | | | | | |
#		    |  | | | | | Diffusion equation
#		    |  | | | | casting (exact method)
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
# 		1) R. Spurzem & C.P. Dullemond
#          Einführung in die Computerphysik - (Zentrum für Astronomie)
# 		   http://www.ita.uni-heidelberg.de/~dullemond/lectures/num_phys_2010
# 		   August 2010, chapter 1, Boundary Values Problem (BVP), pages 1-5
#
def bvp2o1d1euec_diffusion(fD,dfDdx,fK,fq,X,y0,yf):
	# Number of points in the grid
	N = len(X)

	# Solution grid with boundaries values
	Y = [0 for j in range(N)]
	Y[0],Y[-1] = y0,yf

	# A = | a_dc,001   a_ds,001   0.000000   ........   ........   0.000000 |
	#     | a_di,001   a_dc,002   a_ds,002   ........   ........   0.000000 |
	#     | 0.000000   a_di,002   a_dc,003   ........   ........   0.000000 |
	#     | 0.000000   0.000000   a_di,003   ........   ........   0.000000 |
	#     | ........   ........   ........   ........   ........   ........ |
	#     | ........   ........   ........   ........   a_dc,N-1   a_ds,N-1 |
	#     | 0.000000   0.000000   0.000000   ........   a_di,N-1   a_dc,N   |
	A_ds = [0 for j in range(N)]
	A_dc = [0 for j in range(N)]
	A_di = [0 for j in range(N)]

	A_dc[ 0] = 1
	A_dc[-1] = 1

	for i in range(1,N-1):
		# Local coefficients
		x = X[i]
		a = fD(x)
		b = dfDdx(x)
		c = fK(x)

		# Centered h
		x_ip1_m_im1 = X[i+1]-X[i-1]

		# Backward h
		x_ip0_m_im1 = X[i+0]-X[i-1]

		# Forward h
		x_ip1_m_ip0 = X[i+1]-X[i+0]

		# a_{i,i+1} coefficients of A matrix
		A_ds[i] = - 2*a / ( x_ip0_m_im1 * x_ip1_m_im1 ) + b / x_ip1_m_im1

		# a_{i,i} coefficients of A matrix
		A_dc[i] = + 2*a / ( x_ip1_m_ip0 * x_ip0_m_im1 ) + c

		# a_{i+1,i} coefficients of A matrix
		A_di[i] = - 2*a / ( x_ip1_m_ip0 * x_ip1_m_im1 ) - b / x_ip1_m_im1

	"""
	# Old uniform mesh implementation (substituted by the for loop above)
	for i in range(1,N-1):
		# Local coefficients
		x = X[i]
		a = fq(x)
		b = dfqdx(x)
		c = fK(x)

		# Constant h
		h = X[1]-X[0]

		# a_{i,i+1} coefficients of A matrix
		A_ds[i] = - 1*a / h**2 + b / (2*h)

		# a_{i,i} coefficients of A matrix
		A_dc[i] = + 2*a / h**2 + c

		# a_{i+1,i} coefficients of A matrix
		A_di[i] = - 1*a / h**2 - b / (2*h)
	"""
	# Sweep backwards
	for i in range(1,N):
		A_dc[i] -= A_di[i-1] * A_ds[i] / A_dc[i-1]
		Y[i] = fq(X[i]) - Y[i-1] * A_ds[i] / A_dc[i-1]

	# Sweep forward
	for i in reversed(range(N-1)):
		Y[i] -= A_di[i] * Y[i+1]
		Y[i] /= A_dc[i]

	return Y
# End of <function bvp2o1d1euec_diffusion>
