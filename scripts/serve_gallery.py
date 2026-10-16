#!/usr/bin/env python3
"""Serve an images folder over http and open its gallery, so the page discovers images by itself.

Usage (from the repo root):
    python3 scripts/serve_gallery.py manga-dev/generated          # http://localhost:8765/
    python3 scripts/serve_gallery.py style-picks-generated --port 9000

The page reads the folder listing and re-checks it every 10 seconds, so new images
(for example while generation is running) appear without rebuilding anything.
Stop with Ctrl+C.
"""

import argparse
import functools
import json
import http.server
import sys
import threading
import webbrowser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_gallery  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("folder", nargs="?", default="manga-dev/generated")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--no-open", action="store_true", help="do not open the browser")
    args = p.parse_args()
    folder = ROOT / args.folder
    folder.mkdir(parents=True, exist_ok=True)
    if not (folder / "index.html").exists():
        build_gallery.build(folder)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):  # keep the console quiet
            pass

        def do_GET(self):
            if self.path.split("?")[0] == "/__list":  # JSON list of files for the page
                body = json.dumps(sorted(f.name for f in folder.iterdir() if f.is_file())).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)
                return
            super().do_GET()

    handler = functools.partial(Handler, directory=str(folder))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", args.port), handler)
    url = f"http://localhost:{args.port}/"
    print(f"Gallery for {args.folder}: {url}  (Ctrl+C to stop)")
    if not args.no_open:
        threading.Timer(0.5, webbrowser.open, [url]).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
