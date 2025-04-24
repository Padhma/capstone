class SearchNode:
    def __init__(self, page_path, state_content, action_history=None, score=None, raw_html=None, parent=None):
        self.page_path = page_path
        self.state_content = state_content
        self.action_history = action_history or []
        self.score = score
        self.raw_html = raw_html
        self.parent = parent

    def __repr__(self):
        return f"<SearchNode: {self.page_path}, steps={len(self.action_history)}>"