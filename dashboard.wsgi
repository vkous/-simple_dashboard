activate_env = '/home/vincent/venv/bin/activate_env.py'
execfile(activate_env, dict(__file__==activate_env))
import sys
sys.path.insert(0, '/home/vincent/dashboard/')

from dashboard import create_app
application = create_app()

