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


# Ideas for future improvements

 * Add a `pyproject.toml` to mechanize build process and formalize project metadata.
 * Start versioning and keeping track of interesting changes via documentatoin.
 * Investigate source of startup delay.
 * Create an `examples/` folder with usage inspirations. Some ideas:
    - Use `bddc` as a handy interactive calculator (performance many operations using the default context shorthand).
    - Use `bddc` in batch mode from a larger POSIX shell script with stdio piped through other common shell tools like [`jq`](https://jqlang.github.io/jq/).
    - Use `bddc` in service mode, possibly loading a huge serialized BDD created in a preprocesing step before answering several incremental queries in the same session.
    - Invent a naming convention where `foo.bddc.py` identifies a Python-syntax script that is meant to be executed in `bddc` rather than normal Python.
 * Add some command line arguments that offer better in-tool documentation and support for adding new modes/options.
 * Add some helper functions for load/dump of circuits in a way that preserves the meaning of a Context, not just the raw BDD. Can we just stuff the data from `context.vars` into the JSON data that is used by the lower-level BDD serde?
 * Add a usage mode (e.g. `bddc -t`) that allows quickly evaluating simple TLA+ expressions from command line arguments. Optionally allow certain circuits to be populated from external files. Need some way to pick outputs: sat/unsat, count, first-k solutions (where k=0 means all)? What syntax for outputs? TLA+ representing a conjunction of concrete assignments? 

# Credits

Created by [Adam Smith](https://adamsmith.as/).