# Theoretical Current Transients during Electrocrystallization
 Diffusion Current Transients from Spherical Cap Theory During Electrocrystallization

## Evans' Theory for Electrocrystallization

Evans' theory describes the current transient behavior during metal electrodeposition, considering the influence of nucleation rate and diffusion-controlled growth. The number of nucleation sites follows an exponential activation law, while the active surface area expands with a diffusion-limited radius. The transient current follows:


$$I(t) = I_0 (1 - e^{-At}) t^{1/2}$$


where ($I_0$) is a material-dependent prefactor. This theory is particularly useful for analyzing electrochemical deposition processes in metals like **silver (Ag), lithium (Li), and magnesium (Mg)**. The model predicts an initial increase in current due to growing nucleation sites, followed by a decay as diffusion dominates.

## Avrami Theory for Electrocrystallization

The **Avrami theory** models the **time-dependent surface coverage** during electrocrystallization, considering **nucleation rate**, **growth kinetics**, and **diffusion overlap**. The fraction of the electrode covered by diffusion zones is:

$$ S = 1 - \exp(-b d(\theta) \Theta(At) t) $$

where:
- \( b \) depends on nucleation site density,
- \( d(\theta) \) accounts for contact angle effects.

The current density follows:

$$ I(t) = \frac{a}{t^{1/2}} \left[1 - \exp(-b d(\theta) \Theta(At) t) \right] $$

This reflects **diffusion-limited growth** of nuclei.

### **Comparison with Evans Theory**
- **Avrami**: Nucleation + Growth, considers surface coverage evolution.
- **Evans**: Diffusion-controlled deposition, no explicit nucleation model.

For a deeper dive, refer to the full documentation or related literature.