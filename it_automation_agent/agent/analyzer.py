import requests
import json
import re


def analyze_system(cpu, memory, disk):
    issues = []
    recommendations = []

    if cpu > 80:
        issues.append("High CPU usage")
        recommendations.append("cpu_optimization")

    if memory > 80:
        issues.append("High Memory usage")
        recommendations.append("memory_cleanup")

    if disk > 90:
        issues.append("Disk almost full")
        recommendations.append("disk_cleanup")

    return issues, recommendations


# ✅ AI WITH MEMORY-AWARE DECISIONS
def analyze_with_ai(system_summary):
    try:
        prompt = f"""
You are an intelligent IT automation agent.

Return ONLY valid JSON.

Format:
{{
  "issues": ["issue1", "issue2"],
  "actions": ["cpu_optimization", "network_check"],
  "reason": "Explain your decisions"
}}

Rules:
- DO NOT repeat actions listed under "Previous Actions"
- If an action already failed or was used, choose a DIFFERENT one
- You can return MULTIPLE actions
- First action = highest priority
- Use network_check if network issues are present
- Only choose from available actions

Available actions:
- cpu_optimization
- memory_cleanup
- disk_cleanup
- network_check

System data:
{system_summary}
"""

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        output = response.json()["response"]

        # ✅ Extract JSON
        match = re.search(r"\{.*\}", output, re.DOTALL)

        if match:
            json_str = match.group(0)
            data = json.loads(json_str)

            issues = data.get("issues", [])
            actions = data.get("actions", [])
            reason = data.get("reason", "")

            return issues, actions, reason
        else:
            return ["AI Error: No JSON found"], [], ""

    except Exception as e:
        return [f"AI Error: {str(e)}"], [], ""