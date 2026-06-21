def bin_to_hex_spaced(input_file, output_file, bytes_per_line=16):
    """
    将二进制文件转换为带空格分隔的十六进制文本文件
    
    :param input_file: 输入二进制文件路径
    :param output_file: 输出文本文件路径
    :param bytes_per_line: 每行显示的字节数（默认16）
    """
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # 生成带空格的十六进制字符串
    hex_bytes = [format(byte, '02X') for byte in data]
    
    # 按指定字节数分行
    lines = []
    for i in range(0, len(hex_bytes), bytes_per_line):
        line = hex_bytes[i:i+bytes_per_line]
        lines.append(' '.join(line))
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("用法: python bin2hex.py 输入文件.bin 输出文件.txt")
        sys.exit(1)
    bin_to_hex_spaced(sys.argv[1], sys.argv[2])