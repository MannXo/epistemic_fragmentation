# import os

# # Folders to ignore while walking the tree
# IGNORED_DIRS = {'__pycache__', 'venv', '.git', '.mypy_cache', '.idea', '.pytest_cache'}

# def print_tree(root_path, prefix=''):
#     entries = sorted(os.listdir(root_path))
#     entries = [e for e in entries if e not in IGNORED_DIRS and not e.startswith('.')]

#     for i, entry in enumerate(entries):
#         path = os.path.join(root_path, entry)
#         connector = '└── ' if i == len(entries) - 1 else '├── '
#         print(prefix + connector + entry)
#         if os.path.isdir(path):
#             extension = '    ' if i == len(entries) - 1 else '│   '
#             print_tree(path, prefix + extension)

# if __name__ == '__main__':
#     project_root = '.'
#     print_tree(project_root)


import json
from datetime import datetime

# Load data
with open("insights/rq3/narrative_engagement_over_time.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Define cutoff
cutoff_date = datetime.strptime("2024-09", "%Y-%m")

# Initialize counters
totals = {
    "before": {"n3": 0, "all": 0},
    "after": {"n3": 0, "all": 0}
}

# Process data
for record in data:
    date = datetime.strptime(record["created_month"], "%Y-%m")
    narrative = record["narrative"]
    engagement = record["total_engagement"]

    period = "before" if date < cutoff_date else "after"
    totals[period]["all"] += engagement
    if narrative == "N-3":
        totals[period]["n3"] += engagement

# Calculate shares
share_before = totals["before"]["n3"] / totals["before"]["all"]
share_after = totals["after"]["n3"] / totals["after"]["all"]

# Compute % difference
percent_diff = ((share_after - share_before) / share_before) * 100

# Print results
print("Before Sept 2024:")
print(f"- Total Engagement: {totals['before']['all']}")
print(f"- N-3 Engagement: {totals['before']['n3']}")
print(f"- Share: {share_before:.2%}")

print("\nAfter Sept 2024:")
print(f"- Total Engagement: {totals['after']['all']}")
print(f"- N-3 Engagement: {totals['after']['n3']}")
print(f"- Share: {share_after:.2%}")

print(f"\n% Increase in N-3 Share: {percent_diff:.2f}%")
