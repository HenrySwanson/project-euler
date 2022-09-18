"""
The primes 3, 7, 109, and 673, are quite remarkable. By taking any two primes and concatenating them in any order
the result will always be prime. For example, taking 7 and 109, both 7109 and 1097 are prime. The sum of these four
primes, 792, represents the lowest sum for a set of four primes with this property.

Find the lowest sum for a set of five primes for which any two primes concatenate to produce another prime.
"""

from collections import defaultdict
import itertools
from typing import Dict, List, Optional, Tuple

from lib.misc import num_digits
from lib.prime_state import PrimeCache


N = 5


def solve_problem() -> int:
    # I think the hard part here is going to be the "lowest sum" criterion...
    # How do you rule out 3, 7, and three big primes?
    pc = PrimeCache()

    # Iterate with higher and higher bounds
    soln: Optional[Tuple[int]] = None
    for k in itertools.count(1):
        soln = solve_bounded_problem(pc, 10**k)
        if soln is not None:
            break

    assert soln is not None
    return sum(soln)


def solve_bounded_problem(pc: PrimeCache, bound: int) -> Optional[Tuple[int, ...]]:
    pc.init_sieve_of_eratosthenes(bound)

    compatible: Dict[int, List[int]] = defaultdict(list)
    for p in pc.iter_primes(cutoff=bound):
        for q in pc.iter_primes(cutoff=p):
            if is_compatible(pc, p, q):
                compatible[q].append(p)  # q < p

    # We now want to find a clique of size N in this graph.
    # To do this, note that we already have a list of K_2s, and that we can use the
    # edges plus a list of K_ns to find the K_(n+1)s.
    # Also, note that the cliques are stored in increasing order, avoiding duplicates.

    n = 2
    cliques_n: Dict[Tuple[int, ...], List[int]] = {
        (x,): ys
        for x, ys in compatible.items()
        # if < N-1 numbers are compatible with x, it can't be part of
        # a clique of size N
        if len(ys) >= N - 1
    }

    while n != N:
        cliques_n1: Dict[Tuple[int, ...], List[int]] = defaultdict(list)

        for clique, ps in cliques_n.items():
            for p in ps:
                # clique + p is a clique of size n
                # consider adding numbers from compatible[p]
                for q in compatible.get(p, []):
                    if all(is_compatible(pc, r, q) for r in clique):
                        cliques_n1[clique + (p,)].append(q)

        # The tuples are length n at this point, so if there's < N-n possible elements
        # to pair it with, there's no way to form a clique of size N.
        cliques_n = {
            tup: tails for tup, tails in cliques_n1.items() if len(tails) >= N - n
        }
        n += 1

    if not cliques_n:
        return None

    tuples = [tup + (t,) for tup, tails in cliques_n.items() for t in tails]
    return max(tuples, key=sum)


def concat_is_prime(pc: PrimeCache, p: int, q: int) -> bool:
    concat = p * 10 ** num_digits(q) + q
    return pc.is_prime(concat)


def is_compatible(pc: PrimeCache, p: int, q: int) -> bool:
    return concat_is_prime(pc, p, q) and concat_is_prime(pc, q, p)
