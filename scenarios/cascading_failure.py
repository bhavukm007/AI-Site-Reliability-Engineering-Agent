def simulate():
    print("Simulating cascading failure...")

    logs = []
    logs.append("ERROR: service A failed")
    logs.append("ERROR: service B timeout")
    logs.append("CRITICAL: service C crashed")

    return "\n".join(logs)