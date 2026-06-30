param(
    [string]$To,
    [string]$Subject,
    [string]$Body
)

$From       = "YOUR_EMAIL@gmail.com"
$Pass       = "YOUR_GMAIL_APP_PASSWORD"
$SmtpServer = "smtp.gmail.com"        
$Port       = 587

$Cred = New-Object System.Management.Automation.PSCredential(
    $From,
    (ConvertTo-SecureString $Pass -AsPlainText -Force)
)

Send-MailMessage `
    -To $To `
    -From $From `
    -Subject $Subject `
    -Body $Body `
    -SmtpServer $SmtpServer `
    -Port $Port `
    -UseSsl `
    -Credential $Cred
