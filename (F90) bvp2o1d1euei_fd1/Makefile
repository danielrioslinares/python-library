

# This target compiles all the files in the directory
compile: bvp2o1d1euei_fd1.f90
	f2py -m -c bvp2o1d1euei_fd1_f90 bvp2o1d1euei_fd1.f90

# This target generates the python modules
module: bvp2o1d1euei_fd1.f90
	f2py bvp2o1d1euei_fd1.f90 -m bvp2o1d1euei_fd1_f90 -h bvp2o1d1euei_fd1_f90.pyf

# This target removes all libraries created
clean:
	rm *.so ; rm -rf __pycache__ ; rm *.pyf
