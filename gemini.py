import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# --- پارامترهای ثابت سیستم ---
rho = 1000.0     # چگالی آب (kg/m^3)
A_bp = 5.0       # مساحت حوضچه (m^2)
Cp = 4.184       # ظرفیت حرارتی ویژه (kJ/kg.C)
L_steam = 2256.0 # گرمای نهان چگالش بخار ورودی (kJ/kg)
L_eff = 2380.0   # گرمای نهان تبخیر در شرایط خلا اثر (kJ/kg)
kb = 15.0        # ضریب هیدرولیکی خروجی حوضچه (kg/h.m) -> تبدیل به ثانیه در مدل میشود

# --- مقادیر متغیرهای ورودی (Manipulated Variables) ---
F_steam = 1.2    # دبی بخار ورودی به لوله‌ها (kg/s)
F_feed = 10.0    # دبی خوراک ورودی (kg/s)

# --- مقادیر اغتشاش‌ها (Disturbances) ---
T_feed = 25.0    # دمای خوراک (C)
X_feed = 6.0 # غلظت نمک خوراک (ppm)

F_b_prev = 4.0   # دبی آب شور از اثر قبل (kg/s)
T_b_prev = 57.0  # دمای آب شور اثر قبل (C)
X_b_prev = 8.0 # غلظت نمک اثر قبل (ppm)

# --- تعریف معادلات دیفرانسیل (مدل فضای حالت) ---
def med_evaporator_model(t, states):
    # تفکیک متغیرهای حالت
    h_bp, X_bp, T_effect = states
    T_feed = T_feed
    if t > 3000:
        # F_feed = 8.0  # دبی خوراک کاهش می‌یابد
        T_feed = 30.0 # دمای خوراک کاهش می‌یابد
        # X_feed = 5.0  # غلظت نمک خوراک کاهش می‌یابد
    # جلوگیری از مقادیر منفی غیرفیزیکی در محاسبات عددی
    h_bp = max(h_bp, 1e-4)
    M_bp = rho * A_bp * h_bp # جرم مایع در حوضچه
    
    # ۱. محاسبات نرخ تبخیر روی لوله‌ها
    Q_steam = F_steam * L_steam
    # انرژی صرف شده برای پیش‌گرمایش فیلم ریزشی و سپس تبخیر آن
    V_film = (Q_steam - F_feed * Cp * (T_effect - T_feed)) / L_eff
    V_film = max(V_film, 0.0)
    
    # دبی مایعی که از روی لوله‌ها ته‌نشین می‌شود و غلظت آن
    F_film_to_bp = F_feed - V_film
    X_film = (F_feed * X_feed) / max(F_film_to_bp, 1e-3)
    
    # ۲. محاسبات نرخ تبخیر در حوضچه (بر اثر تعادل حرارتی جریان ورودی داغ)
    V_bp = (F_b_prev * Cp * (T_b_prev - T_effect)) / L_eff
    V_bp = max(V_bp, 0.0)
    
    # ۳. دبی آب شور خروجی هیدرولیکی (تابع ارتفاع)
    B_out = kb * h_bp
    
    # ۴. معادلات دیفرانسیل (مشتق‌ها)
    # dh_bp/dt (موازنه جرم کل)
    dh_bp_dt = (F_film_to_bp + F_b_prev - V_bp - B_out) / (rho * A_bp)
    
    # dX_bp/dt (موازنه نمک)
    dX_bp_dt = ((F_film_to_bp * (X_film - X_bp)) + (F_b_prev * (X_b_prev - X_bp))) / M_bp
    
    # dT_effect/dt (موازنه انرژی کل اثر برای دینامیک حرارتی)
    # سیستم کنترل فشار اجازه تغییرات شدید به دما نمی‌دهد، اما دینامیک آن به این صورت است:
    Q_in = Q_steam + F_feed * Cp * T_feed + F_b_prev * Cp * T_b_prev
    Q_out = B_out * Cp * T_effect + (V_film + V_bp) * L_eff
    dT_effect_dt = (Q_in - Q_out) / (M_bp * Cp)
    
    # در صورتی که فشار کاملا قفل باشد، می‌توان dT_effect_dt = 0 قرار داد.
    # اما به عنوان متغیر حالت، اجازه می‌دهیم سیستم به تعادل برسد.
    
    return [dh_bp_dt, dX_bp_dt, dT_effect_dt]

# --- شرایط اولیه سیستم ---
# [ارتفاع حوضچه (متر), غلظت نمک (ppm), دمای اثر (سانتی‌گراد)]
initial_states = [0.5, 6.0, 20.0]

# بازه زمانی شبیه‌سازی (۰ تا ۵۰۰۰ ثانیه)
t_span = (0, 5000)
t_eval = np.linspace(0, 5000, 10000)

# --- حل عددی معادلات ---
sol = solve_ivp(med_evaporator_model, t_span, initial_states, t_eval=t_eval, method='RK45')

# --- رسم نمودارهای خروجی ---
plt.figure(figsize=(12, 10))

# نمودار ارتفاع حوضچه
plt.subplot(3, 1, 1)
plt.plot(sol.t, sol.y[0], 'b-', linewidth=2)
plt.title('Dynamic Response of the MED Evaporator Effect')
plt.ylabel('Brine Pool Level (m)')
plt.grid(True)

# نمودار غلظت نمک
plt.subplot(3, 1, 2)
plt.plot(sol.t, sol.y[1], 'r-', linewidth=2)
plt.ylabel('Salinity X_bp (ppm)')
plt.grid(True)

# نمودار دمای اثر
plt.subplot(3, 1, 3)
plt.plot(sol.t, sol.y[3] if len(sol.y)>3 else sol.y[2], 'g-', linewidth=2)
plt.xlabel('Time (seconds)')
plt.ylabel('Effect Temperature (C)')
plt.grid(True)

plt.tight_layout()
plt.show()