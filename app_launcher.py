import socket
import time
import webbrowser
import subprocess
import sys
import signal
import os

def is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    """Returns True if the given host:port is open, with detailed exception handling."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            sock.connect((host, port))
            return True
    except ConnectionRefusedError:
        # Port is closed
        return False
    except socket.timeout:
        # Connection timed out
        return False
    except socket.gaierror:
        # DNS resolution failed
        return False
    except OSError:
        # Network unreachable, host unreachable, etc.
        return False
    except Exception:
        # Catch any other unexpected exceptions
        return False

def wait_for_port(host: str, port: int, timeout: int = 60, check_interval: float = 1.0) -> bool:
    """Wait for a port to become available with a maximum timeout."""
    print(f"Waiting for {host}:{port} to become available...")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if is_port_open(host, port):
            return True
        time.sleep(check_interval)
    
    return False

def main():
    # Configuration
    HOST = "localhost"
    PORT = 8501
    MAX_WAIT_TIME = 120  # seconds
    SHOW_LOGS = True  # Set to False to run in detached mode without logs
    
    try:
        # Step 1: Check if docker-compose.yaml exists
        if not os.path.exists("docker-compose.yaml"):
            print("Error: docker-compose.yaml not found in current directory")
            sys.exit(1)
        
        # Step 2: Start Docker Compose
        print("Starting Docker Compose...")
        
        if SHOW_LOGS:
            # Option 1: Start with logs visible (non-detached mode)
            print("Starting with logs visible...")
            process = subprocess.Popen(
                ["docker-compose", "up"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Start a thread to print logs in real-time
            import threading
            
            def print_logs():
                for line in iter(process.stdout.readline, ''):
                    if line:
                        print(f"📋 {line.rstrip()}")
            
            log_thread = threading.Thread(target=print_logs, daemon=True)
            log_thread.start()
            
        else:
            # Option 2: Start in detached mode
            process = subprocess.Popen(
                ["docker-compose", "up", "-d"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a moment for the command to execute
            time.sleep(2)
            
            # Check if docker-compose command succeeded
            if process.poll() is not None and process.returncode != 0:
                stdout, stderr = process.communicate()
                print(f"Error starting Docker Compose: {stderr}")
                sys.exit(1)
        
        # Step 3: Wait for port to be available
        if wait_for_port(HOST, PORT, MAX_WAIT_TIME):
            print(f"✅ Streamlit is ready on {HOST}:{PORT}")
            
            # Step 4: Launch browser
            print("Launching browser...")
            webbrowser.open(f"http://{HOST}:{PORT}")
            
            if SHOW_LOGS:
                print("Browser launched. Logs are shown above. Press Ctrl+C to stop the services.")
            else:
                print("Browser launched. Use 'docker-compose logs -f' to see logs. Press Ctrl+C to stop the services.")
            
            # Keep the script running so user can stop it with Ctrl+C
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n🛑 Stopping Docker Compose services...")
                if SHOW_LOGS and process.poll() is None:
                    process.terminate()
                subprocess.run(["docker-compose", "down"], capture_output=True)
                print("Services stopped.")
                
        else:
            print(f"❌ Timeout: Streamlit did not start on {HOST}:{PORT} within {MAX_WAIT_TIME} seconds")
            print("Stopping Docker Compose services...")
            subprocess.run(["docker-compose", "down"], capture_output=True)
            sys.exit(1)
            
    except FileNotFoundError:
        print("Error: docker-compose command not found. Please install Docker Compose.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user. Stopping Docker Compose services...")
        subprocess.run(["docker-compose", "down"], capture_output=True)
        sys.exit(0)
    except Exception as e:
        print(f"Unexpected error: {e}")
        subprocess.run(["docker-compose", "down"], capture_output=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
