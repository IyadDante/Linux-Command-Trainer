import threading
import webbrowser
from app import app

def start_flask():
    app.run(host="127.0.0.1", port=5000)

if __name__ == "__main__":
    # Start Flask in a separate thread
    threading.Thread(target=start_flask, daemon=True).start()

    # Open default browser to the app
    webbrowser.open("http://127.0.0.1:5000")
