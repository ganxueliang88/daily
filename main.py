import json

import melos
import os

if __name__ == "__main__":
    config = os.getenv('CONFIG')
    config = json.loads(config)
    melos.do_daily(config)
