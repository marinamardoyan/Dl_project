import webbrowser
import threading
import time
import sys
import streamlit.web.cli as stcli
import os


def open_browser():
    time.sleep(1)
    webbrowser.open_new("http://localhost:8501")


if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    if getattr(sys, 'frozen', False):
        script_path = os.path.join(sys._MEIPASS, 'main.py')
    else:
        script_path = __file__

    sys.argv = ["streamlit", "run", script_path]
    sys.exit(stcli.main())
