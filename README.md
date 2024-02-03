# bddc

This project implements a command line tool, `bddc`, that offers access to a self-contained Python interpreter with [`omega`](https://github.com/tulip-control/omega) pre-installed. Omega is a high-level wrapper around a powerful library of binary decision diagram (BDD) algorithms.

The user of `bddc` should think of it as like [`dc`](https://en.wikipedia.org/wiki/Dc_(computer_program)) (in that it offers a calculator in a [repl](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) interface) or [`z3`](https://github.com/Z3Prover/z3) (in that it packages up a complex inference engine). While `bddc` can be used iteractively for quick experiments, it can be run as a subprocess of larger applications (similar to how the [`minisat`](http://minisat.se/) SAT solver is often used). The analogy with `z3` goes deeper, however, as `bddc` allows working with expressions over bitvectors rather than elementary Boolean variables. In fact, a subset of the [`TLA+`](https://lamport.azurewebsites.net/tla/tla.html) language is supported for rapidly constructing large circuits from simple expressions over bitvectors.

*If `omega` is just some Python library can be easily installed with pip, why does `bddc` exist?* At least currently, `omega` only offers its full functionality (a wrapper around [`cudd`](https://github.com/ivmai/cudd)) when compiled for Python 3.10 on Linux. By packaging `bddc` as a self-contained executable, it can be integrated into applications without needing to reproduce the environment needed to build `bddc` in the first place. Someday, someone can build an [αcτµαlly pδrταblε εxεcµταblε](https://justine.lol/ape.html) to stretch a single binary for this project across many more platforms.

# Usage

Launch it in a shell:

    $ ./bddc

Interact with it as a repl:

    >>> declare(x=(0,15),y=(0,15))
    >>> pairs = add_expr('x <= y')
    >>> count(pairs)
    136

Alternatively, communicate with it via pipes:

    $ echo "print('meow')" | ./bddc -

Or let it run your scripts:

    $ ./bddc example.bddc.py

Even use it for quick evaluation of TLA+ expressions:

    $ # generete some perfect square
    $ ./bddc -t "\E x: x*x=y" -d "x \in 0..16 & y \in 0..256" -e 0 

# Building from source

Assuming you have downloaded this repository, installed Python 3.10, and installed poetry, run the following commands to install this project's dependencies and build the `bddc` executable binary for your platform.

    $ poetry install
    $ poetry run pip uninstall -y dd
    $ git clone https://github.com/tulip-control/dd.git dd-git
    $ cd dd-git
    $ poetry run python setup.py install --fetch --cudd --cudd_zdd
    $ cd ..
    $ poetry run nuitka3 bddc.py

# Ideas for future improvements

 * Create a poetry script to automate the weird setup process.
 * Investigate source of startup delay.
 * Add more usage examples:
    - Use `bddc` as a handy interactive calculator (performance many operations using the default context shorthand).
    - Use `bddc` in batch mode from a larger POSIX shell script with stdio piped through other common shell tools like [`jq`](https://jqlang.github.io/jq/).
    - Use `bddc` as a long-lived subrocess, possibly loading a huge serialized BDD created in a preprocesing step before answering several incremental queries in the same session.
 * For Python, add some helper functions for load/dump of circuits in a way that preserves the meaning of a Context, not just the raw BDD. Can we just stuff the data from `context.vars` into the JSON data that is used by the lower-level BDD serde?
 
# Credits

Created by [Adam Smith](https://adamsmith.as/).