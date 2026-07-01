import requests
import socket
import ssl
from urllib.parse import urlparse

# ---------- SSL CHECK ----------
def check_ssl(url):
    try:
        hostname = urlparse(url).hostname

        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        return {"valid": True, "score": 20}
    except:
        return {"valid": False, "score": 0}


# ---------- HEADER CHECK ----------
def check_headers(url):
    try:
        res = requests.get(url, timeout=5)
        headers = res.headers

        score = 30
        missing = []

        if "Content-Security-Policy" not in headers:
            score -= 10
            missing.append("CSP")

        if "X-Frame-Options" not in headers:
            score -= 10
            missing.append("XFO")

        if "Strict-Transport-Security" not in headers:
            score -= 10
            missing.append("HSTS")

        return {"score": score, "missing": missing}
    except:
        return {"score": 0, "missing": ["error"]}


# ---------- PORT CHECK ----------
def check_ports(url):
    hostname = urlparse(url).hostname
    ports = [22, 3306, 5432]

    open_ports = []

    for port in ports:
        try:
            sock = socket.socket()
            sock.settimeout(1)
            result = sock.connect_ex((hostname, port))

            if result == 0:
                open_ports.append(port)

            sock.close()
        except:
            pass

    score = 20 - (len(open_ports) * 5)
    return {"open_ports": open_ports, "score": score}


# ---------- VULNERABILITY CHECK ----------
def check_vulns(url):
    try:
        test_url = url + "?id=1'"
        res = requests.get(test_url, timeout=5)

        if "sql" in res.text.lower():
            return {"sqli": True, "score": 0}

        return {"sqli": False, "score": 20}
    except:
        return {"sqli": False, "score": 10}


# ---------- RISK ENGINE ----------
def calculate_risk(data):
    total = (
        data["ssl"]["score"] +
        data["headers"]["score"] +
        data["ports"]["score"] +
        data["vulns"]["score"]
    )

    if total >= 70:
        risk = "LOW"
    elif total >= 40:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {"score": total, "risk": risk}


# ---------- MAIN SCAN ----------
def run_scan(url):
    if not url.startswith("http"):
        url = "https://" + url

    ssl_r = check_ssl(url)
    head_r = check_headers(url)
    port_r = check_ports(url)
    vuln_r = check_vulns(url)

    data = {
        "ssl": ssl_r,
        "headers": head_r,
        "ports": port_r,
        "vulns": vuln_r
    }

    risk = calculate_risk(data)

    return {
        "url": url,
        "data": data,
        "risk": risk
    }


# ---------- TEST ----------
if __name__ == "__main__":
    result = run_scan("https://google.com")
    print(result)