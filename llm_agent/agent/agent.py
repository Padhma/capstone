from llm.gemini_client import call_gemini
from llm.prompt_formatter import format_for_llm
from scraper.page_loader import page_loader
from search_algorithms.dfs import DFSTreeSearchEngine
from search_algorithms.expand import expand_frontier
from agent_logging.search_logger import SearchLogger

def run_agent(task, goal, max_steps, query_id, query_complexity, algorithm):
    logger = SearchLogger()

    engine = DFSTreeSearchEngine(
        page_loader=page_loader,
        invoke_llm=call_gemini,
        formatter=format_for_llm,
        expander=expand_frontier,
        goal_constraints=goal,
        task=task,
        max_steps=max_steps,  # ✅ fixed this line
        logger=logger,
        algorithm=algorithm,
        query_id=query_id,
        query_complexity=query_complexity
    )

    engine.initialize("https://padhma.github.io/capstone/index.html")
    engine.run_until_done()

    return engine.result
