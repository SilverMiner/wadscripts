#SilverMiner Chat uses Windows XP (https://www.youtube.com/watch?v=tfZEXJj3-18) midi file playback
import base64

def encode_and_split(filename, chunk_size=195):
    with open(filename, 'rb') as f:
        data = f.read()
    
    encoded = base64.b85encode(data).decode('ascii')
    
    # Полная команда
    full_cmd = f"py -c \"import base64, zipfile, io; z=base64.b85decode('{encoded}'); zipfile.ZipFile(io.BytesIO(z)).extract('Lost Soul.mid')\""
    
    print(f"=== Файл: {filename} ===")
    print(f"Длина base85: {len(encoded)} символов")
    print(f"Длина полной команды: {len(full_cmd)} символов")
    print(f"Количество частей: {(len(full_cmd) + chunk_size - 1) // chunk_size}")
    print("\n=== ВВОДИ ПОСЛЕДОВАТЕЛЬНО ===\n")
    print("!combo win+r !send cmd\n")
    
    for i, start in enumerate(range(0, len(full_cmd), chunk_size)):
        chunk = full_cmd[start:start + chunk_size]
        print(f"!say {chunk}")
    print('!key enter')
    print('!send mplay32 /play "Lost Soul.mid"\n')

encode_and_split('Lost Soul.zip')
