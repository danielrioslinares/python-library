/* mxinv_gj.c */

/* Python C API */
#include <Python.h>

// <function mxinv_gj(PyObject* list)>
// 	@argument <PyObject* list> : N x N matrix to do the inversion
//
// 	@returns <PyObject* B> : N x N matrix inverse of <PyObject* list>
//
// 	@description : invert the input matrix with Gauss-Jordan algorithm by full
//		pivoting of a secondary matrix B
//
//	@name : mxinv_gj
//		    |     |
//		    |     Gauss-Jordan algorithm (pivoting)
//		    Matrix inversion
//
// 	@author : Daniel Ríos Linares
//
//	@version : 0.1.0 July 8, 2017
//
// 	@references :
// 		1) William H. Press, Saul A. TeuKolsky, W.T. Vetterling & B.P. Flannery
//          Numerical recipes in C - The art of Scientific Computing 2nd Edition
// 		   2002, chapter 2, Gauss-Jordan Elimination, pages 36-43
//
PyObject* mxinv_gj(PyObject* list) {

	/* Check list size */
	int N = PyList_Size(list);

	/* Declare array */
	double A[N][N];

	/* Python list<float> to C double array */
	for (int i = 0 ; i < N ; i++) {
		for (int j = 0 ; j < N ; j++)
			A[i][j] = PyFloat_AsDouble(PyList_GetItem(PyList_GetItem(list, i), j));
	}
	/* End of Python list fill */

	////////////////////////////////////////////////////////////////////////////

	/* Declare output array */
	double B[N][N];

	// A is the input array
	for (int i = 0 ; i < N ; i++) {
		B[i][i] = 1;
	}

	// Matrix inversion (Gauss-Jordan method)
	for (int j = 0 ; j < N ; j++) {

		for (int i = j ; i < N ; i++) {

			if (A[i][j] != 0) {
				// Swap rows i,j
				for (int k = 0 ; k < N ; k++) {
					double tempA = A[j][k];
					A[j][k] = A[i][k];
					A[i][k] = tempA;
					double tempB = B[j][k];
					B[j][k] = B[i][k];
					B[i][k] = tempB;
				}
			}
			double d = A[j][j];

			for (int k = 0 ; k < N ; k++) {
				A[j][k] /= d;
				B[j][k] /= d;
			}

			for (int l = 0 ; l < N ; l++) {
				if (l != j) {
					d = -A[l][j];
					for (int k = 0 ; k < N ; k++) {
						A[l][k] += A[j][k] * d;
						B[l][k] += B[j][k] * d;
					}
				}
			}
		}
	}

	////////////////////////////////////////////////////////////////////////////

	/* C double array to Python list<float> */
	PyObject* result = PyList_New(N);

	for (int i = 0 ; i < N ; i++) {
		PyObject* result_i = PyList_New(N);
		for (int j = 0 ; j < N ; j++)
			PyList_SetItem(result_i, j, PyFloat_FromDouble(B[i][j]));
		PyList_SetItem(result, i, result_i);
	}
	/* End of Python list fill */

    return result;
}
