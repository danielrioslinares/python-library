


! Obtains the trapezoidal integration for Y = f(X) with non uniform mesh
! N is the length of X and Y and inte is the result
subroutine inttp_ue(X, Y, N, inte)

	implicit none

	! Output variables
	real, intent(out)					:: inte

	! Algorithm variables
	integer								:: i, m, N, max_iters
	real								:: x_nm1, x_np0, x_np1, s, out
	real								:: X(N), Y(N)
	real								:: h_np1_p_np0_pow1, h_np1_p_nm1_pow1, h_np0_p_nm1_pow1, h_np1_m_nm1_pow1, h_np1_m_np0_pow1, h_np0_m_nm1_pow1
	real								:: h_np1_x_np0_pow1, h_np1_x_nm1_pow1, h_np0_x_nm1_pow1, h_np1_m_np0_pow2, h_np1_m_np0_pow3

	out = 0

	do i=2,N

		out = out + ( X(i) - X(i-1) ) * ( Y(i) + Y(i-1) ) / 2

	end do

	inte = out

end subroutine inttp_ue
