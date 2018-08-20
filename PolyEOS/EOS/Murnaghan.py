# -*- coding: utf-8 -*-
from __future__ import print_function

"""
This module defines the classes relating to Equation of Stats(EOS)
"""

__author = 'Fei Wang'
__copyright = 'Northwestern Mineral Physics group'
__version__ = '1.0'
__maintainer__ = "Fei Wang"
__date__ = "Tue May  1 16:16 2018"

from Params import Params


'''
This contain the Murnaghan EoS (Murnaghan, 1937). 
All function accept and return values in SI units. 
'''

def Volume(params,pressure):
    """
    Returns the volulme at given pressure
    Angel et al., 2014
    Args:
        params: dictionary, parameters describe the material. Include
                bulk modulus at given temperature(Pa)
                isothermal pressure derivatives at given temperature
                volume at given temperature
        pressure: float, unit pa.
    Returns:
        volume unit m³
    """
    VPT = params['V0T'] * (1 + params['dKdP0T'] * pressure / params['K0T'])\
          ** (-1 / params['dKdT0T'])
    return VPT

def Pressure(params,volume):
    """
    Returns the pressure at given pressure 
    
    Args:
        params: dictionary, parameters describe the material.
        volume: material volume at given temperature and pressure
        voT: material volume at given temperature
    
    Returns:
        volume unit m³
    """        
    PVT = params['K0T'] / params['dKdP0T'] * ((params['V0T'] / volume)\
                ** params['dKdP0T'] -1)
    return PVT
        
    

if __name__ == "__main__":
    from uncertainties import ufloat
    from uncertainties import ufloat
    params = {
            'V0T': ufloat(4.3603e-05,1e-07),
            'K0T': ufloat(1.279555e+11, 1e9),
            "dKdP0T": ufloat(4.21796,0.1),
            "dKdT0T": ufloat(1.1,0.1),
            "d2KdP20T": ufloat(1,0.1),
            'Debye00': ufloat(809.1703,10),
            'grueneisen00': ufloat(0.99282,0.1),
            'q00': ufloat(2.10672,0.1),
            'G00': ufloat(81599990000.0,1599990000),
            "G'00": ufloat(1.46257,0.1),
            'eta_s_0': ufloat(2.29972,0.1),
            }
    
    print (Volume(params,1e10))
    print (Pressure(params,4.2603e-05)/1e9)
  
        
