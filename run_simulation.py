from simulate import *
from library import plot
cfg = MEDConfig(N=1)
y0 = [1.0, 25.0, 8.0]
t_span = (0, 3600)

sol= run_simulation(cfg, y0, t_span, 3600)
plot(sol)