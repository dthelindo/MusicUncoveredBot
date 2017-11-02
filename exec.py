import app
import threading

def main():
    app.main()
    threading.Timer(604800, main).start()

if __name__ == "__main__":
    main()
