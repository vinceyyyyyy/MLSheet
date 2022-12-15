if(test-path "C:\ProgramData\chocolatey\choco.exe"){
    $testchoco = powershell choco -v
    Write-Output "Chocolatey Version $testchoco is already installed"
}
else{
    Write-Output "Seems Chocolatey is not installed, installing now"
    Set-ExecutionPolicy Bypass -Scope Process -Force
    iwr https://chocolatey.org/install.ps1 -UseBasicParsing | iex
}

choco install -y awscli awssamcli docker-desktop