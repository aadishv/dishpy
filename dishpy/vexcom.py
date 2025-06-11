import platform
import sys
import subprocess
import os

def get_platform() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == "linux":
        if machine in ("arm", "armv7l"):
            return "linux-arm32"
        elif machine in ("aarch64", "arm64"):
            return "linux-arm64"
        else:
            return "linux-x64"
    elif system == "darwin":
        return "osx"
    elif system == "windows":
        return "win32"
    else:
        # Fallback based on architecture
        if sys.maxsize > 2**32:
            return "linux-x64"
        else:
            return "linux-arm32"

def run_vexcom(*args):
    platform_name = get_platform()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    vexcom_path = os.path.join(script_dir, "vexcom", platform_name, "vexcom")
    return subprocess.run([vexcom_path] + list(args))
