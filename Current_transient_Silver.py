#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 14:41:44 2025

@author: attari.v
"""


## implenetaiton ofSilver Deposition Current Transients from:
# J Solid State Electrochem (2009) 13:565–571
# DOI 10.1007/s10008-008-0700-6

# The resulting figure corresponds to Fig. 5

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

# Define constants for Silver (Ag) (from paper)
F = 96485  # Faraday constant (C/mol)
D_Ag = 1e-5  # Diffusion coefficient for Ag (cm^2/s)
c_Ag = 5e-6  # Concentration of Ag+ (mol/cm^3)
A_Ag = 4  # Nucleation rate constant (1/s)
N0_Ag = 5e6  # Nucleation site density (cm^-2)
M_Ag = 107.87  # Molar mass (g/mol)
rho_Ag = 10.49  # Density of Ag (g/cm^3)
n_Ag = 1  # Valency of Ag

# Compute k using the provided equation
k_Ag = np.sqrt((8 * np.pi * c_Ag * M_Ag) / rho_Ag)

# Define refined time range (higher resolution)
t_values = np.linspace(1e-6, 2, 200)  

# Compute a and b
a_Ag = (n_Ag * F * np.sqrt(D_Ag)*c_Ag) / np.sqrt(np.pi) 
b_Ag = N0_Ag * np.pi * k_Ag * D_Ag  

# Define Theta(At) function
def Theta(At):
    """ Computes Θ(A t) as given in the paper """
    return 1 - ((1 - np.exp(-At)) / (At))

# Compute F(theta) using numerical integration
def F_theta(theta):
    """ Computes F(theta) via numerical integration """
    integral, _ = integrate.quad(lambda u: 1 - np.tanh(u) * np.tanh(((np.pi - theta) * u) / np.pi), 0, np.inf)
    return integral

# Compute shape factor d(theta)
def shape_factor(theta):
    """ Computes d(theta) for a given contact angle """
    F_theta_val = F_theta(theta)
    d_theta = np.sqrt((16 * F_theta_val**3 * np.sin(theta) * (1 + np.cos(theta))) / 
                      (np.pi**3 * (1 - np.cos(theta)) * (2 + np.cos(theta))))
    return d_theta

# Compute the current using Equation (15) with the correct exponent
def compute_current_eq15(theta, t):
    """ Computes current based on Equation (15) with shape factor d(theta) """
    At = A_Ag * t
    theta_At = Theta(At)
    d_theta = shape_factor(theta)

    # Corrected equation with refined prefactor and shape factor
    I = (a_Ag / np.sqrt(t)) * (1 - np.exp(-b_Ag * d_theta * theta_At * t))
    return I

# Define contact angles to simulate
theta_degrees = [11.25, 22.5, 90, 157.5]
theta_radians = [np.radians(theta) for theta in theta_degrees]

# Compute currents for each contact angle over time
current_silver = {theta: [compute_current_eq15(theta, t) for t in t_values] for theta in theta_radians}

# Plot corrected results
plt.figure(figsize=(7,5))
for theta, current in zip(theta_degrees, current_silver.values()):
    plt.plot(t_values, np.array(current) * 1e3, label=f"Theta = {theta}°")

plt.xlabel("Time (s)")
plt.ylabel(r"Current ($10^3$ A/cm²)")
plt.title("Deposition Current for Silver as a Function of Time (Eq. 15 with d(theta)) - Corrected")
plt.legend()
plt.grid(True)
plt.show()