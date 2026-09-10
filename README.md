# CHMENG162-DynamicControl

## W2 Lab 
 Ordinary Differential Equations (ODEs)

An **Ordinary Differential Equation (ODE)** describes how a dependent variable changes with respect to a single independent variable.

For example,

$$
\frac{dy}{dt} = f(t,y)
$$

where:

- $t$ = independent variable, usually time
- $y$ = dependent variable
- $\frac{dy}{dt}$ = rate of change of $y$
- $f(t,y)$ = model describing the system dynamics

### W2 Concepts
- scipy.integrate import solve_ivp for initial value problem y(0) = y_0
- Explicit and Implicit Solver: Backward Differentiation Formula
- Robertson's Stiff ODE Problem
