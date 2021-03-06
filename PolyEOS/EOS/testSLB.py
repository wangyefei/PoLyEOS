# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 14:47:33 2018

@author: wangf
"""
import numpy as np
from scipy import integrate
from scipy.optimize import newton,bisect
from scipy.constants import gas_constant
#import uncertainties as u
#import uncertainties.unumpy as unp
def Stix_Compressive(P,T,params,Tr=300.):
    '''
    Given pressure (P) and temperature (T),return parameters
    Units is based on input, default is SI units
    r = V0/VPT at PT      No units, but without error propogation 
    Units can changed based on input.
    '''        
    #eq 25，26 2011
    Debye_int_func=lambda t:(t*t*t)/(np.exp(t)-1.)  # from wiki
    aii=6.*params['grueneisen_0']; #Eq47
    aiikk=-12.*params['grueneisen_0']+36.*(params['grueneisen_0'] **2)-18.*params['q_0'] *params['grueneisen_0'] 
    
    
    def fun(r): #r=rho/rho0
        #K2=(-1./self.params['K_0 (GPa)'])*((3-self.params["k'"])*(4-self.params["k'"])+35./9.); # Angel 2000
        K2=(-1./params['K_0 (GPa)'])*((3-params["K'"])*(4-params["K'"])+35./9.); # Angel 2000
        f=0.5*((r)**(2./3.)-1) #eq 20 2011
        Gru=(1./6.)/(1+aii*f+0.5*aiikk*f*f)*(2*f+1)*(aii+aiikk*f)  #  eq41, 44 2005               
        Debye=abs(np.sqrt(1.+aii*f+0.5*aiikk*f*f)*params['Debye_0 (K)'] ) #eq24 2011
                   
        #use scipy to integrae Debye function 
        EthVT =(9.*params['n']*gas_constant*T)  * ((Debye/T)**(-3))*integrate.quad(Debye_int_func,0.,Debye/T)[0]
        EthVT0=(9.*params['n']*gas_constant*Tr) * ((Debye/Tr)**(-3))*integrate.quad(Debye_int_func,0.,Debye/Tr)[0]
                    
        Pth=(EthVT-EthVT0)*(Gru*r/params['V_0 (cm³/mol)'] )
        
        if params['V_0 (cm³/mol)'] !=0.0:
            f=0.5*(r**(2./3.)-1.)
            a=9.*params['K_0 (GPa)'] ;b=27.*params['K_0 (GPa)'] *(params["K'"] -4.);c=81.0*(params['K_0 (GPa)'] *K2 +params["K'"] *(params["K'"] -7.)+143./9.); # eq 21,22 2011
            P0=((1./3.)*((1+2*f)**(5./2.)))*(a*f+0.5*b*f*f+1./6.*c*f*f*f)

            return P-P0-Pth#-1e5
        else:
            return 10.0
         
    try:
        r=newton(fun,1.0);
    except:
        r=bisect(fun,0.1,2.1)
    return r



Debye_int_func=lambda t:(t*t*t)/(np.exp(t)-1.) 
def Energy(Debye,T):
    """
    This function use debye model to calcualte the Gibbs energy
    Args:
        Debye: Debye temperautre, unit K
        T: temperature, unit K
    return:
        Energy: unit J
    """
    def intefrand(t):
        return (t*t*t)/(np.exp(t)-1.)
    #integral, abserr = quad(integrand, 0, 0.9)
    integral, abserr = integrate.quad(Debye_int_func,0.,Debye/T)
    return integral



def Stix_thermal_pressure(Pressure,Temperature,params,Tr=300):
    """
    This function calcaulte the thermal pressure, equation of state from Stixrude
    and Lithgow-Bertelloni (2005)
    Args:
        Pressure: unit Pa
        Temperautre: unit K
        Tr: temperature at reference unit K, default 300K
    """
    r= Stix_Compressive(Pressure,Temperature,params,Tr)
    aii=6.*params['grueneisen_0']; #Eq47
    aiikk=-12.*params['grueneisen_0']+36.*(params['grueneisen_0']**2)-18.*params['q_0']*params['grueneisen_0']    
    f=0.5*(r**(2./3.)-1);
    Gru=(1./6.)/(1+aii*f+0.5*aiikk*f*f)*(2*f+1)*(aii+aiikk*f)
    
    Debye=abs(np.sqrt(1+aii*f+0.5*aiikk*f*f))*params['Debye_0 (K)']
    
    E1 = Energy(Debye,Temperature)
    E2 = Energy(Debye,Tr)
    EthVT =(9.*params['n']*gas_constant*Temperature)  * ((Debye/Temperature)**(-3))*E1#integrate.quad(Debye_int_func,0.,Debye/Temperature)[0]
    EthVT0=(9.*params['n']*gas_constant*Tr) * ((Debye/Tr)**(-3))*E2#integrate.quad(Debye_int_func,0.,Debye/Tr)[0]
    Pth=(EthVT-EthVT0)*(Gru*r/params['V_0 (cm³/mol)'])
    return Pth,aii,aiikk,r,E1,E2
    
    
def Stix_Compressive_EP(Pressure,Temperature,params,Tr=300.):
    '''
    This function calculate with error propogation by pre calcualte the r without
    error propogation
    '''
    Pth, aii, aiikk,r,EthVT,EthVT0= Stix_thermal_pressure(Pressure,Temperature,params,Tr)
    def fun(r): #r=rho/rho0
        K2=(-1./params['K_0 (GPa)'])*((3-params["K'"])*(4-params["K'"])+35./9.); # Angel 2000
        f=0.5*(r**(2./3.)-1);
        a=9.*params['K_0 (GPa)'] ;b=27.*params['K_0 (GPa)'] *(params["K'"] -4.);c=81.0*(params['K_0 (GPa)'] *K2 +params["K'"] *(params["K'"] -7.)+143./9.); # eq 21,22 2011
        P0=((1./3.)*((1+2*f)**(5./2.)))*(a*f+0.5*b*f*f+1./6.*c*f*f*f)
        return Pressure-P0-Pth#-1e5

    try:
        r=newton(fun,r);
    except:
        r=bisect(fun,0.1,2.1)
        
    return r,aii,aiikk,EthVT,EthVT0
    

def Stix_EOS(Pressure,Temperature,params,Tr=298,return_control='needed'):
    '''
    Given pressure (P) and temperature (T),return parameters
    Units is based on input, default is SI units
    r = V0/VPT at PT      No units
    K = bulk modulus at PT     Pa
    G = Shear modulus at PT    Pa
    V = Volume at PT
    Rho = Density at PT   
    a0 = Thermal expansion 
    Debye = Debye temperature K
    Units is based on input, default is 
    '''
    if Pressure<=0:
        Pressure==1
    R=gas_constant
    #eq 25，26 2011
    #Debye_int_func=lambda t:(t*t*t)/(np.exp(t)-1.)  # from wiki       
    r,aii,aiikk,E1,E2 = Stix_Compressive_EP(Pressure,Temperature,params,Tr)
    
    
    f=0.5*(r**(2./3.)-1.);
    rho=r/(params['V_0 (cm³/mol)'])
    V=params['V_0 (cm³/mol)']/r
    Rho=params['molar_mass']/V
    
    Debye=abs(np.sqrt(1+aii*f+0.5*aiikk*f*f))*params['Debye_0 (K)']
    
    EthVT=(9.*params['n']*R*Temperature)  * ((Debye/Temperature)**(-3))*E1
    EthVT -=(9.*params['n']*R*Tr)  * ((Debye/Tr)**(-3))*E2
    
    CVT = 3.0 * params['n']* R * (4.0 * 3*E1/(Debye/Temperature)**(3.) - 3.0 * (Debye/Temperature) / (np.exp(Debye/Temperature) - 1.0))
    CVTr = 3.0 * params['n'] * R * (4.0 * 3*E2/(Debye/Tr)**(3.) - 3.0 * (Debye/Tr) / (np.exp(Debye/Tr) - 1.0))
    
    Gru=(1./6.)/(1+aii*f+0.5*aiikk*f*f)*(2*f+1)*(aii+aiikk*f) 

    a2s=-2.*params['grueneisen_0'] - 2.*params['eta_s_0']  #EQ 47
    ets=-Gru-0.5/(1.+aii*f+0.5*aiikk*f*f)*((2.*f+1.)**2.)*a2s #EQ 46
    
    q=1./9.*(18.*Gru-6.-1./2./ (1.+aii*f+0.5*aiikk*f*f) * (2.*f+1.)*(2.*f+1.)*aiikk/Gru)
    K=(1+2.*f)**(5./2.)*(params['K_0 (GPa)']+(3.*params['K_0 (GPa)']*params["K'"]-5.*params['K_0 (GPa)'])*f+(27./2.)*(params['K_0 (GPa)']*params["K'"]-4.*params['K_0 (GPa)'])*f*f)+(Gru+1-q)*Gru*rho*(EthVT)-Gru*Gru*rho*(CVT*Temperature-CVTr*Tr)
    a0= Gru* CVT/(K*V)  
    G=(1+2.*f)**(5./2.)*(params['K_0 (GPa)']+(3.*params['K_0 (GPa)']*params["G'"]-5.*params['K_0 (GPa)'])*f+(6.*params['K_0 (GPa)']*params["G'"]-24.*params['K_0 (GPa)']-14.*params['K_0 (GPa)']+4.5*params['K_0 (GPa)']*params["K'"])*f*f)-ets*(EthVT)*rho        
    if return_control == 'needed':
        return r,K,G,V,Rho
    else:
        return r,K,G,V,Rho,CVT,Gru,a0,Debye
    
def Stix_Vp_Vs_test(pressure,temperature,params,Tr=300.):
    '''
    Returns unit:[km/s]`
    Returns unit:[km/s]`
    Returns unit:[kg/m3]`
    '''
    r,K,G,V,Rho=Stix_EOS(pressure,temperature,params,Tr)
    Vp=np.sqrt((K+4.*G/3.)/Rho)/1000.
    Vs=np.sqrt(G/Rho)/1000.;#print Vs
    return Vp,Vs,Rho/1000. ,K,G 



if __name__ == "__main__":
    import time
    start_time = time.time()

    from uncertainties import ufloat
    Pressure=1.1e10;Temperature=1000
    params = {
            'V_0 (cm³/mol)': ufloat(4.3603e-05,1e-07),
            'K_0 (GPa)': ufloat(1.279555e+11, 2e9),
            #'K_0 (GPa) (GPa)': ufloat(1.279555e+11, 1e9),
            'G_0 (GPa)': ufloat(81599990000.0,1599990000),            
            #'S_0':ufloat(198.0,10),
            'molar_mass': ufloat(0.1638574,0),
            'n':7,
            #'a_0':ufloat(0.3698,0.1),
            "K'": ufloat(4.21796,0.2),
            #"dKdT": ufloat(1.1,0.1),
            #"K''": ufloat(1,0.1),
            'Debye_0 (K)': ufloat(809.1703,1),
            'grueneisen_0': ufloat(0.99282,0.3),
            'q_0': ufloat(2.10672,0.2),
            #'G': ufloat(81599990000.0,1599990000),
            "G'": ufloat(1.46257,0.1),
            'eta_s_0': ufloat(2.29972,0.1),
            }

    from SLB import Stix_Vp_Vs
    Vp,Vs,Rho,K,G  = Stix_Vp_Vs(Pressure,Temperature,params,Tr=298)


    
    def changeparams(params):
        paramsnew = {}
        for key, value in params.items():
            #print (key,value)
            if key == 'n':
                paramsnew.update({ key: value })
            elif key == 'Formula':
                paramsnew.update({ key: value })
            else:    
                paramsnew.update({ key: np.random.normal(value.n,value.std_dev) })
        return paramsnew
    

    def Compare(Pressure,Temperature,params,num=10000):
        start_time = time.time()
        Vp,Vs,Rho,K,G  = Stix_Vp_Vs(Pressure,Temperature,params,Tr=298)
        print("--- %s stix seconds ---" % (time.time() - start_time))
        VP = np.zeros(num)
        VS = np.zeros(num)
        RHO = np.zeros(num)
        for i in range(num):
            aa = changeparams(params)
            VP[i],VS[i],RHO[i],d,e = Stix_Vp_Vs_test(Pressure,Temperature,params=aa,Tr=298)
        VPstd = np.std(VP)
        #VSstd = np.std(VS)
        #RHOstd = np.std(RHO)
        print("--- %s seconds ---" % (time.time() - start_time))
        return VPstd, Vp.std_dev,Vp.n 
    
    Pressure=1.1e10;Temperature=1000
    #Compare(Pressure,Temperature,params,num=10)
    x=[]
    y=[]
    xerr=[]
    yerr=[]
    P = [1,3,6,9,12,15,18]
    T = [900,1100,1300,1500,1700,1900,2100]
    for Pressure,Temperature in zip(P,T):
        stdMC,std,vp = Compare(Pressure*1e9,Temperature,params,num=10000)
        x.append(vp);y.append(vp)
        xerr.append(stdMC);yerr.append(std)
        
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.errorbar(x, y, xerr=xerr, yerr=yerr,fmt='.', markersize='10', ecolor='red',)
    for i in range(len(P)):
        ax.text(x[i]+0.01,y[i]+0.01, str(P[i]) + 'GPa;' + str(T[i])+ 'K')
    #ax.errorbar(x1, y1, xerr=x1err, yerr=y1err,fmt='.', markersize='10', ecolor='red',)
    
    ax.set_title('SLB 2005 EOS',fontname="Times New Roman",fontsize=13)
    ax.set_xlabel('PolyEOS calculate Vp (km/s)',fontname="Times New Roman",fontsize=13)
    ax.set_ylabel('MC simulate Vp (km/s)',fontname="Times New Roman",fontsize=13)
    fig.savefig('compareSLB',dpi=200)    
    