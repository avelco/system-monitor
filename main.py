import daemon
from monitor import main  # Assume your checking logic is in a function called `main`

def run():
    with daemon.DaemonContext():
        main()

if __name__ == "__main__":
    run()
