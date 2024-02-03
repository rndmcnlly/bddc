# This example `bddc` script attempts to illustrate a mildly interesting
# symbolic algorithm implemented using the `omega` package and some Python
# scripting goodness.

# Problem: Given a directe graph, compute the shortest path between all pairs
# of nodes. Do it using fewer iterations than the diameter of the graph.

# Aproach: Use iterative squaring!

# Start with a bunch of nodes organized into a directed ring:
n = 64
edges = [(i, (i + 1) % n) for i in range(n)]

# Now add a weird extra edge crossing the ring.
edges += [(0, n // 2)]
print(f"{edges=}")

# In interactive mode, `bddc` pre-populates the global namespace with lots of
# useful stuff. In script mode, we'll use explicit imports to make it clear how
# things work without them.

# Let's setup the symbolic context:

from omega.symbolic.fol import Context
context = Context()

NODE_RANGE = (0, n)
DISTANCE_RANGE = (0, n * n)

context.declare(
    x_prev=NODE_RANGE,
    x_next=NODE_RANGE,
    x_temp=NODE_RANGE,

    dist_pn=DISTANCE_RANGE,
    dist_pt=DISTANCE_RANGE,
    dist_tn=DISTANCE_RANGE,
    dist_alt=DISTANCE_RANGE,
)

# Construct the transition relation:
trans_pn = context.false
for u, v in edges:
    trans_pn |= context.assign_from(dict(x_prev=u, x_next=v, dist_pn=1))

# Intially, our distance oracle is only aware of immediate edges:
oracle_pn = trans_pn
print(f"{trans_pn.dag_size=}")

# But we can use iterative squaring to grow it until convergence:

num_iterations = 0
oracle_pn_last = context.false

while oracle_pn != oracle_pn_last:
    oracle_pn_last = oracle_pn
    print(f"iteration {num_iterations}")

    # Rename variables in current oracle to mention a temp node:
    oracle_pt = context.let({"x_next": "x_temp", "dist_pn": "dist_pt"}, oracle_pn)
    oracle_tn = context.let({"x_prev": "x_temp", "dist_pn": "dist_tn"}, oracle_pn)

    # Add paths that pass through a temp node:
    oracle_pn |= context.exist(
        ["x_temp", "dist_pt", "dist_tn"],
        oracle_pt & oracle_tn & context.add_expr("dist_pn = dist_pt + dist_tn"),
    )

    # Remove dominated paths:
    oracle_pn &= ~context.exist(
        ["dist_alt"],
        oracle_pn
        & context.let({"dist_pn": "dist_alt"}, oracle_pn)
        & context.add_expr("dist_alt < dist_pn"),
    )

    print(f"  {oracle_pn.dag_size=}")
    num_iterations += 1


print(f"Converged in {num_iterations} iterations.")


# For this graph, the number it shouldn't take many iteration at all!
import math
assert num_iterations == math.ceil(math.log2(n)) + 1

# Here's how we recover specific distances from the compressed oracle.
sol = context.pick(oracle_pn & context.assign_from(dict(x_prev=0, x_next=0)))
print(f"Length of path from origin back to self: {sol['dist_pn']}")