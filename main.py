import json

import melos
import bsc_test_faucet
import os

if __name__ == "__main__":
    config = os.getenv('CONFIG')
    config = json.loads(config)
    melos.do_daily(config)
    bsc_test_faucet.do_daily(config)
