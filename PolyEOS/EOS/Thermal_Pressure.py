# -*- coding: utf-8 -*-
from __future__ import print_function

"""
This module defines the classes relating to Equation of Stats(EOS)
"""

__author = 'Fei Wang'
__copyright = 'Northwestern Mineral Physics group'
__version__ = '1.0'
__maintainer__ = "Fei Wang"
__date__ = "Sun Aug 1 15:03 2018"

from scipy import integrate
from scipy.constants import gas_constant
import uncertainties.unumpy as unp



def Thermal_pressure_HP(Temperature,params,Tr=300):
    """
    Returns the thermal pressure at given temperature using equation from 
    Holland et al., (2011)  Eq 11-12
    Args:
        params: dictionary, parameters describe the material. Include
                bulk modulus at given temperature(Pa)
                isothermal pressure derivatives at given temperature
                volume at given temperature
        temperature: float, unit K.
        Tr: float, referenece temperautre, unit K. Dedault temperautre is 300K
    Returns:
        thermal pressure: ufloat unit pa
    """
    TD = 10636./(params['S_0']/params['n']+6.44)
    u=TD/Temperature;u0=TD/Tr
    segma=(u0*u0*unp.exp(u0))/(unp.exp(u0)-1)**2 
    Pth=(params['a_0']*params['K0T']*TD/segma)*(1/(unp.exp(u)-1)-1/(unp.exp(u0)-1))  
    return Pth

#def Thermal_Pressure_MGD(Temperature,params,Tr=300):
    


    
    
if __name__ == "__main__":
    from uncertainties import ufloat
    params = {
            'V0T': ufloat(4.3603e-05,1e-07),
            'K0T': ufloat(1.279555e+11, 1e9),
            'S_0':ufloat(198.0,10),
            'n':7,
            'a_0':ufloat(0.3698,0.1),
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

    print (Thermal_pressure_HP(1000,params,Tr=300))