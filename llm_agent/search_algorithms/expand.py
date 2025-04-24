from search_algorithms.node import SearchNode

def expand_frontier(current_node, selected_element, page_loader):
    href = selected_element["href"]
    label = selected_element.get("aria_label", selected_element.get("text", "unknown")).strip()
    new_page_data = page_loader(href)
    # print(f"🔍 Loaded {href}, #elements: {len(new_page_data['elements'])}")

    return SearchNode(
        page_path=href,
        state_content=new_page_data["elements"],
        raw_html=new_page_data["raw"],
        action_history=current_node.action_history + [f"Clicked: {label}"],
        parent=current_node
    )