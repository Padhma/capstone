def format_for_llm(elements, current_page_name, task, previous_action=None, goal_constraints=None, url_path=None):
    lines = ["OBSERVATION:"]

    for el in elements:
        tag = el.get("tag", "")
        if tag not in {"a", "button", "input"}:
            continue

        id_ = el.get("id", "")
        text = el.get("text", "").strip().replace("\n", " ")
        aria = el.get("aria_label", "")
        label = aria or text or tag
        href = el.get("href", "").strip()
        line = f"[{id_}] [{tag}] ['{label}']"
        if href:
            line += f" → {href}"
        lines.append(line)

    if url_path:
        lines.append(f"NAVIGATION PATH: {url_path}")

    lines.append(f"URL: {current_page_name}")
    lines.append(f"OBJECTIVE: {task}")

    if goal_constraints:
        goal_str = ', '.join(f"{k}={v}" for k, v in goal_constraints.items())
        lines.append(f"GOAL CONSTRAINTS: {goal_str}")

    lines.append(f"PREVIOUS ACTION: {previous_action or 'None'}")

    lines.append(
        "You are a smart browsing agent. List any valid links that meet the goal criteria directly, "
        "prioritize diving deeper into sub-categories rather than broad navigation.\n"
        "Confirm directly with '✅ Goal' if possible or suggest focused links.\n"
        "Format:\nAction: <label> → <URL>"
    )

    return "\n".join(lines)