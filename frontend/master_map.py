import urllib.parse
import streamlit as st

def build_master_map_url():
    """Build a horizontal Business Master Map flowchart URL using QuickChart Graphviz API."""
    steps = st.session_state.get('master_steps', [])
    if not steps:
        return None
        
    dot = 'digraph G {\n'
    dot += '    rankdir=LR;\n'
    dot += '    splines=ortho;\n'
    dot += '    nodesep=0.4;\n'
    dot += '    ranksep=0.6;\n'
    dot += '    bgcolor="white";\n'
    dot += '    node [shape=box, fontname="Malgun Gothic", fontsize=10, style="filled", fillcolor="white", color="black"];\n'
    dot += '    edge [color="#334155", penwidth=1.0, fontname="Malgun Gothic", fontsize=9];\n'
    
    # Define Column Headers (as invisible nodes to force rank alignment, or just drawn at top)
    # We can use a subgraph or just rely on Graphviz's natural LR ranking.
    # But for a strict table-like look, HTML tables are better, OR we just let Graphviz do it.
    
    prev_main = None
    
    for i, step in enumerate(steps):
        # Center: Main Process
        main_id = f"main_{i}"
        main_lbl = step.get('main_process', '').replace('\n', '\\n').replace('"', '\\"')
        dot += f'    {main_id} [label="{main_lbl}", penwidth=2.0];\n'
        
        # Connect main processes vertically
        if prev_main:
            dot += f'    {prev_main} -> {main_id} [style=invis];\n'
        prev_main = main_id
        
        # Left side: Pre-activity
        act_l_id = f"act_l_{i}"
        act_l_lbl = step.get('pre_activity', '').replace('\n', '\\n').replace('"', '\\"')
        if act_l_lbl:
            dot += f'    {act_l_id} [label="{act_l_lbl}"];\n'
            dot += f'    {act_l_id} -> {main_id};\n'
            
        # Left-Left: Incoming Data
        for j, inc in enumerate(step.get('incoming_data', [])):
            inc_id = f"inc_{i}_{j}"
            inc_lbl = inc.get('label', '').replace('\n', '\\n').replace('"', '\\"')
            inc_dept = inc.get('department', '').replace('"', '\\"')
            full_inc_lbl = f"{inc_lbl}\\n({inc_dept})"
            dot += f'    {inc_id} [label="{full_inc_lbl}"];\n'
            dot += f'    {inc_id} -> {act_l_id if act_l_lbl else main_id};\n'
            
        # Right side: Post-activity
        act_r_id = f"act_r_{i}"
        act_r_lbl = step.get('post_activity', '').replace('\n', '\\n').replace('"', '\\"')
        if act_r_lbl:
            dot += f'    {act_r_id} [label="{act_r_lbl}"];\n'
            dot += f'    {main_id} -> {act_r_id};\n'
            
        # Right-Right: Outgoing Data
        for j, out in enumerate(step.get('outgoing_data', [])):
            out_id = f"out_{i}_{j}"
            out_lbl = out.get('label', '').replace('\n', '\\n').replace('"', '\\"')
            out_dept = out.get('department', '').replace('"', '\\"')
            full_out_lbl = f"{out_lbl}\\n({out_dept})"
            dot += f'    {out_id} [label="{full_out_lbl}"];\n'
            dot += f'    {act_r_id if act_r_lbl else main_id} -> {out_id};\n'
            
        # Far Right: Standards
        std_lbl = step.get('standards', '').replace('\n', '\\n').replace('"', '\\"')
        if std_lbl:
            std_id = f"std_{i}"
            dot += f'    {std_id} [label="{std_lbl}", style="dashed,filled", color="#64748b"];\n'
            # To ensure it stays on the far right, connect it with an invisible edge or real edge
            # In the screenshot, it's just listed. We can link it with a dashed edge.
            out_target = f"out_{i}_0" if step.get('outgoing_data') else (act_r_id if act_r_lbl else main_id)
            dot += f'    {out_target} -> {std_id} [style=dashed, arrowhead=none];\n'
            
    dot += '}\n'
    encoded = urllib.parse.quote(dot)
    return f"https://quickchart.io/graphviz?format=png&graph={encoded}"
