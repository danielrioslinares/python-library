/* inpsp_cX.c */

/* Header file */
#include "inpsp_cX.h"

// <function inpsp_cs>
// 	@argument <PyObject* PyList_Xnew> : new mesh to be calculated
// 	@argument <PyObject* PyList_X> : Known abscissa
// 	@argument <PyObject* PyList_Y> : Known ordinate
// 	@argument <PyObject* PyFloat_Mi> : initial momentum (second derivative)
// 	@argument <PyObject* PyFloat_Mf> : final momentum (second derivative)
//
//	@returns <PyObject* tuple{PyList_Ynew,PyList_A,PyList_M}>
//		@element <PyObject* PyList_Ynew> : new ordinate base on PyList_Xnew
//		@element <PyObject* PyList_A> : polynomial coefficients
//		@element <PyObject* PyList_M> : momentums
//
// 	@description : interpolation of a set X,Y returning a new oversampled values
//		for Y given X, the polynomial coefficients and the momentums. The bounds
//		must be passed via M_i and M_f (initial and final momentums).
//
//	@name : inpsp_cs
//		    |  |  ||
//		    |  |  |Given second derivative value
//		    |  |  Cubic
//		    |  Spline
//		    Interpolation
//
// 	@author : Daniel Ríos Linares
//
//	@version : 0.1.0 (July 7, 2017) - first coding
//
PyObject* inpsp_cs(
    // New mesh to interpolate
    PyObject* PyList_Xnew,
    // Known X vs Y
    PyObject* PyList_X,
    PyObject* PyList_Y,
    // Momentums, initial and final,typically will be both 0 (natural spline)
    PyObject* PyFloat_Mi,
    PyObject* PyFloat_Mf
    ) {

	/* Check list sizes */
	int N = PyList_Size(PyList_X);
	int L = PyList_Size(PyList_Xnew);

	/* Declare arrays */
	double X[N];
	double Y[N];
    double Xnew[L];
	double Ynew[L];
    double H[N];
    double A[N+1][4]; // Polynomial coefficients
    double M[N]; // Momentums vector
    double Aupp[N-2]; // tridiagonal system of linear equations (upper diagonal)
    double Adia[N-2]; // tridiagonal system of linear equations (main diagonal)
    double Alow[N-2]; // tridiagonal system of linear equations (lower diagonal)
    double B[N-2]; // tridiagonal system of linear equations (B vector)

	/* Python list<float> to C double array */
	for (int i = 0 ; i < N ; i++) {
		X[i] = PyFloat_AsDouble(PyList_GetItem(PyList_X, i));
        Y[i] = PyFloat_AsDouble(PyList_GetItem(PyList_Y, i));
    }
	for (int i = 0 ; i < L ; i++) {
		Xnew[i] = PyFloat_AsDouble(PyList_GetItem(PyList_Xnew, i));
	}
	/* End of Python list fill */

	////////////////////////////////////////////////////////////////////////////

    if (N == 1) { /** For 1 simple point **/
        for (int j = 0 ; j < N+1 ; j++) {
            A[j][0] = Y[0];
            A[j][1] = 0;
            A[j][2] = 0;
            A[j][3] = 0;
            M[j] = 0;
        }
    } else { /** For the rest **/
        // H[0] will never be used
        H[0] = 0;

        // Fill the increment vector H(j) for intervals I_j[{x_j,x_{j+1}}_{j=0}^N]
		for (int j = 0 ; j < N-1 ; j++)
			H[j+1] = X[j+1] - X[j];

        /* Solve tridiagonal system of linear equations for momentums */
        // Main diagonal is filled with 2s
        for (int j = 0 ; j < N-2 ; j++)
            Adia[j] = 2;

        // Fill lower diagonal with H(i) division and with Alow(0) = 0
        Alow[0] = 0;
        for (int j = 1 ; j < N-2 ; j++)
            Alow[j] = H[j+1] / (H[j+1] + H[j+2]);

        // Fill upper diagonal with H(i) division and with Aupp(N-3) = 0
        Aupp[N-3] = 0;
        for (int j = 0 ; j < N-3 ; j++)
            Aupp[j] = H[j+2] / (H[j+1] + H[j+2]);

        // Fill the non-homogeneous vector b
        for (int j = 0 ; j < N-2 ; j++)
            B[j] = 6 / (H[j+1] + H[j+2]) * ( (Y[j+2] - Y[j+1]) / H[j+2] - (Y[j+1] - Y[j]) / H[j+1] );

		/* Solve the tridiagonal system of linear equations */
		// Temporal arrays
		double P[N-2];
		double Q[N-2];

		// Alow[0] and Aupp[-1] are 0 (this must be met)
		Alow[0] = 0;
		Aupp[N-3] = 0;

		// P[0] and Q[0] are known because Alow[0] = 0 always
		P[0] = - Aupp[0] / Adia[0];
		Q[0] = B[0] / Adia[0];

		// Obtain temporal vectors of gaussian elimination
		for (int i = 1 ; i < N-2 ; i++) {
			P[i] = - Aupp[i] / (Adia[i] + Alow[i] * P[i-1]);
			Q[i] = (B[i] - Alow[i] * Q[i-1]) / (Adia[i] + Alow[i] * P[i-1]);
		}

		// X[-1] is known because Aupp[-1] = 0 -> P[-1] = 0
		M[N-2] = Q[N-3];

		// X[i] is obtainable from X[-1]
		for (int i = N-4 ; i >= 0 ; i--)
			M[i+1] = P[i] * X[i+1] + Q[i];

		// Bounds conditions
		M[0] = PyFloat_AsDouble(PyFloat_Mi);
	    M[N-1] = PyFloat_AsDouble(PyFloat_Mf);

        /* Fill the coefficients of the cubic polynomial */
        for (int j = 0 ; j < N-1 ; j++) {
            A[j+1][3] = 1 / (6 * H[j+1]) * (M[j+1] - M[j]);
			A[j+1][2] = (X[j+1] * M[j] - X[j] * M[j+1]) / (2 * H[j+1]);
            A[j+1][1] = X[j]*X[j] / (2 * H[j+1]) * M[j+1] + (Y[j+1] - Y[j]) / H[j+1] - H[j+1] / 6 * (M[j+1] - M[j]) - X[j+1]*X[j+1] / (2 * H[j+1]) * M[j];
			A[j+1][0] = (X[j+1]*X[j+1]*X[j+1] * M[j] - X[j]*X[j]*X[j] * M[j+1]) / (6 * H[j+1]) + Y[j] - H[j+1]*H[j+1] / 6 * M[j] - ((Y[j+1] - Y[j]) / H[j+1] - H[j+1] / 6 * (M[j+1] - M[j])) * X[j];
        }
        A[0][3] = 0;
        A[0][2] = 0;
        A[0][1] = 3 * A[1][3] * X[0]*X[0] + 2 * A[1][2] * X[0] + A[1][1];
        A[0][0] = Y[0] - A[0][1] * X[0];
        A[N][3] = 0;
        A[N][2] = 0;
        A[N][1] = 3 * A[N-1][3] * X[N-1]*X[N-1] + 2 * A[N-1][2] * X[N-1] + A[N-1][1];
        A[N][0] = Y[N-1] - A[N][1] * X[N-1];
    }

    /* Evaluate the new mesh (last_i speeds up the loop for sorted new_X) */
    int last_i = 1;
    int i;

    for (int j = 0 ; j < L ; j++) {
        if (Xnew[j] <= X[0]) {
            i = 0;
        } else if (Xnew[j] >= X[N-1]) {
            i = N;
        } else if (Xnew[j] >= X[last_i] && Xnew[j] <= X[last_i+1]) {
            i = last_i+1;
        } else {
            // For all intervals
            for (int k = 0 ; k < N-1 ; k++) {
                // Interval selection
                if (Xnew[j] >= X[k] && Xnew[j] <= X[k+1]) {
                    i = k+1;
                }
            }
        }

        // Remember last interval
        last_i = i;

        // Fill the new mesh output Ynew
        Ynew[j] = A[i][3] * Xnew[j]*Xnew[j]*Xnew[j] + A[i][2] * Xnew[j]*Xnew[j] + A[i][1] * Xnew[j] + A[i][0];
		//printf("f(Xnew[%i] = %f) = %f\n",j,Xnew[j],Ynew[j]);
    }

    ////////////////////////////////////////////////////////////////////////////

	/* C double array to Python list<float> */
	PyObject* PyTuple_out = PyTuple_New(3);

	// New mesh
	PyObject* PyList_Ynew = PyList_New(L);
    for (int j = 0; j < L; j++)
    	PyList_SetItem(PyList_Ynew, j, PyFloat_FromDouble( Ynew[j] ));
	PyTuple_SetItem(PyTuple_out, 0, PyList_Ynew);
	// Polynomial coefficients
	PyObject* PyList_A = PyList_New(N+1);
    for (int j = 0; j < N+1; j++) {
		PyObject* PyList_A_j = PyList_New(4);
		for (int i = 0 ; i < 4 ; i++)
			PyList_SetItem(PyList_A_j, i, PyFloat_FromDouble( A[j][i] ));
    	PyList_SetItem(PyList_A, j, PyList_A_j);
	}
	PyTuple_SetItem(PyTuple_out, 1, PyList_A);
	// Momentums vector
	PyObject* PyList_M = PyList_New(N+1);
    for (int j = 0; j < N+1; j++)
    	PyList_SetItem(PyList_M, j, PyFloat_FromDouble( M[j] ));
	PyTuple_SetItem(PyTuple_out, 2, PyList_M);

	/* Return */
    return PyTuple_out;

}
/******************************************************************************/


// <function inpsp_cf>
// 	@argument <PyObject* PyList_Xnew> : new mesh to be calculated
// 	@argument <PyObject* PyList_X> : Known abscissa
// 	@argument <PyObject* PyList_Y> : Known ordinate
// 	@argument <PyObject* PyFloat_Ci> : initial momentum (second derivative)
// 	@argument <PyObject* PyFloat_Cf> : final momentum (second derivative)
//
//	@returns <PyObject* tuple{PyList_Ynew,PyList_A,PyList_M}>
//		@element <PyObject* PyList_Ynew> : new ordinate base on PyList_Xnew
//		@element <PyObject* PyList_A> : polynomial coefficients
//		@element <PyObject* PyList_M> : momentums
//
// 	@description : interpolation of a set X,Y returning a new oversampled values
//		for Y given X, the polynomial coefficients and the momentums. The bounds
//		must be passed via Ci and Cf (first derivative).
//
//	@name : inpsp_cf
//		    |  |  ||
//		    |  |  |First derivative approach (given boundary ds/dx)
//		    |  |  Cubic
//		    |  Spline
//		    Interpolation
//
// 	@author : Daniel Ríos Linares
//
//	@version : 0.1.0 (July 7, 2017) - first coding
//
PyObject* inpsp_cf(
    // New mesh to interpolate
    PyObject* PyList_Xnew,
    // Known X vs Y
    PyObject* PyList_X,
    PyObject* PyList_Y,
    // Momentums, initial and final,typically will be both 0 (natural spline)
    PyObject* PyFloat_Ci,
    PyObject* PyFloat_Cf
    ) {

	/* Check list sizes */
	int N = PyList_Size(PyList_X);

	//
	double Ci = PyFloat_AsDouble(PyFloat_Ci);
	double Cf = PyFloat_AsDouble(PyFloat_Cf);


	// Calculate from a fake Xnew (empty)
	PyObject* PyList_fake_Xnew = PyList_New(0);
	PyObject* PyTuple_in;
	PyTuple_in = inpsp_cs(PyList_fake_Xnew, PyList_X, PyList_Y, PyFloat_FromDouble(0), PyFloat_FromDouble(0));

	// Get momentums vector
	PyObject* PyList_M;
	PyList_M = PyTuple_GetItem(PyTuple_in, 2);
	double M1 = PyFloat_AsDouble(PyList_GetItem(PyList_M, 1));
	double X1 = PyFloat_AsDouble(PyList_GetItem(PyList_X, 1));
	double X0 = PyFloat_AsDouble(PyList_GetItem(PyList_X, 0));
	double Y1 = PyFloat_AsDouble(PyList_GetItem(PyList_Y, 1));
	double Y0 = PyFloat_AsDouble(PyList_GetItem(PyList_Y, 0));
	double Mi = M1 * (X1-X0)*(X1-X0) - 6 * (X1-X0) * Ci + 6 * (Y1-Y0) / (X1-X0)*(X1-X0) + 6 * X1 * X0 - 3 * (X0*X0 + X1*X1);
	double MNm2 = PyFloat_AsDouble(PyList_GetItem(PyList_M, N-2));
	double XNm1 = PyFloat_AsDouble(PyList_GetItem(PyList_X, N-1));
	double XNm2 = PyFloat_AsDouble(PyList_GetItem(PyList_X, N-2));
	double YNm1 = PyFloat_AsDouble(PyList_GetItem(PyList_Y, N-1));
	double YNm2 = PyFloat_AsDouble(PyList_GetItem(PyList_Y, N-2));
	double Mf = -MNm2 * (XNm1-XNm2) + 6 * (XNm1-XNm2) * Cf + 6 * (YNm1-YNm2) / ((XNm1-XNm2)*(XNm1-XNm2)) + 6 * XNm1 * XNm2 - 3 * (XNm1*XNm1 + XNm2*XNm2);

	// Compute with the modified momentums
	PyObject* PyTuple_out;
	PyTuple_out = inpsp_cs(PyList_Xnew, PyList_X, PyList_Y, PyFloat_FromDouble(Mi), PyFloat_FromDouble(Mf));

	// Return it
	return PyTuple_out;

}
/******************************************************************************/
