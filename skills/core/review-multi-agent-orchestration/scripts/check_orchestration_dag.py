#!/usr/bin/env python3
"""Audits a multi-agent orchestration topology JSON for write collisions and dependency cycles."""
import argparse
import json
import sys

def has_cycle(tasks):
    graph = {t["task_id"]: t.get("depends_on", []) for t in tasks}
    visited = {}
    def dfs(node):
        state = visited.get(node, 0)
        if state == 1:
            return True
        if state == 2:
            return False
        visited[node] = 1
        for dep in graph.get(node, []):
            if dfs(dep):
                return True
        visited[node] = 2
        return False
    return any(dfs(n) for n in graph)

def main():
    parser = argparse.ArgumentParser(description="Check multi-agent orchestration topology.")
    parser.add_argument("--topology", required=True, help="Path to topology JSON")
    args = parser.parse_args()

    with open(args.topology, "r", encoding="utf-8") as f:
        data = json.load(f)

    tasks = data.get("tasks", [])
    if has_cycle(tasks):
        print("[FAIL] Dependency cycle detected in orchestration task graph.")
        sys.exit(1)

    writers = {}
    for t in tasks:
        tid = t["task_id"]
        for path in t.get("write_paths", []):
            if path in writers:
                print(f"[FAIL] Write-path collision on '{path}' between {writers[path]} and {tid}.")
                sys.exit(1)
            writers[path] = tid

    print(f"[PASS] Orchestration DAG verified: {len(tasks)} tasks, 0 cycles, 0 write collisions.")

if __name__ == "__main__":
    main()
