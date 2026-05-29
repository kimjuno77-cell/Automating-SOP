import requests

dot = """digraph G {
    rankdir=TB;
    splines=ortho;
    margin=0.5;
    node_0 [label="사장"];
    node_1 [label="팀장1"];
    node_2 [label="팀장2"];
    node_3 [label="팀장3"];
    node_4 [label="팀장4"];
    node_5 [label="팀장5"];
    node_0 -> node_1;
    node_0 -> node_2;
    node_0 -> node_3;
    node_0 -> node_4;
    node_0 -> node_5;
    { rank=same; node_1; node_2; node_3; node_4; node_5; }
}"""

resp = requests.post("https://quickchart.io/graphviz", json={"graph": dot, "format": "png"})
with open("test_ortho.png", "wb") as f:
    f.write(resp.content)
