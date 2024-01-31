# bddc: the interactive BDD calculator

# nuitka-project: --onefile
# nuitka-project: --static-libpython=yes

# XXX: hack to avoid bloat of likely-unused networkx
# nuitka-project: --nofollow-import-to=networkx
import sys
from types import SimpleNamespace
sys.modules['networkx'] = SimpleNamespace(MultiDiGraph=None)

import code
from omega.symbolic.fol import Context

default_context = Context()
convenience_functions = {k: getattr(default_context, k) for k in dir(default_context)}

env = {
  'Context': Context,
  'default_context': default_context,
  **convenience_functions,
  'exit': sys.exit
}

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
  console = code.InteractiveConsole(env)
  if sys.stdin.isatty():
    console.interact(banner, exitmsg)
  else:
    for line in sys.stdin:
      console.push(line)

if __name__ == "__main__":
  main()