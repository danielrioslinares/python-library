/* arr_simo.c */

/* Header file */
#include "arr_simo.h"

// <function input_1x_PyList1D__output_2x_PyList1D(PyObject* list)>
// 	@argument <PyObject* list> : input Python list (C API)
//
//	@returns <PyObject tuple{<PyObject* list>,<PyObject* list>}> : output Python
//		list with two lists inside (C API)
//
// 	@description : Python list treatment of 1 input list with 2 new output list
//
//	@name : input_1x_PyList1D__output_2x_PyList1D
//		    |     |  |     |   |      |  |     |
//		    |     |  |     |   |      |  |     1D
//		    |     |  |     |   |      |  PyList
//		    |     |  |     |   |      2
//		    |     |  |     |   returns
//		    |     |  |     1D
//		    |     |  PyList
//		    |     1
//		    With an input of
//
// 	@author : Daniel Ríos Linares
//
//	@version : 0.1.0 July 7, 2017
//
PyObject* input_1x_PyList1D__output_2x_PyList1D(PyObject* list) {

	/* Check if list is a PyList_Type */
	//if (!PyList_Check(list)) return NULL;

	/* Check list size */
	int N = PyList_Size(list);

	/* Declare array */
	double array[N];

	/* Python list<float> to C double array */
	for (int i = 0 ; i < N ; i++)
		array[i] = PyFloat_AsDouble(PyList_GetItem(list, (Py_ssize_t) i));
	/* End of Python list fill */

	////////////////////////////////////////////////////////////////////////////

	/* Declare output array */
	double output1[N];
	double output2[N];



	// Do what you wanna do, for example, duplicate all values in the input list
	for (int i = 0 ; i < N ; i++) {
		output1[i] = array[i] * 2;
		output2[i] = array[i] * 3;
	}




	////////////////////////////////////////////////////////////////////////////

	/* C double array to Python list<float> */
	// Output 1
	PyObject* result1 = PyList_New(N);
    for (int i = 0; i < N; i++)
    	PyList_SetItem(result1, i, PyFloat_FromDouble(output1[i]));

	// Output 2
	PyObject* result2 = PyList_New(N);
    for (int i = 0; i < N; i++)
    	PyList_SetItem(result2, i, PyFloat_FromDouble(output2[i]));

	// Final output
	PyObject* result = PyList_New(2);
	PyList_SetItem(result, 0, result1);
	PyList_SetItem(result, 1, result2);
	/* End of Python list fill */

    return result;
}

// <function input_1x_PyList1D__output_3x_PyList1D(PyObject* list)>
// 	@argument <PyObject* list> : input Python list (C API)
//
//	@returns <PyObject tuple{<PyObject* list>,<PyObject* list>,
//		<PyObject* list>}> : output Python list with two lists inside (C API)
//
// 	@description : Python list treatment of 1 input list with 2 new output list
//
//	@name : input_1x_PyList1D__output_3x_PyList1D
//		    |     |  |     |   |      |  |     |
//		    |     |  |     |   |      |  |     1D
//		    |     |  |     |   |      |  PyList
//		    |     |  |     |   |      3
//		    |     |  |     |   returns
//		    |     |  |     1D
//		    |     |  PyList
//		    |     1
//		    With an input of
//
// 	@author : Daniel Ríos Linares
//
//	@version : 0.1.0 July 7, 2017
//
PyObject* input_1x_PyList1D__output_3x_PyList1D(PyObject* list) {

	/* Check if list is a PyList_Type */
	//if (!PyList_Check(list)) return NULL;

	/* Check list size */
	int N = PyList_Size(list);

	/* Declare array */
	double array[N];

	/* Python list<float> to C double array */
	for (int i = 0 ; i < N ; i++)
		array[i] = PyFloat_AsDouble(PyList_GetItem(list, (Py_ssize_t) i));
	/* End of Python list fill */

	////////////////////////////////////////////////////////////////////////////

	/* Declare output array */
	double output1[N];
	double output2[N];
	double output3[N];



	// Do what you wanna do, for example, duplicate all values in the input list
	for (int i = 0 ; i < N ; i++) {
		output1[i] = array[i] * 2;
		output2[i] = array[i] * 3;
		output3[i] = array[i] * 4;
	}




	////////////////////////////////////////////////////////////////////////////

	/* C double array to Python list<float> */
	// Output 1
	PyObject* result1 = PyList_New(N);
    for (int i = 0; i < N; i++)
    	PyList_SetItem(result1, i, PyFloat_FromDouble(output1[i]));

	// Output 2
	PyObject* result2 = PyList_New(N);
    for (int i = 0; i < N; i++)
    	PyList_SetItem(result2, i, PyFloat_FromDouble(output2[i]));

	// Output 2
	PyObject* result3 = PyList_New(N);
    for (int i = 0; i < N; i++)
    	PyList_SetItem(result3, i, PyFloat_FromDouble(output3[i]));

	// Final output
	PyObject* result = PyList_New(3);
	PyList_SetItem(result, 0, result1);
	PyList_SetItem(result, 1, result2);
	PyList_SetItem(result, 2, result3);
	/* End of Python list fill */

    return result;
}

// <function input_1x_PyList1D__output_4x_PyList1D(PyObject* list)>
// 	@argument <PyObject* list> : input Python list (C API)
//
//	@returns <PyObject tuple{<PyObject* list>,<PyObject* list>,
//		<PyObject* list>, <PyObject* list>}> : output Python list with two lists
//		inside (C API)
//
// 	@description : Python list treatment of 1 input list with 2 new output list
//
//	@name : input_1x_PyList1D__output_4x_PyList1D
//		    |     |  |     |   |      |  |     |
//		    |     |  |     |   |      |  |     1D
//		    |     |  |     |   |      |  PyList
//		    |     |  |     |   |      4
//		    |     |  |     |   returns
//		    |     |  |     1D
//		    |     |  PyList
//		    |     1
//		    With an input of
//
// 	@author : Daniel Ríos Linares
//
//	@version : 0.1.0 July 7, 2017
//
PyObject* input_1x_PyList1D__output_4x_PyList1D(PyObject* list) {

	/* Check if list is a PyList_Type */
	//if (!PyList_Check(list)) return NULL;

	/* Check list size */
	int N = PyList_Size(list);

	/* Declare array */
	double array[N];

	/* Python list<float> to C double array */
	for (int i = 0 ; i < N ; i++)
		array[i] = PyFloat_AsDouble(PyList_GetItem(list, (Py_ssize_t) i));
	/* End of Python list fill */

	////////////////////////////////////////////////////////////////////////////

	/* Declare output array */
	double output1[N];
	double output2[N];
	double output3[N];
	double output4[N];



	// Do what you wanna do, for example, duplicate all values in the input list
	for (int i = 0 ; i < N ; i++) {
		output1[i] = array[i] * 2;
		output2[i] = array[i] * 3;
		output3[i] = array[i] * 4;
		output4[i] = array[i] * 5;
	}




	////////////////////////////////////////////////////////////////////////////

	/* C double array to Python list<float> */
	// Output 1
	PyObject* result1 = PyList_New(N);
    for (int i = 0; i < N; i++)
    	PyList_SetItem(result1, i, PyFloat_FromDouble(output1[i]));

	// Output 2
	PyObject* result2 = PyList_New(N);
    for (int i = 0; i < N; i++)
    	PyList_SetItem(result2, i, PyFloat_FromDouble(output2[i]));

	// Output 3
	PyObject* result3 = PyList_New(N);
    for (int i = 0; i < N; i++)
    	PyList_SetItem(result3, i, PyFloat_FromDouble(output3[i]));

	// Output 4
	PyObject* result4 = PyList_New(N);
	for (int i = 0; i < N; i++)
		PyList_SetItem(result4, i, PyFloat_FromDouble(output4[i]));

	// Final output
	PyObject* result = PyList_New(4);
	PyList_SetItem(result, 0, result1);
	PyList_SetItem(result, 1, result2);
	PyList_SetItem(result, 2, result3);
	PyList_SetItem(result, 3, result4);
	/* End of Python list fill */

    return result;
}
