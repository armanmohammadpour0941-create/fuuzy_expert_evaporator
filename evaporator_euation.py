def evaporator_dynamic_model(t, X, U, D):
    l, x, T_b, T_t = X
    W_s, W_f = U
    T_f, x_f, W_bin, x_bin, T_bin = D
    
    # Constants
    sea_dens = 1050    # kg/m3
    A = 8.64           # evaporator cross area m2
    A_o = 0.114        # cross area of brine outlet pipe
    C_d = 0.7          # discharge coefficient
    Cp = 4.2           # kJ/kg°C
    A_heat = 2000      # heat transfer area m2
    