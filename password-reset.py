#!/usr/bin/env python3

# Python script to install and configure OpenSSH server on Windows

import subprocess
import argparse
import getpass
import time


parser = argparse.ArgumentParser(description='Python script to install and '
                                             'configure OpenSSH server on '
                                             'Windows')


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

    # if DEBUG:
    #     return ' '.join(execute)

    try:
        proc = subprocess.Popen(execute,
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT,
                                stdin=subprocess.PIPE,
                                cwd=os.getcwd(),
                                env=os.environ)
        proc.stdin.close()
        outs, errs = proc.communicate(timeout=15)
        return outs.decode('U8')
    except Exception as e:
        print(e)
        # logging.warning(e)


def install():
    clear_screen()
    print('Installing RSAT tools...')
    install_rsat_server()


def install_rsat_server():
    powershell(['Add-WindowsCapability -Online -Name '
                'OpenSSH.Server~~~~0.0.1.0'])
    time.sleep(120)
    print('- RSAT Tools installed')
    set_service_and_firewall()


def check_domain() -> bool:
    domain_check = powershell(['(Get-WmiObject -Class Win32_ComputerSystem).'
                               'PartOfDomain'])
    if domain_check == "True":
        return True
    else:
        return False


def check_rsat() -> bool:
    rsat_check = powershell(['(get-module -list activedirectory).name'])
    if rsat_check == "":
        return False
    else:
        return True


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
            self.password_fault = (
                'Het wachtwoord niet complex genoeg.\n'
                'Maak gebruik van tekens, letters en cijfers')
            return False

        return True


def reset_password():
    clear_screen()
    if not check_domain():
        print('Computer not part of a domain')
        exit()
    elif not check_rsat():
        print('RSAT tools')
        exit()
    elif not check_user_group():
        print('You have insufficient rights to change usser passwords')
    else:
        username = input("Enter username: ")
        password = input("Enter password: ")

        while True:
            if username == "":
                print("Enter username")
            elif check_user_ad(username):
                print("Unknown user")
            elif password == "":
                print("Enter password")
            elif not checkout_password(password, username):
                print("Password does not meet password requirements")
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

args = parser.parse_args()

if args.install:
    reset_password()
elif args.show:
    install()
else:
    parser.print_help()