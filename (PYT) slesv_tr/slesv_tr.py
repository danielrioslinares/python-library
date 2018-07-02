


# <subroutine slesv_tr(<list<float>> Aupp, <list<float>> Adia, <list<float>> Alow, <list<float>> B)>
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
#	@version : 0.1.0 July 2, 2018
#
def slesv_tr(Aupp, Adia, Alow, B):
	# Init
	X = [0 for i in range(len(B))]
	P = [0 for i in range(len(B))]
	Q = [0 for i in range(len(B))]

 	# Alow[0] and Aupp[-1] are 0 (this must be met)
	Alow[0] = 0
	Aupp[-1] = 0

	# P[0] and Q[0] are known because Alow[0] = 0 always
	P[0] = - Aupp[0] / Adia[0]
	Q[0] = B[0] / Adia[0]

	# Obtain temporal vectors of gaussian elimination
	for i in range(1,len(B)):
		P[i] = - Aupp[i] / (Adia[i] + Alow[i] * P[i-1])
		Q[i] = (B[i] - Alow[i] * Q[i-1]) / (Adia[i] + Alow[i] * P[i-1])

	# X[-1] is known because Aupp[-1] = 0 -> P[-1] = 0
	X[-1] = Q[-1]

	# X[i] is obtainable from X[-1]
	for i in reversed(range(len(B)-1)):
		X[i] = P[i] * X[i+1] + Q[i]

	# Ax = B is solved
	return X

# Simple example
if __name__ == '__main__':
	Aupp = [1,0,0]
	Alow = [0,-1,0]
	Adia = [1,1,-0.5]
	B = [1,1,1]

	X = slesv_tr(Aupp, Adia, Alow, B)

	print(X)
