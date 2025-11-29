import sys

def encode(data):
    """RLE компрессия PackBits на чистом Python."""
    out = bytearray()
    if isinstance(data, bytes):
        data = bytearray(data)
    elif not isinstance(data, bytearray):
        # Если пришел memoryview или array
        data = bytearray(data)
        
    src_len = len(data)
    i = 0
    while i < src_len:
        # Ищем серию повторяющихся байт
        run_start = i
        while i < src_len - 1 and data[i] == data[i+1] and (i - run_start) < 127:
            i += 1
        
        if i > run_start: # Найдена серия повторов
            # Пишем флаг повтора (от -1 до -127) и сам байт
            count = i - run_start + 1
            out.append(257 - count) # эквивалент (256 - (count - 1)) для unsigned byte
            out.append(data[run_start])
            i += 1
            continue
            
        # Ищем серию НЕ повторяющихся байт (литералов)
        literal_start = i
        while i < src_len:
            # Останавливаемся, если нашли повтор или достигли лимита 128 байт
            if i < src_len - 1 and data[i] == data[i+1]:
                break
            if (i - literal_start) >= 127:
                break
            i += 1
            
        # Пишем серию литералов
        count = i - literal_start
        if count > 0:
            out.append(count - 1)
            out.extend(data[literal_start:i])
            
    return bytes(out)

def decode(data):
    """Декомпрессия PackBits на чистом Python."""
    out = bytearray()
    i = 0
    data_len = len(data)
    while i < data_len:
        header = data[i]
        i += 1
        if header < 128: # Литеральные данные
            count = header + 1
            out.extend(data[i:i+count])
            i += count
        elif header > 128: # Повторяющиеся данные
            count = 257 - header
            byte = data[i]
            i += 1
            out.extend([byte] * count)
        # header 128 (0x80) - это NOP (пустая операция), пропускаем
    return bytes(out)