from agent.agent import run_agent
from scraper.page_loader import close_driver

task = "find a gaming laptop"
goal = {"brand": "hp", "price": "under 2000$"}
max_search_steps = 20
algorithm = "DFS"
query_id = "Q5"
query_complexity = 2

result = run_agent(
    task=task,
    goal=goal,
    max_steps=max_search_steps,
    query_id=query_id,
    query_complexity=query_complexity,
    algorithm=algorithm
)

if result and result.get("success"):
    # print(f"\n🎯 Goal Details: {result}")
    for step in result.get("path", []):
        print("•", step)
else:
    print("⚠️ No steps were taken. The agent may have failed on the first page.")

# Clean up Selenium
close_driver()
