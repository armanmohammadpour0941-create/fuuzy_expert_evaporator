from scipy.integrate import solve_ivp
from evaporator_euation import evaporator_dynamic_model
from library import calculate_vapor_flow, calculate_liquid_flow, plot

def evaporator_ode_solver(t_span, t_eval, X0, U, D, T_sin):
    sol = solve_ivp(
        evaporator_dynamic_model,
        t_span,
        X0,
        args=(U, D, T_sin),
        t_eval=t_eval,
        rtol=1e-6,
        atol=1e-9,
        max_step=10  # Limit step size for stability
    )
    
    w_v = calculate_vapor_flow(sol, U, T_sin, D)
    w_bout = calculate_liquid_flow(sol)
    plot(sol, w_v, w_bout)
    