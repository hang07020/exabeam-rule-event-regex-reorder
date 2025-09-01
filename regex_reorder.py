import re

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Load sample input from external files
SAMPLE_INPUT_FILE = load_file("samples/regex_input.txt")


def regex_reorder(input_file):
    # Step 1: Detect the Fields section and all lines below it
    fields_pattern = r'"{3}Fields"{3}.*(\n.*)+'
    fields_match = re.search(fields_pattern, input_file)

    if not fields_match:
        return "No Fields section detected."

    before_fields = input_file[:fields_match.start()]  # Content before the Fields section

    fields_section = fields_match.group(0)  # Get the content of the Fields section

    # Step 2: Extract all strings matching the triple-quoted format
    extracted_fields = re.findall(r'(?:"""Fields""" = |"{3}(.*)"{3},? ]?\n)', fields_section)

    # Step 2.1: Delete the first extracted field
    if extracted_fields:
        extracted_fields.pop(0)

    # Step 3: Reorder fields as 54321
    reordered_fields = extracted_fields[::-1]  # Reverse the list order

    # Step 4: Construct the new Fields section
    reordered_fields_content = ", \n\t\t".join([f'"""{field}"""' for field in reordered_fields])
    new_fields_section = f'"""Fields""" = [ {reordered_fields_content} ]\n    }}\n]'

    # Combine the content before Fields with the new reordered Fields section
    reorder_file = before_fields + new_fields_section

    return reorder_file
