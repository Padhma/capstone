from search_algorithms.node import SearchNode

class AStarSearchNode(SearchNode):
    def __init__(self, page_path, state_content, action_history=None, g=0, h=0, f=0, raw_html=None, parent=None):
        super().__init__(page_path, state_content, action_history=action_history, raw_html=raw_html, parent=parent)
        self.g = g
        self.h = h
        self.f = f

    def __repr__(self):
        return f"<AStarSearchNode: {self.page_path}, g={self.g}, h={self.h}, f={self.f}, steps={len(self.action_history)}>"

    # Define comparison methods based on the f value
    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def __eq__(self, other):
        return self.f == other.f
