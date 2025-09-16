from generate_model import *
from percolation import *
from scpp import scp
from theo_solution import *
import matplotlib.pyplot as plt
from italy_graph import *

dataset = create_world_dataset(pop=25000)
italy_graph = create_graph(dataset)
plot_graph(dataset,italy_graph)


p_values = np.arange(0.0, 1.001, 0.05)
q_target = [2,3]  

S_qswap, S_noswap = [], []
clusters_qswap, clusters_noswap = [], []
edges_qswap, edges_noswap = [], []   # nuove liste

for p in p_values:
    print(p)
    S_p_swapped, S_p_noswapped = [], []
    c_p_swapped, c_p_noswapped = [], []
    e_p_swapped, e_p_noswapped = [], []  # edges per trial

    g_swap, swapped_edges = apply_qswap(italy_graph, q_target)
    
    for trial in range(10):
        use_distill = 'two'
        g_qswap_perc = quantum_percolation(g_swap, swapped_edges, p, use_distill)
        g_perc = quantum_percolation(italy_graph, set(), p, use_distill)

        # Giant component
        S_p_swapped.append(giant_component_fraction(g_qswap_perc))
        S_p_noswapped.append(giant_component_fraction(g_perc))

        # Cluster sizes
        comp_swap = g_qswap_perc.connected_components(mode="weak")  
        c_p_swapped.append(np.mean(comp_swap.sizes()))

        comp_noswap = g_perc.connected_components(mode="weak")  
        c_p_noswapped.append(np.mean(comp_noswap.sizes()))

        # Numero edges
        e_p_swapped.append(g_qswap_perc.ecount())
        e_p_noswapped.append(g_perc.ecount())

    # Medie sui trials
    S_qswap.append(np.mean(S_p_swapped))
    S_noswap.append(np.mean(S_p_noswapped))
    clusters_qswap.append(np.mean(c_p_swapped))
    clusters_noswap.append(np.mean(c_p_noswapped))
    edges_qswap.append(np.mean(e_p_swapped))
    edges_noswap.append(np.mean(e_p_noswapped))

# --- plotting ---
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Percolation on Italy network')
# --- grafico S ---
axes[0].scatter(p_values, S_noswap, marker='o', label='MC no q-swap', color='black', s=15)
axes[0].scatter(p_values, S_qswap, marker='s', label=f"MC q-swap {q_target}", color='red', s=15)
axes[0].legend()
axes[0].set_ylim(0, 1)
axes[0].grid(alpha=0.2)
axes[0].set_xlabel("p")
axes[0].set_ylabel("S")
axes[0].set_title("GCC size")

# --- grafico clusters ---
axes[1].scatter(p_values, clusters_noswap, marker='o', label='Cluster no q-swap', color='black', s=15)
axes[1].scatter(p_values, clusters_qswap, marker='s', label=f"Cluster q-swap {q_target}", color='red', s=15)
axes[1].legend()
axes[1].grid(alpha=0.2)
axes[1].set_xlabel("p")
axes[1].set_ylabel("avg size")
axes[1].set_title("avg connected component size")

# --- grafico edges ---
axes[2].scatter(p_values, edges_noswap, marker='o', label='Edges no q-swap', color='black', s=15)
axes[2].scatter(p_values, edges_qswap, marker='s', label=f"Edges q-swap {q_target}", color='red', s=15)
axes[2].legend()
axes[2].grid(alpha=0.2)
axes[2].set_xlabel("p")
axes[2].set_ylabel("N")
axes[2].set_title("N.of edges")

plt.tight_layout()
plt.show()