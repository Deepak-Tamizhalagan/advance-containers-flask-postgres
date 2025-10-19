param(
  [string]$BaseUrl = "http://localhost:8000"
)

Write-Host "== Health =="
Invoke-RestMethod -Uri "$BaseUrl/" -Method Get | Format-Table

Write-Host "`n== Create user (id=101) =="
$body = @{ id = 101; first_name = "Demo"; last_name = "User" } | ConvertTo-Json
Invoke-RestMethod -Uri "$BaseUrl/user" -Method Post -ContentType 'application/json' -Body $body | Format-List

Write-Host "`n== Get user (id=101) =="
Invoke-RestMethod -Uri "$BaseUrl/user/101" -Method Get | Format-List
