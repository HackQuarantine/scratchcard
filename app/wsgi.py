from . import create_app

try:
  import googleclouddebugger
  googleclouddebugger.enable()
except ImportError:
  pass


app = create_app()
