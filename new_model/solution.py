
def plot_solver_result(sol):
    import matplotlib.pyplot as plt

    plt.figure(1)
    plt.plot(sol.t, sol.y[0], label="brine level")
    plt.xlabel("time (s)")
    plt.ylabel("level")
    plt.grid()
    plt.legend()

    plt.figure(2)
    plt.plot(sol.t, sol.y[1], label="salinity")
    plt.xlabel("time (s)")
    plt.ylabel("x")
    plt.grid()
    plt.legend()

    plt.figure(3)
    plt.plot(sol.t, sol.y[2], label="brine temperature")
    plt.xlabel("time (s)")
    plt.ylabel("Temperature")
    plt.grid()
    plt.legend()

    plt.show() 

# def plot(sol, W_v, W_b):
#     import matplotlib.pyplot as plt

#     plt.figure(1)
#     plt.plot(sol.t, sol.y[0], label="brine level")
#     plt.xlabel("time (s)")
#     plt.ylabel("level")
#     plt.grid()
#     plt.legend()

#     plt.figure(2)
#     plt.plot(sol.t, sol.y[1], label="salinity")
#     plt.xlabel("time (s)")
#     plt.ylabel("x")
#     plt.grid()
#     plt.legend()

#     plt.figure(3)
#     plt.plot(sol.t, sol.y[2], label="brine temperature")
#     plt.xlabel("time (s)")
#     plt.ylabel("Temperature")
#     plt.grid()
#     plt.legend()

#     plt.figure(4)
#     plt.plot(sol.t, W_v, label="vapor rate")
#     plt.xlabel("time (s)")
#     plt.ylabel("kg/h")
#     plt.grid()
#     plt.legend()

#     plt.figure(5)
#     plt.plot(sol.t, W_b, label="brine liq rate")
#     plt.xlabel("time (s)")
#     plt.ylabel("kg/h")
#     plt.grid()
#     plt.legend()

#     plt.show() 
