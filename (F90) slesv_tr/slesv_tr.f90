


! <subroutine sle_tr(<array 1-by-N> Aupp, <array 1-by-N> Adia, <array 1-by-N> Alow, <array 1-by-N> B, <integer> N, <array 1-by-N> X)>
! 	@argument <array 1-by-N> Aupp : upper diagonal vector
! 	@argument <array 1-by-N> Adia : main diagonal vector
! 	@argument <array 1-by-N> Alow : lower diagonal vector
! 	@argument <array 1-by-N> B : B vector
! 	@argument <array 1-by-N> N : number of unknowns (lenght of Aupp, Adia...)
!
!	@returns <array 1-by-N> X : exact solution
!
! 	@description : implementation of the tridiagonal solver of system of linear
!		equations, being the matrix of coefficients N-by-N:
!			[a_{d,1} a_{u,1}    0       0       ...           0         0   ]
!			[a_{l,2} a_{d,2} a_{u,2}    0       ...           0         0   ]
!			[   0    a_{l,3} a_{d,3} a_{u,3}    ...           0         0   ]
!			[   0       0      ...     ...      ...           0         0   ]
!			[   0       0       0       0     a_{l,N-1} a_{d,N-1} a_{u,N-1} ]
!			[   0       0       0       0           0   a_{l,N}   a_{d,N}   ]
!		with
!			Aupp = [a_{u,1} a_{u,2} ... a_{u,N-1}    0   ]
!			Adia = [a_{d,1} a_{d,2} ... a_{d,N-1} a_{d,N}]
!			Alow = [   0    a_{l,2} ... a_{l,N-1} a_{l,N}]
!		the B matrix (transposed) 1-by-N:
!			B^T = [b_1 b_2 ... b_{N-1} b_N]
!
!	@name : slesv_tr
!		    ||||  |
!		    ||||  Tridiagonal
!		    |||Solver
!		    ||Equations
!			|Linear
!		    System of
!
! 	@author : Daniel Ríos Linares
!
!	@version : 0.1.0 June 15, 2018
!
! 	@references :
!		@TODO XXX
!
subroutine sle_tr(Aupp, Adia, Alow, B, N, X)

	implicit none

	! Input settings
	integer								:: N ! Number of diagonal coefficients

	! Input arrays
	real								:: Aupp(N),Adia(N),Alow(N),B(N)

	! Pointers and temporal variables
	integer								:: i
	real								:: P(N),Q(N)

	! Output arrays
	real, intent(out)					:: X(N)

	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	! Alow(0) and Aupp(N) are 0 (this must be met)
	Alow(1) = 0
	Aupp(N) = 0

	! P(1) and Q(1) are known because Alow(1) = 0 always
	P(1) = -Aupp(1) / Adia(1)
	Q(1) = B(1) / Adia(1)

	! Obtain temporal vectors of gaussian elimination
	do i=2,N
		P(i) = - Aupp(i) / (Adia(i) + Alow(i) * P(i-1))
		Q(i) = (B(i) - Alow(i) * Q(i-1)) / (Adia(i) + Alow(i) * P(i-1))
	end do

	! X(N) is known because Aupp(N) = 0 -> P(N) = 0
	X(N) = Q(N)

	! X(i) is obtainable from X(N)
	do i=N-1,1,-1
		X(i) = P(i) * X(i+1) + Q(i)
	end do

end subroutine sle_tr
