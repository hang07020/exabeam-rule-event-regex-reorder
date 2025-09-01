from tkinter import Tk, Text, Label, Button, Radiobutton, StringVar, END, Scale, HORIZONTAL
from tkinter.font import Font
from rule_reorder import rule_reorder, SAMPLE_INPUT_FILE as RULE_INPUT, SAMPLE_TEMPLATE_FILE as RULE_TEMPLATE
from event_builder_reorder import event_builder_reorder, SAMPLE_INPUT_FILE as EVENT_INPUT, SAMPLE_TEMPLATE_FILE as EVENT_TEMPLATE
from regex_reorder import regex_reorder, SAMPLE_INPUT_FILE as REGEX_INPUT

def process(input_text, template_text, reorder_type):
    """Process the text based on the selected reorder type."""
    if reorder_type == "Rule Reorder":
        return rule_reorder(input_text, template_text)
    elif reorder_type == "Event Builder Reorder":
        return event_builder_reorder(input_text, template_text)
    elif reorder_type == "Regex Reorder":
        return regex_reorder(input_text)
    else:
        return "Error: Unknown reorder type."

def populate_SAMPLEs(reorder_type, input_text, template_text, template_label, output_text):
    
    output_text.delete("1.0", END)

    """Populate the SAMPLE content based on the selected reorder type."""
    if reorder_type == "Rule Reorder":
        input_text.delete("1.0", END)
        input_text.insert("1.0", RULE_INPUT)
        template_text.delete("1.0", END)
        template_text.insert("1.0", RULE_TEMPLATE)
        template_label.grid()  # Show the "Template File" label
        template_text.grid()   # Show the template text area
    elif reorder_type == "Event Builder Reorder":
        input_text.delete("1.0", END)
        input_text.insert("1.0", EVENT_INPUT)
        template_text.delete("1.0", END)
        template_text.insert("1.0", EVENT_TEMPLATE)
        template_label.grid()  # Show the "Template File" label
        template_text.grid()   # Show the template text area
    elif reorder_type == "Regex Reorder":
        input_text.delete("1.0", END)
        input_text.insert("1.0", REGEX_INPUT)
        template_label.grid_remove()  # Hide the "Template File" label
        template_text.grid_remove()   # Hide the template text area
        output_text.delete("1.0", END)
    else:
        input_text.delete("1.0", END)
        template_text.delete("1.0", END)

def main():
    root = Tk()
    root.title("Reorder Tool")
    root.geometry("1200x600")  # Set default window size

    # Configure grid resizing
    root.grid_rowconfigure(5, weight=1)  # Make row 5 (text areas) stretchable
    root.grid_columnconfigure(0, weight=1)  # Make column 0 stretchable
    root.grid_columnconfigure(1, weight=1)  # Make column 1 stretchable
    root.grid_columnconfigure(2, weight=1)  # Make column 2 stretchable

    # Font for Text widgets
    text_font = Font(family="Arial", size=12)

    # Reorder Type Selection (above Input File in column 0)
    reorder_type = StringVar(value="Rule Reorder")
    Label(root, text="Reorder Type:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    Radiobutton(root, text="Rule Reorder", variable=reorder_type, value="Rule Reorder",
                command=lambda: populate_SAMPLEs(reorder_type.get(), input_text, template_text, template_label, output_text)).grid(row=1, column=0, sticky="w", padx=5)
    Radiobutton(root, text="Event Builder Reorder", variable=reorder_type, value="Event Builder Reorder",
                command=lambda: populate_SAMPLEs(reorder_type.get(), input_text, template_text, template_label, output_text)).grid(row=2, column=0, sticky="w", padx=5)
    Radiobutton(root, text="Regex Reorder", variable=reorder_type, value="Regex Reorder",
                command=lambda: populate_SAMPLEs(reorder_type.get(), input_text, template_text, template_label, output_text)).grid(row=3, column=0, sticky="w", padx=5)

    # Input Text
    Label(root, text="Input File:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    input_text = Text(root, wrap="word", font=text_font)
    input_text.grid(row=5, column=0, padx=5, pady=5, sticky="nsew")

    # Template Label and Template Text Area
    template_label = Label(root, text="Template File:")
    template_label.grid(row=4, column=1, padx=5, pady=5, sticky="w")
    template_text = Text(root, wrap="word", font=text_font)
    template_text.grid(row=5, column=1, padx=5, pady=5, sticky="nsew")

    # Output Text
    Label(root, text="Output:").grid(row=4, column=2, padx=5, pady=5, sticky="w")
    output_text = Text(root, wrap="word", font=text_font)
    output_text.grid(row=5, column=2, padx=5, pady=5, sticky="nsew")

    def run_process():
        input_content = input_text.get("1.0", END).strip()
        template_content = template_text.get("1.0", END).strip()
        reorder_choice = reorder_type.get()
        output_content = process(input_content, template_content, reorder_choice)
        output_text.delete("1.0", END)
        output_text.insert("1.0", output_content)

    def adjust_font_size(value):
        new_size = int(value)
        text_font.configure(size=new_size)

    # Process Button with proportional width
    button_frame = Label(root)  # Create a frame for the button
    button_frame.grid(row=6, column=0, columnspan=3, sticky="nsew")
    button_frame.grid_columnconfigure(0, weight=1)
    button_frame.grid_columnconfigure(1, weight=1)
    button_frame.grid_columnconfigure(2, weight=1)

    Button(button_frame, text="Process", command=run_process).grid(row=0, column=1, pady=10, sticky="nsew")

    # Font Size Slider with Merged Rows
    Label(root, text="Font Size:               ").grid(row=0, column=2, padx=5, pady=5, sticky="e")  # Merge rows 0-3 for the label
    font_size_slider = Scale(root, from_=8, to=20, orient=HORIZONTAL, command=adjust_font_size)
    font_size_slider.set(12)  # Default font size
    font_size_slider.grid(row=1, column=2, rowspan=3, sticky="ne")  # Merge rows 0-3 for the slider

    # Populate SAMPLEs on startup
    populate_SAMPLEs(reorder_type.get(), input_text, template_text, template_label, output_text)

    root.mainloop()

if __name__ == "__main__":
    main()
