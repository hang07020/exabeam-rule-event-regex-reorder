import re

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Load sample input and template from external files
SAMPLE_INPUT_FILE = load_file("samples/rule_input.txt")
SAMPLE_TEMPLATE_FILE = load_file("samples/rule_template.txt")

def group_rules(file_content):
    """Extract rules from the input content."""
    rules = []
    current_rule = ""
    inside_rule = False

    for line in file_content.splitlines():
        stripped_line = line.strip()

        # Start of a rule
        if re.match(r'^\s{2}[\w\d-]+\s*{', line):  # Matches "  RuleName {"
            if current_rule:
                rules.append(current_rule.strip())
            current_rule = line.rstrip()
            inside_rule = True
            continue

        # End of a rule
        if re.match(r'^\s{2}}', line) and inside_rule:  # Matches "  }"
            current_rule += "\n" + line.rstrip()
            rules.append(current_rule.strip())
            current_rule = ""
            inside_rule = False
            continue

        # Inside a rule
        if inside_rule:
            current_rule += "\n" + line.rstrip()

    return rules

def extract_rule_name(rule):
    """Extract the name of the rule."""
    match = re.match(r'^\s*([\w\d-]+)\s*{', rule.split("\n")[0])
    return match.group(1) if match else "Unknown"

def group_fields(rule):
    """Extract groups of fields from a rule."""
    groups = []
    current_group = []
    brace_count = 0  # Track opening and closing braces

    # Split rule into lines and skip the first and last lines
    lines = rule.split("\n")[1:-1]

    for line in lines:
        stripped_line = line.strip()

        # Update brace count
        brace_count += stripped_line.count("{") + stripped_line.count("[")
        brace_count -= stripped_line.count("}") + stripped_line.count("]")

        current_group.append(line.rstrip())

        # If brace count is balanced and we have content, we close the current group
        if brace_count == 0 and current_group:
            groups.append("\n".join(current_group).strip())
            current_group = []

    return groups

def reorder_fields(input_fields, template_fields):
    """Reorder input fields to match the order of template fields."""
    template_field_names = [field.split("=", 1)[0].strip() for field in template_fields]
    input_field_dict = {field.split("=", 1)[0].strip(): field for field in input_fields}

    reordered_fields = [input_field_dict[name] for name in template_field_names if name in input_field_dict]
    return reordered_fields

def reorder_rules(input_rules, template_rules):
    """Reorder input rules and their fields to match the template rules."""
    template_order = [extract_rule_name(rule) for rule in template_rules]
    input_rules_dict = {extract_rule_name(rule): rule for rule in input_rules}
    reordered_rules = []

    for template_rule in template_rules:
        template_rule_name = extract_rule_name(template_rule)
        if template_rule_name in input_rules_dict:
            # Match the corresponding rule in input_rules
            input_rule = input_rules_dict[template_rule_name]

            # Group fields for both template and input rule
            input_fields = group_fields(input_rule)
            template_fields = group_fields(template_rule)

            # Reorder input fields based on the template fields
            reordered_fields = reorder_fields(input_fields, template_fields)

            # Format fields with indentation
            formatted_fields = [f"    {field}" for field in reordered_fields]

            # Rebuild the rule with reordered fields
            rule_header = "  " + input_rule.split("\n")[0]  # Add 2 spaces to the rule header
            rule_footer = input_rule.split("\n")[-1]  # Add 2 spaces to the rule footer
            reordered_rule = f"{rule_header}\n" + "\n".join(formatted_fields) + f"\n{rule_footer}"

            reordered_rules.append(reordered_rule)

    return "\n".join(reordered_rules)

def rule_reorder(input_content, template_content):
    """Interface for reordering rules and wrapping them in a Rules block."""
    input_rules = group_rules(input_content)
    template_rules = group_rules(template_content)

    # Reorder rules
    reordered_rules = reorder_rules(input_rules, template_rules)

    # Wrap in a Rules block
    wrapped_rules = f"Rules {{\n{reordered_rules}\n}}"
    return wrapped_rules
