import argparse
from os import path

import rpyc
from rpyc.utils.classic import DEFAULT_SERVER_PORT

# YOU should run on the target pc this: rpyc_classic.py -m threaded --host 0.0.0.0 -p 11223

DRIVER_FILE_TO_UPLOAD = 'sample.sys'
DRIVER_DEST_DIR = "C:\\"
PROJECT_DIR = path.dirname(__file__)


def parse_arguments(args=None):
    parser = argparse.ArgumentParser(description="Connect to testing VM for deployment and testing of the Driver")

    parser.add_argument('host', help="IP of the target computer")
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_SERVER_PORT,
                        help="Listening port on the target computer")

    parser.add_argument('--release', action="store_const", const="release", default="debug",
                        help="Use the Release version of the driver instead of the debug")

    return parser.parse_args(args)

if __name__ == "__main__":
    args = parse_arguments()

    connection = rpyc.classic.connect(args.host)
    driver_file = path.join(PROJECT_DIR, 'Sample', args.release, DRIVER_FILE_TO_UPLOAD)
    rpyc.utils.classic.upload(connection, driver_file, path.join(DRIVER_DEST_DIR, DRIVER_FILE_TO_UPLOAD))


