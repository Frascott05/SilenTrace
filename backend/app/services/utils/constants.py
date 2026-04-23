LOLBINS = {
    "powershell.exe",
    "cmd.exe",
    "wscript.exe",
    "cscript.exe",
    "rundll32.exe",
    "mshta.exe",
}

SUSPICIOUS_PARENTS = {
    "winword.exe",
    "excel.exe",
    "outlook.exe",
}

SUSPICIOUS_PORTS = {4444, 1337, 8080, 9001}

SUSPICIOUS_CMD_PATTERNS = [
    " -enc ",
    "encodedcommand",
    "invoke-expression",
    "downloadstring",
    "iwr ",
    "wget ",
    "curl ",
    "bitsadmin",
    "certutil",
]
