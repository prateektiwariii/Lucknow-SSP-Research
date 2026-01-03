#define _USE_MATH_DEFINES
#define NOMINMAX 
#include <cmath>
#include <osmium/io/any_input.hpp>
#include <osmium/handler.hpp>
#include <osmium/visitor.hpp>
#include <osmium/index/map/sparse_mem_array.hpp>
#include <osmium/handler/node_locations_for_ways.hpp>
#include <iostream>
#include <vector>
#include <queue>
#include <chrono>
#include <unordered_map>
#include <algorithm>
#include <fstream>
#include <random>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

using namespace std;

// Data structures for the Research Study
struct Point { double lat, lon; };
struct Edge { long long to; double weight; };
struct TrialResult {
    double distance;
    int dijkstra_visited;
    int astar_visited;
    double time_ms;
};

unordered_map<long long, vector<Edge>> adj;
unordered_map<long long, Point> node_coords;

// Haversine formula for spherical distance (The Paper's Core Math)
double haversine(Point p1, Point p2) {
    double r = 6371.0; 
    double dLat = (p2.lat - p1.lat) * M_PI / 180.0;
    double dLon = (p2.lon - p1.lon) * M_PI / 180.0;
    double a = sin(dLat/2) * sin(dLat/2) + cos(p1.lat * M_PI/180.0) * cos(p2.lat * M_PI/180.0) * sin(dLon/2) * sin(dLon/2);
    return 2 * r * asin(sqrt(a));
}

class LucknowHandler : public osmium::handler::Handler {
public:
    void way(const osmium::Way& way) {
        if (way.get_value_by_key("highway")) {
            const auto& nodes = way.nodes();
            for (size_t i = 0; i < nodes.size() - 1; ++i) {
                long long u = nodes[i].ref();
                long long v = nodes[i+1].ref();
                node_coords[u] = {nodes[i].lat(), nodes[i].lon()};
                node_coords[v] = {nodes[i+1].lat(), nodes[i+1].lon()};
                double d = haversine(node_coords[u], node_coords[v]);
                adj[u].push_back({v, d});
                adj[v].push_back({u, d});
            }
        }
    }
};

TrialResult runExperiment(long long start, long long goal) {
    // Dijkstra Algorithm (Baseline)
    priority_queue<pair<double, long long>, vector<pair<double, long long>>, greater<>> pq_d;
    unordered_map<long long, double> dist_d;
    int visited_d = 0;
    pq_d.push({0.0, start});
    dist_d[start] = 0.0;
    while (!pq_d.empty()) {
        long long u = pq_d.top().second; pq_d.pop();
        visited_d++;
        if (u == goal) break;
        for (auto& e : adj[u]) {
            if (dist_d.find(e.to) == dist_d.end() || dist_d[u] + e.weight < dist_d[e.to]) {
                dist_d[e.to] = dist_d[u] + e.weight;
                pq_d.push({dist_d[e.to], e.to});
            }
        }
    }

    // A* Algorithm (Optimized)
    auto start_time = chrono::high_resolution_clock::now();
    priority_queue<pair<double, long long>, vector<pair<double, long long>>, greater<>> pq_a;
    unordered_map<long long, double> dist_a;
    int visited_a = 0;
    pq_a.push({0.0, start});
    dist_a[start] = 0.0;
    while (!pq_a.empty()) {
        long long u = pq_a.top().second; pq_a.pop();
        visited_a++;
        if (u == goal) break;
        for (auto& e : adj[u]) {
            double g = dist_a[u] + e.weight;
            if (dist_a.find(e.to) == dist_a.end() || g < dist_a[e.to]) {
                dist_a[e.to] = g;
                double h = haversine(node_coords[e.to], node_coords[goal]);
                pq_a.push({g + h, e.to});
            }
        }
    }
    auto end_time = chrono::high_resolution_clock::now();
    double time_ms = chrono::duration<double, milli>(end_time - start_time).count();

    return {dist_a[goal], visited_d, visited_a, time_ms};
}

int main() {
    string file = "../planet_80.494,26.595_81.284,27.068.osm.pbf";
    cout << "Loading Lucknow Dataset..." << endl;
    
    try {
        osmium::io::File input{file};
        using index_type = osmium::index::map::SparseMemArray<osmium::unsigned_object_id_type, osmium::Location>;
        index_type index;
        osmium::handler::NodeLocationsForWays<index_type> location_handler{index};
        LucknowHandler lh;
        osmium::io::Reader reader{input};
        osmium::apply(reader, location_handler, lh);
        reader.close();
    } catch (const exception& e) {
        cerr << "Error loading PBF: " << e.what() << endl;
        return 1;
    }

    cout << "Graph Built: " << adj.size() << " nodes." << endl;
    
    // Preparation for 1,000-Trial Experiment
    vector<long long> all_node_ids;
    for(auto const& [id, _] : adj) all_node_ids.push_back(id);
    
    mt19937 rng(1337); // Seed for reproducible research
    ofstream csv("lucknow_research_data.csv");
    csv << "Trial,Distance_KM,Dijkstra_Visited,AStar_Visited,Efficiency_Gain_Percent,Time_AStar_MS\n";

    cout << "Starting Batch Testing (1,000 trials)..." << endl;
    
    for(int i = 0; i < 1000; ++i) {
        long long start = all_node_ids[rng() % all_node_ids.size()];
        long long goal = all_node_ids[rng() % all_node_ids.size()];
        
        TrialResult res = runExperiment(start, goal);
        
        // Ensure path exists before logging
        if(res.distance > 0 && res.dijkstra_visited > 1) {
            double gain = (double)(res.dijkstra_visited - res.astar_visited) / res.dijkstra_visited * 100.0;
            csv << i << "," << res.distance << "," << res.dijkstra_visited << "," 
                << res.astar_visited << "," << gain << "," << res.time_ms << "\n";
            
            if(i % 100 == 0) cout << "Progress: " << i << "/1000 trials logged." << endl;
        } else {
            i--; // Retry another random pair if no path found
        }
    }

    csv.close();
    cout << "SUCCESS: 'lucknow_research_data.csv' generated for analysis." << endl;
    return 0;
}