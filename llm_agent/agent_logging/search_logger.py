import csv
import os

class SearchLogger:
    def __init__(self, filepath="search_results.csv"):
        self.filepath = filepath
        self.run_id = 1
        self._init_file()

    def _init_file(self):
        if not os.path.exists(self.filepath) or os.path.getsize(self.filepath) == 0:
            with open(self.filepath, mode="w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=self.fieldnames())
                writer.writeheader()

    def fieldnames(self):
        return [
            "run_id", "algorithm", "query_id", "query_complexity",
            "success", "execution_time_ms", "nodes_expanded", "path_length"
        ]

    def log_run(self, algorithm, query_id, query_complexity, result, node_count, path_length):
        with open(self.filepath, mode="a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames())
            writer.writerow({
                "run_id": self.run_id,
                "algorithm": algorithm,
                "query_id": query_id,
                "query_complexity": query_complexity,
                "success": result.get("success", False),
                "execution_time_ms": result.get("execution_time_ms", None),
                "nodes_expanded": node_count,
                "path_length": path_length if path_length is not None else None
            })
        self.run_id += 1
