import os
def remove_bom(input_path, output_path):
    # Open the input file in binary mode to read raw bytes
    with open(input_path, 'rb') as file:
        content = file.read()
    
    # Check for BOM and remove it if present
    bom = b'\xef\xbb\xbf'
    if content.startswith(bom):
        content = content[len(bom):]

    # Write the content to the output file in UTF-8 encoding
    with open(output_path, 'wb') as file:
        file.write(content)

# Main script
if __name__ == "__main__":
    input_file = 'C:/utf8_bom_test.txt'  # Replace with your input file path
    output_file = 'C:/utf8_bom_test.txt'  # Replace with your output file path
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    remove_bom(input_file, output_file)
    print(f"BOM removed and file saved as {output_file}")