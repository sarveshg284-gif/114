import numpy as np
import matplotlib.pyplot as plt
import heapq
import streamlit as st

# -------------------------------
# 1. Demand Growth Model
# -------------------------------
def simulate_growth(P0, K, r, alpha, T, dt=0.1):
    time_steps = int(T / dt)
    P = np.zeros(time_steps)
    t = np.linspace(0, T, time_steps)

    P[0] = P0

    for i in range(1, time_steps):
        dP = r * P[i-1] * (1 - P[i-1]/K) * (1 + alpha * (P[i-1]/K))
        P[i] = P[i-1] + dP * dt

    return t, P


# -------------------------------
# 2. Dijkstra Algorithm
# -------------------------------
def dijkstra_with_path(graph, start):
    pq = [(0, start)]
    distances = {node: float('inf') for node in graph}
    previous = {node: None for node in graph}

    distances[start] = 0

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))

    return distances, previous


def get_path(previous, target):
    path = []
    while target:
        path.append(target)
        target = previous[target]
    return path[::-1]


# -------------------------------
# 3. UI
# -------------------------------
st.title("🚚 Logistics + Demand Growth Simulator")

st.sidebar.header("📊 Demand Parameters")

P0 = st.sidebar.number_input("Initial Users", value=10)
K = st.sidebar.number_input("Market Capacity", value=10000)
r = st.sidebar.slider("Growth Rate (r)", 0.01, 1.0, 0.3)
alpha1 = st.sidebar.slider("Network Effect - Scenario 1", 0.0, 2.0, 0.3)
alpha2 = st.sidebar.slider("Network Effect - Scenario 2", 0.0, 2.0, 1.2)
T = st.sidebar.slider("Time Horizon", 10, 100, 50)


# -------------------------------
# 4. Graphs
# -------------------------------
graph1 = {
    'Warehouse': {'A': 10, 'B': 15},
    'A': {'C': 12, 'D': 15},
    'B': {'D': 10},
    'C': {'Hub1': 5},
    'D': {'Hub2': 10},
    'Hub1': {},
    'Hub2': {}
}

graph2 = {
    'Warehouse': {'A': 10, 'B': 15},
    'A': {'C': 12, 'D': 15},
    'B': {'D': 10},
    'C': {'Hub1': 5},
    'D': {'Hub2': 10},
    'Hub1': {'Hub2': 3},  # shortcut
    'Hub2': {}
}


# -------------------------------
# 5. Run Simulation
# -------------------------------
t1, demand1 = simulate_growth(P0, K, r, alpha1, T)
t2, demand2 = simulate_growth(P0, K, r, alpha2, T)

dist1, prev1 = dijkstra_with_path(graph1, 'Warehouse')
dist2, prev2 = dijkstra_with_path(graph2, 'Warehouse')


# -------------------------------
# 6. Display Results
# -------------------------------
st.subheader("📈 Demand Results")

col1, col2 = st.columns(2)
col1.metric("Final Demand (Scenario 1)", f"{demand1[-1]:.0f}")
col2.metric("Final Demand (Scenario 2)", f"{demand2[-1]:.0f}")


# -------------------------------
# 7. Plot Growth
# -------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(t1, demand1, label="Scenario 1 (Normal)")
ax.plot(t2, demand2, label="Scenario 2 (Improved Network)")

ax.set_xlabel("Time")
ax.set_ylabel("Users")
ax.set_title("Demand Growth Comparison")
ax.legend()
ax.grid(True)

st.pyplot(fig)


# -------------------------------
# 8. Route Results
# -------------------------------
st.subheader("🚚 Route Optimization")

for scenario_name, dist, prev in [
    ("Scenario 1", dist1, prev1),
    ("Scenario 2", dist2, prev2)
]:
    st.markdown(f"### {scenario_name}")
    for hub in ['Hub1', 'Hub2']:
        path = get_path(prev, hub)
        st.write(f"{hub}: Distance = {dist[hub]}, Path = {path}")
