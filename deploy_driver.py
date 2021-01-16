import argparse
import subprocess
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
    
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_SERVER_PORT,
                        help="Listening port on the target computer")

    parser.add_argument('--release', action="store_const", const="release", default="debug",
                        help="Use the Release version of the driver instead of the debug")

    return parser.parse_args(args)

def install_driver_on_input(connection, driver_name, bin_path):
    input("Trying to install using SC. Press Enter to start the driver")
    print(connection.modules.subprocess.check_output(
        "sc create {} type= kernel binPath= {}".format(driver_name, bin_path)).decode('utf-8'))
    print("Driver installed")

def start_driver_on_input(connection, driver_name):
    input("Ready to start. Press Enter to start the driver")
    print(connection.modules.subprocess.check_output(
            "sc start {}".format(driver_name)).decode('utf-8'))

def stop_driver_on_input(connection, driver_name):
    input("Stopping using SC. Press Enter to stop the driver")
    print(connection.modules.subprocess.check_output(
        "sc stop {}".format(driver_name)).decode('utf-8'))


def uninstall_driver_on_input(connection, driver_name):
    input("Ready to uninstall. Press Enter to uninstall the driver and delete the service")
    print(connection.modules.subprocess.check_output(
        "sc delete {}".format(driver_name)).decode('utf-8'))

if __name__ == "__main__":
    args = parse_arguments()

    dest_driver_path = path.join(DRIVER_DEST_DIR, DRIVER_FILE_TO_UPLOAD)

    connection = rpyc.classic.connect(args.host)
    driver_file = path.join(PROJECT_DIR, 'Sample', 'x64', args.release, DRIVER_FILE_TO_UPLOAD)
    rpyc.utils.classic.upload(connection, driver_file, dest_driver_path)
    print("Upload {} to {}".format(DRIVER_FILE_TO_UPLOAD, dest_driver_path))

    
    command = input("What should we do? ")
    while command.lower() not in ['q', 'quit', 'exit']:
        try:
            if command.lower() in ['i', 'install']:
                install_driver_on_input(connection, KERNEL_SERVICE_NAME, dest_driver_path)
            elif command.lower() in ['start', 's']:
                start_driver_on_input(connection, KERNEL_SERVICE_NAME)
            elif command.lower() == 'stop':
                stop_driver_on_input(connection, KERNEL_SERVICE_NAME)
            elif command.lower() in ['u', 'uninstall']:
                uninstall_driver_on_input(connection, KERNEL_SERVICE_NAME)
            else:
                print("unknown command")
        
        except subprocess.CalledProcessError as e:
            print("Command {} failed with the following output:\n{}".format(e.cmd, e.output.decode('utf-8')))

        command = input("What do you want to do now? ")
    
    print("Exiting")




