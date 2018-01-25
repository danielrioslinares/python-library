

! BVP 2nd order 1D uneven iterative by finite differences y'' = f(y,x)
subroutine bvp2o1d1euei_fd1(fcn,X,Y,N,tol,max_iters,Z)
	implicit none

	! Output variables
	real, intent(out)					:: Z(N)
	real								:: X(N), Y(N), temp_Y(N), last_Y(N)
	real								:: h, tol, tol_temp

	! External function
	external							:: fcn
	real								:: fcn

	! Stop conditions variables
	integer								:: i, count, N, max_iters

	temp_Y = Y

	tol_temp = tol
	h = X(2)-X(1)
	count = 0
	do while ((count < max_iters).and.(tol_temp >= tol))
		last_Y = temp_Y
		tol_temp = 0
		do i = 2,N-1
			temp_Y(i) = (last_Y(i-1)+last_Y(i+1))/2
			temp_Y(i) = temp_Y(i) - (0.5*h**2)*fcn(temp_Y(i),X(i))
			if (abs(temp_Y(i)-last_Y(i)) > tol_temp) then
				tol_temp = abs(temp_Y(i)-last_Y(i))
			end if
		end do

		count = count + 1

	end do

	Z = temp_Y

end subroutine bvp2o1d1euei_fd1
! End of <subroutine bvp2o1d1euei_fd1>
