# ✈️ Multi-Criteria Flight Route Optimizer

**🔗 Live App:** [flightrouteoptimisation.streamlit.app](https://flightrouteoptimisation.streamlit.app/)

A **Streamlit + Python** web app that optimizes flight routes based on **cost, time, layovers, and CO₂ emissions**.  
It models flight networks using **NetworkX** and provides real-time visualization via **Folium interactive maps**.

---

## 🧭 Features

- 🌍 **Multi-criteria optimization** using customizable weights:
  - 💰 Cost
  - ⏱️ Travel time
  - 🛫 Number of layovers
  - 🌱 CO₂ emissions

- 🧠 **Algorithms used:**
  - Dijkstra’s Algorithm  
  - Bellman-Ford Algorithm  
  - K-Shortest Path (alternative routes)

- 🗺️ **Interactive map visualization**
  - Real-time route plotting with tooltips
  - Colored routes for comparison (Best, Alternative, Dijkstra, Bellman-Ford)

- 📊 **Performance metrics displayed**
  - Total cost, total travel time, CO₂ emissions, and layovers per route

---

## 🚀 Demo

> Try it live here → [https://flightrouteoptimisation.streamlit.app/](https://flightrouteoptimisation.streamlit.app/)

**Example usage:**
1. Choose **Source** and **Destination** airports.
2. Adjust your preferences (Cost, Time, Layovers, CO₂).
3. Click **“Find Routes”**.
4. Explore optimized routes on an interactive Folium map!

---

## 🧩 Tech Stack

| Component | Technology |
|------------|-------------|
| Frontend UI | Streamlit |
| Graph Modeling | NetworkX |
| Map Visualization | Folium + Streamlit-Folium |
| Data Handling | Pandas |
| Language | Python 3 |

---

## ⚙️ Installation

### 1️⃣ Clone this repository
```bash
git clone https://github.com/<your-username>/flight-route-optimizer.git
cd flight-route-optimizer
