import sys, os

# Set up Python interpreter path (will be configured in cPanel)
INTERP = "/home/<user>/virtualenv/<python>/bin/python"

# Check if we're using the right interpreter
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)

# Add current directory to Python path
sys.path.append(os.getcwd())

# Import the Flask app
from axiomhive_flask import app as application  # WSGI export

# Configure for production
application.config['ENV'] = 'production'
application.config['DEBUG'] = False

# Add any additional production configurations
if not application.config.get('SECRET_KEY'):
    application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'axiomhive-4d-nexus-2025')

print("AxiomHive 4D Nexus WSGI initialized (t=2025-09-20)", file=sys.stderr)
