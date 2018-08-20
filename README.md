
#**PoLyEOS**


Fei Wang, and Steven D. Jacobsen
Department of Earth and Planetary Sciences, Northwestern University, Evanston IL, 60202

##**Overview**

PoLyEOS is a program for calculating and displaying the uncertainties in the calculated seismic velocities in a single mineral. The user enters the ambient thermoelastic properties of the mineral and calculates the seismic velocities at the temperatures and pressures inside the Earth, and then examines the influence of the measurement error in the input data on the seismic velocities and density. If the user does not have the bulk and shear moduli, the program can first calculate these from the elasticity tensor. The user chooses an equation of state (EOS), inputs thermodynamics data for the mineral, and specifies the depth, pressure and temperature in the Earth for which the seismic velocities are required. The output of PoLyEOS is Vp, Vs and density, which are shown in a Table and can be plotted as a figure. PoLyEOS is a visualization tool for understanding the error propagated to the seismic velocities from the uncertainties in the thermodynamics data and EOS used. All data/output can be exported for producing customized graphs. 

##**Installation**

PoLyEOS is a Python script with the following dependencies:
Python version 3.5 or higher :: PyQt5 or PyQt4:: matplotlib :: numpy :: scipy :: uncertainties. 
The program is available for download from GitHub. To launch the program, run Main.py. 

##**Usage**
Executing Main.py brings up the screen shown as Figure 1.
The run consists of going through a series of steps, which are:
1.	Enter the elasticity tensor (not needed if the user already has the bulk and shear moduli).
2.	Select an EOS and enter thermodynamics data (the example here uses forsterite).
3.	Enter depth, pressure and temperature at which calculated results are wanted. 
4.	Run the program.
There is no necessary order for steps 1 to 3.
