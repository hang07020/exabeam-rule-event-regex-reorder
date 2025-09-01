import re

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

# Load sample input and template from external files
SAMPLE_INPUT_FILE = load_file("samples/event_input.txt")
SAMPLE_TEMPLATE_FILE = load_file("samples/event_template.txt")


def group_events(text):
    """Extract events from the input text."""
    events = []
    current_event = ""
    inside_event = False

    for line in text.splitlines():
        stripped_line = line.strip()

        # Start of an event
        if re.match(r'^([^\s]*)\s=\s{', stripped_line):  # Matches "EventName {"
            if current_event:
                events.append(current_event.strip())
            current_event = line.rstrip()
            inside_event = True
            continue

        # End of an event
        if stripped_line == "}":
            current_event += "\n" + line.rstrip()
            events.append(current_event.strip())
            current_event = ""
            inside_event = False
            continue

        # Inside an event
        if inside_event:
            current_event += "\n" + line.rstrip()

    return events

def extract_event_name(event):
    """Extract the name of the event."""
    match = re.match(r'^([^\s]*)\s=\s{', event.split("\n")[0])
    return match.group(1) if match else "Unknown"

def process_text(input_text, template_text):
    """Process the text inputs and reorder events based on the template."""
    try:
        # Extract events from both inputs
        input_events = group_events(input_text)
        template_events = group_events(template_text)

        # Extract event names from the template
        template_event_names = [extract_event_name(event) for event in template_events]

        # Reorder events in input based on the template
        reordered_events = []
        for template_name in template_event_names:
            for event in input_events:
                event_name = extract_event_name(event)
                if template_name in event_name:
                    reordered_events.append(event)

        # Add unmatched events at the end
        matched_event_names = [extract_event_name(event) for event in reordered_events]
        unmatched_events = [event for event in input_events if extract_event_name(event) not in matched_event_names]
        reordered_events.extend(unmatched_events)

        # Adjust closing braces
        for i in range(len(reordered_events)):
            lines = reordered_events[i].split("\n")
            if i == len(reordered_events) - 1:  # Last rule
                if lines[-1] == "}}":  # Ensure only one closing brace
                    lines[-1] = "}"
            else:  # All other rules
                if lines[-1] == "}":  # Ensure double closing braces
                    lines[-1] = "}}"
            reordered_events[i] = "\n".join(lines)

        return "\n".join(reordered_events)
    except Exception as e:
        return f"Error: {e}"

def event_builder_reorder(input_content, template_content):
    """Interface for reordering events."""
    return process_text(input_content, template_content)

# SAMPLE usage
if __name__ == "__main__":
    event_builder_reorder(SAMPLE_INPUT_FILE,SAMPLE_TEMPLATE_FILE)