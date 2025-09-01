from http.server import BaseHTTPRequestHandler, HTTPServer
import html

HOST, PORT = "127.0.0.1", 8000

# Data: TCP/IP protocol suite grouped by layer
TCP_IP_PROTOCOLS = {
    "Application Layer": [
        "HTTP / HTTPS", "DNS", "SMTP", "IMAP", "POP3",
        "FTP", "DHCP", "SNMP", "NTP", "SSH", "Telnet",
        "TLS/SSL", "MQTT"
    ],
    "Transport Layer": [
        "TCP", "UDP", "SCTP", "DCCP"
    ],
    "Internet Layer": [
        "IPv4", "IPv6", "ICMP", "IGMP", "IPsec"
    ],
    "Link (Network Access) Layer": [
        "Ethernet (IEEE 802.3)", "Wi-Fi (IEEE 802.11)", "ARP", "PPP"
    ]
}

def page(title: str, body_html: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
  <style>
    :root {{ font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif; }}
    body {{ margin: 0; background: #f7f7fb; color: #1f2937; }}
    header {{ background: #111827; color: white; padding: 1rem 1.25rem; }}
    header h1 {{ margin: 0; font-size: 1.25rem; }}
    nav a {{ color: #93c5fd; margin-right: 1rem; text-decoration: none; }}
    main {{ max-width: 900px; margin: 2rem auto; padding: 0 1rem; }}
    .card {{ background: white; border-radius: 14px; padding: 1.25rem; box-shadow: 0 6px 20px rgba(0,0,0,0.06); }}
    .grid {{ display: grid; gap: 1rem; }}
    @media(min-width: 700px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    h2 {{ margin: 0.25rem 0 0.75rem; font-size: 1.1rem; }}
    ul {{ margin: 0; padding-left: 1.1rem; }}
    footer {{ text-align:center; color:#6b7280; padding: 2rem 1rem; font-size: .9rem; }}
    .btn {{ display:inline-block; padding:.6rem .9rem; border-radius:10px; background:#111827; color:#fff; text-decoration:none; }}
    .muted {{ color:#6b7280; }}
  </style>
</head>
<body>
  <header>
    <h1>Mini Web Server Demo</h1>
    <nav>
      <a href="/">Home</a>
      <a href="/protocols">TCP/IP Protocols</a>
    </nav>
  </header>
  <main>
    {body_html}
  </main>
  <footer>Running on http://{HOST}:{PORT}</footer>
</body>
</html>"""

def home_page():
    return page(
        "Home",
        """
        <div class="card">
          <h2>Welcome 👋</h2>
          <p>This is a simple Python web server that serves HTML pages.</p>
          <p>Use the navigation above or jump straight to the protocol list:</p>
          <p><a class="btn" href="/protocols">View TCP/IP Protocol Suite</a></p>
          <p class="muted">Built with <code>http.server</code> from Python’s standard library.</p>
        </div>
        """
    )

def protocols_page():
    # Build a nice grid of layers and protocols
    sections = []
    for layer, protos in TCP_IP_PROTOCOLS.items():
        items = "".join(f"<li>{html.escape(p)}</li>" for p in protos)
        sections.append(f"""
          <section class="card">
            <h2>{html.escape(layer)}</h2>
            <ul>{items}</ul>
          </section>
        """)
    body = f"""
      <div class="grid">
        {''.join(sections)}
      </div>
    """
    return page("TCP/IP Protocol Suite", body)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            content = home_page().encode("utf-8")
            self._send(200, content, "text/html; charset=utf-8")
        elif self.path == "/protocols":
            content = protocols_page().encode("utf-8")
            self._send(200, content, "text/html; charset=utf-8")
        else:
            self._send(404, b"Not Found", "text/plain; charset=utf-8")

    def _send(self, code, content: bytes, content_type: str):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

if __name__ == "__main__":
    print(f"Serving on http://{HOST}:{PORT} (Ctrl+C to stop)")
    HTTPServer((HOST, PORT), Handler).serve_forever()
