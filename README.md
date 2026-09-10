# CHMENG162-DynamicControl

- Textbook:
Process Control: Modeling, Design, and Simulation
Wayne Bequette (Publisher: Prentice Hall, 2003)

- Definition:
What is a Mathematical Model? > A model is an abstraction of reality!

Eykhoff (1974):
“a representation of the essential aspects of an existing system (or
a system to be constructed) which represents knowledge of that
system in a usable form”

Dynamic model:
Mathematical description of the transient (unsteady state) behavior of a process

- Concepts:

Physics-based process modeling: 
Analysis of dynamical systems
Empirical process modeling
Feedback control and PID control design
Direct control synthesis
Internal model control
Feedforward/cascade control
Closed-loop interactions in multi-loop control systems
Frequency-response analysis
Statistical process control


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



