# -*- coding: utf-8 -*-
from __future__ import print_function

"""
This module defines the classes relating to Equation of Stats(EOS)
"""

__author = 'Fei Wang'
__copyright = 'Northwestern Mineral Physics group'
__version__ = '1.0'
__maintainer__ = "Fei Wang"
__date__ = "Mon May  7 13:05:06 2018"


'''
This contain the Tait EoS (Freund & Ingalls (1989)). 
All function accept and return values in SI units. 
'''    

def CoverParams(params):
    '''
    This function return a,b,c defined in terms of the bulk modulus and its
    detivatives at room pressures
    
    Args:
        params: dictionary, parameters describe the material. Include
                bulk modulus at given temperature(Pa)
                isothermal pressure derivatives at given temperature
                volume at given temperature
    retrun:
        a,b,c: defined in terms of the
                bulk modulus and its derivatives at room pressure
    '''
    a=(1 + params["dKdP0T"]) / (1 + params["dKdP0T"] + params['K0T'] * params["dKdP0T"])
    b=(params["dKdP0T"] / params['K0T']) - (params["dKdP0T"] / (1 + params["dKdP0T"]))
    c=(1 + params["dKdP0T"] + params['K0T'] * params["dKdP0T"]) / (params["dKdP0T"] **2\
      + params["dKdP0T"] - params['K0T'] * (params["d2KdP20T"]**2))
    return a,b,c    
    
def Volume(Pressure):
    """
    Returns the volulme at given pressure
    Angel et al., 2014; Holland and Powdell 2011; 
    Args:
        params: dictionary, parameters describe the material. Include
                bulk modulus at given temperature(Pa)
                isothermal pressure derivatives at given temperature
                volume at given temperature
        pressure: float, unit pa.
    Returns:
        volume unit m³
    """    
    a,b,c=CoverParams()
    VP0=(1-a*(1-(1+b*Pressure)**(-c)))*params['V0T']
    return VP0         
   

if __name__ == "__main__":
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
    a,b,c = CoverParams(params)    
        
        
        
        
        
        
        
        
