



# Libraries required
PYT_LIB := $(shell pkg-config --cflags --libs python3)
LOC_LIB := $(shell pwd)
NPY_LIB := $(shell python -c "import numpy ; print(str(numpy.get_include()))")


# Create the wrappers and compile the library
compile:
	# arr_mimo library
	swig -python -debug-tmsearch arr_mimo.i ; rm arr_mimo.py ; sed -i 's/_arr_mimo/arr_mimo/g' arr_mimo_wrap.c
	gcc -fPIC -shared arr_mimo.c arr_mimo_wrap.c $(PYT_LIB) -o arr_mimo.so

# Clean the directory
clean:
	rm -r *.o ; rm -r *.out ; rm -rf __pycache__ ; rm *.so

# Test
test:
	python -c "import arr_mimo ; print(arr_mimo.input_2x_PyList1D__output_2x_PyList1D([1,2,3],[4,5,6])) ; print(arr_mimo.input_2x_PyList2D__output_2x_PyList2D([[1,2,3],[4,5,6]],[[1,2,3],[4,5,6]]))"
