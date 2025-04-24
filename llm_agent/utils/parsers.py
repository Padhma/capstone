import re

def parse_llm_action_list(response, elements):
    """
    Parses Gemini's markdown-style or plain action lines.
    Matches: ... → https://some-url
    """
    matches = re.findall(r'→\s*(https?://\S+)', response)
    selected = []
    # print(f"Matches found: {matches}")

    for href in matches:
        for el in elements:
            if el.get("tag") == "a" and el.get("href") == href.strip():
                selected.append(el)
                # print(f"Selected element: {el}")
                break

    return selected


def parse_price(text):
    match = re.search(r"\$([\d,]+\.?\d*)", text)
    if match:
        return float(match.group(1).replace(",", ""))
    return None

def parse_ram(text):
    match = re.search(r"(\d+)\s*gb", text.lower())
    return int(match.group(1)) if match else None