import argparse
from os import path

import rpyc
from rpyc.utils.classic import DEFAULT_SERVER_PORT

# YOU should run on the target pc this (with admin): rpyc_classic.py -m threaded --host 0.0.0.0
DRIVER_FILE_TO_UPLOAD = 'sample.sys'
DRIVER_DEST_DIR = "C:\\"
PROJECT_DIR = path.dirname(__file__)

KERNEL_SERVICE_NAME = "DriverTest"


def parse_arguments(args=None):
    parser = argparse.ArgumentParser(description="Connect to testing VM for deployment and testing of the Driver")

    parser.add_argument('host', help="IP of the target computer")
    parser.add_argument('-i', '--install', action="store_true", default=False,
                        help="Install the driver as a service")
    parser.add_argument('-s', '--start', action="store_true", default=False,
                        help="Start the driver as a service")
    
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_SERVER_PORT,
                        help="Listening port on the target computer")

    parser.add_argument('--release', action="store_const", const="release", default="debug",
                        help="Use the Release version of the driver instead of the debug")

    return parser.parse_args(args)

if __name__ == "__main__":
    args = parse_arguments()

    dest_driver_path = path.join(DRIVER_DEST_DIR, DRIVER_FILE_TO_UPLOAD)

    connection = rpyc.classic.connect(args.host)
    driver_file = path.join(PROJECT_DIR, 'Sample', 'x64', args.release, DRIVER_FILE_TO_UPLOAD)
    rpyc.utils.classic.upload(connection, driver_file, dest_driver_path)
    print("Upload {} to {}".format(DRIVER_FILE_TO_UPLOAD, dest_driver_path))

    if args.install:
        import subprocess # used for exception testing
        remote_subprocess = connection.modules.subprocess

        try:
            print("Trying to install using SC")
            print(remote_subprocess.check_output(
                "sc create {} type= kernel binPath= {}".format(KERNEL_SERVICE_NAME, dest_driver_path)).decode('utf-8'))
            print("Driver installed")

            if args.start:
                print("Trying to start using SC")
                print(remote_subprocess.check_output(
                    "sc start {}".format(KERNEL_SERVICE_NAME)).decode('utf-8'))

        except subprocess.CalledProcessError as e:
            print("Command {} failed with the following output:\n{}".format(e.cmd, e.output.decode('utf-8')))
        




    

import subprocess
subprocess.check_output

