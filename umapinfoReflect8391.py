from sys import argv
from dataclasses import dataclass, fields, field
from typing import Optional, List, Tuple
import copy

@dataclass
class ourbase_t:
    index: int = 0
    name: str = ""
    
    def __getitem__(self, index):
        return getattr(self, fields(self)[index].name)

    def __setitem__(self, index, value):
        field_name = fields(self)[index].name
        setattr(self, field_name, value)
        
    def __len__(self):
        return len(fields(self))

@dataclass
class guga2_t(ourbase_t):
    a: str = ""
    b: str = ""
    c: str = ""

@dataclass
class level_t(ourbase_t):
    levelname: str = ""
    author: str = ""
    label: str = ""
    levelpic: str = ""
    next: str = ""
    nextsecret: str = ""
    skytexture: str = ""
    music: str = ""
    exitpic: str = ""
    enterpic: str = ""
    partime: int = 0
    endgame: Optional[bool] = None
    endpic: str = ""
    endbunny: bool = False
    endcast: bool = False
    nointermission: Optional[bool] = None
    intertext: str = ""
    intertextsecret: str = ""
    interbackdrop: str = ""
    intermusic: str = ""
    episode: List[Tuple[str, str, str]] = field(default_factory=list)
    bossaction: List[Tuple[str, str, int]] = field(default_factory=list)

    _parsed_fields: set = field(default_factory=set, init=False, compare=False, repr=False)

    def set_field_value(self, field_name, value):
        """Устанавливает значение поля и отмечает его как измененное"""
        setattr(self, field_name, value)
        self._parsed_fields.add(field_name)

def parse_levels_robust(filename):
    """Парсер для блоков MAP с поддержкой многострочных значений"""
    level_dict = {}
    
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    #print(f"//Всего строк в файле: {len(lines)}")
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Ищем начало блока MAP
        if line.upper().startswith('MAP '):
            # Получаем название карты
            parts = line.split()
            if len(parts) >= 2:
                map_name = parts[1].strip('{').strip()
            else:
                map_name = ""
            
            #print(f"Начало блока MAP: {map_name}")
            
            # Создаем объект уровня
            level = level_t(index=len(level_dict), name=map_name)
            
            # Начинаем читать поля со следующей строки
            i += 1
            
            # Флаг для обработки многострочного значения
            multiline_value = False
            current_field = ""
            accumulated_lines = []
            
            while i < len(lines):
                current_line = lines[i].rstrip('\n')
                stripped_line = current_line.strip()
                
                # Проверяем, не конец ли это блока
                if '}' in stripped_line and not multiline_value:
                    # Если это простая строка с } (не внутри многострочного значения)
                    #print(f"Конец блока {map_name}")
                    i += 1
                    break
                
                # Если мы в процессе сбора многострочного значения
                if multiline_value:
                    # Проверяем, заканчивается ли значение на этой строке
                    if stripped_line.endswith('"'):
                        # Закрывающая кавычка - конец значения
                        # Убираем последнюю кавычку
                        line_without_end_quote = current_line.rstrip('"')
                        accumulated_lines.append(line_without_end_quote)
                        full_value = '\n'.join(accumulated_lines)
                        
                        # Устанавливаем значение поля
                        if hasattr(level, current_field):
                            level.set_field_value(current_field, full_value)
                        
                        # Сбрасываем флаги
                        multiline_value = False
                        current_field = ""
                        accumulated_lines = []
                    else:
                        # Продолжение многострочного значения
                        accumulated_lines.append(current_line)
                else:
                    # Обычная строка (не многострочное значение)
                    if stripped_line and not stripped_line.startswith('//'):
                        # Проверяем, есть ли присваивание
                        if '=' in stripped_line:
                            # Разделяем на ключ и значение
                            key_part, value_part = stripped_line.split('=', 1)
                            key = key_part.strip().lower()
                            value = value_part.strip()
                            
                            # Проверяем, начинается ли значение с кавычки
                            if value.startswith('"') and key != 'episode' and key != 'bossaction':
                                # Если значение заканчивается кавычкой в той же строке
                                if value.endswith('"') and not value.endswith('",'):
                                    # Простое строковое значение
                                    value = value[1:-1]
                                    if hasattr(level, key):
                                        level.set_field_value(key, value)
                                else:
                                    # Начинается многострочное значение
                                    multiline_value = True
                                    current_field = key
                                    # Убираем начальную кавычку
                                    accumulated_lines.append(value[1:])
                            else:
                                # Нестроковое значение
                                # Обработка числовых значений
                                if key == 'partime':
                                    try:
                                        value = int(value)
                                        level.set_field_value(key, value)
                                    except ValueError:
                                        print(f"//Неверное значение partime: {value}")
                                # Обработка списка episode (БОЛЕЕ ТОЧНАЯ ВЕРСИЯ)
                                elif key == 'episode':
                                    try:
                                        # Формат: episode = "M_EPI1", "Pick Your Eggnog", "P"
                                        cleaned_value = value.strip()
                                        
                                        # Разделяем строку с учетом кавычек
                                        parts = []
                                        current_part = ""
                                        in_quotes = False
                                        escape_next = False
                                        
                                        # ИЗМЕНЕНИЕ: используем другую переменную для индекса
                                        for char_index, char in enumerate(cleaned_value):
                                            if escape_next:
                                                current_part += char
                                                escape_next = False
                                            elif char == '\\':
                                                escape_next = True
                                            elif char == '"':
                                                in_quotes = not in_quotes
                                                current_part += char
                                            elif char == ',' and not in_quotes:
                                                parts.append(current_part.strip())
                                                current_part = ""
                                            else:
                                                current_part += char
                                        
                                        # Добавляем последнюю часть
                                        if current_part:
                                            parts.append(current_part.strip())
                                        
                                        # Убираем внешние кавычки из каждой части
                                        cleaned_parts = []
                                        for part in parts:
                                            if part.startswith('"') and part.endswith('"'):
                                                part = part[1:-1]
                                            cleaned_parts.append(part)
                                        
                                        # Должно быть 3 части
                                        if len(cleaned_parts) >= 3:
                                            episode_tuple = (cleaned_parts[0], cleaned_parts[1], cleaned_parts[2])
                                            level.set_field_value('episode', [episode_tuple])
                                            #print(episode_tuple) #14:05 04.01.2026 was for debug
                                        else:
                                            print(f"//Предупреждение: episode содержит {len(cleaned_parts)} частей вместо 3: {cleaned_parts}")
                                            
                                    except Exception as e:
                                        print(f"//Ошибка обработки episode: {e}, значение: {value}")
                                # Обработка списка bossaction
                                elif key == 'bossaction':
                                    try:
                                        # Формат: bossaction = thingtype, linespecial, tag
                                        cleaned_value = value.strip()
                                        
                                        # Разделяем на три части
                                        parts = []
                                        in_quotes = False
                                        current_part = ""
                                        
                                        for char in cleaned_value:
                                            if char == '"':
                                                in_quotes = not in_quotes
                                            elif char == ',' and not in_quotes:
                                                parts.append(current_part.strip())
                                                current_part = ""
                                            else:
                                                current_part += char
                                        
                                        if current_part:
                                            parts.append(current_part.strip())
                                        
                                        # Убираем кавычки из строковых частей
                                        parts = [p.strip('"') if '"' in p else p.strip() for p in parts]
                                        
                                        if len(parts) >= 3:
                                            try:
                                                tag = int(parts[2])
                                                level.set_field_value('bossaction', level.bossaction + [(parts[0], parts[1], tag)])
                                            except ValueError:
                                                print(f"//Неверный tag в bossaction: {parts[2]}")
                                    except Exception as e:
                                        print(f"//Ошибка обработки bossaction: {e}, значение: {value}")
                                # Обработка логических полей
                                elif key in ['endbunny', 'endcast', 'endgame', 'nointermission']:
                                    if value.lower() == 'true':
                                        level.set_field_value(key, True)
                                    elif value.lower() == 'false':
                                        level.set_field_value(key, False)
                                    else:
                                        level.set_field_value(key, None)
                                # Обработка других полей
                                elif hasattr(level, key):
                                    level.set_field_value(key, value)
                
                i += 1
                
                # Защита от бесконечного цикла
                if i > len(lines):
                    print("//Превышен лимит строк. Возможно, ошибка в формате файла.")
                    break
            
            # Добавляем уровень в словарь
            level_dict[map_name] = level
        else:
            i += 1
    
    #print(f"//Найдено блоков: {len(level_dict)}")
    return level_dict

def parse_file_robust(filename):
    """Более надежный парсер для произвольных блоков"""
    level_dict = parse_levels_robust(filename)
    
    if level_dict:
        return level_dict
    
    return {}

def main():
    if len(argv) < 2:
        print("Использование: python umapinfoReflect26.py <имя_файла>")
        return
    
    filename = argv[1]
    
    try:
        level_dict = parse_file_robust(filename)
        
        # Выводим результат
        if level_dict:
            #print(f"\nНайдено уровней: {len(level_dict)}")
            for map_name, level in level_dict.items():
                print(f"\nmap {map_name}")
                print("{")
                
                # Выводим только те поля, которые были найдены при парсинге
                excluded_fields = {'index', 'name', '_parsed_fields'}
                
                # Получаем все поля dataclass
                for field_info in fields(level_t):
                    field_name = field_info.name
                    
                    if field_name in excluded_fields:
                        continue
                        
                    value = getattr(level, field_name)
                    
                    # Пропускаем пустые значения
                    if value is None or value == "" or value == []:
                        continue
                    
                    # Обработка episode (список кортежей)

                    # Обработка episode (список кортежей)
                    # Обработка episode (список кортежей)
                    if field_name == 'episode' and value:
                        if isinstance(value, list):
                            for episode_item in value:
                                if isinstance(episode_item, (list, tuple)) and len(episode_item) >= 3:
                                    print(f'    episode = "{episode_item[0]}", "{episode_item[1]}", "{episode_item[2]}"')
                                else:
                                    print(f'    # Ошибка: некорректный формат episode: {episode_item}')
                        else:
                            # Если по какой-то причине это не список, попробуем вывести как есть
                            print(f'    episode = {value}')
                    # Обработка bossaction (список кортежей)
                    elif field_name == 'bossaction' and value:
                        for action in value:
                            if isinstance(action, (list, tuple)) and len(action) >= 3:
                                print(f'    bossaction = "{action[0]}", "{action[1]}", {action[2]}')
                    # Числовые значения
                    elif isinstance(value, int):
                        print(f'    {field_name} = {value}')
                    # Логические значения
                    elif isinstance(value, bool):
                        print(f'    {field_name} = {str(value).lower()}')
                    # Опциональные логические значения
                    elif field_name in ['endgame', 'nointermission'] and value is not None:
                        print(f'    {field_name} = {str(value).lower()}')
                    # Строковые значения
                    elif isinstance(value, str):
                        # Для intertext выводим как многострочное значение
                        if field_name == 'intertext' and '\n' in value:
                            print(f'    {field_name} = "{value}"')
                        else:
                            print(f'    {field_name} = "{value}"')
                
                print("}")
        else:
            print("Блоки map не найдены в файле")
            
    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден")
    except Exception as e:
        print(f"Ошибка при обработке файла: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
