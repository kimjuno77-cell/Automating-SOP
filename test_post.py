import requests

dot = """digraph G {
    rankdir=TB;
    node [shape=box];
    A [label="Test Node 1"];
    B [label="Test Node 2"];
    A -> B;
}"""

resp = requests.post("https://quickchart.io/graphviz", json={"graph": dot, "format": "png"}, timeout=10)
print(f"Status: {resp.status_code}")
print(f"Content-Type: {resp.headers.get('content-type')}")
print(f"Size: {len(resp.content)} bytes")
