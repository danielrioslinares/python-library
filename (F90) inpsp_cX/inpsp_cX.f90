
! <subroutine inpsp_cs(<array 1-by-L> new_X, <array 1-by-N> X, <array 1-by-N> Y,
!		<real> M_i, <real> M_f, <integer> N, <integer> L, <array 1-by-L> new_Y,
!		<array 1-by-N> M)>
! 	@argument <array 1-by-L> new_X : new X mesh
! 	@argument <array 1-by-N> X : interpolation data for abscissa
! 	@argument <array 1-by-N> Y : interpolation data for ordinate
! 	@argument <real> M_i : initial momentum
! 	@argument <real> M_f : final momentum
!	@argument <integer> N : lenght of interpolation data
!	@argument <integer> L : lenght of new mesh
!
!	@returns <array 1-by-L> new_Y : new Y mesh interpolated
!	@returns <array 1-by-N> M : momentum
!
! 	@description : implementation of the cubic spline interpolation with the
!		mixed approach (intial and final momentums are set by the user)
!
!	@name : inpsp_cs
!		    |  |  ||
!		    |  |  |Given second derivative value
!		    |  |  Cubic
!		    |  Spline
!		    Interpolation
!
! 	@author : Daniel Ríos Linares
!
!	@version : 0.1.0 June 16, 2018
!
subroutine inpsp_cs(new_X, X, Y, M_i, M_f, N, L, new_Y, A, M)

	implicit none

	! Input settings
	integer								:: N,L ! Number of points to interpolate

	! Input variables
	real*8								:: M_i,M_f ! Initial and final momentums

	! Input arrays
	real*8								:: X(0:N-1),Y(0:N-1),new_X(0:L-1)

	! Pointers and temporal variables
	integer								:: i,j,k,last_i
	real*8								:: H(0:N-1) ! Increment I_j
	real*8								:: Aupp(0:N-3),Adia(0:N-3),Alow(0:N-3)
	real*8								:: B(0:N-3) ! Momentum calcs
	real*8								:: P(0:N-3),Q(0:N-3)
	real*8								:: dydx

	! Output arrays
	real*8, intent(out)					:: new_Y(0:L-1) ! output new sampling
	real*8, intent(out)					:: A(-1:N-1,0:3) ! polinomial coefficients
	real*8, intent(out)					:: M(0:N-1) ! Momentum vector

	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	if (N == 1) then

		do i=-1,N-1

			A(i,0) = Y(0)
			A(i,1) = 0
			A(i,2) = 0
			A(i,3) = 0
			M(i) = 0

		end do

	else if (N == 2) then

		dydx = (Y(N-1) - Y(0)) / (X(N-1) - X(0))

		do i=-1,N-1

			A(i,0) = Y(0)
			A(i,1) = dydx
			A(i,2) = 0
			A(i,3) = 0
			M(i) = 0

		end do

	else

		! H(0) will never be used
		H(0) = 0

		! Fill the increment vector H(j) for intervals I_j[{x_j,x_{j+1}}_{j=0}^N]
		do j=0,N-2

			H(j+1) = X(j+1) - X(j)

		end do

		!! Solve tridiagonal system of linear equations for momentums

		! Fill main diagonal with 2s
		do i=0,N-3

			Adia(i) = 2

		end do

		! Fill lower diagonal with H(i) division and with Alow(0) = 0
		Alow(0) = 0

		do i=1,N-3

			Alow(i) = H(i+1) / (H(i+1) + H(i+2))

		end do

		! Fill upper diagonal with H(i) division and with Aupp(N-3) = 0
		Aupp(N-3) = 0

		do i=0,N-4

			Aupp(i) = H(i+2) / (H(i+1) + H(i+2))

		end do

		! Fill the non-homogeneous vector b
		do i=0,N-3

			B(i) = 6 / (H(i+1) + H(i+2)) * ( (Y(i+2) - Y(i+1)) / H(i+2) &
				- (Y(i+1) - Y(i)) / H(i+1) )

		end do

		! Add the limits
		M(0) = M_i
		call slesv_tr(Aupp, Adia, Alow, B, N-2, M(1:N-2))
		M(N-1) = M_f

		! Fill the coefficients of the cubic polynomial
		do j=0,N-2

			A(j,3) = 1 / (6 * H(j+1)) * (M(j+1) - M(j))
			A(j,2) = (X(j+1) * M(j) - X(j) * M(j+1)) / (2 * H(j+1))
			A(j,1) = X(j)**2 / (2 * H(j+1)) * M(j+1) + (Y(j+1) - Y(j)) / H(j+1) &
				- H(j+1) / 6 * (M(j+1) - M(j)) - X(j+1)**2 / (2 * H(j+1)) * M(j)
			A(j,0) = (X(j+1)**3 * M(j) - X(j)**3 * M(j+1)) / (6 * H(j+1)) + Y(j) - H(j+1)**2 / 6 * M(j) &
				- ((Y(j+1) - Y(j)) / H(j+1) - H(j+1) / 6 * (M(j+1) - M(j))) * X(j)

		end do

		A(-1,3) = 0
		A(-1,2) = 0
		A(-1,1) = 3 * A(0,3) * X(0)**2 + 2 * A(0,2) * X(0) + A(0,1)
		A(-1,0) = Y(0) - A(-1,1) * X(0)
		A(N-1,3) = 0
		A(N-1,2) = 0
		A(N-1,1) = 3 * A(N-2,3) * X(N-1)**2 + 2 * A(N-2,2) * X(N-1) + A(N-2,1)
		A(N-1,0) = Y(N-1) - A(N-1,1) * X(N-1)

	end if

	! Evaluate the new mesh new_X (last_i speeds up the loop for sorted new_X)
	last_i = 0
	do j=0,L-1

		if (new_X(j) <= X(0)) then

			i = -1

		else if (new_X(j) >= X(N-1)) then

			i = N-1

		else if (new_X(j) >= X(last_i) .and. new_X(j) <= X(last_i+1)) then

			i = last_i

		else
			! For all intervals
			do k=0,N-2

				! Interval selection
				if (new_X(j) >= X(k) .and. new_X(j) <= X(k+1)) then

					i = k

				end if

			end do

		end if

		! Remember the last interval
		last_i = i

		! Fill the new mesh output new_Y
		new_Y(j) = A(i,3) * new_X(j)**3 + A(i,2) * new_X(j)**2 &
			+ A(i,1) * new_X(j) + A(i,0)

	end do

end subroutine inpsp_cs

! <subroutine inpsp_cf(<array 1-by-L> new_X, <array 1-by-N> X, <array 1-by-N> Y,
!		<real> C_i, <real> C_f, <integer> N, <integer> L, <array 1-by-L> new_Y,
!		<array 1-by-N> M)>
! 	@argument <array 1-by-L> new_X : new X mesh
! 	@argument <array 1-by-N> X : interpolation data for abscissa
! 	@argument <array 1-by-N> Y : interpolation data for ordinate
! 	@argument <real> C_i : initial ds/dx
! 	@argument <real> C_f : final ds/dx
!	@argument <integer> N : lenght of interpolation data
!	@argument <integer> L : lenght of new mesh
!
!	@returns <array 1-by-L> new_Y : new Y mesh interpolated
!	@returns <array 4-by-N+2> A : matrix with polynomial coefficients
!	@returns <array 1-by-N> M : momentum
!
! 	@description : implementation of the cubic spline interpolation with the
!		first derivative approach (intial and final momentums are set)
!
!	@name : inpsp_cf
!		    |  |  ||
!		    |  |  |First derivative approach (given boundary ds/dx)
!		    |  |  Cubic
!		    |  Spline
!		    Interpolation
!
! 	@author : Daniel Ríos Linares
!
!	@version : 0.1.0 June 16, 2018
!
subroutine inpsp_cf(new_X, X, Y, C_i, C_f, N, L, new_Y, A, M)

	implicit none

	! Input settings
	integer								:: N,L ! Number of points to interpolate

	! Input variables
	real								:: C_i,C_f ! Initial and final ds/dx
	real								:: M_i,M_f ! Initial and final ds/dx

	! Input arrays
	real								:: X(0:N-1),Y(0:N-1),new_X(0:L-1)
	real								:: fake_new_X(0:1),fake_new_Y(0:1)

	! Output arrays
	real, intent(out)					:: new_Y(0:L-1) ! output new sampling
	real, intent(out)					:: A(-1:N-1,0:3) ! polinomial coefficients
	real, intent(out)					:: M(0:N-1) ! Momentum vector

	!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

	call inpsp_cs(fake_new_X, X, Y, M_i, M_f, N, 2, fake_new_Y, A, M)

	M_i = M(1) * (X(1) - X(0))**2 - 6 * (X(1) - X(0)) * C_i + 6 * (Y(1) - Y(0)) &
		/ ((X(1) - X(0))**2 + 6 * X(1) * X(0) - 3 * (X(0)**2 + X(1)**2))
	M_f = -M(N-2) * (X(N-1) - X(N-2)) + 6 * (X(N-1) - X(N-2)) * C_f + 6 * (Y(N-1) - Y(N-2)) &
		/ ((X(N-1) - X(N-2))**2 + 6 * X(N-1) * X(N-2) - 3 * (X(N-1)**2 + X(N-2)**2))

	call inpsp_cs(new_X, X, Y, M_i, M_f, N, L, new_Y, A, M)

end subroutine inpsp_cf

! <subroutine slesv_tr(<array 1-by-N> Aupp, <array 1-by-N> Adia,
!		<array 1-by-N> Alow, <array 1-by-N> B, <integer> N, <array 1-by-N> X)>
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
subroutine slesv_tr(Aupp, Adia, Alow, B, N, X)

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

end subroutine slesv_tr
