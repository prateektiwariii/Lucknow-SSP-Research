import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Set ultra-high resolution and professional styling
plt.rcParams.update({
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'font.size': 12,
    'font.family': 'serif',
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'legend.fontsize': 12,
    'figure.titlesize': 18,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--'
})
sns.set_palette("bright")

# 1. LOAD DATA
df = pd.read_csv('lucknow_research_data.csv')

# Preprocessing: Calculate Expansion Factors and Efficiency
df['Dijkstra_Factor'] = df['Dijkstra_Visited'] / df['Distance_KM']
df['AStar_Factor'] = df['AStar_Visited'] / df['Distance_KM']

# Distance Binning for Geographic Scale Analysis
bins = [0, 5, 15, 30, 50, 100]
labels = ['Ultra-Short (<5km)', 'Short (5-15km)', 'Medium (15-30km)', 'Long (30-50km)', 'Ultra-Long (>50km)']
df['Distance_Category'] = pd.cut(df['Distance_KM'], bins=bins, labels=labels)

# 2. FIGURE 1: BIVARIATE REGRESSION ANALYSIS
# Shows the divergence of search effort
plt.figure(figsize=(10, 7))
sns.regplot(data=df, x='Distance_KM', y='Dijkstra_Visited', scatter_kws={'alpha':0.1, 's':10}, 
            line_kws={'color':'#e74c3c', 'linewidth': 2}, label='Dijkstra (Uninformed)')
sns.regplot(data=df, x='Distance_KM', y='AStar_Visited', scatter_kws={'alpha':0.1, 's':10}, 
            line_kws={'color':'#3498db', 'linewidth': 2}, label='A* (Haversine Informed)')
plt.title('Fig 1. State-Space Expansion Dynamics vs. Urban Scale')
plt.xlabel('Geodesic Path Distance (Kilometers)')
plt.ylabel('Nodes Popped from Priority Queue')
plt.legend(frameon=True, shadow=True)
plt.tight_layout()
plt.savefig('fig1_regression_detailed.png')

# 3. FIGURE 2: BOXENPLOT OF EFFICIENCY GAIN
# "Boxenplots" are better for large datasets (N=1000) than standard boxplots
plt.figure(figsize=(12, 7))
sns.boxenplot(data=df, x='Distance_Category', y='Efficiency_Gain_Percent', palette='viridis')
plt.title('Fig 2. Search Efficiency Distribution by Geographic Sector')
plt.xlabel('Scale Category')
plt.ylabel('Efficiency Gain (%)')
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig('fig2_efficiency_boxen.png')

# 4. FIGURE 3: EXPANSION FACTOR DENSITY (PROBABILITY ANALYSIS)
plt.figure(figsize=(10, 7))
sns.kdeplot(df['Dijkstra_Factor'], fill=True, color='#e74c3c', label='Dijkstra (Nodes/KM)', bw_adjust=0.5)
sns.kdeplot(df['AStar_Factor'], fill=True, color='#3498db', label='A* (Nodes/KM)', bw_adjust=0.5)
plt.title('Fig 3. Probability Density of Node Expansion Factor')
plt.xlabel('Expansion Intensity (Nodes Explored per Kilometer)')
plt.ylabel('Density of Trials')
plt.legend()
plt.tight_layout()
plt.savefig('fig3_expansion_density_detailed.png')

# 5. FIGURE 4: CUMULATIVE DISTRIBUTION FUNCTION (CDF)
plt.figure(figsize=(10, 7))
sorted_gain = np.sort(df['Efficiency_Gain_Percent'])
yvals = np.arange(len(sorted_gain))/float(len(sorted_gain)-1)
plt.plot(sorted_gain, yvals, color='#2ecc71', linewidth=4, label='A* Search Advantage')
plt.fill_between(sorted_gain, yvals, color='#2ecc71', alpha=0.1)
plt.title('Fig 4. Empirical Cumulative Distribution of Algorithmic Savings')
plt.xlabel('Search Space Reduction (%)')
plt.ylabel('Cumulative Probability')
plt.axhline(0.5, color='gray', linestyle=':', label='Median Gain')
plt.legend()
plt.tight_layout()
plt.savefig('fig4_efficiency_cdf_detailed.png')

# 6. FIGURE 5: THE GOMTI RIVERINE PARADOX (SIMULATED GEOSPATIAL CONTEXT)
# Creating a much more detailed simulation of the search frontier
def generate_gomti_simulation():
    # Grid of Lucknow Central
    lu_start = np.array([80.937, 26.865]) 
    gn_end = np.array([81.020, 26.840]) 
    bridge_node = np.array([80.975, 26.855])
    
    # River path (The Barrier)
    river_x = np.linspace(80.95, 80.99, 100)
    river_y = 26.88 - 0.5 * (river_x - 80.95) + np.sin((river_x-80.95)*50)*0.005

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8), sharey=True)
    
    # DIJKSTRA SIMULATION: Circular Expansion
    np.random.seed(42)
    # Dijkstra expands until it covers the bridge area
    d_points = np.random.normal(lu_start, 0.045, (6000, 2))
    ax1.scatter(d_points[:,0], d_points[:,1], s=1, color='#e74c3c', alpha=0.15, label='Frontier Expansion')
    ax1.plot(river_x, river_y, color='#34495e', linewidth=8, alpha=0.4, label='Gomti River Barrier')
    ax1.scatter(lu_start[0], lu_start[1], color='black', s=150, edgecolors='white', label='Source (LU)', zorder=10)
    ax1.scatter(gn_end[0], gn_end[1], color='#27ae60', marker='X', s=200, edgecolors='white', label='Goal (Gomti Nagar)', zorder=10)
    ax1.set_title('A. Dijkstra: Stochastic Global Expansion', fontsize=18)
    ax1.legend(loc='lower left')

    # A* SIMULATION: Heuristic Constriction
    # Path is Start -> Bridge -> Goal
    # Generate points along these vectors with noise
    a_points = []
    for _ in range(1500):
        if np.random.rand() < 0.6:
            # Traveling toward bridge
            lerp = np.random.rand()
            p = lu_start + (bridge_node - lu_start) * lerp
        else:
            # Traveling from bridge to goal
            lerp = np.random.rand()
            p = bridge_node + (gn_end - bridge_node) * lerp
        p += np.random.normal(0, 0.004, 2)
        a_points.append(p)
    a_points = np.array(a_points)
    
    ax2.scatter(a_points[:,0], a_points[:,1], s=4, color='#3498db', alpha=0.5, label='Heuristic Corridor')
    ax2.plot(river_x, river_y, color='#34495e', linewidth=8, alpha=0.4)
    ax2.scatter(bridge_node[0], bridge_node[1], color='#f1c40f', marker='s', s=150, edgecolors='black', label='Nishatganj Bridge Gateway', zorder=11)
    ax2.scatter(lu_start[0], lu_start[1], color='black', s=150, edgecolors='white', zorder=10)
    ax2.scatter(gn_end[0], gn_end[1], color='#27ae60', marker='X', s=200, edgecolors='white', zorder=10)
    ax2.set_title('B. A*: Bridge-Targeted Beam Search', fontsize=18)
    ax2.legend(loc='lower left')

    plt.suptitle('Fig 5. The Gomti Riverine Bottleneck Paradox: Informed vs. Uninformed Frontiers', fontsize=22, y=1.02)
    plt.tight_layout()
    plt.savefig('fig5_gomti_geospatial_detailed.png', bbox_inches='tight')
    plt.close()

generate_gomti_simulation()

# 7. FIGURE 6: TIME-DISTANCE COMPLEXITY
plt.figure(figsize=(10, 7))
sns.scatterplot(data=df, x='Distance_KM', y='Time_AStar_MS', hue='Distance_Category', size='AStar_Visited',
                palette='magma', alpha=0.6, sizes=(10, 200))
plt.title('Fig 6. A* Performance Profile: Execution Time vs. Euclidean Magnitude')
plt.xlabel('Traversal Distance (KM)')
plt.ylabel('CPU Execution Time (Milliseconds)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title='Scale Categories')
plt.tight_layout()
plt.savefig('fig6_time_complexity_detailed.png')

print("Exhaustive Research Figures Generated.")