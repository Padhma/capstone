import time
from collections import deque
from search_algorithms.node import SearchNode
from utils.goal_checker import goal_checker
from utils.parsers import parse_llm_action_list
from search_algorithms.expand import expand_frontier

class BreadthFirstSearch:
    def __init__(self, page_loader, invoke_llm, formatter, expander, task, goal_constraints,
                 max_steps=10, logger=None, algorithm=None, query_id=None, query_complexity=None):
        self.page_loader = page_loader
        self.invoke_llm = invoke_llm
        self.formatter = formatter
        self.expander = expander
        self.goal_constraints = goal_constraints
        self.max_steps = max_steps
        self.frontier = deque()  # Use deque for BFS queue behavior
        self.explored = []
        self.task = task
        self.result = {
            "success": False,
            "target_found": None,
            "price": None,
            "ram": None,
            "path_length": 0,
            "path": []
        }
        self.logger = logger
        self.algorithm = algorithm
        self.query_id = query_id
        self.query_complexity = query_complexity
        self.start_time = None

    def initialize(self, start_url):
        page_data = self.page_loader(start_url)
        root_node = SearchNode(
            page_path=start_url,
            state_content=page_data["elements"],
            raw_html=page_data["raw"],
            action_history=[]
        )
        self.frontier.append(root_node)
        self.start_state = start_url
        self.start_time = time.time()
        self.navigation_path = [start_url]  # Initialize navigation path

    def step(self):
        if not self.frontier:
            print("Frontier is empty. Search finished.")
            return None

        current_node = self.frontier.popleft()
        self.navigation_path.append(current_node.page_path)
        print(f"Exploring: {current_node.page_path}")

        prompt = self.formatter(
            current_node.state_content,
            current_page_name=current_node.page_path,
            task=self.task,
            previous_action=current_node.action_history[-1] if current_node.action_history else None,
            goal_constraints=self.goal_constraints,
            url_path=" > ".join(self.navigation_path)
        )

        response = self.invoke_llm(prompt)
        print("\n🧠 Gemini Response:")
        print(response)

        if "✅ Goal" in response:
            print("🎯 Goal confirmation received from LLM.")
            self.result.update({
                "success": True,
                "target_found": "Goal confirmed by LLM",
                "price": "Confirmed",
                "ram": "Confirmed",
                "path_length": len(current_node.action_history),
                "path": current_node.action_history,
            })
            self.frontier.clear()  # Stop the search
            return current_node

        selected_elements = parse_llm_action_list(response, current_node.state_content)

        if "products.html" in current_node.page_path:
            success, details = goal_checker(current_node.state_content, self.goal_constraints)
        else:
            success, details = False, {}

        if success:
            print("🎯 Goal reached!")
            self.result.update({
                "success": True,
                "target_found": details.get("target_found", "NULL"),
                "price": details.get("price", "NULL"),
                "ram": details.get("ram", "NULL"),
                "path_length": len(current_node.action_history),
                "path": current_node.action_history,
            })
            self.frontier.clear()  # Stop the search
            return current_node

        if not selected_elements:
            print("⚠️ No valid actions found in LLM response.")
            self.explored.append(current_node)
            return None

        for el in selected_elements:
            new_node = expand_frontier(current_node, el, self.page_loader)
            if any(n.page_path == new_node.page_path and n.action_history == new_node.action_history for n in self.explored):
                continue
            self.frontier.append(new_node)

        self.explored.append(current_node)
        return current_node

    def run_until_done(self):
        steps = 0
        while self.frontier and steps < self.max_steps:
            node = self.step()

            if self.result.get("success"):
                print(f"🎉 Success criteria met. Ending search after {steps} steps.")
                break

            if node is None and not self.frontier:
                print(f"⚠️ Frontier exhausted - terminating search.")
                break

            steps += 1

        print("Final path taken:")
        for step in (self.result.get("path") or []):
            print("→", step)
        print(f"Search ended after {steps} steps.")

        execution_time = int((time.time() - self.start_time) * 1000)
        if not self.result.get("path"):
            self.result["path"] = node.action_history if node else []
            self.result["path_length"] = len(self.result["path"])
        self.result["execution_time_ms"] = execution_time

        self.logger.log_run(
            algorithm=self.algorithm,
            query_id=self.query_id,
            query_complexity=self.query_complexity,
            result=self.result,
            node_count=len(self.explored),
            path_length=self.result.get("path_length", 0)
        )