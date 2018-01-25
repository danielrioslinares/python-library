

! Finds the root of the function func(x) located between xa and xb
subroutine bisection(fcn,xa,xb,tol,max_iters,x)

	implicit none

	! Output variables
	real, intent(out)					:: x

	! External function
	external							:: fcn
	real								:: fcn

	! Algorithm variables
	real								:: fa, fb, fc
	real								:: xa, xb, xc

	! Stop conditions variables
	real								:: tol
	integer								:: i, N, max_iters
	N = min( int(log((xb-xa)/tol)/log(2.0)), max_iters )

	fa = fcn(xa)
	fb = fcn(xb)

	i = 0
	do while (i < N)
		xc = (xa+xb)/2.0
		fc = fcn(xc)

		if (fa*fc < 0) then
			xb = xc
			fb = fc
		end if

		if (fc*fb < 0) then
			xa = xc
			fa = fc
		end if

		if (fa*fb == 0) then
			exit
		end if

		i = i + 1

	end do

	x = (xa+xb)/2.0

end subroutine bisection

! Finds the root of the function func(x) located between xa and xb
subroutine secant(fcn,x0,x1,tol,max_iters,x)

	implicit none

	! Output variables
	real, intent(out)					:: x

	! External function
	external							:: fcn
	real								:: fcn

	! Algorithm variables
	real								:: fp1, fp0, fm1
	real								:: x0, x1
	real								:: xp1, xp0, xm1, last_xt

	! Stop conditions variables
	real								:: tol
	integer								:: i, N, max_iters
	N = max_iters

	fp0 = fcn(x1)
	fm1 = fcn(x0)

	xp0 = x1
	xm1 = x0

	i = 0
	do while (i < N)

		xp1 = xp0 - fp0 * (xp0 - xm1) / (fp0 - fm1)

		if (abs(xp1 - xp0) < tol) then
			exit
		end if

		fp1 = fcn(xp1)

		xm1 = xp0
		xp0 = xp1

		fm1 = fp0
		fp0 = fp1

		i = i + 1

	end do

	x = xp1

end subroutine secant

! Finds the root of the function func(x) located between xa and xb
subroutine regulafalsi(fcn,xa,xb,tol,max_iters,x)

	implicit none

	! Output variables
	real, intent(out)					:: x

	! External function
	external							:: fcn
	real								:: fcn

	! Algorithm variables
	real								:: fa, fb, fc
	real								:: xa, xb, xc, last_xc

	! Stop conditions variables
	real								:: tol
	integer								:: i, N, max_iters
	N = max_iters

	fa = fcn(xa)
	fb = fcn(xb)

	i = 0
	do while (i < N)

		xc = (xa*fb-xb*fa)/(fb-fa)

		if (abs(last_xc - xc) < tol) then
			exit
		end if

		fc = fcn(xc)

		if (fa*fc < 0) then
			xb = xc
			fb = fc
		end if

		if (fc*fb < 0) then
			xa = xc
			fa = fc
		end if

		if (fa*fb == 0) then
			exit
		end if

		i = i + 1

	end do

	x = xc

end subroutine regulafalsi

! Finds the root of the function func(x) located between xa and xb
subroutine ridders(fcn,xa,xb,tol,max_iters,x)

	implicit none

	! Output variables
	real, intent(out)					:: x

	! External function
	external							:: fcn
	real								:: fcn

	! Algorithm variables
	real								:: f1, f2, f3, f4
	real								:: xa, xb
	real								:: x1, x2, x3, x4

	! Stop conditions variables
	real								:: tol
	integer								:: i, N, max_iters
	N = max_iters

	x1 = xa
	x2 = xb
	x3 = (x1 + x2) / 2

	f1 = fcn(x1)
	f2 = fcn(x2)
	f3 = fcn(x3)

	i = 0
	do while (i < N)

		x4 = x3 + (x3-x1) * (sign(f1,f2) * f3) / sqrt(f3*f3 - f1*f2)

		if (abs(x4 - x3) < tol) then
			exit
		end if

		f4 = fcn(x4)

		x1 = x2
		x2 = x3
		x3 = x4

		f1 = f2
		f2 = f3
		f3 = f4

		i = i + 1

	end do

	x = x4

end subroutine ridders

! Finds the root of the function func(x) located between xa and xb
subroutine newtonraphson(fcn,x0,tol,max_iters,x)

	implicit none

	! Output variables
	real, intent(out)					:: x

	! External function
	external							:: fcn
	real								:: fcn

	! Algorithm variables
	real								:: f0, f1
	real								:: x0, xt, last_xt

	! Stop conditions variables
	real								:: tol
	integer								:: i, N, max_iters
	N = max_iters

	xt = x0

	i = 0
	do while (i < N)

		f0 = fcn(xt,0)
		f1 = fcn(xt,1)

		last_xt = xt
		xt = xt-f0/f1

		if (abs(last_xt - xt) < tol) then
			exit
		end if

		i = i + 1
	end do

	x = xt

end subroutine newtonraphson

! Finds the root of the function func(x) located between x1 and x1
subroutine brent(fcn,x1,x2,tol,max_iters,x)

	implicit none

	! Output variables
	real, intent(out)					:: x

	! External function
	external							:: fcn
	real								:: fcn

	! Algorithm variables
	real								:: fa, fb, fc
	real								:: x0, x1, x2
	real								:: xa, xb, xc, xd, xe, xm
	real								:: p, q, r, s

	! Stop conditions variables
	real								:: tol, tol1, EPS
	real								:: min, min1, min2
	integer								:: i, N, max_iters
	N = max_iters

	EPS = 3.0e-8

	xa = x1
	xb = x2
	xc = x2

	fa = fcn(xa)
	fb = fcn(xb)
	fc = fb !fb = fcn(xc)

	i = 0
	do while (i < N)

		if (((fb > 0).and.(fc > 0)).or.((fb < 0).and.(fc < 0))) then
			xc = xa
			fc = fa
			xe = xd
			xd = xb - xa
		end if

		if (abs(fc) < abs(fb)) then
			xa = xb
			xb = xc
			xc = xa
			fa = fb
			fb = fc
			fc = fa
		end if

		tol1 = 2 * EPS * abs(xb) + 0.5 * tol
		xm = (xc - xb) / 2

		if ((abs(xm) <= tol1).or.(fb == 0)) then
			exit
		end if

		if ((abs(xe) >= tol1).and.(abs(fa) > abs(fb))) then

			s = fb/fa

			if (xa == xc) then
				p = 2 * xm * s
				q = 1 - s
			else
				q = fa/fc
				r = fb/fc
				p = s * (2 * xm * q * (q - r)-(xb - xa) * (r-1))
				q = (q - 1) * (r - 1) * (s - 1)
			end if

			if (p > 0) then
				q = -q
			end if

			p = abs(p)

			min1 = 3 * xm * q - abs(tol1 * q)
			min2 = abs(xe * q)

			if (min1 < min2) then
				min = min1
			else
				min = min2
			end if

			if (2*p < min) then
				xe = xd
				xd = p / q
			else
				xd = xm
				xe = xd
			end if
		else
			xd = xm
			xe = xd
		end if

		xa = xb
		fa = fb

		if (abs(xd) > tol) then
			xb = xb + xd
		else
			xb = xb + sign(tol1,xm)
		end if

		fb = fcn(xb)

		i = i + 1
	end do

	x = xb

end subroutine brent
