from scipy.integrate import solve_ivp
from equation import med_equation
import solution as sl

def evaporator_ode_solver(t_span, t_eval, X0, u, distur, params):
    sol = solve_ivp(
        med_equation,
        t_span,
        X0,
        args=(u, distur, params),
        t_eval=t_eval,
        method='BDF',
        rtol=1e-6,
        atol=1e-9,
        max_step=10  # Limit step size for stability
    )
    w_v = sl.calculate_vapor_flow_from_sol(sol, u, distur, params)
    w_b = sl.calculate_liquid_flow_from_sol(sol, params)
    sl.plot_complete_solution(sol, w_v, w_b)

    
    