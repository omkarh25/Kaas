import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import KaasApp
from utils import log_exception

def main():
    """
    Main entry point for the Kaas application.
    """
    try:
        kaas_app = KaasApp()
        sys.exit(kaas_app.run())
    except Exception as e:
        log_exception(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
