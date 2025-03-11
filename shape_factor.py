#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 14:41:44 2025

@author: attari.v
"""

import numpy as np
import scipy.integrate as integrate
import matplotlib.pyplot as plt

# Define a range of contact angles (theta) from 0 to 180 degrees
theta_range_degrees = np.linspace(6, 179, 100)  # Avoid 0 and 180 to prevent singularities
theta_range_radians = np.radians(theta_range_degrees)  # Convert to radians

# Define improved Theta function
def Theta(At):
    """ Theta(At) function as defined in the paper """
    return np.where(At < 1e-6, At / 2, 1 - ((1 - np.exp(-At)) / (At)))  # Taylor expansion for small At

# Define function to compute F(theta) via integration
def F_theta(theta):
    """ Computes F(theta) using numerical integration """
    integral, _ = integrate.quad(lambda u: 1 - np.tanh(u) * np.tanh(((np.pi - theta) * u) / np.pi), 0, np.inf)
    return integral

# Compute shape factor d(theta) with rechecking
def shape_factor(theta):
    """ Computes d(theta) using the defined shape factor equation """
    F_theta_val = F_theta(theta)
    d_theta = np.sqrt((16 * F_theta_val**3 * np.sin(theta) * (1 + np.cos(theta))) / 
                      (np.pi**3 * (1 - np.cos(theta)) * (2 + np.cos(theta))))
    return d_theta

# Compute d(theta) for each theta in the range
d_theta_values = [shape_factor(theta) for theta in theta_range_radians]

# Plot d(theta) as a function of theta
plt.figure(figsize=(7,5))
plt.plot(theta_range_degrees, d_theta_values, label=r"Shape Factor $d(\theta)$", linestyle="-", color="b")

plt.xlabel(r"Contact Angle $\theta$ (degrees)")
plt.ylabel(r"Shape Factor $d(\theta)$")
plt.title(r"Shape Factor $d(\theta)$ as a Function of Contact Angle $\theta$")
plt.legend()
plt.grid(True)
plt.show()