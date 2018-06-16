#/usr/bin/env python

"""
inpsp_cX
	@version : 0.1.0
	@author : Daniel Ríos Linares (c) 2018, hasbornasu@gmail.com
	@description : A simple program to demonstrate the cubic spline
		interpolation for momentum and first derivative
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
import inpsp_cX_f90

# <function inpsp_cs(<list<float>> new_X, <list<float>> X, <list<float>> Y,
#		<real> M_i, <real> M_f, <integer> N, <integer> L, <list<float>> new_Y,
#		<list<float>> M)>
# 	@argument <list<float>> new_X : new X mesh
# 	@argument <list<float>> X : interpolation data for abscissa
# 	@argument <list<float>> Y : interpolation data for ordinate
# 	@argument <float> M_i : initial momentum
# 	@argument <float> M_f : final momentum
#	@argument <int> N : lenght of interpolation data
#	@argument <int> L : lenght of new mesh
#
#	@returns <list<float>> new_Y : new Y mesh interpolated
#	@returns <list<list<float>>> A : matrix with polynomial coefficients
#	@returns <list<float>> M : momentum
#
# 	@description : implementation of the cubic spline interpolation with the
#		mixed approach (intial and final momentums are set by the user)
#
#	@name : inpsp_cs
#		    |  |  ||
#		    |  |  |Second derivative given d²s/dx²
#		    |  |  Cubic
#		    |  Spline
#		    Interpolation
#
# 	@author : Daniel Ríos Linares
#
#	@version : 0.1.0 June 16, 2018
#
def inpsp_cs(new_X, X, Y, M_i, M_f): return inpsp_cX_f90.inpsp_cs(new_X, X, Y, M_i, M_f)

# <function inpsp_cf(<list<float>> new_X, <list<float>> X, <list<float>> Y,
#		<float> M_i, <float> M_f, <int> N, <int> L, <list<float>> new_Y,
#		<list<list<float>>> A, <list<float>> M)>
# 	@argument <list<float>> new_X : new X mesh
# 	@argument <list<float>> X : interpolation data for abscissa
# 	@argument <list<float>> Y : interpolation data for ordinate
# 	@argument <float> C_i : initial ds/dx
# 	@argument <float> C_f : final ds/dx
#	@argument <int> N : lenght of interpolation data
#	@argument <int> L : lenght of new mesh
#
#	@returns <list<float>> new_Y : new Y mesh interpolated
#	@returns <list<list<float>>> A : matrix with polynomial coefficients
#	@returns <list<float>> M : momentum vector
#
# 	@description : implementation of the cubic spline interpolation with the
#		first derivative approach (intial and final momentums are set)
#
#	@name : inpsp_cf
#		    |  |  ||
#		    |  |  |First derivative approach (given boundary ds/dx)
#		    |  |  Cubic
#		    |  Spline
#		    Interpolation
#
# 	@author : Daniel Ríos Linares
#
#	@version : 0.1.0 June 16, 2018
#
def inpsp_cf(new_X, X, Y, C_i, C_f): return inpsp_cX_f90.inpsp_cf(new_X, X, Y, C_i, C_f)
