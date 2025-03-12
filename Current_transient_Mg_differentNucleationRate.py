#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 07:56:56 2025

@author: attari.v
"""

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

# Define constants for Magnesium (Mg) cases
ELEMENTS = {
    "Mg - case 1": {
        "F": 96485,
        "D": 0.706e-5,  # Diffusion coefficient (cm²/s)
        "c": 5e-6,  
        "A": 0.01,  
        "N0": 1e5,  # 10⁴ to 10⁶ nuclei per cm²
        "M": 24.31,  
        "rho": 1.738,  
        "n": 2  
    },
    "Mg - case 2": {
        "F": 96485,
        "D": 0.706e-5,  # Diffusion coefficient (cm²/s)
        "c": 5e-6,  
        "A": 400,  
        "N0": 1e5,  # 10⁴ to 10⁶ nuclei per cm²
        "M": 24.31,  
        "rho": 1.738,  
        "n": 2  
    }
}

# Define time range (avoid singularity at t=0)
t_values = np.linspace(1e-6, 200, 400)

# Define contact angles (in degrees, converted to radians)
theta_degrees = [90]  # Single theta value for simplicity
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

# Compute currents separately for each element
theta = theta_radians[0]  # Use the only available theta

current_mg1 = np.array([compute_current_eq15("Mg - case 1", theta, t) for t in t_values]) * 1e3
current_mg2 = np.array([compute_current_eq15("Mg - case 2", theta, t) for t in t_values]) * 1e3

# Plot results
plt.figure(figsize=(7, 5))

plt.plot(t_values, current_mg1, label="Mg - A=400, Theta = 90°", color="blue")
plt.plot(t_values, current_mg2, label="Mg - A=0.01, Theta = 90°", color="orange")

# Fill area between two cases
plt.fill_between(t_values, current_mg1, current_mg2, color="gray", alpha=0.3)

# Add Quivers (Arrows) at key locations
arrow_indices = np.linspace(50, len(t_values)-50, 5, dtype=int)  # Select indices for quivers
for i in arrow_indices:
    plt.quiver(t_values[i], current_mg1[i], 10, (current_mg1[i+1] - current_mg1[i]), 
               angles='xy', scale_units='xy', scale=100, color='blue', width=0.003)
    plt.quiver(t_values[i], current_mg2[i], 10, (current_mg2[i+1] - current_mg2[i]), 
               angles='xy', scale_units='xy', scale=100, color='orange', width=0.003)

# Annotations
peak_idx_mg1 = np.argmax(current_mg1)
peak_idx_mg2 = np.argmax(current_mg2)

plt.annotate("Peak Current", xy=(t_values[peak_idx_mg1], current_mg1[peak_idx_mg1]), 
             xytext=(t_values[peak_idx_mg1] + 10, current_mg1[peak_idx_mg1] - 0.04),
             arrowprops=dict(facecolor='blue', arrowstyle="->"), fontsize=12, color='blue')

plt.annotate("Peak Current", xy=(t_values[peak_idx_mg2], current_mg2[peak_idx_mg2]), 
             xytext=(t_values[peak_idx_mg2] + 30, current_mg2[peak_idx_mg2] - 0.02),
             arrowprops=dict(facecolor='orange', arrowstyle="->"), fontsize=12, color='orange')

plt.annotate("Steady-State Current", xy=(t_values[-1], current_mg1[-1]), 
             xytext=(t_values[-1] - 50, current_mg1[-1] - 0.05),
             arrowprops=dict(facecolor='blue', arrowstyle="->"), fontsize=12, color='blue')

plt.annotate("Steady-State Current", xy=(t_values[-1], current_mg2[-1]), 
             xytext=(t_values[-1] - 50, current_mg2[-1] + 0.05),
             arrowprops=dict(facecolor='orange', arrowstyle="->"), fontsize=12, color='orange')

#

plt.annotate("progressive nucleation", xy=(t_values[-250], current_mg2[-250]), 
             xytext=(t_values[-150] - 50, current_mg2[-250] + 0.05),
             arrowprops=dict(facecolor='orange', arrowstyle="->"), fontsize=12, color='orange')

plt.annotate("instantanous nucleation", xy=(t_values[50], current_mg1[50]), 
             xytext=(t_values[50] + 20, current_mg1[50] - 0.05),
             arrowprops=dict(facecolor='blue', arrowstyle="->"), fontsize=12, color='blue')


plt.xlabel("Time (s)", fontsize=14)
plt.ylabel(r"Current ($10^3$ A/cm²)", fontsize=14)
plt.title(f"Deposition Current for Mg as a Function of Time", fontsize=13)
plt.tick_params(axis='both', which='major', labelsize=14)
plt.legend(fontsize=12)
plt.grid(False)

plt.show()