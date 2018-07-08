/* array_simo.c */

/* Header file */
#include "arr_mimo.h"

// <function input_2x_PyList1D__output_2x_PyList1D(PyObject* list1,
//		PyObject* list2)>
// 	@argument <PyObject* list1> : input Python list (C API)
// 	@argument <PyObject* list2> : input Python list (C API)
//
//	@returns <PyObject* tuple{<PyObject* list>,<PyObject* list>}> : output
//		Python list with two lists inside (C API)
//
// 	@description : Python list treatment of 2 input 1D lists with 2 new output
//		1D lists
//
//	@name : input_2x_PyList1D__output_2x_PyList1D
//		    |     |  |     |   |      |  |     |
//		    |     |  |     |   |      |  |     1D
//		    |     |  |     |   |      |  PyList
//		    |     |  |     |   |      2
//		    |     |  |     |   returns
//		    |     |  |     1D
//		    |     |  PyList
//		    |     2
//		    With an input of
//
// 	@author : Daniel Ríos Linares
//
//	@version : 0.1.0 July 7, 2017
//
PyObject* input_2x_PyList1D__output_2x_PyList1D(PyObject* list1, PyObject* list2) {

	/* Check list size */
	int N1 = PyList_Size(list1);
	int N2 = PyList_Size(list2);

	/* Declare array */
	double array1[N1];
	double array2[N2];

	/* Python list<float> to C double array */
	for (int i = 0 ; i < N1 ; i++)
		array1[i] = PyFloat_AsDouble(PyList_GetItem(list1, i));
	for (int i = 0 ; i < N2 ; i++)
		array2[i] = PyFloat_AsDouble(PyList_GetItem(list2, i));
	/* End of Python list fill */

	////////////////////////////////////////////////////////////////////////////

	/* Declare output array */
	double output1[N1];
	double output2[N2];



	// Do what you wanna do, for example, duplicate all values in the input list
	for (int i = 0 ; i < N1 ; i++)
		output1[i] = array1[i] * 2;

	for (int i = 0 ; i < N2 ; i++)
		output2[i] = array2[i] * 3;




	////////////////////////////////////////////////////////////////////////////

	/* C double array to Python list<float> */
	// Output 1
	PyObject* result1 = PyList_New(N1);
    for (int i = 0; i < N1; i++)
    	PyList_SetItem(result1, i, PyFloat_FromDouble(output1[i]));

	// Output 2
	PyObject* result2 = PyList_New(N2);
    for (int i = 0; i < N2; i++)
    	PyList_SetItem(result2, i, PyFloat_FromDouble(output2[i]));

	// Final output
	PyObject* result = PyTuple_New(2);
	PyTuple_SetItem(result, 0, result1);
	PyTuple_SetItem(result, 1, result2);
	/* End of Python list fill */

    return result;
}

// <function input_2x_PyList2D__output_2x_PyList2D(PyObject* list1,
//		PyObject* list2)>
// 	@argument <PyObject* list1> : input Python 2D list (C API)
// 	@argument <PyObject* list2> : input Python 2D list (C API)
//
//	@returns <PyObject* tuple{<PyObject* list>,<PyObject* list>}> : output
//		Python list with two lists inside (C API)
//
// 	@description : Python list treatment of 2 input 1D lists with 2 new output
//		2D lists
//
//	@name : input_2x_PyList2D__output_2x_PyList2D
//		    |     |  |     |   |      |  |     |
//		    |     |  |     |   |      |  |     2D
//		    |     |  |     |   |      |  PyList
//		    |     |  |     |   |      2
//		    |     |  |     |   returns
//		    |     |  |     2D
//		    |     |  PyList
//		    |     2
//		    With an input of
//
// 	@author : Daniel Ríos Linares
//
//	@version : 0.1.0 July 7, 2017
//
PyObject* input_2x_PyList2D__output_2x_PyList2D(PyObject* list1, PyObject* list2) {

	/* Check list size */
	int N1 = PyList_Size(list1);
	int M1 = PyList_Size(PyList_GetItem(list1, 0));
	int N2 = PyList_Size(list2);
	int M2 = PyList_Size(PyList_GetItem(list2, 0));

	/* Declare array */
	double array1[N1][M1];
	PyObject* list1_i = PyList_New(M1);
	double array2[N2][M2];
	PyObject* list2_i = PyList_New(M2);

	/* Python list<float> to C double array */
	for (int i = 0 ; i < N1 ; i++) {
		list1_i = PyList_GetItem(list1, i);
		for (int j = 0 ; j < M1 ; j++)
			array1[i][j] = PyFloat_AsDouble(PyList_GetItem(list1_i, j));

	}
	for (int i = 0 ; i < N2 ; i++) {
		list2_i = PyList_GetItem(list2, i);
		for (int j = 0 ; j < M2 ; j++)
			array2[i][j] = PyFloat_AsDouble(PyList_GetItem(list2_i, j));
	}
	/* End of Python list fill */

	////////////////////////////////////////////////////////////////////////////

	/* Declare output array */
	double output1[N1][M1];
	double output2[N2][M2];



	// Do what you wanna do, for example, duplicate all values in the input list
	for (int i = 0 ; i < N1 ; i++) {
		for (int j = 0 ; j < M1 ; j++)
			output1[i][j] = 2 * array1[i][j];
	}
	for (int i = 0 ; i < N2 ; i++) {
		for (int j = 0 ; j < M2 ; j++)
			output2[i][j] = 3 * array2[i][j];
	}





	////////////////////////////////////////////////////////////////////////////

	/* C double array to Python list<float> */
	// Output 1
	PyObject* result1 = PyList_New(N1);
	for (int i = 0 ; i < N1 ; i++) {
		PyObject* result1_i = PyList_New(M1);
		for (int j = 0 ; j < M1 ; j++)
			PyList_SetItem(result1_i, j, PyFloat_FromDouble(output1[i][j]));
		PyList_SetItem(result1, i, result1_i);
	}

	// Output 2
	PyObject* result2 = PyList_New(N2);
	for (int i = 0 ; i < N2 ; i++) {
		PyObject* result2_i = PyList_New(M2);
		for (int j = 0 ; j < M2 ; j++)
			PyList_SetItem(result2_i, j, PyFloat_FromDouble(output2[i][j]));
		PyList_SetItem(result2, i, result2_i);
	}

	// Final output
	PyObject* result = PyTuple_New(2);
	PyTuple_SetItem(result, 0, result1);
	PyTuple_SetItem(result, 1, result2);
	/* End of Python list fill */

    return result;
}
