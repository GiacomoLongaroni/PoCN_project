import math 
import numpy as np 

def clip01(x):
    return 0.0 if x < 0.0 else x#(1.0 if x > 1.0 else x)

## probability and generating functions
def P(k,z):
    return math.exp(-z) * (z**k) / math.factorial(k)

def P1(q, z):
    if q <= 0: return 0.0
    return math.exp(-z) * (z**(q-1)) / math.factorial(q-1)

def G_1(x,z):
    return np.exp(z*(x-1))

def scp_two_no_distill(p):
    return  2*p - p**2



## NUMERICAL COMPUTATION OF H WITHOUT QUANTUM SWAP
def u_step(u,p2,z):
    return 1.0 - p2 + p2 * G_1(u, z)

def u_solver(p2,z):
    precision = 1e-18
    u_star = 1-1e-13
    max_iter = 2000

    for _ in range(max_iter):
        u = u_step(u_star,p2,z)
        u = clip01(u)
        if abs(u_star - u) < precision: break
        u_star = u 
    
    return u_star

def compute_S_noswap(z, p):
    p2 = scp_two_no_distill(p)
    u  = u_solver(p2, z)
    return 1.0 - G_1(u,z)  



## NUMERICAL COMPUTATION OF S WITH QUANTUM SWAP 

def eta_q_approx(q, z):
    return 1.0 / (1.0 + 0.5 * q * P1(q, z))

def compute_Cq(p,z,u,q):

    val = 0 

    for l in range(q-1):
        val += (l+1) * p**l * (1-p)**2 * G_1(u,z)**l 
    
    val += (q * (p**(q-1)) * (1-p) + p**q) * G_1(u,z)**(q-1)
    
    return val


def compute_Hq(p,z,u,q):

    p2 = scp_two_no_distill(p)
    Cq = compute_Cq(p,z,u,q)

    return P1(q,z) * ((p2-1) - p2 * (u**(q-1)) + Cq)

def u_step_qswap(u,p,z,q_target):
    val = 0
    p2 = scp_two_no_distill(p)

    for q in q_target:
        val += compute_Hq(p,z,u,q)

    return 1-p2+(p2*G_1(u,z)) + val 

def u_solver_qswap(p,z,q_target):

    u_star = 1-1e-10
    precision = 1e-18
    maxiter = 2000
    for _ in range(maxiter):
        u = u_step_qswap(u_star,p,z,q_target)
        if abs(u_star - u) < precision: break
        u_star = u 
    
    return u_star

def compute_S_qswap(p,z,q_target):

    u = u_solver_qswap(p,z,q_target)

    val = 0

    for q in q_target:
        val += eta_q_approx(q,z) * P(q,z)*(1-u**q)
    
    return 1 - G_1(u,z) - val