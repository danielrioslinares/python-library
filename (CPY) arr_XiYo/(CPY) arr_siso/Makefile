



# Libraries required
PYT_LIB := $(shell pkg-config --cflags --libs python3)
LOC_LIB := $(shell pwd)
NPY_LIB := $(shell python -c "import numpy ; print(str(numpy.get_include()))")


# Create the wrappers and compile the library
compile:
	# arr_siso library
	swig -python -debug-tmsearch arr_siso.i ; rm arr_siso.py ; sed -i 's/_arr_siso/arr_siso/g' arr_siso_wrap.c
	gcc -fPIC -shared arr_siso.c arr_siso_wrap.c $(PYT_LIB) -o arr_siso.so

# Clean the directory
clean:
	rm -r *.o ; rm -r *.out ; rm -rf __pycache__ ; rm *.so

# Test
test:
	python -c "import arr_siso ; print(arr_siso.input_1x_PyList1D__output_1x_PyList1D([1,2,3])) ; print(arr_siso.input_1x_PyList2D__output_1x_PyList2D([[1,2,3],[4,5,6]]))"
