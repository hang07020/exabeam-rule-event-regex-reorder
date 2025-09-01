# Exabeam Config Reorder Tool

A Python GUI tool to reorder Exabeam configuration files (Rules, Event Builder, and Regex) for improved readability and consistency.  
This project demonstrates how security engineers can automate tedious configuration management tasks with Python and Tkinter.

---

## Features
- **GUI-based** (Tkinter) for easy use  
- **Three supported modes**:
  - **Rule Reorder**: Aligns rule configuration with a template
  - **Event Builder Reorder**: Reorders Event Builder definitions to match a template
  - **Regex Reorder**: Reorders regex `Fields` section (reverse order)  
- **Sample input and templates** are stored under the `/samples` directory for demonstration  

---

## Project Structure
```
exabeam-config-reorder-tool/
├── MainGUI.py               # Main GUI entry point
├── rule_reorder.py          # Logic for reordering Rule configurations
├── event_builder_reorder.py # Logic for reordering Event Builder configurations
├── regex_reorder.py         # Logic for reordering Regex fields
├── samples/                 # Sample input and template files (dummy data)
│   ├── rule_input.txt
│   ├── rule_template.txt
│   ├── event_input.txt
│   ├── event_template.txt
│   └── regex_input.txt
```

---

## Requirements
- Python 3.x  
- Standard libraries only (`tkinter`, `re`)  

---

## Installation
Clone the repository:
```bash
git clone https://github.com/yourusername/exabeam-config-reorder-tool.git
cd exabeam-config-reorder-tool
```

(Optional) create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

---

## Usage
Run the main GUI:
```bash
python MainGUI.py
```

1. Select a **Reorder Type** (Rule / Event Builder / Regex)  
2. Paste or load your configuration into the *Input* text area  
3. Paste a template into the *Template* area (not required for Regex mode)  
4. Click **Process** to generate the reordered output  

---
