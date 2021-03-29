Set-ExecutionPolicy Unrestricted

# Systeem Controles
# 1. Controleer of de computer lid is van een domein
# 2. Controleer of RSAT tools zijn geinstalleerd
# 3. Controleer of de gebruiker lid is van domain admins of system operator

$domain = (Get-WmiObject -Class Win32_ComputerSystem).PartOfDomain  # geeft True or False
$rsat_tools = wmic qfe list full | findstr KB2693643  # geeft code of None
$admin_operator = (get-aduser -Identity $env:USERNAME -properties Memberof).memberof  # dit geeft lijst met groepen

#Get-ADGroupMember -identity "GROUPNAME" -Recursive | Get-ADUser -Property DisplayName | Select Name,ObjectClass,DisplayName﻿

# Init PowerShell Gui
Add-Type -AssemblyName System.Windows.Forms
# Create a new form
$LocalPrinterForm                    = New-Object system.Windows.Forms.Form
# Define the size, title and background color
$LocalPrinterForm.ClientSize         = '500,300'
$LocalPrinterForm.text               = "Password reset tool"
$LocalPrinterForm.BackColor          = "#ffffff"



$AddPrinterBtn                   = New-Object system.Windows.Forms.Button
$AddPrinterBtn.BackColor         = "#a4ba67"
$AddPrinterBtn.text              = "Add Printer"
$AddPrinterBtn.width             = 90
$AddPrinterBtn.height            = 30
$AddPrinterBtn.location          = New-Object System.Drawing.Point(370,250)
$AddPrinterBtn.Font              = 'Microsoft Sans Serif,10'
$AddPrinterBtn.ForeColor         = "#ffffff"
$LocalPrinterForm.Controls.Add($AddPrinterBtn)

$cancelBtn                       = New-Object system.Windows.Forms.Button
$cancelBtn.BackColor             = "#ffffff"
$cancelBtn.text                  = "Cancel"
$cancelBtn.width                 = 90
$cancelBtn.height                = 30
$cancelBtn.location              = New-Object System.Drawing.Point(260,250)
$cancelBtn.Font                  = 'Microsoft Sans Serif,10'
$cancelBtn.ForeColor             = "#000"
$cancelBtn.DialogResult          = [System.Windows.Forms.DialogResult]::Cancel
$LocalPrinterForm.CancelButton   = $cancelBtn
$LocalPrinterForm.Controls.Add($cancelBtn)


# Display the form
[void]$LocalPrinterForm.ShowDialog()





