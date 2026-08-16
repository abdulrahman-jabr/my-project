# High-Performance Asynchronous TCP Port Scanner

A professional, minimal, and high-speed TCP Port Scanner written in Python. This tool leverages the `asyncio` library for asynchronous input/output, allowing it to scan thousands of ports concurrently, offering a significant speed advantage over traditional synchronous scanners.

## Features
- **Asynchronous & Concurrent**: Drastically reduces scanning time by handling multiple port connection attempts simultaneously.
- **Robust Argument Parsing**: Flexible command-line interface supporting hostnames/IPs and port ranges (`1-1024`, `80`, `22,80,443`).
- **Target Validation**: Resolves hostnames and validates IP inputs.
- **Customizable Timeout**: Fine-tune the connection timeout for reliable results across different network environments.

## Prerequisite
- Python 3.6 or higher.

## Usage

```bash
# Basic scan: Scan ports 1 to 1024 (default) on localhost
python async_port_scanner.py 127.0.0.1 --ports 1-1024

# Full scan: Scan all 65535 ports on a target
python async_port_scanner.py <target_ip> --ports 1-65535

# Targeted scan: Scan common web ports
python async_port_scanner.py <target_ip> --ports 80,443,8080

# Advanced: Full scan on a target hostname with a 1-second timeout
python async_port_scanner.py myserver.example.com --ports 1-65535 --timeout 1.0
