# bddc: the interactive BDD calculator

# Various portions of this file were created with the help of GitHub Copilot.

# nuitka-project: --onefile
# nuitka-project-if: {OS} != 'Windows':
#   nuitka-project: --static-libpython=yes

# XXX: hack to avoid bloat of likely-unused networkx
# nuitka-project: --nofollow-import-to=networkx
import sys
import code
import argparse

from types import SimpleNamespace

sys.modules["networkx"] = SimpleNamespace(MultiDiGraph=None)

from omega.symbolic.fol import Context

banner = f"""
 .o8             .o8        .o8            
"888            "888       "888            
 888oooo.   .oooo888   .oooo888   .ooooo.  
 d88' `88b d88' `888  d88' `888  d88' `"Y8 
 888   888 888   888  888   888  888       
 888   888 888   888  888   888  888   .o8 
 `Y8bod8P' `Y8bod88P" `Y8bod88P" `Y8bod8P' 
                                           
Execute symbolic algorithms using binary decision diagrams (BDDs)!
Docs: https://github.com/tulip-control/omega/blob/main/doc/doc.md

Use functions like `declare`, `add_expr`, and `count` to act on the
default `omega.symbolic.fol.Context` instance or use the `Context`
constructor to create your own.
"""

exitmsg = "bddc you later!"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s with Python {sys.version}",
    )
    parser.add_argument(
        "-t",
        "--tla",
        metavar="EXPR",
        action="store",
        help="just interpret a TLA+ expression (otherwise offer Python repl)",
    )

    tla_group = parser.add_argument_group("TLA+ evaluator mode")
    tla_group.add_argument("-b", "--bits", action="store", type=int, default=7, help="number of bits used for each variable (default: 7)")
    tla_group.add_argument("-d", "--declare", action="store", type=str, default=None, help="declare a variable ranges (e.g., \"x \in -5..5 & y \in 0..10\"")

    tla_mutex = tla_group.add_mutually_exclusive_group()
    tla_mutex.add_argument(
        "-c", "--count", action="store_true", help="output model count"
    )
    tla_mutex.add_argument(
        "-e",
        "--enumerate",
        metavar="N",
        action="store",
        default=None,
        type=int,
        help="enumerate solutions (0 means all)",
    )
    tla_mutex.add_argument(
        "-p",
        "--pick",
        action="store_const",
        const=1,
        dest="enumerate",
        help="output just one solution",
    )

    args = parser.parse_args()
    if args.tla:
        eval_tla(args)
    else:
        run_repl()


def eval_tla(args: argparse.Namespace):
    from omega.logic.lexyacc import Parser
    from omega.logic.ast import Nodes

    parser = Parser()
    expr_ast = parser.parse(args.tla)
    vars = set()

    def collect_variables(node):
        if hasattr(node, "operands"):
            for op in node.operands:
                collect_variables(op)
        if isinstance(node, Nodes.Var):
            vars.add(node.value)

    collect_variables(expr_ast)

    decls = {v: (-1 << args.bits-1, +1 << args.bits-1) for v in vars}

    if args.declare:
        decl_ast = parser.parse(args.declare)
        def visit_decl(node):
            if isinstance(node, Nodes.Binary) and node.operator == '/\\':
                visit_decl(node.operands[0])
                visit_decl(node.operands[1])
            elif isinstance(node, Nodes.Binary) and node.operator == '\\in':
                decls[node.operands[0].value] = (int(node.operands[1].operands[0].value), int(node.operands[1].operands[1].value))
        visit_decl(decl_ast)

    context = Context()    
    context.declare(**decls)

    f = context.add_expr(args.tla)
    if args.count:
        print(context.count(f))
    elif args.enumerate is not None:
        if args.enumerate == 0:
            args.enumerate = float("inf")
        for i, sol in enumerate(context.pick_iter(f)):
            print(sol)
            if i + 1 >= args.enumerate:
                break
    else:
        print("false" if f == context.false else "true")


def run_repl():
    default_context = Context()
    convenience_functions = {
        k: getattr(default_context, k) for k in dir(default_context)
    }

    env = {
        "Context": Context,
        "default_context": default_context,
        **convenience_functions,
        "exit": sys.exit,
    }

    console = code.InteractiveConsole(env)
    if sys.stdin.isatty():
        console.interact(banner, exitmsg)
    else:
        for line in sys.stdin:
            console.push(line)


if __name__ == "__main__":
    main()
