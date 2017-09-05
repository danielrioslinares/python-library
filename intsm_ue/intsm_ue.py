#!/usr/bin/env python

"""
intsm_ue
	@version : 0.1.0

	@author : Daniel Ríos Linares (c) 2017, riv@hotmail.es

	@description : A simple program to demonstrate the classical Simpson 1D
	 	integration of a set of data X,Y with a non-uniform mesh (uneven), if
		you need the even version (faster) check for "int1d_sm_even" in the
		source.

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
#		    |  gration method
#		    Integration
#
# 	@author : Daniel Ríos Linares
#
#	@version : 0.1.0 August 22, 2017
#
# 	@references :
#		@TODO all the mathematical treatment made by myself
#
def intsm_ue(X, Y):
	# Integration
	inte = 0
	# Number of points
	N = len(X)
	# Main loop
	for j in range(1,int(N/2)+1):
		n = 2*j - 1

		# If N is even, is required a trapezoidal approximation at final:
		if n+1 >= N:
			break

		# X[n-1],X[n],X[n+1]
		x_nm1 = X[n-1]
		x_np0 = X[n  ]
		x_np1 = X[n+1]

		# Increments h
		h_np1_p_np0_pow1 = x_np1    + x_np0
		h_np1_p_nm1_pow1 = x_np1    + x_nm1
		h_np0_p_nm1_pow1 = x_np0    + x_nm1
		h_np1_m_nm1_pow1 = x_np1    - x_nm1
		h_np1_m_np0_pow1 = x_np1    - x_np0
		h_np0_m_nm1_pow1 = x_np0    - x_nm1
		h_np1_x_np0_pow1 = x_np1    * x_np0
		h_np1_x_nm1_pow1 = x_np1    * x_nm1
		h_np0_x_nm1_pow1 = x_np0    * x_nm1
		h_np1_m_np0_pow2 = x_np1**2 - x_nm1**2
		h_np1_m_np0_pow3 = x_np1**3 - x_nm1**3

		# Simpson's method
		s = 0
		s += Y[n-1] * h_np1_m_np0_pow1 * ( h_np1_m_np0_pow3/3 - h_np1_p_np0_pow1
			* h_np1_m_np0_pow2/2 + h_np1_x_np0_pow1 * h_np1_m_nm1_pow1 )
		s -= Y[n  ] * h_np1_m_nm1_pow1 * ( h_np1_m_np0_pow3/3 - h_np1_p_nm1_pow1
			* h_np1_m_np0_pow2/2 + h_np1_x_nm1_pow1 * h_np1_m_nm1_pow1 )
		s += Y[n+1] * h_np0_m_nm1_pow1 * ( h_np1_m_np0_pow3/3 - h_np0_p_nm1_pow1
			* h_np1_m_np0_pow2/2 + h_np0_x_nm1_pow1 * h_np1_m_nm1_pow1 )
		inte += s / ( h_np1_m_np0_pow1 * h_np1_m_nm1_pow1 * h_np0_m_nm1_pow1 )

	# Trapezoidal rule for N even
	if N % 2 == 0:
		inte -= ( X[-2] - X[-1] ) * ( Y[-1] + Y[-2] ) / 2
	return inte

# End of <function intsm_ue>
