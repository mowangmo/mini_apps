import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from ATM.core import main_f
from ATM.lib import log_f
from ATM.core import atm_f

if __name__ == '__main__':
    log_f.load_my_logging_cfg()
    atm_f.interest()
    main_f.main()
