import json, sys
from client import PricingModelIterationSimulatorClient

def handle_mcp_request(payload):
    method = payload.get("method")
    req_id = payload.get("id", 1)
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"protocolVersion": "2024-11-05", "serverInfo": {"name": "pricing-model-iteration-simulator", "version": "1.0.0"}}}
    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [{"name": "simulate_pricing_iteration", "description": "Simulates seat-based, usage-based, and hybrid pricing models side-by-side to identify optimal revenue strategy."}]}}
    elif method == "tools/call":
        client = PricingModelIterationSimulatorClient()
        res = client.simulate_pricing_iteration()
        return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
    return {"jsonrpc": "2.0", "id": req_id, "result": {"status": "ACTIVE"}}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(handle_mcp_request({"method": "tools/list"})))
    else:
        client = PricingModelIterationSimulatorClient()
        print(json.dumps(client.simulate_pricing_iteration(), indent=2))
