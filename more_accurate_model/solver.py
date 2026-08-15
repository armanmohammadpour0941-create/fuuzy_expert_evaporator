from scipy.integrate import solve_ivp

from more_accurate_model.equation import med_equation


def evaporator_ode_solver(t_span, t_eval, X0, u, distur, time_vec, params):
    sol = solve_ivp(
        med_equation,
        t_span,
        X0,
        args=(u, distur, params, time_vec),
        t_eval=t_eval,
        method="RK45",
        rtol=1e-6,
        atol=1e-9,
        max_step=10,  # Limit step size for stability
    )
    return sol

