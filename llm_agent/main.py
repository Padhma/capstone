from agent.agent import run_agent
from scraper.page_loader import close_driver
from search_algorithms.dfs import DepthFirstSearch
from search_algorithms.bfs import BreadthFirstSearch
from search_algorithms.astar import AStarSearch

# task = "find a high performance laptop"
# goal = {"brand": "acer"}
# query_id = "Q9"
# query_complexity = 2
# search_engine = DepthFirstSearch
# search_engine = BreadthFirstSearch
# search_engine = AStarSearch


queries = [
    {
        "query_id": "Q1",
        "task": "Find a Business laptop",
        "goal": {"brand": "dell"},
        "query_complexity": 2
    },
]
max_search_steps = 20
algorithms =[DepthFirstSearch, BreadthFirstSearch, AStarSearch]

for query in queries:
    for search_engine in algorithms:
        result = run_agent(
            task=query["task"],
            goal=query["goal"],
            max_steps=max_search_steps,
            query_id=query["query_id"],
            query_complexity=query["query_complexity"],
            engine_class=search_engine
        )

if result and result.get("success"):
    # print(f"\n🎯 Goal Details: {result}")
    for step in result.get("path", []):
        print("•", step)
else:
    print("⚠️ No steps were taken. The agent may have failed on the first page.")

# Clean up Selenium
close_driver()
