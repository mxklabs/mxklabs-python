import importlib
import logging
import os

from .exprset import ExprSet

logger = logging.getLogger(f'mxklabs.expr.ExprContext')

class ExprContext:

  def __init__(self, load_mxklabs_exprsets=True):
    if load_mxklabs_exprsets:
      exprsets = self._get_mxklabs_exprsets()
      for exprset in exprsets:
        self.load_exprset(exprset)

  def load_exprset(self, name):
    """
        Load an expression set via a module name.
        For example:

        ```
        from mxklabs.expr import ExprBuilder

        builder = ExprBuilder()
        builder.load_exprset("mxklabs.expr.exprsets.bitvector")

        # Now use the bitvector exprset.
        x = builder.bitvector.variable(width=10)
        ```
    """
    logger.info(f'Loading exprset \'{name}\'')
    module = importlib.import_module(name)
    exprset = ExprSet(module)

    if '.' in name:
      exprset_name = name[name.rfind('.')+1:]
    else:
      exprset_name = name

    # This is where we set the exprset attribute.
    setattr(self, exprset_name, exprset)

  def _get_mxklabs_exprsets(self):
    exprsets_dir = os.path.join(os.path.dirname(__file__), "exprsets")
    names = [e for e in os.listdir(exprsets_dir)
        if os.path.isdir(os.path.join(exprsets_dir, e))]
    return [f"mxklabs.expr.exprsets.{name}" for name in names]

