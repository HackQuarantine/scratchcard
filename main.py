from app import create_app

try:
  import googleclouddebugger
  googleclouddebugger.enable()
except ImportError:
  pass

import os
print(os.listdir('/'))
print(os.listdir('/cloudsql/'))
app = create_app()
