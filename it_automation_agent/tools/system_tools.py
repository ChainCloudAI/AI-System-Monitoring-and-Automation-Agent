import psutil
import time
import subprocess
import os
import json


# ✅ CPU usage
def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


# ✅ Memory usage
def get_memory_usage():
    mem = psutil.virtual_memory()
    return mem.percent


# ✅ Disk usage
def get_disk_usage():
    disk = psutil.disk_usage('/')
    return disk.percent


# ✅ Safe Top CPU processes
def get_top_processes():
    processes = []

    for p in psutil.process_iter(['pid', 'name']):
        try:
            p.cpu_percent(interval=None)
        except:
            pass

    time.sleep(1)

    for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
        try:
            info = p.info
            cpu = info.get('cpu_percent')

            if cpu is None:
                cpu = 0.0

            info['cpu_percent'] = cpu
            processes.append(info)
        except:
            pass

    processes = sorted(processes, key=lambda x: x['cpu_percent'], reverse=True)
    return processes[:5]


# ✅ Kill process
def kill_process(pid):
    try:
        p = psutil.Process(pid)
        p.terminate()
        return f"✅ Process {pid} terminated."
    except Exception as e:
        return f"❌ Failed: {e}"


# ✅ Network check
def network_check():
    try:
        result = subprocess.run(
            ["ping", "-c", "3", "8.8.8.8"],
            capture_output=True,
            text=True
        )

        return "✅ Network OK" if result.returncode == 0 else "❌ Network issue"

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ✅ Find screenshots
def find_screenshots():
    desktop = os.path.expanduser("~/Desktop")
    screenshots = [
        f for f in os.listdir(desktop)
        if "Screenshot" in f and f.endswith(".png")
    ]

    if screenshots:
        return f"FOUND:{len(screenshots)}"
    return "FOUND:0"


# ✅ ✅ DELETE screenshots + CORRECT LOGGING
def delete_screenshots():
    try:
        desktop = os.path.expanduser("~/Desktop")
        deleted = 0

        for file in os.listdir(desktop):
            if "Screenshot" in file and file.endswith(".png"):
                path = os.path.join(desktop, file)
                try:
                    os.remove(path)
                    deleted += 1
                except:
                    pass

        # ✅ ROOT PATH (FINAL FIX)
        ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        LOG_FILE = os.path.join(ROOT_DIR, "screenshot_log.json")

        # ✅ Load + update
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                data = json.load(f)
        else:
            data = {"deleted": 0}

        data["deleted"] += deleted

        with open(LOG_FILE, "w") as f:
            json.dump(data, f)

        return f"✅ Deleted {deleted}"

    except Exception as e:
        return f"❌ Error: {str(e)}"