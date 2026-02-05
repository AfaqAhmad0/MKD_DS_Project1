# =============================================================================
# Marketing Assistant AI - Application Runner
# =============================================================================
# Convenience script to run the application.
# This provides an easy way to start the server without remembering uvicorn args.
#
# Usage:
#   python run.py
#   python run.py --port 8080
#   python run.py --reload
# =============================================================================

import argparse
import socket
import uvicorn

from backend.config import settings


def _get_lan_ip() -> str:
    """
    Best-effort LAN IP detection for display purposes.
    Falls back to localhost if detection fails.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            # The address doesn't need to be reachable; no packets are sent.
            sock.connect(("8.8.8.8", 80))
            return sock.getsockname()[0]
    except OSError:
        return "127.0.0.1"


def main():
    """
    Main function to run the Marketing Assistant AI server.
    
    Parses command-line arguments and starts the uvicorn server
    with appropriate configuration.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Run the Marketing Assistant AI server"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default=settings.api_host,
        help=f"Host to bind to (default: {settings.api_host})"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=settings.api_port,
        help=f"Port to bind to (default: {settings.api_port})"
    )
    
    parser.add_argument(
        "--reload",
        action="store_true",
        default=settings.debug,
        help="Enable auto-reload on code changes"
    )
    
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of worker processes (default: 1)"
    )
    
    args = parser.parse_args()
    
    # Print startup banner
    print("=" * 60)
    print("  Marketing Assistant AI")
    print("=" * 60)
    display_host = _get_lan_ip() if args.host == "0.0.0.0" else args.host
    print(f"  Starting server at http://{display_host}:{args.port}")
    print(f"  API Documentation: http://{display_host}:{args.port}/docs")
    print(f"  Auto-reload: {'enabled' if args.reload else 'disabled'}")
    print("=" * 60)
    print()
    
    # Run the server
    uvicorn.run(
        "backend.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        workers=args.workers if not args.reload else 1,  # Can't use workers with reload
        log_level="debug" if settings.debug else "info"
    )


if __name__ == "__main__":
    main()
