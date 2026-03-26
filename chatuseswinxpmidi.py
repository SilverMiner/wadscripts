YOURZIPWITHMIDI = 'Lost Soul.zip'
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
                print("Архив пуст")
                return None
    except Exception as e:
        print(f"Ошибка при чтении архива: {e}")
        return None
    
def encode_and_split(filename, chunk_size=195):
    with open(filename, 'rb') as f:
        data = f.read()
    
    encoded = base64.b85encode(data).decode('ascii')
    file_inside_zip = get_zip_filename(filename)
    
    # Полная команда
    #full_cmd = f"py -c \"import base64, zipfile, io; z=base64.b85decode('{encoded}'); zipfile.ZipFile(io.BytesIO(z)).extract('Lost Soul.mid')\""
    full_cmd = f"py -c \"import base64, zipfile, io; z=base64.b85decode('{encoded}'); zipfile.ZipFile(io.BytesIO(z)).extract('{file_inside_zip}')\""
    print(f"=== Файл: {filename} ===")
    print(f"length of base85: {len(encoded)} символов")
    print(f"length of command: {len(full_cmd)} символов")
    print(f"count of parts: {(len(full_cmd) + chunk_size - 1) // chunk_size}")
    print("\n=== INPUT SEQUENTIALLY ===\n")
    print("!combo win+r !send cmd\n")
    
    for i, start in enumerate(range(0, len(full_cmd), chunk_size)):
        chunk = full_cmd[start:start + chunk_size]
        print(f"!say {chunk}")

    print(f'!combo !key enter !send mplay32 /play "{file_inside_zip}"\n')
encode_and_split(YOURZIPWITHMIDI)

