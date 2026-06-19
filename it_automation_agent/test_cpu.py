from tools.system_tools import (
    get_cpu_usage,
    get_memory_usage,
    get_disk_usage,
    get_top_processes,
    network_check,
    find_screenshots,
    delete_screenshots
)
from agent.analyzer import analyze_with_ai
from agent.memory import add_action, get_actions
import requests
import re

print("=== SYSTEM HEALTH CHECK ===\n")

# 🔥 TEST MODE
cpu = 85
memory = 75
disk = 95

print(f"CPU Usage: {cpu}%")
print(f"Memory Usage: {memory}%")
print(f"Disk Usage: {disk}%\n")

# ✅ Memory
past_actions = get_actions()
print(f"🧠 Past actions: {past_actions}\n")

# ✅ System summary
system_summary = f"""
System Status:
- CPU Usage: {cpu}%
- Memory Usage: {memory}%
- Disk Usage: {disk}%
- Network Status: Unstable / Slow connection detected

Previous Actions:
{past_actions}
"""

# ✅ AI analysis
ai_issues, ai_recommendations, ai_reason = analyze_with_ai(system_summary)

if ai_issues:
    print("🤖 AI Analysis:")
    for issue in ai_issues:
        print(f"- {issue}")

if ai_reason:
    print(f"\n🧠 AI Reason:\n{ai_reason}")


def ai_select_process(processes):
    try:
        process_text = "\n".join([
            f"{i+1}. {p['name']} (CPU: {p['cpu_percent']}%) PID: {p['pid']}"
            for i, p in enumerate(processes)
        ])

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": process_text, "stream": False}
        )

        output = response.json()["response"]
        match = re.search(r"\d+", output)

        if match:
            choice = int(match.group())
            if 1 <= choice <= len(processes):
                return choice

        return 1

    except:
        return 1


def execute_action(action):
    print(f"\n👉 Executing action: {action}")
    add_action(action)

    if action == "cpu_optimization":
        processes = get_top_processes()

        print("\n🔍 Top CPU Processes:\n")
        for i, p in enumerate(processes, 1):
            print(f"{i}. {p['name']} | CPU: {p['cpu_percent']}%")

        ai_choice = ai_select_process(processes)
        selected = processes[ai_choice - 1]

        print(f"\n🤖 Suggested process: {selected['name']}")

    elif action == "memory_cleanup":
        print("🔧 Simulating: memory cleanup")

    elif action == "disk_cleanup":
        print("🔧 Simulating: disk cleanup")

    elif action == "network_check":
        print(network_check())


# ✅ RUN AI ACTIONS
if ai_recommendations:
    print("\n⚡ AUTO MODE ENABLED")
    for action in ai_recommendations:
        execute_action(action)


# ✅ ✅ NEW — SCREENSHOT CLEANUP FLOW
print("\n📸 Screenshot Check:")
result = find_screenshots()
print(result)

# ✅ Ask user BEFORE deleting
if "Found" in result:
    confirm = input("\nDelete these screenshots? (y/n): ")

    if confirm.lower() == "y":
        print(delete_screenshots())
    else:
        print("❌ Deletion cancelled.")


print("\n=== CHECK COMPLETE ===")
