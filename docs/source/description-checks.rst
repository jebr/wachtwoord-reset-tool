Programma controles
===================

Tijdens het programma worden de volgende controles uitgevoerd.
Wanneer er gebruik wordt gemaakt van Powershell om gegevens op te halen zal
deze syntax bij het onderdeel worden vermeld.

Controles bij het opstarten van het programma
---------------------------------------------

1. **Controle op Windows server of Windows 10**

.. code-block:: powershell

   (Get-WmiObject -class Win32_OperatingSystem).Caption

2. **Controle of de computer onderdeel is van een domein**

.. code-block:: powershell

   (Get-WmiObject -Class Win32_ComputerSystem).PartOfDomain

3. **Controleer of Windows Remote Server Administration Tools (RSAT) is
geïnstalleerd op de Pc**

.. code-block:: powershell

   (Get-Module -List ActiveDirectory).Name

4. **Controleer of de huidige gebruiker lid is van de groep Domain Admins of
Account Operators**

.. code-block:: powershell

   (Get-ADUser -Identity $env:USERNAME -Properties Memberof).Memberof

Controles bij het aanpassen van het wachtwoord
----------------------------------------------

1. **Controleer of de ingevoerde gebruiker voorkomt in de Active Directory**

.. code-block:: powershell

   (Get-ADUser -Filter *).SamAccountName

2. **Controleer of het ingevoerde wachtwoord voldoet aan de ingestelde criteria**

.. code-block:: python

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

