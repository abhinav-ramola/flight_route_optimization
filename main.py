import pandas as pd
import networkx as nx
import folium

class FlightOptimizer:
    def __init__(self, flight_data_path):
        self.graph = nx.DiGraph()
        self.flights = pd.read_csv(flight_data_path)
        self._build_graph()

    def _build_graph(self):
        for _, row in self.flights.iterrows():
            self.graph.add_edge(
                row['source'], row['dest'],
                cost=row['cost'],
                time=row['time_minutes'],
                co2=row['co2_kg'],
                source_lat=row['source_lat'],
                source_lon=row['source_lon'],
                dest_lat=row['dest_lat'],
                dest_lon=row['dest_lon']
            )

    def find_all_paths(self, src, dst, max_hops=3):
        return list(nx.all_simple_paths(self.graph, source=src, target=dst, cutoff=max_hops))

    def score_path(self, path, weights):
        cost_w, time_w, layover_w, co2_w = weights
        total_cost, total_time, total_co2 = 0, 0, 0
        for i in range(len(path)-1):
            edge = self.graph[path[i]][path[i+1]]
            total_cost += edge['cost']
            total_time += edge['time']
            total_co2 += edge['co2']
        score = (
            total_cost * cost_w +
            total_time * time_w +
            total_co2 * co2_w +
            (len(path)-2) * layover_w
        )
        return score, total_cost, total_time, total_co2, len(path)-2

    def best_paths(self, src, dst, weights, top_k=3):
        all_paths = self.find_all_paths(src, dst)
        scored = []
        for path in all_paths:
            score, cost, time, co2, layovers = self.score_path(path, weights)
            scored.append((score, path, cost, time, co2, layovers))
        scored.sort(key=lambda x: x[0])
        return scored[:top_k]

    def visualize_paths(self, best_paths, output_file="multi_criteria_flight_paths.html"):
        if not best_paths:
            print("No paths to visualize.")
            return

        first_leg = best_paths[0][1]
        src_node = first_leg[0]
        lat = self.graph[first_leg[0]][first_leg[1]]['source_lat']
        lon = self.graph[first_leg[0]][first_leg[1]]['source_lon']
        fmap = folium.Map(location=[lat, lon], zoom_start=4)

        for idx, (score, path, cost, time, co2, layovers) in enumerate(best_paths):
            color = 'red' if idx == 0 else 'blue'
            for i in range(len(path)-1):
                edge = self.graph[path[i]][path[i+1]]
                points = [(edge['source_lat'], edge['source_lon']),
                          (edge['dest_lat'], edge['dest_lon'])]
                label = f"{path[i]} → {path[i+1]}<br>Cost: ₹{edge['cost']}<br>Time: {edge['time']} min<br>CO₂: {edge['co2']} kg"
                folium.PolyLine(
                    points,
                    color=color,
                    weight=5 if idx == 0 else 3,
                    opacity=0.7,
                    tooltip=label
                ).add_to(fmap)
            # Add total path summary at destination
            last = path[-1]
            last_lat = self.graph[path[-2]][last]['dest_lat']
            last_lon = self.graph[path[-2]][last]['dest_lon']
            folium.Marker(
                [last_lat, last_lon],
                popup=(f"Path {idx+1}<br>Total Score: {score:.2f}<br>Cost: ₹{cost}<br>Time: {time} min<br>CO₂: {co2} kg<br>Layovers: {layovers}"),
                icon=folium.Icon(color='red' if idx == 0 else 'blue', icon='plane')
            ).add_to(fmap)

        fmap.save(output_file)
        print(f"Map with multiple paths saved as '{output_file}'")


def main():
    flight_data_path = "flights.csv"
    optimizer = FlightOptimizer(flight_data_path)

    src = input("Enter source airport code: ").strip().upper()
    dst = input("Enter destination airport code: ").strip().upper()

    print("Rate your preferences from 1 (least) to 10 (most importance):")
    cost_w = int(input("Cost weight (1-10): "))
    time_w = int(input("Time weight (1-10): "))
    layover_w = int(input("Layover weight (1-10): "))
    co2_w = int(input("CO2 weight (1-10): "))

    weights = (cost_w, time_w, layover_w, co2_w)

    paths = optimizer.best_paths(src, dst, weights)
    if not paths:
        print("No valid paths found between the given airports.")
        return

    print("\nTop paths found (score and route):")
    for idx, (score, path, cost, time, co2, layovers) in enumerate(paths, 1):
        print(f"Path {idx}: Score={score:.2f}, Route={' -> '.join(path)}")

    optimizer.visualize_paths(paths)

if __name__ == "__main__":
    main()
