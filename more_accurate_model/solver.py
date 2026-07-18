from scipy.integrate import solve_ivp
from equation import med_equation
import solution as sl

def evaporator_ode_solver(t_span, t_eval, X0, u, distur, time_vec, params):
    sol = solve_ivp(
        med_equation,
        t_span,
        X0,
        args=(u, distur, params, time_vec),
        t_eval=t_eval,
        method='RK45',
        rtol=1e-6,
        atol=1e-9,
        max_step=10  # Limit step size for stability
    )
    w_v = sl.calculate_vapor_flow_from_sol(sol, u, distur, params)
    w_b = sl.calculate_liquid_flow_from_sol(sol, params)
    sl.print_final_value(sol, w_v, w_b)
    # sl.plot_complete_solution(sol, w_v, w_b)
    # sl.plot_solver_result(sol)

    
    