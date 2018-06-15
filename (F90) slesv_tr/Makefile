

# This target compiles all the files in the directory
compile: slesv_tr.f90
	f2py -m -c slesv_tr_f90 slesv_tr.f90

# This target generates the python modules
module: slesv_tr
	f2py slesv_tr.f90 -m slesv_tr_f90 -h slesv_tr_f90.pyf

# This target removes all libraries created
clean:
	rm *.so ; rm -rf __pycache__ ; rm *.pyf
