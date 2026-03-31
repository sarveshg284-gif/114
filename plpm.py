import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# --- Model ---
def simulate_growth(P0, K, r, alpha, T, dt=0.1):
    time_steps = int(T / dt)
    P = np.zeros(time_steps)
    t = np.linspace(0, T, time_steps)

    P[0] = P0

    for i in range(1, time_steps):
        dP = r * P[i-1] * (1 - P[i-1]/K) * (1 + alpha * (P[i-1]/K))
        P[i] = P[i-1] + dP * dt

    return t, P


# --- UI ---
st.title("📈 Product Launch Popularity Simulator")
st.markdown("Logistic Growth + Network Effects Model")

# Sidebar inputs
st.sidebar.header("Scenario Parameters")

P0 = st.sidebar.number_input("Initial Users (P0)", value=10)
K = st.sidebar.number_input("Market Capacity (K)", value=10000)
r = st.sidebar.slider("Growth Rate (r)", 0.01, 1.0, 0.3)
alpha = st.sidebar.slider("Network Effect (alpha)", 0.0, 2.0, 0.5)
T = st.sidebar.slider("Time Horizon", 10, 100, 50)

# --- Simulation ---
t, P = simulate_growth(P0, K, r, alpha, T)

# --- Metrics ---
st.subheader("📊 Results")
col1, col2 = st.columns(2)

col1.metric("Final Popularity", f"{P[-1]:.0f}")
col2.metric("Peak Popularity", f"{np.max(P):.0f}")

# --- Plot ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(t, P, label="Popularity Growth")
ax.set_xlabel("Time")
ax.set_ylabel("Users")
ax.set_title("Growth Curve")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# --- Scenario Comparison ---
st.subheader("🔁 Compare with Another Scenario")

with st.expander("Add Comparison Scenario"):
    P0_2 = st.number_input("Initial Users (Scenario 2)", value=10, key="p02")
    K_2 = st.number_input("Market Capacity (Scenario 2)", value=10000, key="k2")
    r_2 = st.slider("Growth Rate (Scenario 2)", 0.01, 1.0, 0.3, key="r2")
    alpha_2 = st.slider("Network Effect (Scenario 2)", 0.0, 2.0, 1.2, key="a2")

    if st.button("Run Comparison"):
        t2, P2 = simulate_growth(P0_2, K_2, r_2, alpha_2, T)

        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.plot(t, P, label="Scenario 1")
        ax2.plot(t2, P2, label="Scenario 2")
        ax2.set_xlabel("Time")
        ax2.set_ylabel("Users")
        ax2.set_title("Scenario Comparison")
        ax2.legend()
        ax2.grid(True)

        st.pyplot(fig2)
