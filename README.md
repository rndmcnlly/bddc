# bddc

This project implements a command line tool, `bddc`, that offers access to a self-contained Python interpreter with [`omega`](https://github.com/tulip-control/omega) pre-installed. Omega is a high-level wrapper around a powerful library of binary decision diagram (BDD) algorithms.

The user of `bddc` should think of it as like [`dc`](https://en.wikipedia.org/wiki/Dc_(computer_program)) (in that it offers a calculator in a [repl](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) interface) or [`z3`](https://github.com/Z3Prover/z3) (in that it packages up a complex inference engine). While `bddc` can be used iteractively for quick experiments, it can be run as a subprocess of larger applications (similar to how the [`minisat`](http://minisat.se/) SAT solver is often used). The analogy with `z3` goes deeper, however, as `bddc` allows working with expressions over bitvectors rather than elementary Boolean variables. In fact, a subset of the [`TLA+`](https://lamport.azurewebsites.net/tla/tla.html) language is supported for rapidly constructing large circuits from simple expressions over bitvectors.

# Usage

Launch it in a shell:

    $ ./bddc

Interact with it as a repl:

    >>> declare(x=(0,15),y=(0,15))
    >>> pairs = add_expr('x <= y')
    >>> count(pairs)
    136

Alternatively, communicate with it via pipes:

    $ echo "print('meow')" | ./bddc

# Building

    $ python3 -m venv venv
    $ . ./venv/bin/activate
    $ pip install -r requirements.txt
    $ nuitka3 --onefile bddc.py

# Credits

Created by [Adam Smith](https://adamsmith.as/).