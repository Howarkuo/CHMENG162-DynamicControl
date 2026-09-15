"""
CBE 162 - Problem 3
Dynamic CSTR model for radical / living polymerization

States
------
h      : liquid height
CM     : monomer concentration
gamma  : total concentration of active polymer chains

Reaction mechanism
------------------
Initiation:
    M + * -> P1
    r_init = ks * CM

Propagation:
    M + Pi -> P(i+1)
    r_prop = k * CM * gamma

Outlet:
    qout = alpha * sqrt(h)

References
----------
H. Vale, PRE-Notebooks, "Population Balances for Polymer Systems"
https://hugomvale.github.io/PRE-Notebooks/notebooks/01/population_balances.html

H. Vale, PRE-Notebooks,
"Residence Time Distribution Effects in Living Polymerization"
https://hugomvale.github.io/PRE-Notebooks/notebooks/11/living_polymerization_rtd.html

PolyKin:
https://github.com/HugoMVale/polykin

The implementation follows the population-balance / CSTR ODE
structure in the above references and uses scipy.integrate.solve_ivp.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp


# ============================================================
# 1. MODEL
# ============================================================

def polymer_cstr(t, y, qin, CMin, A, alpha, k, ks):
    """
    Dynamic model of the polymerization CSTR.

    Parameters
    ----------
    t : float
        Time.

    y : array_like
        State vector:
        y[0] = h
        y[1] = CM
        y[2] = gamma

    qin : float
        Inlet volumetric flow rate.

    CMin : float
        Monomer concentration in feed.

    A : float
        Constant tank cross-sectional area.

    alpha : float
        Outlet-flow coefficient:
            qout = alpha * sqrt(h)

    k : float
        Propagation rate constant.

    ks : float
        Initiation rate constant.

    Returns
    -------
    dydt : ndarray
        [dh/dt, dCM/dt, dgamma/dt]
    """

    # --------------------------------------------------------
    # States
    # --------------------------------------------------------
    h, CM, gamma = y

    # Prevent numerical problems if solver approaches h = 0
    h = max(h, 1e-12)

    # --------------------------------------------------------
    # Algebraic quantities
    # --------------------------------------------------------

    # Reactor volume
    V = A * h

    # Outlet flow
    qout = alpha * np.sqrt(h)

    # Reaction rates
    r_init = ks * CM
    r_prop = k * CM * gamma

    # ========================================================
    # ODE 1: LIQUID LEVEL
    #
    # dV/dt = qin - qout
    #
    # V = A*h
    #
    # A*dh/dt = qin - qout
    # ========================================================

    dhdt = (qin - qout) / A


    # ========================================================
    # ODE 2: MONOMER CONCENTRATION
    #
    # d(CM*V)/dt =
    #       qin*CMin
    #     - qout*CM
    #     - V*r_init
    #     - V*r_prop
    #
    # After applying dV/dt = qin - qout:
    #
    # dCM/dt =
    #     qin/V * (CMin - CM)
    #     - ks*CM
    #     - k*CM*gamma
    # ========================================================

    dCMdt = (
        (qin / V) * (CMin - CM)
        - r_init
        - r_prop
    )


    # ========================================================
    # ODE 3: TOTAL POLYMER-CHAIN CONCENTRATION gamma
    #
    # Initiation creates a new polymer chain.
    #
    # Propagation:
    #       Pi + M -> P(i+1)
    #
    # does NOT change the total number of polymer chains.
    #
    # d(gamma*V)/dt =
    #       + V*ks*CM
    #       - qout*gamma
    #
    # After applying dV/dt:
    #
    # dgamma/dt =
    #       ks*CM
    #       - qin/V * gamma
    # ========================================================

    dgammadt = (
        r_init
        - (qin / V) * gamma
    )

    return [dhdt, dCMdt, dgammadt]


# ============================================================
# 2. PARAMETERS
# ============================================================
#
#
# These values are ONLY examples so that the code is runnable.
# Replace  with assigned/experimental values.
#
# ============================================================

A = 1.0               # m^2
qin = 0.010           # m^3/s
alpha = 0.020         # m^(5/2)/s because qout = alpha*sqrt(h)

CMin = 1000.0         # mol/m^3  = 1 mol/L

k = 1.0e-3            # m^3/(mol*s)
ks = 1.0e-2           # 1/s


# ============================================================
# 3. INITIAL CONDITIONS
# ============================================================

h0 = 0.10             # m
CM0 = 0.0             # mol/m^3
gamma0 = 0.0          # mol/m^3

y0 = [h0, CM0, gamma0]


# ============================================================
# 4. TIME RANGE
# ============================================================

t_start = 0.0
t_end = 500.0         # s

t_eval = np.linspace(t_start, t_end, 1000)


# ============================================================
# 5. SOLVE COUPLED ODEs
# ============================================================

sol = solve_ivp(
    fun=polymer_cstr,
    t_span=(t_start, t_end),
    y0=y0,
    t_eval=t_eval,
    args=(qin, CMin, A, alpha, k, ks),
    method="RK45",
    rtol=1e-8,
    atol=1e-10
)


# Check integration
if not sol.success:
    raise RuntimeError(sol.message)


# ============================================================
# 6. EXTRACT RESULTS
# ============================================================

t = sol.t

h = sol.y[0]
CM = sol.y[1]
gamma = sol.y[2]

# Calculate outlet flow for plotting
qout = alpha * np.sqrt(h)

# Propagation and initiation rates
r_init = ks * CM
r_prop = k * CM * gamma


# ============================================================
# 7. PLOT RESULTS
# ============================================================

plt.figure(figsize=(7, 5))

plt.plot(t, h)

plt.xlabel("Time [s]")
plt.ylabel("Liquid level, h [m]")
plt.title("CSTR Liquid Level")

plt.grid(True)
plt.tight_layout()
plt.show()


plt.figure(figsize=(7, 5))

plt.plot(t, CM / 1000)

plt.xlabel("Time [s]")
plt.ylabel(r"$C_M$ [mol/L]")
plt.title("Monomer Concentration")

plt.grid(True)
plt.tight_layout()
plt.show()


plt.figure(figsize=(7, 5))

plt.plot(t, gamma / 1000)

plt.xlabel("Time [s]")
plt.ylabel(r"$\gamma$ [mol/L]")
plt.title("Total Active Polymer-Chain Concentration")

plt.grid(True)
plt.tight_layout()
plt.show()


plt.figure(figsize=(7, 5))

plt.plot(t, qout, label=r"$q_{out}$")
plt.axhline(
    qin,
    linestyle="--",
    label=r"$q_{in}$"
)

plt.xlabel("Time [s]")
plt.ylabel(r"Flow rate [m$^3$/s]")
plt.title("Inlet and Outlet Flow Rates")

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# ============================================================
# 8. PRINT FINAL STATE
# ============================================================

print("Final state")
print("-----------------------------")
print(f"h      = {h[-1]:.6f} m")
print(f"CM     = {CM[-1]:.3f} mol/m^3")
print(f"gamma  = {gamma[-1]:.3f} mol/m^3")
print(f"qout   = {qout[-1]:.6f} m^3/s")


# Final state

# -----------------------------

# h      = 0.249994 m

# CM     = 312.317 mol/m^3

# gamma  = 78.077 mol/m^3

# qout   = 0.010000 m^3/s

