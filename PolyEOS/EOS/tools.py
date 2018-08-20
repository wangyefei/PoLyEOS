# -*- coding: utf-8 -*-
"""
Created on Wed Aug 17 16:27:40 2016
@author: Fei

Update: 10/3/2016
"""




from __future__ import absolute_import
import re
import os
from fractions import Fraction
import numpy as np
from scipy.odr import RealData,Model,ODR
from scipy.interpolate import interp1d


'''
These functions are from Burnman, but not being use in HyMaTZ anymore.
'''
def read_masses():
    """
    This function read atom's mass from a txt file and stored it into a dictionary
    datafile from Burnman
    """
    directory=os.path.dirname(__file__) 
    newfile_name = os.path.join( directory , "EXPDATA","atomic_masses.txt")
    d = {}
    with open(newfile_name) as f:
        for line in f:
           (key, val) = line.split()
           d[(key)] = float(val)
    return d
    
atomic_masses = read_masses()

def dictionarize_formula(formula):
    """
    A function to read a chemical formula string and
    convert it into a dictionary
    This function is from Burnman
    """
    f = dict()
    elements = re.findall('[A-Z][^A-Z]*', formula)
    for element in elements:
        element_name = re.split('[0-9][^A-Z]*', element)[0]
        element_atoms = re.findall('[0-9][^A-Z]*', element)
        if len(element_atoms) == 0:
            element_atoms = Fraction(1.0)
        else:
            element_atoms = Fraction(element_atoms[0])
        f[element_name] = f.get(element_name, 0.0) + element_atoms

    return f


def formula_mass(formula, atomic_masses):
    """
    This function calculate the Mineral's mass
    This function is from Burnman
    """
    mass = sum(
        formula[element] * atomic_masses[element] for element in formula)
    return mass
if __name__ == "__main__":
    formula = 'Mg2SiO4'
    n = sum(dictionarize_formula(formula).values())
    molar_mass = formula_mass(dictionarize_formula(formula),atomic_masses)