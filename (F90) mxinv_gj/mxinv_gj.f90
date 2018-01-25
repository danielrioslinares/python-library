

! Matrix inversion using Gauss-Jordan pivoting method
subroutine mxinv_gj(C,N,B)

	implicit none
	! i : row, j : column, k : column, l : row, N is size of the matrix
	integer								:: i, j, k, l, N

	! C : input array, A : pivoting array, B : output array (inverted)
	real								:: C(N,N), A(N,N)
	real, intent(out)					:: B(N,N)

	! d : diagonal temporal value, save : register for traspose
	real								:: save, d

	! Copy input to to A
	do i = 1,N
		do j = 1,N
			A(i,j) = C(i,j)
		end do
	end do

	! Identity matrix (pivoting)
	do i = 1,N
		B(i,i) = 1
	end do

	do j = 1,N
		do i = j,N
			if (A(i,j) /= 0) then
				do k = 1,N
					save = A(j,k)
					A(j,k) = A(i,k)
					A(i,k) = save
					save = B(j,k)
					B(j,k) = B(i,k)
					B(i,k) = save
				end do
			end if

			d = A(j,j)

			do k = 1,N
				A(j,k) = A(j,k)/d
				B(j,k) = B(j,k)/d
			end do

			do l = 1,N
				if (l /= j) then
					d = -A(l,j)
					do k = 1,N
						A(l,k) = A(l,k) + A(j,k)*d
						B(l,k) = B(l,k) + B(j,k)*d
					end do
				end if
			end do
		end do
	end do

end subroutine mxinv_gj
! End of <subroutine mxinv_gj>
