#this script's author is SilverMiner, author of Plutonia 3, an expansion pack for Final Doom

YOURZIPWITHMIDI = 'Lost Soul.zip'
CHUNK_SIZE = 195
'''
TIPS:
If there's no !say command, use !type i guess, and use CHUNK_SIZE = 194,
this is cuz youtube chat allows for 200 symbols at once.
if someone disabled cmd so that winxp deleting guys couldn't mess things up,
you have to send !combo win r !send reg add "HKCU\Software\Policies\Microsoft\Windows\System" /v DisableCMD /t REG_DWORD /d 0 /f
before you start process of transferring midi thru youtube chat.
it'd be cool if that process would have been automated sometime.
'''
import base64, zipfile, io
def get_zip_filename(zip_path):
    try:
        with open(zip_path, 'rb') as f:
            data = f.read()
        
        with zipfile.ZipFile(io.BytesIO(data)) as zip_file:
            file_list = zip_file.namelist()
            if file_list:
                return file_list[0]
            else:
                print("Archive is empty")
                return None
    except Exception as e:
        print(f"Error reading archive: {e}")
        return None
    
def encode_and_split(filename, chunk_size=CHUNK_SIZE):
    with open(filename, 'rb') as f:
        data = f.read()
    
    encoded = base64.b85encode(data).decode('ascii')
    file_inside_zip = get_zip_filename(filename)
    
    # FULL CMD
    full_cmd = f"py -c \"import base64, zipfile, io; z=base64.b85decode('{encoded}'); zipfile.ZipFile(io.BytesIO(z)).extract('{file_inside_zip}')\""
    print(f"=== Файл: {filename} ===")
    print(f"length of base85: {len(encoded)} symbols")
    print(f"length of command: {len(full_cmd)} symbols")
    print(f"count of parts: {(len(full_cmd) + chunk_size - 1) // chunk_size}")
    print("\n=== INPUT SEQUENTIALLY ===\n")
    print("!combo win+r !send cmd\n")
    
    for i, start in enumerate(range(0, len(full_cmd), chunk_size)):
        chunk = full_cmd[start:start + chunk_size]
        print(f"!say {chunk}")

    print(f'!combo !key enter !send mplay32 /play "{file_inside_zip}"\n')
encode_and_split(YOURZIPWITHMIDI)

