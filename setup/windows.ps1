param([switch]$Elevated)
function Test-Admin
{
    $currentUser = New-Object Security.Principal.WindowsPrincipal $([Security.Principal.WindowsIdentity]::GetCurrent() )
    $currentUser.IsInRole([Security.Principal.WindowsBuiltinRole]::Administrator)
}
if ((Test-Admin) -eq $false)
{
    if ($elevated)
    {
        # tried to elevate, did not work, aborting
    }
    else
    {
        Start-Process powershell.exe -Verb RunAs -ArgumentList ('-noprofile -noexit -file "{0}" -elevated' -f ($myinvocation.MyCommand.Definition))
    }
    exit
}
Write-Output "running with full privileges"


if (test-path "C:\ProgramData\chocolatey\choco.exe")
{
    $testchoco = powershell choco -v
    Write-Output "Chocolatey Version $testchoco is already installed"
}
else
{
    Write-Output "Chocolatey is not installed, installing now"
    Set-ExecutionPolicy Bypass -Scope Process -Force
    Invoke-WebRequest https://chocolatey.org/install.ps1 -UseBasicParsing | Invoke-Expression
}


$ProgramList = @{ "awscli" = "aws"; "awssamcli" = "sam"; "docker-desktop" = "docker" }
ForEach ($Program in $ProgramList.GetEnumerator())
{
    $ProgramName = $Program.Key
    $ProgramCommand = $Program.Value + " --version"
    try
    {
        Invoke-Expression $ProgramCommand | Out-Null
        Write-Output "$ProgramName already installed. Skipping..."
    }
    catch
    {
        Write-Output "Installing $ProgramName"
        choco install ProgramName -y
        Write-Output "$ProgramName installed"
    }
}
Write-Output "AWS CLI, AWS SAM and Docker Desktop are installed."