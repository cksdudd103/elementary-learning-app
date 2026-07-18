import os
import socket
import sys
from pathlib import Path

from app import create_app

LOCK_FILE = Path(os.environ.get("TEMP", "/tmp")) / "harussukssuk_server.lock"
PORT = int(os.environ.get("PORT", 5000))


def is_server_running(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def acquire_lock():
    try:
        LOCK_FILE.write_text(str(os.getpid()), encoding="utf-8")
        return True
    except OSError:
        return False


def main():
    if is_server_running(PORT):
        print(f"서버가 이미 http://127.0.0.1:{PORT} 에서 실행 중입니다.")
        sys.exit(0)

    if LOCK_FILE.exists():
        try:
            LOCK_FILE.unlink()
        except OSError:
            pass

    if not acquire_lock():
        print("락 파일 생성에 실패했습니다. 이미 다른 인스턴스가 시작 중일 수 있습니다.")
        sys.exit(0)

    try:
        app = create_app()
        app.run(host="127.0.0.1", port=PORT, debug=True, threaded=True)
    finally:
        try:
            LOCK_FILE.unlink()
        except OSError:
            pass


if __name__ == "__main__":
    main()
