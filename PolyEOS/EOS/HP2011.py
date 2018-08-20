# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 16:40:11 2018

@author: wangf
"""
import uncertainties.unumpy as unp

def HP_K_abs1(params):
    """
    Using equation from Holland et al., (2011) 
    Args:
        params: dictionary, parameters describe the material. Include
                bulk modulus at given temperature(Pa)
                isothermal pressure derivatives at given temperature
                volume at given temperature
    Returns:
        a,b,c
    """   
    a=(1+params["K'"])/(1+params["K'"]+params['K_0 (GPa)']*params["K''"])
    b=(params["K'"]/params['K_0 (GPa)'])-(params["K''"]/(1+params["K'"]))
    c=(1+params["K'"]+params['K_0 (GPa)']*params["K''"])/(params["K'"]**2+params["K'"]-params['K_0 (GPa)']*(params["K''"]**2))
    return a,b,c       

def HP_VP0(Pressure,params):#return VP0
    """
    Using equation from Holland et al., (2011) 
    Args:
        params: dictionary, parameters describe the material. Include
                bulk modulus at given temperature(Pa)
                isothermal pressure derivatives at given temperature
                volume at given temperature
        Pressure: unit GPa
    Returns:
        VP0: 
    """       
    a,b,c=HP_K_abs1(params)
    VP0=(1-a*(1-(1+b*Pressure)**(-c)))*params['V_0 (cm³/mol)']
    return VP0    

def HP_Pth(Temperature,params,Tr=298.):
    """
    Using equation from Holland et al., (2011) 
    Args:
        params: dictionary, parameters describe the material. Include
                bulk modulus at given temperature(Pa)
                isothermal pressure derivatives at given temperature
                volume at given temperature
        Pressure: unit GPa
        temperature: float, unit K.
        Tr: float, referenece temperautre, unit K. Dedault temperautre is 298K
    Returns:
        a,b,c
    """         
    a,b,c=HP_K_abs1(params)
    TD = 10636./(params['S_0 J/(K*mol)']/params['n']+6.44)
    u=TD/Temperature;u0=TD/Tr
    segma=(u0*u0*unp.exp(u0))/(unp.exp(u0)-1)**2
    Pth=(params['a_0 (1/K)']*params['K_0 (GPa)']*TD/segma)*(1/(unp.exp(u)-1)-1/(unp.exp(u0)-1))
    return Pth #return Pth    

def HP_VPT(Pressure,Temperature,params,Tr=298.):
    a,b,c=HP_K_abs1(params)    
    Pth=HP_Pth(Temperature,params,Tr) 
    VPT=(1-a*(1-(1+b*(Pressure-Pth))**(-c)))*params['V_0 (cm³/mol)']
    return VPT 

def HP_K(Pressure,Temperature,params,Tr=298.):
    a,b,c=HP_K_abs1(params)    
    Pth=HP_Pth(Temperature,params,Tr) 
    K=params['K_0 (GPa)']*(1+b*(Pressure-Pth))*(a+(1-a)*(1+b*(Pressure-Pth))**c)  
    return K

def HP_G(Pressure,Temperature,params,Tr=298.,return_Rho=False):
    '''
    Shear modulus from Connolly & Kerrick (2002) and Connolly (2005)
    '''

    V=HP_VPT(Pressure,Temperature,params,Tr) 
    r=params['V_0 (cm³/mol)']/V               
    f = 0.5 * (pow(r, 2. / 3.) - 1.0)               
    #G=self.params['G(Pa)'] + (Temperature-Tr)*self.params['Gprime_0T'] + Pressure*self.params["G'"]
    G=(1+2.*f)**(5./2.)*(params['G_0 (GPa)']+(3.*params['K_0 (GPa)']*params["G'"]-5.*params['G_0 (GPa)'])*f+(6.*params['K_0 (GPa)']*params["G'"]-24.*params['K_0 (GPa)']-14.*params['G_0 (GPa)']+4.5*params['K_0 (GPa)']*params["K'"])*f*f)#-ets*(EthVT)*rho        
    #Rho =params['molar_mass']/V
    if return_Rho:
        return G,params['Rho (kg/m³)']/1000.
    else:
        return G
    

def HP_Vp_Vs(Pressure,Temperature,params,Tr=298):
    '''
    Returns unit:[km/s]`
    Returns unit:[km/s]`
    Returns unit:[kg/m3]`
    '''
    K=HP_K(Pressure,Temperature,params)
    G,Rho = HP_G(Pressure,Temperature,params,Tr,return_Rho=True)    
    Vp=unp.sqrt((K+4.*G/3.)/Rho)
    Vs=unp.sqrt(G/Rho);#print Vs
    return Vp,Vs,Rho,K,G 


if __name__ == "__main__":
    from uncertainties import ufloat
    params = {
            'Formula': 'Mg2SiO4',
            'V_0 (cm³/mol)': ufloat(4.366e-05,1e-6),         
            'K_0 (GPa)': ufloat(127,1),
            'G_0 (GPa)': ufloat(81,1),   
            'S_0 J/(K*mol)':ufloat(95.1,1),
            'Rho (kg/m³)':ufloat(3233.,1.),
            'n': 7,
            'a_0 (1/K)':ufloat(2.85e-05,1e-6),
            "K'": ufloat(4.21796,0.1),
            "G'": ufloat(1.21796,0.1),
            "K''": ufloat(0.0127, 0.001),
            }
    #a =  ufloat(4.3603e-05,1e-07)
    Pressure=11;Temperature=1000.
    #print (HP_K_abs1(params))
    #print (HP_VP0(Pressure,params))
    #print (HP_Pth(Temperature,params,Tr=300))
    #print (HP_VPT(Pressure,Temperature,params,Tr=298.))
    #print (HP_K(Pressure,Temperature,params,Tr=298.))
    #print (HP_G(Pressure,Temperature,params,Tr=298.,return_Rho=True))
    #print (HP_Vp_Vs(Pressure,Temperature,params,Tr=298))
    
    
    import random
    def changeparams(params):
        paramsnew = {}
        for key, value in params.items():
            if key == 'n':
                paramsnew.update({ key: value })
            elif key == 'Formula':
                paramsnew.update({ key: value })
            else:    
                paramsnew.update({ key: np.random.normal(value.n,value.std_dev) })
        return paramsnew

    import numpy as np    
    
    def Compare(Pressure,Temperature,params,num=10000):
        start_time = time.time()
        Vp,Vs,Rho,K,G  = HP_Vp_Vs(Pressure,Temperature,params,Tr=298)
        print("--- %s HP seconds ---" % (time.time() - start_time))
        VP = np.zeros(num)
        VS = np.zeros(num)
        RHO = np.zeros(num)
        for i in range(num):
            aa = changeparams(params)
            VP[i],VS[i],RHO[i],d,e = HP_Vp_Vs(Pressure,Temperature,params=aa,Tr=298)
        VPstd = np.std(VP)
        #VSstd = np.std(VS)
        print("--- %s HP MC seconds ---" % (time.time() - start_time))
        return VPstd, Vp.all().std_dev,Vp.all().n
        #print (VPstd, Vp.all().std_dev)
    x=[]
    y=[]
    xerr=[]
    yerr=[]
    P = [1,3,6,9,12,15,18]
    T = [900,1100,1300,1500,1700,1900,2100]
    for Pressure,Temperature in zip(P,T):
        stdMC,std,vp = Compare(Pressure,Temperature,params)
        x.append(vp);y.append(vp)
        xerr.append(stdMC);yerr.append(std)
        
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.errorbar(x, y, xerr=xerr, yerr=yerr,fmt='.', markersize='10', ecolor='red',)
    for i in range(len(P)):
        ax.text(x[i]+0.01,y[i]+0.01, str(P[i]) + 'GPa;' + str(T[i])+ 'K')
    #ax.errorbar(x1, y1, xerr=x1err, yerr=y1err,fmt='.', markersize='10', ecolor='red',)
    
    ax.set_title('HP 2011 EOS',fontname="Times New Roman",fontsize=13)
    ax.set_xlabel('PolyEOS calculate Vp (km/s)',fontname="Times New Roman",fontsize=13)
    ax.set_ylabel('MC simulate Vp (km/s)',fontname="Times New Roman",fontsize=13)
    fig.savefig('compareHP',dpi=200)


        
        
        