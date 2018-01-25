

# This target compiles all the files in the directory
compile: intsm_ue.f90
	f2py -m -c intsm_ue_f90 intsm_ue.f90

# This target generates the python modules
module: intsm_ue.f90
	f2py intsm_ue.f90 -m intsm_ue_f90 -h intsm_ue_f90.pyf

# This target removes all libraries created
clean:
	rm *.so ; rm -rf __pycache__ ; rm *.pyf
