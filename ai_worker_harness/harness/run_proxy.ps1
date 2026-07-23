# Get-Content .env | ForEach-Object {
#     if ($_ -match '^\s*([^#][^=]*)=(.*)$') {
#         [System.Environment]::SetEnvironmentVariable($Matches[1].Trim(), $Matches[2].Trim())
#     }
# }

# $env:PYTHONUTF8 = "1"

# litellm --config harness/litellm_config.yaml --port 4000

Get-Content .env | ForEach-Object {
    if ($_ -match '^([^#=]+)=(.*)$') {
        $name = $Matches[1].Trim()
        $value = $Matches[2].Trim()
        [System.Environment]::SetEnvironmentVariable($name, $value)
    }
}

litellm --config harness/litellm_config.yaml --port 4000