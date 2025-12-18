from backend.agents.decision_graph import run_agent
import json

query = "8 seconds left, down by 2, defender 1 meter away on left wing"

result = run_agent(query)

print("\nDECISION:")
print(result["decision"])

print("\nCRITIQUE:")
print(result["critique"])