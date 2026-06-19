import streamlit as st
import os
import json
from tools.system_tools import get_cpu_usage, get_memory_usage, get_disk_usage, find_screenshots
from agent.memory import get_actions


# ✅ DARK STYLING
st.markdown("""
<style>
body { background-color: #0e1117; color: white; }
.block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)


# ✅ HEADER
st.title("🧠 AI Automation Dashboard")
st.caption("System Monitoring + AI Activity")


# ✅ SYSTEM HEALTH
st.subheader("📊 System Health")

cpu = get_cpu_usage()
memory = get_memory_usage()
disk = get_disk_usage()

c1, c2, c3 = st.columns(3)
c1.metric("CPU", f"{cpu:.1f}%")
c2.metric("Memory", f"{memory:.1f}%")
c3.metric("Disk", f"{disk:.1f}%")


# ✅ ALERTS
if cpu > 80:
    st.error("High CPU")

if memory > 80:
    st.warning("High Memory")

if disk > 90:
    st.warning("Disk Full")


# ✅ AI COUNTS
st.subheader("🧠 AI Activity Summary")

actions = get_actions()
counts = {}

for a in actions:
    counts[a] = counts.get(a, 0) + 1

if counts:
    cols = st.columns(len(counts))
    for i, (k, v) in enumerate(counts.items()):
        cols[i].metric(k, v)
else:
    st.info("No actions yet")


# ✅ SCREENSHOT ANALYTICS
st.subheader("📸 Screenshot Analytics")

res = find_screenshots()
found = int(res.split(":")[1])


# ✅ SAME ROOT FILE (matches backend)
ROOT_DIR = os.path.dirname(__file__)
LOG_FILE = os.path.join(ROOT_DIR, "screenshot_log.json")

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        data = json.load(f)
    deleted = data.get("deleted", 0)
else:
    deleted = 0

c1, c2 = st.columns(2)
c1.metric("Found", found)
c2.metric("Deleted", deleted)


# ✅ HISTORY
st.subheader("📜 Action History")

for act in actions[-10:][::-1]:
    st.write("- " + act)


st.markdown("---")
st.caption("AI Agent • Dark UI • Production Style")