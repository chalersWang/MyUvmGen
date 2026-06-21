def calculate_checksum(words):
    """
    Calculate checksum for words 0 to 6 and store in low byte of word 7
    Using polynomial x^8 + x^2 + x + 1 (CRC-8) with initial value 0xFF
    
    Args:
        words: List of 16-bit words (at least 7 words)
    
    Returns:
        Updated list with checksum in low byte of word 7
    """
    # Make sure we have at least 7 words
    if len(words) < 7:
        raise ValueError("Input must contain at least 7 words")
    
    # CRC-8 polynomial x^8 + x^2 + x + 1 = 0x07
    polynomial = 0x07
    
    # Initial value
    crc = 0xFF
    
    # Process each word from 0 to 6
    for i in range(7):
        # Process high byte
        crc ^= (words[i] >> 8) & 0xFF
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ polynomial
            else:
                crc = crc << 1
            crc &= 0xFF
        
        # Process low byte
        crc ^= words[i] & 0xFF
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ polynomial
            else:
                crc = crc << 1
            crc &= 0xFF
    
    # Set the low byte of word 7 to the calculated CRC
    if len(words) <= 7:
        words.append((words[7] & 0xFF00) | crc if len(words) > 7 else crc)
    else:
        words[7] = (words[7] & 0xFF00) | crc
    
    return words


# Example usage
if __name__ == "__main__":
    # Example data: 7 words (16-bit values)
    test_words = [0x0401, 0x0000, 0x0A00, 0x00FF, 0x0000, 0x0000, 0x0000]
    
    # Calculate and add checksum
    result = calculate_checksum(test_words)
    
    print("Words with checksum:")
    for i, word in enumerate(result):
        print(f"Word {i}: 0x{word:04X}")
    
    print(f"Checksum (low byte of word 7): 0x{result[7] & 0xFF:02X}")