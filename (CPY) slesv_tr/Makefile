



# Libraries required
PYT_LIB := $(shell pkg-config --cflags --libs python3)
LOC_LIB := $(shell pwd)
NPY_LIB := $(shell python -c "import numpy ; print(str(numpy.get_include()))")


# Create the wrappers and compile the library
compile:
	# slesv_tr library
	swig -python -debug-tmsearch slesv_tr.i ; rm slesv_tr.py ; sed -i 's/_slesv_tr/slesv_tr/g' slesv_tr_wrap.c
	gcc -fPIC -shared slesv_tr.c slesv_tr_wrap.c $(PYT_LIB) -o slesv_tr.so

# Clean the directory
clean:
	rm -r *.o ; rm -r *.out ; rm -rf __pycache__ ; rm *.so

# Test
test:
	python -c "import slesv_tr ; print(slesv_tr.slesv_tr([7,8,9],[4,5,6],[1,2,3],[10,11,12]))"
