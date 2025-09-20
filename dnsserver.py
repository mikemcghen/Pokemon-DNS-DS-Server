from dnslib import DNSRecord, QTYPE, RR, A
from dnslib.server import DNSServer, BaseResolver
import socket
import datetime

# Your server's LAN IP
REDIRECT_IP = "192.168.0.30"
LOG_FILE = "dns_queries.log"

def log_query(qname, qtype, action, target):
    """Log queries to a file and print them to console"""
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {qname} ({qtype}) -> {action} {target}\n"
    print(line.strip())
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line)

class NintendoResolver(BaseResolver):
    def resolve(self, request, handler):
        reply = request.reply()
        qname = str(request.q.qname)
        qtype = QTYPE[request.q.qtype]

        # Redirect Nintendo domains to our Flask server
        if "nintendowifi.net" in qname.lower() or "nintendo.net" in qname.lower():
            reply.add_answer(RR(request.q.qname, QTYPE.A, rdata=A(REDIRECT_IP), ttl=60))
            log_query(qname, qtype, "REDIRECT", REDIRECT_IP)
        else:
            # Forward everything else
            try:
                ip = socket.gethostbyname(qname[:-1])  # strip trailing dot
                reply.add_answer(RR(request.q.qname, QTYPE.A, rdata=A(ip), ttl=60))
                log_query(qname, qtype, "FORWARD", ip)
            except Exception as e:
                log_query(qname, qtype, "FAILED", str(e))

        return reply

if __name__ == "__main__":
    resolver = NintendoResolver()
    server = DNSServer(resolver, port=53, address="0.0.0.0", tcp=False)
    print(f"[*] DNS server started on 0.0.0.0:53 (redirecting Nintendo domains to {REDIRECT_IP})")
    server.start()
