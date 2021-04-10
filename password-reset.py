#!/usr/bin/env python3

# Python script to install and configure OpenSSH server on Windows

import subprocess
import argparse
import getpass
import time
import sys
import os


parser = argparse.ArgumentParser(description='Python script to reset '
                                             'domain users password')


def check_domain() -> bool:
    domain_check = powershell(['(Get-WmiObject -Class Win32_ComputerSystem).'
                               'PartOfDomain'])
    if domain_check == "True":
        return True
    else:
        return False


def check_user_group() -> bool:
    group_check = powershell(['(Get-ADUser -Identity $env:USERNAME '
                              '-Properties Memberof).Memberof'])
    if "Domain Admins" in group_check:
        return True
    elif "Account Operators" in group_check:
        return True
    else:
        return False


def check_user_ad(samaccountname) -> bool:
    ad_users = powershell(['(Get-ADUser -Filter *).SamAccountName'])
    if samaccountname in ad_users:
        return True
    else:
        return False


def check_os_version():
    windows_version = powershell(['(Get-WmiObject -class Win32_OperatingSystem).Caption'])
    if 'server' in windows_version.lower():
        sys.exit(f'\nERROR: {windows_version} is not supported\n')


def escape_cmd(command):
    return command.replace('&', '^&')


def powershell(input_: list) -> str:
    """
    Returns a string when no error
    If an exception occurs the exeption is logged and None is returned
    """
    if sys.platform == 'win32':
        input_ = [escape_cmd(elem) for elem in input_]
    execute = ['powershell.exe'] + input_

    try:
        proc = subprocess.Popen(execute,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                stdin=subprocess.PIPE,
                                cwd=os.getcwd(),
                                env=os.environ)
        proc.stdin.close()
        outs, errs = proc.communicate(timeout=180)
        return outs.decode('U8')
    except Exception as e:
        print(e)
        # logging.warning(e)


def get_ad_users():
    clear_screen()
    ad_users = powershell(['(Get-ADUser -Filter *).SamAccountName'])
    print(ad_users)


# TODO: Weergave maken van lijst met AD gebruikers (tabulate module)
# TODO: Eventuele overige informatie over de gebruiker in de tabel zetten,
# TODO: bijvoorbeel groep e.d.
def list_ad_users():
    pass


def checkout_password(password, samaccountname) -> bool:
        """Password requirements based on
        https://docs.microsoft.com/en-us/windows/security/threat-protection/
        security-policy-settings/password-must-meet-complexity-requirements
        """
        password_fault = ''
        if samaccountname.lower() in password.lower() and len \
                    (samaccountname) > 3:
            password_fault = (
                'De gebruikersnaam mag niet voorkomen in het wachtwoord')
            return False

        if len(password) < 8:
            password_fault = (
                'Het wachtwoord is te kort\ngebruik minimaal 8 karakters.')
            return False

        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        alphabet_up = alphabet.upper()
        special = '~!@#$%^&*_-+=`|\\(){}[]:;"`\'<>,.?/'
        number = '1234567890'

        categories_in_password = 0
        for category in [alphabet, alphabet_up, special, number]:
            for char in category:
                if char in password:
                    categories_in_password += 1
                    break
        if categories_in_password < 3:
            password_fault = (
                'Het wachtwoord niet complex genoeg.\n'
                'Maak gebruik van tekens, letters en cijfers')
            return False

        return True


def check_rsat() -> bool:
    # Windows server
    # (Get-WindowsFeature -name rsat).installstate return Installed or Available
    # Windows 10
    # Get-WindowsCapability -Name Rsat.WSUS.Tools~~~~0.0.1.0 –online
    rsat_check = powershell(['(Get-Module -List ActiveDirectory).Name'])
    if rsat_check == "ActiveDirectory":
        return True
    else:
        return False


def install():
    clear_screen()
    print('Installing RSAT tools...')
    install_rsat_server()


def install_rsat_tools():
    clear_screen()
    powershell(['Add-WindowsCapability -Online -Name '
                    'Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0'])
    print('- RSAT Tools installed')


def remove_rsat_tools():
    clear_screen()
    print("Remove RSAT Tools")
    powershell(['Remove-WindowsCapability -Online -Name '
                    'Rsat.ActiveDirectory.DS-LDS.Tools~~~~0.0.1.0'])
    print('- RSAT Tools removed')


def system_checks():
    domain = check_domain()
    rsat = check_rsat()
    group = check_user_group()
    if not domain:
        # print('Computer not part of a domain')
        sys.exit('\nERROR: Computer not part of a domain\n')
    elif not rsat:
        # print('RSAT tools')
        sys.exit('\nERROR: RSAT Tools are not installed\n')
    elif not group:
        # print('You have insufficient rights to change usser passwords')
        sys.exit('\nERROR: You have insufficient rights to change '
                 'user passwords\n')


def reset_password():
    while True:
        print("\nEnter SamAccountName (q to quit)\n")
        username = input("Enter username: ")
        if username == "":
            clear_screen()
            print("\nUsername can't be empty\n")
        elif username == "q":
            clear_screen()
            sys.exit('\nProgram stopped by the user\n')
        elif not check_user_ad(username):
            clear_screen()
            print("\nThe user does not exist in the active directory\n")
        else:
            break

    while True:
        print("\nEnter Password (q to quit)\n")
        password = getpass.getpass("Enter password: ")
        if password == "":
            clear_screen()
            print("\nPassword can't be empty\n")
        elif password == "q":
            clear_screen()
            sys.exit('\nProgram stopped by the user\n')
        elif not checkout_password(password, username):
            clear_screen()
            print("\nPassword does not meet password requirements\n")
        else:
            break

    powershell([f'set-adaccountpassword -identity {username} -Reset '
                f'-NewPAssword (convertto-securestring '
                f'-asplaintext "{password}" -force)'])

    print(f"Password of {username} changed to {password}")


def clear_screen():
    powershell(["clear"])


clear_screen()

# Optional arguments
parser.add_argument("--reset", help="Reset user password",
                    action="store_true")
parser.add_argument("--install", help="Install RSAT tools (Admin rights needed)",
                    action="store_true")
parser.add_argument("--getusers", help="list Active Directory Users)",
                    action="store_true")

# Pre-checks
check_os_version()
system_checks()

args = parser.parse_args()

if args.reset:
    reset_password()
elif args.install:
    install()
elif args.getusers:
    get_ad_users()
else:
    parser.print_help()