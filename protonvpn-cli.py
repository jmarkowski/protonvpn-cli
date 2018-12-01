#!/usr/bin/env python
import argparse
import os
import shlex
import subprocess
import sys


version = '1.1.2'


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def exec_shell_fn(fn):
    sh_script = 'protonvpn-lib.sh'
    command = shlex.split("sh -c 'source {} && {}'".format(sh_script, fn))

    env = os.environ.copy()
    env['PATH'] = env['PATH'] + ':.:/usr/local/lib'

    proc = subprocess.Popen(command,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            env=env)
    (stdout, stderr) = proc.communicate()

    if stdout:
        stdout = stdout.decode('utf-8')
        print(stdout, end='')

    if stderr:
        stderr = stderr.decode('utf-8')
        eprint(stderr, end='')
        return 1

    return 0


def parse_arguments():
    desc = '\nProtonVPN Command-Line Tool v{}\n' \
           'Copyright (c) 2013-2018 Proton Technologies A.G. (Switzerland)\n' \
           'Distributed under the MIT software license ' \
           '(see the accompanying file license.md).\n\n' \
           .format(version)

    parser = argparse.ArgumentParser(
        description=desc,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument('pos_args', nargs='*', help=argparse.SUPPRESS)

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-v', '--v', '-version', '--version',
                       dest='version', action='store_true',
                       help='Display version.')

    group.add_argument('-d', '--d', '-disconnect', '--disconnect',
                       dest='disconnect', action='store_true',
                       help='Disconnect the current session.')

    group.add_argument('-reconnect', '--reconnect',
                       dest='reconnect', action='store_true',
                       help='Reconnect to the current ProtonVPN server.')

    group.add_argument('-r', '--r', '-random', '--random',
                       '-random-connet', '--random-connect',
                       dest='random', action='store_true',
                       help='Connect to a random ProtonVPN server.')

    group.add_argument('-l', '--l', '-last-connect', '--last-connect',
                       dest='last_connect', action='store_true',
                       help='Connect to the previously used ProtonVPN server.')

    group.add_argument('-f', '--f', '-fastest', '--fastest',
                       '-fastest-connect', '--fastest-connect',
                       dest='fastest_connect', action='store_true',
                       help='Connect to the fastest available ProtonVPN server.')

    group.add_argument('-p2p', '--p2p', '-p2p-connect', '--p2p-connect',
                       dest='p2p_connect', action='store_true',
                       help='Connect to the fastest available P2P ProtonVPN server.')

    group.add_argument('-tor', '--tor', '-tor-connect', '--tor-connect',
                       dest='tor_connect', action='store_true',
                       help='Connect to the fastest available ProtonVPN TOR server.')

    group.add_argument('-sc', '--sc', '-secure-core-connect',
                       '--secure-core-connect',
                       dest='secure_core_connect', action='store_true',
                       help='Connect to the fastest available ProtonVPN SecureCore server.')

    group.add_argument('-cc [country-name] [protocol]',
                       '--cc [country-name] [protocol]',
                       '-country-connect [country-name] [protocol]',
                       '--country-connect [country-name] [protocol]',
                       dest='country_connect', action='store_true',
                       help='Select and connect to a ProtonVPN server by country.')

    group.add_argument('-c [server-name] [protocol]',
                       '--c [server-name] [protocol]',
                       '-connect [server-name] [protocol]',
                       '--connect [server-name] [protocol]',
                       dest='connect', action='store_true',
                       help='Select and connect to a ProtonVPN server.')

    group.add_argument('-m', '--m', '-menu', '--menu',
                       dest='connect_via_menu', action='store_true',
                       help='Select and connect to a ProtonVPN server from a menu.')

    group.add_argument('-ip', '--ip',
                       dest='check_ip', action='store_true',
                       help='Print the current public IP address.')

    group.add_argument('-status', '--status',
                       dest='status', action='store_true',
                       help='Print connection status.')

    group.add_argument('-update', '--update',
                       dest='update', action='store_true',
                       help='Update protonvpn-cli.')

    group.add_argument('-init', '--init',
                       dest='init', action='store_true',
                       help='Initialize ProtonVPN profile on the machine.')

    group.add_argument('-install', '--install',
                       dest='install', action='store_true',
                       help='Install protonvpn-cli.')

    group.add_argument('-uninstall', '--uninstall',
                       dest='uninstall', action='store_true',
                       help='Uninstall protonvpn-cli.')

    return parser.parse_args()


def main():
    args = parse_arguments()

    rc = 1

    if args.version:
        rc = exec_shell_fn('show_version')
    elif args.disconnect:
        rc = exec_shell_fn('openvpn_disconnect')
    elif args.reconnect:
        rc = exec_shell_fn('reconnect_to_current_vpn')
    elif args.random:
        rc = exec_shell_fn('connect_to_random_vpn')
    elif args.last_connect:
        rc = exec_shell_fn('connect_to_previous_vpn')
    elif args.fastest_connect:
        rc = exec_shell_fn('connect_to_fastest_vpn')
    elif args.p2p_connect:
        rc = exec_shell_fn('connect_to_fastest_p2p_vpn')
    elif args.tor_connect:
        rc = exec_shell_fn('connect_to_fastest_tor_vpn')
    elif args.secure_core_connect:
        rc = exec_shell_fn('connect_to_fastest_secure_core_vpn')
    elif args.country_connect:
        if len(args.pos_args) == 0:
            rc = exec_shell_fn('connection_to_vpn_via_dialog_menu "countries"')
        elif len(args.pos_args == 2):
            rc = exec_shell_fn('connection_to_vpn_via_dialog_menu "{}" "{}" "country"' \
                         .format(args.pos_args[0], args.pos_args[1]))
            #connect_to_specific_server "$2" "$3" "country"
    elif args.connect:
        if len(args.pos_args) == 0:
            rc = exec_shell_fn('connection_to_vpn_via_dialog_menu "servers"')
        if len(args.pos_args) == 2:
            rc = exec_shell_fn('connect_to_specific_server "{}" "{}" "server"' \
                         .format(args.pos_args[0], args.pos_args[1]))
    elif args.connect_via_menu:
        rc = exec_shell_fn('connection_to_vpn_via_general_dialog_menu')
    elif args.check_ip:
        rc = exec_shell_fn('check_ip')
    elif args.status:
        rc = exec_shell_fn('print_console_status')
    elif args.update:
        rc = exec_shell_fn('update_cli')
    elif args.init:
        rc = exec_shell_fn('init_cli')
    elif args.install:
        rc = exec_shell_fn('install_cli')
    elif args.uninstall:
        rc = exec_shell_fn('uninstall_cli')

    return rc

if __name__ == '__main__':
    sys.exit(main())
