# bddc: the interactive BDD calculator

# nuitka-project: --onefile
# nuitka-project: --static-libpython=yes
# nuitka-project: --remove-output
# nuitka-project: --output-filename=bddc

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
  **convenience_functions
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

def main():
  if sys.stdin.isatty():
    code.interact(
      banner=banner,
      local=env,
      exitmsg="bddc you later!",
    )
  else:
    for line in sys.stdin:
      exec(line, None, env)

if __name__ == "__main__":
  main()