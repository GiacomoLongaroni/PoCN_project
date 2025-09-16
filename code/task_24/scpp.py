def scp(p, use_distill):
    if use_distill == 'one':
        val = p
    elif use_distill == 'two':
        val = 2*p - p**2
    elif use_distill == 'two_opt':
        val = min(1, 2*p - 0.5*(p**2))
    return val