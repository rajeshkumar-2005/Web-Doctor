def generate_pdf(data):
    filename = "report.txt"

    with open(filename, "w") as f:
        f.write("Web Doctor Security Audit Report\n")
        f.write("="*40 + "\n\n")

        f.write(f"URL: {data['url']}\n")
        f.write(f"Risk: {data['risk']['risk']}\n")
        f.write(f"Score: {data['risk']['score']}\n\n")

        f.write("Findings:\n")

        if not data["data"]["ssl"]["valid"]:
            f.write("- SSL not valid\n")

        if data["data"]["headers"]["missing"]:
            f.write(f"- Missing headers: {data['data']['headers']['missing']}\n")

        if data["data"]["ports"]["open_ports"]:
            f.write(f"- Open ports: {data['data']['ports']['open_ports']}\n")

        if data["data"]["vulns"]["sqli"]:
            f.write("- SQL Injection risk detected\n")

    return filename