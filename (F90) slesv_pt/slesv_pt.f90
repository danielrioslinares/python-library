


! <subroutine slesv_pt(<array 1-by-N> Aupp2, <array 1-by-N> Aupp,
!		<array 1-by-N> Adia, <array 1-by-N> Alow, <array 1-by-N> Alow,
!		<array 1-by-N> B, <integer> N, <array 1-by-N> X)>
! 	@argument <array 1-by-N> Aupp2 : upper upper diagonal vector
! 	@argument <array 1-by-N> Aupp : upper diagonal vector
! 	@argument <array 1-by-N> Adia : main diagonal vector
! 	@argument <array 1-by-N> Alow : lower diagonal vector
! 	@argument <array 1-by-N> Alow2 : lower lower diagonal vector
! 	@argument <array 1-by-N> B : B vector
! 	@argument <array 1-by-N> N : number of unknowns (length of Aupp, Adia...)
!
!	@returns <array 1-by-N> X : exact solution
!
! 	@description : implementation of the pentadiagonal solver of system of
!		linear equations, being the matrix of coefficients N-by-N:
!			[a_{d,1}  a_{u,1}  a_{u2,1}       0        ...       0         0       ]
!			[a_{l,2}  a_{d,2}  a_{u,2}  a_{u2,2}       ...       0         0       ]
!			[a_{l2,2} a_{l,3}  a_{d,3}  a_{u,3}        ...       0         0       ]
!			[   0     a_{l2,3} a_{l,3}    ...          ...    a_{u,N-2} a_{u2,N-2} ]
!			[  ...     ...     ...        ...          ...      ...       ...      ]
!			[   0       0       0       a_{l2,N-1}  a_{l,N-1} a_{d,N-1} a_{u,N-1}  ]
!			[   0       0       0       0           a_{l2,N}  a_{l,N}   a_{d,N}    ]
!		with
!			Aupp2 = [a_{u2,1} a_{u2,2} ... a_{u2,N-2}    0         0      ]
!			Aupp  = [a_{u,1}  a_{u,2}  ... a_{u,N-2}  a_{u,N-1}    0      ]
!			Adia  = [a_{d,1}  a_{d,2}  ... a_{d,N-2}  a_{d,N-1}  a_{d,N}  ]
!			Alow  = [   0     a_{l,2}  ... a_{l,N-2}  a_{l,N-1}  a_{l,N}  ]
!			Alow2 = [   0        0     ... a_{l2,N-2} a_{l2,N-1} a_{l2,N} ]
!		the B matrix (transposed) 1-by-N:
!			B^T = [b_1 b_2 ... b_{N-1} b_N]
!
!	@name : slesv_pt
!		    ||||  |
!		    ||||  Pentadiagonal
!		    |||Solver
!		    ||Equations
!			|Linear
!		    System of
!
! 	@author : Daniel Ríos Linares
!
!	@version : 0.1.0 June 23, 2018
!
! 	@references :
!		[1] https://www.researchgate.net/publication/274377813_On_Solving_Pentadiagonal_Linear_Systems_via_Transformations
!
subroutine slesv_pt(Aupp2, Aupp, Adia, Alow, Alow2, B, N, X)

	implicit none

	! Input settings
	integer								:: N ! Number of diagonal coefficients

	! Input arrays
	real*8								:: Aupp2(N),Aupp(N),Adia(N),Alow(N),Alow2(N),B(N)

	! Pointers and temporal variables
	integer								:: i
	real*8								:: al(N),be(N),ze(N),ga(N),mu(N)

	! Output arrays
	real*8, intent(out)					:: X(N)

	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	! This must be met
	Aupp2(N) = 0
	Aupp2(N-1) = 0
	Aupp(N) = 0
	Alow(1) = 0
	Alow2(1) = 0
	Alow2(2) = 0

	! Fill the new matrix coefficients
	al(1) = Aupp(1) / Adia(1)
	al(2) = Aupp(2) / (Adia(2) - al(1) * Alow(2))
	mu(1) = Adia(1)
	mu(2) = Adia(2) - al(1) * Alow(2)
	be(1) = 0
	be(2) = Aupp2(2) / mu(2)
	ga(1) = 0
	ga(2) = Alow(2)
	ze(1) = B(1) / mu(1)
	ze(2) = (B(2) - ze(1) * ga(2)) / mu(2)

	do i=3,N-1

		ga(i) = Alow(i) - al(i-2) * Alow2(i)
		mu(i) = Adia(i) - be(i-2) * Alow2(i) - al(i-1) * ga(i)
		be(i) = Aupp2(1) / mu(i)
		ze(i) = (B(i) - ze(i-2) * Alow2(i) - ze(i-1) * ga(i)) / mu(i)

	end do

	ga(N) = Alow(N) - al(N-2) * Alow2(N)
	mu(i) = Adia(N) - be(N-2) * Alow2(N) - al(N-1) * ga(N)
	be(N) = 0
	ze(N) = (B(N) - ze(N-2) * Alow2(N) - ze(N-1) * ga(N)) / mu(N)

	! Backward solution x_i + alpha_i x_{i+1} + beta_i x_{i+2} = z_i
	X(N) = ze(N)
	X(N-1) = ze(N-1) - al(N) * X(N)

	do i=N,1,-1

		X(i) = ze(i) - al(i) * X(i+1) - be(i) * X(i+2)

	end do

end subroutine slesv_pt
