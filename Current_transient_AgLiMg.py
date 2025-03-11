#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 14:48:24 2025

@author: attari.v
"""

## Diffuson rate constants for Mg, Li and Ag are from:
# J Chem Theory Comput . 2022 May 10; 18(5): 3017–3026. doi:10.1021/acs.jctc.1c01189.
#The ciurrent transients formula is from J Solid State Electrochem (2009) 13:565–571


import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

# Define constants for Silver (Ag), Lithium (Li), and Magnesium (Mg)
ELEMENTS = {
    "Ag": {
        "F": 96485,  # Faraday constant (C/mol)
        "D": 1.64e-5,# Diffusion coefficient (cm^2/s)
        "c": 5e-6,   # Concentration (mol/cm^3)
        "A": 4,      # Nucleation rate constant (1/s)
        "N0": 5e6,   # Nucleation site density (cm^-2) - 10⁶ to 10⁹ nuclei per cm²
        "M": 107.87, # Molar mass (g/mol)
        "rho": 10.49,  # Density (g/cm^3)
        "n": 1  # Valency
    },
    "Li": {
        "F": 96485,
        "D": 1.029e-5,
        "c": 5e-6,  
        "A": 4,  
        "N0": 2e7,  # 1.9 × 10⁷ to 5.1 × 10⁷ particles per square centimeter (particles/cm²)
        "M": 6.94,  
        "rho": 0.534,  
        "n": 1  
    },
    "Mg": {
        "F": 96485,
        "D": 0.706e-5,  # 
        "c": 5e-6,  
        "A": 4,  
        "N0": 1e5,      # 10⁴ to 10⁶ nuclei per cm².
        "M": 24.31,  
        "rho": 1.738,  
        "n": 2  
    }
}

# Define time range (avoid singularity at t=0)
t_values = np.linspace(1e-6, 10, 200)

# Define contact angles (in degrees, converted to radians)
theta_degrees = [11.25, 22.5, 90, 157.5]
theta_radians = [np.radians(theta) for theta in theta_degrees]

# Define improved Theta function
def Theta(At):
    return np.where(At < 1e-6, At / 2, 1 - ((1 - np.exp(-At)) / (At)))

# Define function to compute F(theta) via integration
def F_theta(theta):
    integral, _ = integrate.quad(lambda u: 1 - np.tanh(u) * np.tanh(((np.pi - theta) * u) / np.pi), 0, np.inf)
    return integral

# Compute shape factor d(theta)
def shape_factor(theta):
    F_theta_val = F_theta(theta)
    d_theta = np.sqrt((16 * F_theta_val**3 * np.sin(theta) * (1 + np.cos(theta))) / 
                      (np.pi**3 * (1 - np.cos(theta)) * (2 + np.cos(theta))))
    return d_theta

# Compute the current using Equation (15) for different elements
def compute_current_eq15(element, theta, t):
    """ Computes current for a given element """
    props = ELEMENTS[element]
    F, D, c, A, N0, M, rho, n = props["F"], props["D"], props["c"], props["A"], props["N0"], props["M"], props["rho"], props["n"]

    # Compute k
    k = np.sqrt((8 * np.pi * c * M) / rho)

    # Compute prefactors
    a = (n * F * np.sqrt(D) * c) / np.sqrt(np.pi)
    b = N0 * np.pi * k * D

    # Compute transient parameters
    At = A * t
    theta_At = Theta(At)
    d_theta = shape_factor(theta)

    # Corrected equation with shape factor
    I = (a / np.sqrt(t)) * (1 - np.exp(-b * d_theta * theta_At * t))   # Scaling to match paper

    return I

# Compute currents for each element
elements_to_plot = ["Ag", "Li", "Mg"]

for element in elements_to_plot:
    plt.figure(figsize=(7, 5))
    for theta, theta_rad in zip(theta_degrees, theta_radians):
        current = [compute_current_eq15(element, theta_rad, t) for t in t_values]
        plt.plot(t_values, np.array(current) * 1e3, label=f"Theta = {theta}°")

    plt.xlabel("Time (s)")
    plt.ylabel(r"Current ($10^3$ A/cm²)")
    plt.title(f"Deposition Current for {element} as a Function of Time")
    plt.legend()
    plt.grid(True)
    plt.show()