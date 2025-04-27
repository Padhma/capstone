import time
import json
import datetime
import sys
from agent.agent import run_agent
from scraper.page_loader import close_driver
from search_algorithms.dfs import DepthFirstSearch
from search_algorithms.bfs import BreadthFirstSearch
from search_algorithms.astar import AStarSearch

# Redirect stdout and stderr to a file
logfile = open('entire_logs.txt', 'w')
sys.stdout = logfile
sys.stderr = logfile

# sample simulation data
# task = "find a high performance laptop"
# goal = {"brand": "acer"}
# query_id = "Q9"
# query_complexity = 2
# search_engine = DepthFirstSearch
# search_engine = BreadthFirstSearch
# search_engine = AStarSearch

# Load queries from agent_queries.json
with open('simulation_queries.json', 'r') as f:
    queries = json.load(f)

max_search_steps = 50
algorithms =[DepthFirstSearch, BreadthFirstSearch, AStarSearch]

for query in queries:
    print("This is query: ", query["query_id"])
    for search_engine in algorithms:
        print("This is search engine: ", search_engine.__name__)
        result = run_agent(
            task=query["task"],
            goal=query["goal"],
            max_steps=max_search_steps,
            query_id=query["query_id"],
            query_complexity=query["query_complexity"],
            engine_class=search_engine
        )
    time.sleep(30)

if result and result.get("success"):
    # print(f"\n🎯 Goal Details: {result}")
    for step in result.get("path", []):
        print("•", step)
else:
    print("⚠️ No steps were taken. The agent may have failed on the first page.")

# Clean up Selenium
close_driver()
