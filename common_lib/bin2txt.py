import os
file_list = [x for x in os.listdir('./')  if 'processed' not in x and x.endswith('bin')]

for filename in file_list:
    # 1. 读取 dump 出来的二进制文件

    with open(filename, 'rb') as f:
        data = f.read()

    # 2. 按 1024 bit (128 byte) 分组处理
    chunk_size = 128  # 1024 bit = 128 byte
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

    # 3. 对每个块进行字节反转
    reversed_chunks = [chunk[::-1] for chunk in chunks]

     # 4. 将处理后的数据保存到新文件，并在每个块后加上换行符
    new_filename = filename.replace('.bin', '_processed.bin')
    with open(new_filename, 'w') as f:
        for chunk in reversed_chunks:
            chunk_str = ''.join(f'{byte:02x}' for byte in chunk)
            f.write(f'{chunk_str}\n')  # 每个 128 字节/1024bit的块后加一个换行符

            