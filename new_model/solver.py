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
    sl.plot_solver_result(sol)

    
    