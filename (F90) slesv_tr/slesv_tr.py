##/usr/bin/env python

"""
slesv_tr
	@version : 0.1.0
	@author : Daniel Ríos Linares (c) 2018, hasbornasu@gmail.com
	@description : A simple program to demonstrate tridiagonal typical system of
		equation solution (for example Poisson's equation)
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
import slesv_tr_f90

# <function sle_tr(<list> Aupp, <list<float>> Adia, <list<float>> Alow, <list<float>> B, <integer> N, <list<float>> X)>
# 	@argument <list<float>> Aupp : upper diagonal vector
# 	@argument <list<float>> Adia : main diagonal vector
# 	@argument <list<float>> Alow : lower diagonal vector
# 	@argument <list<float>> B : B vector
# 	@argument <list<float>> N : number of unknowns (lenght of Aupp, Adia...)
#
#	@returns <list<float>> X : exact solution
#
# 	@description : implementation of the tridiagonal solver of system of linear
#		equations, being the matrix of coefficients N-by-N:
#			[a_{d,1} a_{u,1}    0       0       ...           0         0   ]
#			[a_{l,2} a_{d,2} a_{u,2}    0       ...           0         0   ]
#			[   0    a_{l,3} a_{d,3} a_{u,3}    ...           0         0   ]
#			[   0       0      ...     ...      ...           0         0   ]
#			[   0       0       0       0     a_{l,N-1} a_{d,N-1} a_{u,N-1} ]
#			[   0       0       0       0           0   a_{l,N}   a_{d,N}   ]
#		with
#			Aupp = [a_{u,1} a_{u,2} ... a_{u,N-1}    0   ]
#			Adia = [a_{d,1} a_{d,2} ... a_{d,N-1} a_{d,N}]
#			Alow = [   0    a_{l,2} ... a_{l,N-1} a_{l,N}]
#		the B matrix (transposed) 1-by-N:
#			B^T = [b_1 b_2 ... b_{N-1} b_N]
#
#	@name : slesv_tr
#		    ||||  |
#		    ||||  Tridiagonal
#		    |||Solver
#		    ||Equations
#			|Linear
#		    System of
#
# 	@author : Daniel Ríos Linares
#
#	@version : 0.1.0 June 15, 2018
#
# 	@references :
#		@TODO XXX
#
def slesv_tr(Aupp, Adia, Alow, B): return slesv_tr_f90.slesv_tr(Aupp, Adia, Alow, B, len(Adia))
