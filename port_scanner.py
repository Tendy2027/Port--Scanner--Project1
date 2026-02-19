import socket
import threading
import logging
import argparse

# Setup the log file (our "diary" of what happens)
logging.basicConfig(
    filename='scan_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

def scan_port(host, port):
    try:
        # Create a new "phone" (socket) for each port - important!
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Wait only 1 second max - prevents hanging forever
        # Try to knock on the door
        result = sock.connect_ex((host, port))
        if result == 0:
            message = f"Port {port} is OPEN on {host}"
        else:
            message = f"Port {port} is CLOSED on {host}"
        print(message)
        logging.info(message)
        sock.close()  # Always close the phone after knocking
    except socket.timeout:
        message = f"Port {port} TIMED OUT on {host}"
        print(message)
        logging.info(message)
    except Exception as e:
        message = f"Error on port {port}: {str(e)}"
        print(message)
        logging.error(message)

def main():
    # Menu to choose what to scan
    parser = argparse.ArgumentParser(description="My Beginner Port Scanner")
    parser.add_argument("host", help="Host to scan (use 127.0.0.1 for your own computer)")
    parser.add_argument("--start", type=int, default=1, help="Start port (default 1)")
    parser.add_argument("--end", type=int, default=100, help="End port (default 100 - keep small at first)")
    args = parser.parse_args()

    print(f"Scanning {args.host} from port {args.start} to {args.end}...")
    print("Be patient - it might take a few seconds...")

    threads = []

    for port in range(args.start, args.end + 1):
        t = threading.Thread(target=scan_port, args=(args.host, port))
        threads.append(t)
        t.start()

    # Wait for everyone to finish
    for t in threads:
        t.join()

    print("\nDone! Check scan_log.txt for full results.")

if __name__ == "__main__":
    main()

