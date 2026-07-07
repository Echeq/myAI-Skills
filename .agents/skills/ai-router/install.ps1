$root = Resolve-Path "$PSScriptRoot\..\..\.."

$config = @{
  '$schema' = "https://opencode.ai/config.json"
  skills = @{
    paths = @(".agents/skills")
  }
}

$jsonPath = Join-Path $root "opencode.json"
$config | ConvertTo-Json -Depth 10 | Set-Content -Path $jsonPath -Encoding UTF8
Write-Host "Created $jsonPath"
Write-Host "ai-router installed. Restart opencode, then run @ai-router --init to set up sub-agents interactively."
