# This target compiles all the files in the directory
compile: slesv_pt.f90
	f2py -m -c slesv_pt_f90 slesv_pt.f90

# This target generates the python modules
module: slesv_pt
	f2py slesv_pt.f90 -m slesv_pt_f90 -h slesv_pt_f90.pyf

# This target removes all libraries created
clean:
	rm *.so ; rm -rf __pycache__ ; rm *.pyf
