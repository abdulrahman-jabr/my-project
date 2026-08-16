import asyncio
import socket
import argparse
import sys
from datetime import datetime
from ipaddress import ip_address, ip_network


# ---------------------------------------------------------
# Tool: Advanced Asynchronous Port Scanner
# Author: Abdulrahman Jabr (@abdulrahman-jabr)
# Description: Minimalistic & High-Performance TCP Port Scanner 
#              using Python's asyncio library for concurrency.
# ---------------------------------------------------------

class PortScanner:
    def __init__(self, target, ports, timeout):
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.open_ports = []

    async def _check_port(self, port):
        """
        Attempts to connect to a specific TCP port on the target.
        If connection succeeds, the port is marked as open.
        """
        conn_coro = asyncio.open_connection(self.target, port)
        try:
            # Try connecting within the timeout limits
            _, _ = await asyncio.wait_for(conn_coro, timeout=self.timeout)
            # Successfully connected
            self.open_ports.append(port)
        except (asyncio.TimeoutError, ConnectionRefusedError, socket.error):
            # Port closed or filtered
            pass

    async def run(self):
        """
        Orchestrates the scanning process, creating asynchronous tasks 
        for each port.
        """
        print(f"\n[+] Scanning Target: {self.target}")
        print(f"[+] Ports to scan: {min(self.ports)} - {max(self.ports)}")
        print(f"[+] Scanning started at: {datetime.now()}\n")

        # Create a list of async coroutine tasks for each port
        tasks = [self._check_port(p) for p in self.ports]
        
        # Execute all tasks concurrently and wait for them to finish
        await asyncio.gather(*tasks)

        # Print results
        print("-" * 40)
        print("Final Results:")
        print("-" * 40)
        if self.open_ports:
            # Sort open ports before printing
            self.open_ports.sort()
            for op in self.open_ports:
                print(f"[+] Port {op}: OPEN")
        else:
            print("[!] No open ports found on the target.")
        
        print("-" * 40)
        print(f"[*] Completed in: {datetime.now()}")


def parse_arguments():
    """
    Handles command-line argument parsing.
    """
    parser = argparse.ArgumentParser(
        description="High-Performance Asynchronous TCP Port Scanner.",
        epilog="Usage Example: python async_port_scanner.py 192.168.1.1 --ports 1-1024"
    )
    
    # Required: Target IP/Hostname
    parser.add_argument("target", help="Target IP address or hostname to scan.")
    
    # Optional: Port range (default 1-65535)
    parser.add_argument(
        "--ports", "-p",
        default="1-65535",
        help="Port range to scan (e.g., 80, 1-1024, or 1-65535)."
    )
    
    # Optional: Connection Timeout (default 0.5 seconds)
    parser.add_argument(
        "--timeout", "-t",
        type=float,
        default=0.5,
        help="Connection timeout in seconds (default: 0.5)."
    )
    
    return parser.parse_args()


def validate_target(target):
    """
    Validates if the target input is a proper IP or Hostname.
    """
    try:
        # Check if it's a valid individual IP address
        ip_address(target)
        return target
    except ValueError:
        try:
            # Check if it's a valid network (CIDR notation) - 
            # In this minimalistic tool, we restrict to single IP.
            # However, this adds depth to target validation logic.
            raise ValueError
        except:
            # Assume it's a hostname and try resolving it
            try:
                resolved_ip = socket.gethostbyname(target)
                return resolved_ip
            except socket.gaierror:
                print(f"[!] Error: Unable to resolve hostname or invalid IP: '{target}'.")
                sys.exit(1)


def parse_ports(port_arg):
    """
    Parses the port range argument string into a list of integers.
    Supports single ports, comma-separated ports, and ranges.
    """
    ports = []
    try:
        if '-' in port_arg:
            # Case: 1-1024
            start, end = map(int, port_arg.split('-'))
            if start < 1 or end > 65535 or start > end:
                raise ValueError
            ports = list(range(start, end + 1))
        elif ',' in port_arg:
            # Case: 80,443
            ports = [int(p) for p in port_arg.split(',') if 1 <= int(p) <= 65535]
        else:
            # Case: Single port 80
            p = int(port_arg)
            if 1 <= p <= 65535:
                ports.append(p)
            else:
                raise ValueError
                
        if not ports:
            raise ValueError
            
        return ports
    except (ValueError, TypeError):
        print(f"[!] Error: Invalid port range argument: '{port_arg}'. Must be between 1-65535.")
        sys.exit(1)


def main():
    """
    The main entry point of the script.
    """
    # 1. Parse CLI arguments
    args = parse_arguments()
    
    # 2. Validate and resolve target
    resolved_target = validate_target(args.target)
    
    # 3. Parse port range
    ports_to_scan = parse_ports(args.ports)
    
    # 4. Initiate the scanner object
    scanner = PortScanner(resolved_target, ports_to_scan, args.timeout)
    
    # 5. Execute the scanner asynchronously
    try:
        # For compatibility with different Python versions:
        if sys.version_info >= (3, 7):
            asyncio.run(scanner.run())
        else:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(scanner.run())
            loop.close()
    except KeyboardInterrupt:
        print("\n[!] Execution interrupted by user. Exiting...\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    # Ensure tool prints header (adds professionalism)
    print("\n=============================================")
    print("      AsyncPortScanner - Professional TCP Port Tool")
    print("=============================================")
    main()
