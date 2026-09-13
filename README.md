# CHMENG162-DynamicControl

- Textbook:
Process Control: Modeling, Design, and Simulation
Wayne Bequette (Publisher: Prentice Hall, 2003)

- Definition:
What is a Mathematical Model? > A model is an abstraction of reality! /  George E. P. Box(1976): All models are wrong, but some are useful

- Eykhoff (1974):
“a representation of the essential aspects of an existing system (or
a system to be constructed) which represents knowledge of that
system in a usable form”

- Dynamic model:
Mathematical description of the transient (unsteady state) behavior of a process

## General Procedure for Developing Dynamic Models
1. State model objective and end use (level of complexity)
2. Draw schematic diagram of process and label all process variables
3. List all assumptions
4. Write balance equation
5. Introduce constitutive equations
6. Perform degrees of freedom (Is the model solvable?)
7. Classify input as Dependent Variables I(What effect outcome but I cannot control)or Manipulate variable (What can I do to controk)

## Concepts:

- Physics-based process modeling(Assumption Must be made!): Mass Balance for Blending System, Steady State Mass Balance , Possible Control Strategies (Feedforward, FeedBack),  
- Analysis of dynamical systems
- Empirical process modeling
- Feedback control and PID control design
- Direct control synthesis
- Internal model control
- Feedforward/cascade control
- Closed-loop interactions in multi-loop control systems
- Frequency-response analysis
- Statistical process control


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


### Examples1 : Spatial ODE iPFR in steady state
![Q1note-PFR.png](Q1note-PFR.png)


- 1.Consider a **steady-state plug flow reactor**, with flow rate $F= 1 m^3/s$ , length $L=5 m$ and cross-sectional
area $A=1 m^2$. Consider a single step first-order, irreversible reaction : $$A→B$$ Consider the initial concentration of $A$ to be $1 M$  at the inlet. Perform a component balance over a differential element $dx$ along the reactor. Assume $k=1 s^{-1}$ to be the rate constant for the reaction. Now, could you frame a first-order differential equation from this balance? Solve it and plot the concentration profile of A and B along the $x$ direction. 

- 1.1 Objective: Steady state spatial model , indepent variable is location x(0<x<L) (not time t!) 

- 1.2 Diagram and variables
 
```
x = 0                                             x = L
Inlet                                               Outlet
  |                                                   |
  v                                                   v
-------------------------------------------------------
|                                                     |
|              Plug Flow Reactor                      |
|                                                     |
-------------------------------------------------------
          ---> flow direction --->

       |---- dx ----|

       differential volume:
       dV = Ac dx
       F= Volumetric flow rate , A = reactor cross section area , k = first order rate constant
```

- **1.3 Assumptions**: steady state concentration no accumulation , uniform concentration over each cross section C = C(x) , Constant volumetric flow rate / cross section area / isothermal operation (k = constant) / reaction stoichiometry 1:1
- **1.4 Mass Balance Equations** - Acc= In - Out + Gen - Consume / Steady State : Acc = 0 
- **1.5 Constituitive Equations** $$F C_A(x)$$, 2 Methods Approach
- A)  The molar flow leaving at $x+dx$ is:
 $$F C_A(x+dx)$$ Using a **first-order Taylor expansion**: $$C_A(x+dx) \approx C_A(x) + \frac{dC_A}{dx}dx$$ Therefore, the outlet flow is: $$F \left( C_A + \frac{dC_A}{dx}dx \right)$$
- B) $$\{F(C_A(x+dx)-C_A(x))=-kC_AA_cdx}$$ and use the **definition of derivative** $$\frac{dC_A}{dx}=\lim_{dx\to0}\frac{C_A(x+dx)-C_A(x)}{dx}$$

 | Method              | Main idea                                                    | Key equation                                                   |
| ------------------- | ------------------------------------------------------------ | -------------------------------------------------------------- |
| Taylor expansion    | Approximate \(C_A(x+dx)\) using the derivative               | $$C_A(x+dx)\approx C_A(x)+\frac{dC_A}{dx}dx$$                |
| Difference quotient | Keep the inlet-outlet difference first, then take \(dx\to0\) | $$\frac{dC_A}{dx}=\lim_{dx\to0}\frac{C_A(x+dx)-C_A(x)}{dx}$$ |

- Result

$$
\frac{dC_A}{dx}=-\frac{kA_c}{F}C_A
$$

$$
\frac{dC_B}{dx}=\frac{kA_c}{F}C_A
$$


 - **1.6  Degrees of Freedom for  Unknown dependent variables**: $$C_A(x),\ C_B(x)$$ Number of unknowns: $$N_{\text{unknowns}}=2$$ Number of independent equations: $$N_{\text{equations}}=2$$ Therefore: $$DOF=N_{\text{unknowns}}-N_{\text{equations}}$$ $$DOF=2-2=0$$ Thus: $$\{DOF=0}$$ The model is fully specified and solvable.
 -   Final Analytical Solution Because: $$A_c=1,\ k=1,\ F=1$$ the concentration of A is:  $${C_A(x)=e^{-x}}$$  The concentration of B is: $${C_B(x)=1-e^{-x}}$$
 -   Spatial ODE vs. Dynamic ODE For this steady-state PFR, the model is a spatial ODE: $$\{\frac{dC}{dx}=f(C)}$$ The independent variable is position $x$. For a dynamic reactor model: $$\boxed{\frac{dC}{dt}=f(C,u)}$$ The independent variable is time $t$.

 -   **1.7 Variables**
 -   MV(what i can change): flow rate,
 -   CV (what i want to change): C_A(x) out concentration or Conversion rate
 -   DV (what i cannot change): Inlet Concentration

![PFR1.png](PFR1.png)

### Example 2: Well mixed time-dependent Batch Reactor (Accumulation is not zero!), with Stiff Problem 
for 2. it is a non-continious batch reactor, object is to build concentration time profile C(t), assumption is isothermal, Both reactions are irreversible. balance is also **mass accumulation = Generation, so not in steady state!**, consecutive equations are pure reaction kinetic of time since the concentration does not depend on location and volume , degree of freedom is 0 since equation =3, variable =3, DVs are concentration of C , 

```
        Batch Reactor
    ---------------------
    |                   |
    |     A → B → C     |
    |                   |
    |   Well mixed      |
    |   V = 3 m³        |
    ---------------------

        No inlet
        No outlet

        C = C(t)
```
![PFR1.png](PFR1.png)



