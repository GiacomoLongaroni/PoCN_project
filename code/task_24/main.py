from generate_model import *
from percolation import *
from scpp import scp
from theo_solution import *
import matplotlib.pyplot as plt

n =10000
z = 2.5
trials = 10
# Grafo ER iniziale
g0, edges0 = generate_er_graph(n, z)
# Senza q-swap
p_values = np.arange(0.0, 1.001, 0.02)
q_target = [2,3] 

S_qswap = []
S_noswap = []
print('ER entanglement percolation')
for p in p_values:
    if p%0.1==0:
        print('p: ',p)
    S_p_swapped = []
    S_p_noswapped = []

    g_swap, swapped_edges = apply_qswap(g0,q_target)
    
    for trial in range(trials):
        use_distill = 'two'
        g_qswap_perc = quantum_percolation(g_swap, swapped_edges, p, use_distill)
        g_perc = quantum_percolation(g0, set(), p, use_distill)

        qswapped_GCC = giant_component_fraction(g_qswap_perc)
        noswapped_gCC = giant_component_fraction(g_perc)

        S_p_swapped.append(qswapped_GCC)
        S_p_noswapped.append(noswapped_gCC)
    
    
    S_qswap.append(np.mean(S_p_swapped))
    S_noswap.append(np.mean(S_p_noswapped))


S_theory_noswap = [compute_S_noswap(z, p) for p in p_values]
S_theory_qswap = [compute_S_qswap(p, z, q_target) for p in p_values]



fig, axes = plt.subplots(1, 1, figsize=(8, 6))
axes.scatter(p_values, S_noswap,marker = 'o', label='MC no q-swap', color = 'black', s = 15)
axes.plot(p_values, S_theory_noswap, '--', label='Theory no q-swap', alpha = 0.5, linewidth = 1, color = 'black')
axes.scatter(p_values, S_qswap,marker = 's', label=f"MC q-swap {q_target}", color = 'red', s = 15)
axes.plot(p_values, S_theory_qswap, '--', label='Theory  q-swap', alpha = 0.5, linewidth = 1, color = 'red')
axes.legend()
axes.set_xlabel('p')
axes.set_ylabel('S')
axes.set_title(f'Quantum percolation on ER (n={n}, z={z:.2f})')
axes.grid(alpha = 0.2)

plt.show()

