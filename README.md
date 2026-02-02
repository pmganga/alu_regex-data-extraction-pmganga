#Regex Assignment

This is my project for the data extraction task using regex in Python.

## What it does
- Extracts stuff like emails, URLs, phones, credit cards, and times from text.
- Checks if input is safe (like no hacking code).
- Masks credit cards so they're not fully shown.
- I used Python because it's easier for me.

## Files here
- extract_data.py: the main code I wrote
- sample_input.txt: test text with bad stuff (triggers safety check)
- sample_output.txt: output from bad input
- sample_input_safe.txt: clean test text
- sample_output_safe.txt: output from clean input

## How to run it
python3 extract_data.py sample_input_safe.txt

Or with output to file:
python3 extract_data.py sample_input_safe.txt > output.txt


