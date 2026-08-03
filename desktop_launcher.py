import os
import socket
import subprocess
import sys
import threading
import time
import webbrowser
from pathlib import Path


def find_free_port(start=5000, end=9000):
    for port in range(start, end):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return 0


def start_server(port, project_root):
    env = os.environ.copy()
    env["PORT"] = str(port)
    env["FLASK_ENV"] = "production"
    python_exe = Path(sys.executable)
    return subprocess.Popen(
        [str(python_exe), "-c", "from app import create_app; app = create_app(); app.run(host='127.0.0.1', port=int(__import__('os').environ['PORT']), threaded=True)"],
        cwd=str(project_root),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )


def wait_for_server(port, timeout=30):
    url = f"http://127.0.0.1:{port}"
    end = time.time() + timeout
    while time.time() < end:
        try:
            import urllib.request
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.5)
    return False


def main():
    if getattr(sys, "frozen", False):
        project_root = Path(sys.executable).parent
    else:
        project_root = Path(__file__).resolve().parent
    os.chdir(project_root)
    port = int(os.environ.get("PORT", 0))
    if not port:
        port = find_free_port()
    url = f"http://127.0.0.1:{port}"

    process = start_server(port, project_root)

    def monitor():
        while True:
            line = process.stdout.readline()
            if not line:
                break
            print(line.strip())

    threading.Thread(target=monitor, daemon=True).start()

    if wait_for_server(port):
        webbrowser.open(url)
    else:
        print("서버를 시작하지 못했습니다.")
        process.terminate()
        sys.exit(1)

    try:
        import pystray
        from PIL import Image, ImageDraw

        def on_clicked(icon, item):
            if str(item) == "열기":
                webbrowser.open(url)
            elif str(item) == "종료":
                process.terminate()
                icon.stop()

        def create_image():
            width = 64
            height = 64
            image = Image.new("RGB", (width, height), "white")
            dc = ImageDraw.Draw(image)
            dc.ellipse((4, 4, width - 4, height - 4), fill="#0b9f7a")
            dc.text((20, 20), "✦", fill="white")
            return image

        icon = pystray.Icon(
            "harussukssuk",
            create_image(),
            "하루쑥쑥",
            menu=pystray.Menu(
                pystray.MenuItem("열기", on_clicked),
                pystray.MenuItem("종료", on_clicked),
            ),
        )
        icon.run()
    except Exception:
        print(f"트레이 아이콘 없이 실행 중입니다. {url}")
        process.wait()


if __name__ == "__main__":
    main()
