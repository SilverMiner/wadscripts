import lzma
import os
import glob
import io
import time
from pathlib import Path
from collections import defaultdict

def analyze_compression_stats(input_file, dict_size_kb=64, nice_len=273):
    """
    Анализирует сжатие MIDI файла без сохранения результата
    Возвращает статистику сжатия
    """
    
    # Настройка фильтра LZMA2 для максимального сжатия
    filters = [{
        "id": lzma.FILTER_LZMA2,
        "dict_size": dict_size_kb * 1024,  # 64 КБ
        "lc": 3,
        "lp": 0,
        "pb": 2,
        "mode": lzma.MODE_NORMAL,
        "nice_len": nice_len,
        "mf": lzma.MF_BT4,
        "depth": 0,
    }]
    
    try:
        # Читаем исходный файл
        with open(input_file, 'rb') as f_in:
            data = f_in.read()
        
        original_size = len(data)
        
        # Измеряем время сжатия
        start_time = time.time()
        
        # Сжимаем данные в память (без записи на диск)
        compressed_data = lzma.compress(
            data, 
            format=lzma.FORMAT_XZ,
            filters=filters
        )
        
        compression_time = time.time() - start_time
        
        compressed_size = len(compressed_data)
        ratio = compressed_size / original_size * 100
        compression_ratio = original_size / compressed_size
        savings = original_size - compressed_size
        
        return {
            'filename': input_file,
            'original_size': original_size,
            'compressed_size': compressed_size,
            'compression_ratio': compression_ratio,
            'compression_percent': ratio,
            'savings': savings,
            'savings_percent': (savings / original_size) * 100,
            'compression_time': compression_time,
            'speed_mbps': (original_size / 1024 / 1024) / compression_time if compression_time > 0 else 0
        }
        
    except Exception as e:
        print(f"✗ Ошибка при анализе {input_file}: {e}")
        return None


def analyze_all_midi_files(dict_size_kb=64, nice_len=273, show_details=True):
    """
    Анализирует все MIDI файлы и выводит статистику без сохранения
    """
    
    # Поиск всех MIDI файлов
    #midi_patterns = ['*.mid', '*.midi', '*.MID', '*.MIDI']
    midi_patterns = ['*.mid']
    midi_files = []
    
    for pattern in midi_patterns:
        midi_files.extend(glob.glob(pattern))
    
    if not midi_files:
        print("MIDI файлы не найдены в текущей папке.")
        print("Поддерживаемые расширения: .mid, .midi")
        return
    
    print("=" * 80)
    print("АНАЛИЗ СЖАТИЯ MIDI ФАЙЛОВ (без сохранения результатов)")
    print(f"Параметры: dict_size={dict_size_kb}KB, nice_len={nice_len}, mf=MF_BT4, mode=NORMAL")
    print("=" * 80)
    print(f"Найдено MIDI файлов: {len(midi_files)}")
    print()
    
    results = []
    total_original = 0
    total_compressed = 0
    total_time = 0
    
    for i, midi_file in enumerate(sorted(midi_files), 1):
        print(f"[{i}/{len(midi_files)}] Анализ: {midi_file}")
        
        stats = analyze_compression_stats(midi_file, dict_size_kb, nice_len)
        
        if stats:
            results.append(stats)
            total_original += stats['original_size']
            total_compressed += stats['compressed_size']
            total_time += stats['compression_time']
            
            if show_details:
                print(f"  Исходный: {stats['original_size']:>10,} байт")
                print(f"  Сжатый:   {stats['compressed_size']:>10,} байт")
                print(f"  Экономия: {stats['savings']:>10,} байт ({stats['savings_percent']:>5.1f}%)")
                print(f"  Коэффициент: {stats['compression_ratio']:>6.2f}x")
                print(f"  Время: {stats['compression_time']:.3f} сек ({stats['speed_mbps']:.1f} MB/сек)")
                print()
        else:
            print("  [ОШИБКА] Не удалось проанализировать файл")
            print()
    
    # Итоговая статистика
    if results:
        print("=" * 80)
        print("ИТОГОВАЯ СТАТИСТИКА")
        print("=" * 80)
        
        # Основные показатели
        avg_ratio = total_original / total_compressed if total_compressed > 0 else 0
        avg_percent = (total_compressed / total_original) * 100 if total_original > 0 else 0
        
        print(f"\n📊 ОБЩИЕ ПОКАЗАТЕЛИ:")
        print(f"  Успешно проанализировано: {len(results)} из {len(midi_files)} файлов")
        print(f"  Общий исходный размер:    {total_original:>10,} байт ({total_original/1024:>8.2f} KB)")
        print(f"  Общий сжатый размер:      {total_compressed:>10,} байт ({total_compressed/1024:>8.2f} KB)")
        print(f"  Общая экономия:           {total_original - total_compressed:>10,} байт")
        print(f"  Средний коэффициент:      {avg_ratio:>6.2f}x")
        print(f"  Средняя степень сжатия:   {avg_percent:>6.1f}% от оригинала")
        print(f"  Общее время сжатия:       {total_time:.3f} сек")
        
        # Дополнительная статистика
        sizes = [r['original_size'] for r in results]
        compressed_sizes = [r['compressed_size'] for r in results]
        ratios = [r['compression_ratio'] for r in results]
        
        print(f"\n📈 ДЕТАЛЬНАЯ СТАТИСТИКА:")
        print(f"  Самый большой файл:       {max(sizes):>10,} байт ({max(sizes)/1024:.1f} KB)")
        print(f"  Самый маленький файл:     {min(sizes):>10,} байт ({min(sizes)/1024:.1f} KB)")
        print(f"  Средний размер файла:     {sum(sizes)/len(sizes):>10,.0f} байт")
        print(f"  Максимальный коэффициент: {max(ratios):>6.2f}x")
        print(f"  Минимальный коэффициент:  {min(ratios):>6.2f}x")
        
        # Распределение по размерам
        print(f"\n📁 РАСПРЕДЕЛЕНИЕ ПО РАЗМЕРАМ:")
        size_ranges = [
            (0, 1024, "0-1 KB"),
            (1024, 10240, "1-10 KB"),
            (10240, 102400, "10-100 KB"),
            (102400, 1048576, "100 KB - 1 MB"),
            (1048576, float('inf'), "> 1 MB")
        ]
        
        for min_size, max_size, label in size_ranges:
            count = sum(1 for s in sizes if min_size <= s < max_size)
            if count > 0:
                print(f"  {label:15} : {count:3} файлов ({count/len(sizes)*100:5.1f}%)")
        
        # Топ-5 лучших сжатий
        sorted_by_ratio = sorted(results, key=lambda x: x['compression_ratio'], reverse=True)[:5]
        print(f"\n🏆 ТОП-5 ЛУЧШИХ СЖАТИЙ:")
        for i, r in enumerate(sorted_by_ratio, 1):
            print(f"  {i}. {r['filename']:30} : {r['compression_ratio']:>6.2f}x ({r['compression_percent']:.1f}%)")
        
        # Топ-5 худших сжатий
        sorted_by_ratio = sorted(results, key=lambda x: x['compression_ratio'])[:5]
        print(f"\n⚠️ ТОП-5 ХУДШИХ СЖАТИЙ:")
        for i, r in enumerate(sorted_by_ratio, 1):
            print(f"  {i}. {r['filename']:30} : {r['compression_ratio']:>6.2f}x ({r['compression_percent']:.1f}%)")
    
    return results


def compare_dict_sizes(midi_file=None):
    """
    Сравнивает эффективность сжатия с разными размерами словаря
    """
    if midi_file is None:
        # Берем первый MIDI файл в папке
        midi_files = glob.glob('*.mid') + glob.glob('*.midi')
        if not midi_files:
            print("MIDI файлы не найдены")
            return
        midi_file = midi_files[0]
    
    print(f"Сравнение размеров словаря для файла: {midi_file}")
    print("=" * 70)
    
    dict_sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
    
    results = []
    for size_kb in dict_sizes:
        stats = analyze_compression_stats(midi_file, dict_size_kb=size_kb, nice_len=273)
        if stats:
            results.append(stats)
            print(f"Словарь {size_kb:4} KB: {stats['compressed_size']:>8,} байт "
                  f"({stats['compression_percent']:5.1f}%) "
                  f"коэф={stats['compression_ratio']:5.2f}x "
                  f"время={stats['compression_time']:.3f}с")
    
    # Находим оптимальный размер
    if results:
        best = min(results, key=lambda x: x['compressed_size'])
        print("\n" + "=" * 70)
        print(f"Оптимальный размер словаря: {best['filename'].split('_') if '_' in best['filename'] else ''}")
        print(f"  {best['dict_size']//1024} KB дает наименьший сжатый размер: {best['compressed_size']:,} байт")
        print(f"  Коэффициент сжатия: {best['compression_ratio']:.2f}x")


def export_statistics_to_file(results, output_file="compression_stats.txt"):
    """
    Экспортирует статистику в текстовый файл
    """
    if not results:
        print("Нет данных для экспорта")
        return
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("СТАТИСТИКА СЖАТИЯ MIDI ФАЙЛОВ\n")
        f.write("=" * 80 + "\n\n")
        
        total_original = sum(r['original_size'] for r in results)
        total_compressed = sum(r['compressed_size'] for r in results)
        
        f.write(f"Всего файлов: {len(results)}\n")
        f.write(f"Общий размер: {total_original:,} байт → {total_compressed:,} байт\n")
        f.write(f"Общая экономия: {total_original - total_compressed:,} байт\n")
        f.write(f"Средний коэффициент: {total_original/total_compressed:.2f}x\n\n")
        
        f.write("ДЕТАЛЬНАЯ СТАТИСТИКА ПО ФАЙЛАМ:\n")
        f.write("-" * 80 + "\n")
        
        for r in results:
            f.write(f"\n{r['filename']}:\n")
            f.write(f"  Исходный размер: {r['original_size']:,} байт\n")
            f.write(f"  Сжатый размер:   {r['compressed_size']:,} байт\n")
            f.write(f"  Экономия:        {r['savings']:,} байт ({r['savings_percent']:.1f}%)\n")
            f.write(f"  Коэффициент:     {r['compression_ratio']:.2f}x\n")
            f.write(f"  Время сжатия:    {r['compression_time']:.3f} сек\n")
    
    print(f"\n📄 Статистика сохранена в файл: {output_file}")


if __name__ == "__main__":
    # Основной анализ всех MIDI файлов
    results = analyze_all_midi_files(
        dict_size_kb=64,      # 64 КБ словарь
        nice_len=273,         # максимальная длина совпадений
        show_details=True     # показывать детали для каждого файла
    )
    
    # Если нужно экспортировать статистику в файл
    #if results:
    #    export_statistics_to_file(results)
    
    # Опционально: сравнить разные размеры словаря на первом файле
    # compare_dict_sizes()
