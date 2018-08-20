# -*- coding: utf-8 -*-
"""
Created on Mon May  7 13:02:42 2018

@author: wangf
"""

from scipy.optimize import newton,bisect


"""
This moduls contain method that use Birch Murnahan method to calcualte EOS
"""
def B_M_2rd(params,pressure):
    """
    Returns the ration of VPT and V00 at given pressure using 
    second order BM equation

    Args:
        params: dictionary, parameters describe the material. Include
                bulk modulus at given temperature(Pa)
                isothermal pressure derivatives at given temperature
                volume at given temperature
        pressure: float, unit pa.
    Returns:
        ratio
        
    """
    def fun(r):    
        return pressure - 1.5 * params['K0T'] * (r ** (7. / 3.) - r ** (5. / 3.))
    try:
        r=newton(fun,1.0);
    except:
        r=bisect(fun,0.1,2.1)    
    return r

def B_M_3rd(params,pressure):
    """
    Returns the ration of V00 and VPT at given pressure using 
    second order BM equation

    Args:
        params: dictionary, parameters describe the material. Include
                bulk modulus at given temperature(Pa)
                isothermal pressure derivatives at given temperature
                volume at given temperature
        pressure: float, unit pa.
    Returns:
        ratio
        
    """        
    def fun(r):    
        return pressure - 1.5 * params['K0T'] * (r ** (7./3.) - r ** (5./3.))\
                * (1. + 0.75 * (r ** (2. / 3.) - 1.) * (params["dKdP0T"] - 4.))
    try:
        r=newton(fun,1.0);
    except:
        r=bisect(fun,0.1,2.1)          
    return r    

def B_M_4rd(params,pressure):
    """
    Returns the ration of V00 and VPT at given pressure using 
    second order BM equation

    Args:
        params: dictionary, parameters describe the material. Include
                bulk modulus at given temperature(Pa)
                isothermal pressure derivatives at given temperature
                volume at given temperature
        pressure: float, unit pa.
    Returns:
        ratio
        
    """  
    def fun(fE):
        '''
        Expansion to fourth order in the strain yileds an EOS 
        Angel et al., 2014
        '''
        return pressure - 3 * params['K0T'] * fE * (1 + 2 * fE) **(5. / 2.) \
                * (1 + 1.5 * (params['dKdP0T'] - 4) * fE 
                + 1.5 * (params['K0T'] * params['d2KdP20T']  \
                + (params['dKdP0T'] - 4) * (params['dKdP0T'] - 3) \
                + (35. / 9. )) * fE ** 2 )
    try:
        fE = newton(fun,1.0);
    except:
        fE = bisect(fun,0.1,2.1)       
        
    r = (fE * 2 + 1) ** (3. / 2.)
    
    return r         


def Volume(params,pressure,order = 3):
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
    if order == 2:
        r = B_M_2rd(params,pressure)
    elif order == 4:
        r = B_M_4rd(params,pressure)
    else:
        r = B_M_3rd(params=params,pressure=pressure)
    
    VPT = params['V0T'] / r
    return VPT


    
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
    #test = BirchMurnaghan()
    #print (B_M_2rd(params,ufloat(1e10,1e8)))
    print (B_M_3rd(params,ufloat(1e10,1.5e8)))
    #print (B_M_4rd(params,ufloat(1e10,1e8)))
    #print (Volume(params,1e10))
    r = ufloat(1.0701,0.0010)
    cccc = - 1.5 * params['K0T'] * (r ** (7./3.) - r ** (5./3.))\
                * (1. + 0.75 * (r ** (2. / 3.) - 1.) * (params["dKdP0T"] - 4.))     
    print (cccc)