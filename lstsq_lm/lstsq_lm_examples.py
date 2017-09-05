#!/usr/bin/python

# You need to have the lstsq_lm.py file in the same folder, if not change it!
from lstsq_lm import LeastSquares

# Other stuff
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from random import randint
import numpy as np
import math

################################################################################
# EXAMPLE 001 : Linear regression with random noise
################################################################################
def example_001():
	# Parameter list
	P = [2,3]

	# X and Y data (Y with a random noise between -0.5 and +0.5)
	X = np.linspace(0,4,11)
	Y = [P[0]*x+P[1]+randint(-100,100)/200 for x in X]

	# Create the fitter (without f defined is a linear fit)
	fitter = LeastSquares(X,Y)
	fitter.solve()

	# Plotting
	plt.scatter(X,Y, label = 'scattered data')
	X2 = np.linspace(0,4,100)
	plt.plot(X2,[fitter.f(x,fitter.P) for x in X2], label = 'fitted')
	plt.plot(X2,[fitter.f(x,P) for x in X2], label = 'real without noise')

	plt.legend()
	plt.show()

################################################################################
# EXAMPLE 002 : Nonlinear fit of a RC discharge
################################################################################
def example_002():
	# Model to fit function
	def f(t,P):
		V0,RC = P
		return V0*math.exp(-t/RC)

	# Guess parameters
	V0 = 2 # initial voltage of 2 Volts
	R = 8 # resistor of 8 Ohms
	C = 35 # capacitor of 35 Farads
	P = [V0,R*C]

	# X (T) and Y (V) data
	T = [0,141,272,451,698]
	V = [2.0,1.0,0.5,0.2,0.064]

	# Create the fitter
	fitter = LeastSquares(T,V,f,P)
	fitter.solve()

	# Plotting
	plt.scatter(T,V, label = 'scattered data')
	T2 = np.linspace(0,700,100)
	plt.plot(T2,[f(x,fitter.P) for x in T2], label = 'fitted')

	plt.legend()
	plt.show()

################################################################################
# EXAMPLE 003 : Linear regression (planar) of a 2D set of points
################################################################################
def example_003():
	# Guess parameters
	P = [1,2,3]

	# X and Z data (Z with a random noise between -0.5 and +0.5)
	X = [[0,0],[0,1],[0,2],[1,0],[1,1],[1,2],[2,0],[2,1],[2,2]]
	Z = [P[0]*x[0]+P[1]*x[1]+P[2]+randint(-100,100)/200 for x in X]

	# Create the fitter
	fitter = LeastSquares(X,Z)
	fitter.solve()

	# Plotting
	fig = plt.figure()
	ax = fig.gca(projection='3d')

	ax.plot_trisurf(np.array(X)[:,0],np.array(X)[:,1],[fitter.f(x,fitter.P) for x in X], color = 'blue', label = 'fit')
	ax.scatter(np.array(X)[:,0],np.array(X)[:,1],Z, color = 'r', label = 'data')
	ax.set_xlabel('x')
	ax.set_ylabel('y')
	ax.set_zlabel('z')

	plt.show()
################################################################################
# EXAMPLE 004 : Nonlinear family of curves weighted region
################################################################################
def example_004():
	# Equation of a FET transitor
	def f(x,P):
		VGS,VDS = x
		kn,Vth,lambd = P
		if VGS >= Vth:
			if VGS-Vth <= VDS: # : saturation
				return 0.5*kn*(VGS-Vth)**2*(1+lambd*VDS)
			else: # if VDS < VGS-Vth : triode
				return kn*(VGS-Vth-0.5*VDS)*VDS*(1+lambd*VDS)
		else: # if VGS < Vth : cutoff
			return 0

	# Weight importance Equation
	def w(x,P):
		VGS,VDS = x
		if VDS > 10:
			return 1
		else:
			return 0

	# Guess parameters (typical for a non-power transistor, even if the IRF-530 is a
	# power transistor, you'll notice the convergence speed with 6 magnitude orders
	# of difference in kn, you can try with [0.1,2.0,0.1], that will converge in
	# less than 10 iterations)
	P = [33e-6,2.0,0.1]

	# X (VDS,VGS) and Y (ID) data calculated with ngSPICE with a DC sweep from 6 to
	# 10 Volts in VGS
	X = [[6,0.00E+00],[6,5.00E-01],[6,1.00E+00],[6,1.50E+00],[6,2.00E+00],
		[6,2.50E+00],[6,3.00E+00],[6,3.50E+00],[6,4.00E+00],[6,4.50E+00],
		[6,5.00E+00],[6,5.50E+00],[6,6.00E+00],[6,6.50E+00],[6,7.00E+00],
		[6,7.50E+00],[6,8.00E+00],[6,8.50E+00],[6,9.00E+00],[6,9.50E+00],
		[6,1.00E+01],[6,1.05E+01],[6,1.10E+01],[6,1.15E+01],[6,1.20E+01],
		[6,1.25E+01],[6,1.30E+01],[6,1.35E+01],[6,1.40E+01],[6,1.45E+01],
		[6,1.50E+01],[6,1.55E+01],[6,1.60E+01],[6,1.65E+01],[6,1.70E+01],
		[6,1.75E+01],[6,1.80E+01],[6,1.85E+01],[6,1.90E+01],[6,1.95E+01],
		[6,2.00E+01],[8,0.00E+00],[8,5.00E-01],[8,1.00E+00],[8,1.50E+00],
		[8,2.00E+00],[8,2.50E+00],[8,3.00E+00],[8,3.50E+00],[8,4.00E+00],
		[8,4.50E+00],[8,5.00E+00],[8,5.50E+00],[8,6.00E+00],[8,6.50E+00],
		[8,7.00E+00],[8,7.50E+00],[8,8.00E+00],[8,8.50E+00],[8,9.00E+00],
		[8,9.50E+00],[8,1.00E+01],[8,1.05E+01],[8,1.10E+01],[8,1.15E+01],
		[8,1.20E+01],[8,1.25E+01],[8,1.30E+01],[8,1.35E+01],[8,1.40E+01],
		[8,1.45E+01],[8,1.50E+01],[8,1.55E+01],[8,1.60E+01],[8,1.65E+01],
		[8,1.70E+01],[8,1.75E+01],[8,1.80E+01],[8,1.85E+01],[8,1.90E+01],
		[8,1.95E+01],[8,2.00E+01],[10,0.00E+00],[10,5.00E-01],[10,1.00E+00],
		[10,1.50E+00],[10,2.00E+00],[10,2.50E+00],[10,3.00E+00],[10,3.50E+00],
		[10,4.00E+00],[10,4.50E+00],[10,5.00E+00],[10,5.50E+00],[10,6.00E+00],
		[10,6.50E+00],[10,7.00E+00],[10,7.50E+00],[10,8.00E+00],[10,8.50E+00],
		[10,9.00E+00],[10,9.50E+00],[10,1.00E+01],[10,1.05E+01],[10,1.10E+01],
		[10,1.15E+01],[10,1.20E+01],[10,1.25E+01],[10,1.30E+01],[10,1.35E+01],
		[10,1.40E+01],[10,1.45E+01],[10,1.50E+01],[10,1.55E+01],[10,1.60E+01],
		[10,1.65E+01],[10,1.70E+01],[10,1.75E+01],[10,1.80E+01],[10,1.85E+01],
		[10,1.90E+01],[10,1.95E+01],[10,2.00E+01]]

	Y = [5.92E-38,7.86E-01,1.48E+00,2.05E+00,2.49E+00,2.74E+00,2.79E+00,2.80E+00,
		2.82E+00,2.83E+00,2.84E+00,2.85E+00,2.86E+00,2.87E+00,2.89E+00,2.90E+00,
		2.91E+00,2.92E+00,2.93E+00,2.94E+00,2.96E+00,2.97E+00,2.98E+00,2.99E+00,
		3.00E+00,3.01E+00,3.03E+00,3.04E+00,3.05E+00,3.06E+00,3.07E+00,3.08E+00,
		3.09E+00,3.11E+00,3.12E+00,3.13E+00,3.14E+00,3.15E+00,3.16E+00,3.17E+00,
		3.19E+00,0.00E+00,1.13E+00,2.21E+00,3.25E+00,4.24E+00,5.18E+00,6.06E+00,
		6.86E+00,7.58E+00,8.20E+00,8.70E+00,9.06E+00,9.23E+00,9.27E+00,9.30E+00,
		9.33E+00,9.37E+00,9.40E+00,9.44E+00,9.47E+00,9.50E+00,9.54E+00,9.57E+00,
		9.61E+00,9.64E+00,9.67E+00,9.71E+00,9.74E+00,9.77E+00,9.81E+00,9.84E+00,
		9.87E+00,9.91E+00,9.94E+00,9.97E+00,1.00E+01,1.00E+01,1.01E+01,1.01E+01,
		1.01E+01,1.02E+01,0.00E+00,1.31E+00,2.60E+00,3.87E+00,5.11E+00,6.33E+00,
		7.52E+00,8.68E+00,9.80E+00,1.09E+01,1.19E+01,1.29E+01,1.39E+01,1.48E+01,
		1.56E+01,1.64E+01,1.70E+01,1.76E+01,1.81E+01,1.84E+01,1.85E+01,1.86E+01,
		1.86E+01,1.87E+01,1.88E+01,1.88E+01,1.89E+01,1.89E+01,1.90E+01,1.91E+01,
		1.91E+01,1.92E+01,1.92E+01,1.93E+01,1.94E+01,1.94E+01,1.95E+01,1.95E+01,
		1.96E+01,1.97E+01,1.97E+01]

	# Create the fitter with w(x,P) as weight function
	fitter = LeastSquares(X,Y,f,P,w)
	fitter.solve()

	# Plotting
	for i,c in zip(range(3),['r','b','g']):
		plt.scatter(np.array(X)[int(i*len(X)/3):int((i+1)*len(X)/3),1],np.array(Y)[int(i*len(X)/3):int((i+1)*len(X)/3)], color = c, label = 'IRF530 LtSPICE VGS = '+str(X[int(i*len(X)/3)][0])+' V')
		plt.plot(np.array(X)[int(i*len(X)/3):int((i+1)*len(X)/3),1],np.array([f(x,fitter.P) for x in X])[int(i*len(X)/3):int((i+1)*len(X)/3)], color = c, label = 'least squares VGS = '+str(X[int(i*len(X)/3)][0])+' V')

	plt.ylabel('drain current ID (A)')
	plt.legend()
	plt.xlabel('drain-source voltage VDS (V)')

	plt.show()











if __name__ == '__main__':
	example_001()
	example_002()
	example_003()
	example_004()
