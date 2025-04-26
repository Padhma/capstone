import re

def parse_llm_action_list(response, elements):
    # Assuming that URLs wrapped in open or close link characters were causing issues
    matches = re.findall(r'→\s*(https?://[^\s]*)', response)
    selected = []

    for href in matches:
        href = href.rstrip('**').strip()  # Remove potential formatting artifacts
        for el in elements:
            if el.get("tag") == "a" and el.get("href") == href:
                selected.append(el)
                break
    
    # Diagnostic output to verify actions
    print("Valid actions extracted from LLM response:")
    for action in selected:
        print(action.get("text", ""), "→", action.get("href", ""))

    return selected