#11:31 25.03.2026
import base64

def encode_file_to_b85(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    
    encoded = base64.b85encode(data).decode('ascii')
    
    print(f"Закодированный файл '{filename}':")
    print(encoded)
    print(f"\nДлина строки: {len(encoded)} символов")
    print("\nГотовая команда для извлечения:")
    print(f"py -c \"import base64, zipfile, io; z=base64.b85decode('{encoded}'); zipfile.ZipFile(io.BytesIO(z)).extract('Lost Soul.mid')\"")

# Использование:
encode_file_to_b85('lost soul.zip')
