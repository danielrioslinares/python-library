



# Libraries required
PYT_LIB := $(shell pkg-config --cflags --libs python3)
LOC_LIB := $(shell pwd)
NPY_LIB := $(shell python -c "import numpy ; print(str(numpy.get_include()))")


# Create the wrappers and compile the library
compile:
	# arr_miso library
	swig -python -debug-tmsearch arr_miso.i ; rm arr_miso.py ; sed -i 's/_arr_miso/arr_miso/g' arr_miso_wrap.c
	gcc -fPIC -shared arr_miso.c arr_miso_wrap.c $(PYT_LIB) -o arr_miso.so

# Clean the directory
clean:
	rm -r *.o ; rm -r *.out ; rm -rf __pycache__ ; rm *.so

# Test
test:
	python -c "import arr_miso ; print(arr_miso.input_2x_PyList1D__output_1x_PyList1D([1,2,3],[4,5,6])) ; print(arr_miso.input_3x_PyList1D__output_1x_PyList1D([1,2,3],[4,5,6],[7,8,9])) ; print(arr_miso.input_4x_PyList1D__output_1x_PyList1D([1,2,3],[4,5,6],[7,8,9],[10,11,12]))"
