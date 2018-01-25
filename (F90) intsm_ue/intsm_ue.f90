


! Obtains the simpson integration for Y = f(X) with non-uniform mesh
! N is the length of X and Y and inte is the result
subroutine intsm_ue(X, Y, N, inte)

	implicit none

	! Output variables
	real, intent(out)					:: inte

	! Algorithm variables
	integer								:: j, m, N, max_iters
	real								:: x_nm1, x_np0, x_np1, s, out
	real								:: X(N), Y(N)
	real								:: h_np1_p_np0_pow1, h_np1_p_nm1_pow1, h_np0_p_nm1_pow1, h_np1_m_nm1_pow1, h_np1_m_np0_pow1, h_np0_m_nm1_pow1
	real								:: h_np1_x_np0_pow1, h_np1_x_nm1_pow1, h_np0_x_nm1_pow1, h_np1_m_np0_pow2, h_np1_m_np0_pow3

	out = 0

	do j=2,N/2+1

		m = 2*j - 2

		if ( m+1 >= N ) then
			exit
		end if

		! X[n-1],X[n],X[n+1]
		x_nm1 = X(m-1)
		x_np0 = X(m  )
		x_np1 = X(m+1)
		PRINT *, x_nm1,x_np0,x_np1

		! Increments h
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

		! Simpson's method
		s = 0
		s = s + Y(m-1) * h_np1_m_np0_pow1 * ( h_np1_m_np0_pow3/3 - h_np1_p_np0_pow1 &
			* h_np1_m_np0_pow2/2 + h_np1_x_np0_pow1 * h_np1_m_nm1_pow1 )
		s = s - Y(m  ) * h_np1_m_nm1_pow1 * ( h_np1_m_np0_pow3/3 - h_np1_p_nm1_pow1 &
			* h_np1_m_np0_pow2/2 + h_np1_x_nm1_pow1 * h_np1_m_nm1_pow1 )
		s = s + Y(m+1) * h_np0_m_nm1_pow1 * ( h_np1_m_np0_pow3/3 - h_np0_p_nm1_pow1 &
			* h_np1_m_np0_pow2/2 + h_np0_x_nm1_pow1 * h_np1_m_nm1_pow1 )
		out = out + s / ( h_np1_m_np0_pow1 * h_np1_m_nm1_pow1 * h_np0_m_nm1_pow1 )

	end do

    ! Trapezoidal rule for N even
	if ( mod(N,2) == 0 ) then
		out = out - ( X(N-1) - X(N) ) * ( Y(N) + Y(N-1)) / 2
	end if

	inte = out

end subroutine intsm_ue
