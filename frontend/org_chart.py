import urllib.parse
import streamlit as st
from collections import defaultdict

def build_org_chart_url():
    """Build a vertical Org Chart flowchart URL using QuickChart Graphviz API.
    Supports hierarchical (상하관계) and parallel (평행관계) layouts.
    Nodes with the same parent are automatically placed on the same rank (parallel).
    """
    roles = st.session_state.get('org_roles', [])
    if not roles:
        return None
        
    dot = 'digraph G {\n'
    dot += '    rankdir=TB;\n'
    dot += '    splines=ortho;\n'
    dot += '    nodesep=1.0;\n'
    dot += '    ranksep=1.0;\n'
    dot += '    node [shape=plaintext, fontname="Malgun Gothic", fontsize=10];\n'
    dot += '    edge [color="#334155", penwidth=1.5];\n'
    
    # Build nodes
    for i, role in enumerate(roles):
        name = role.get('role_name', '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        desc = role.get('role_desc', '').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        resp_lines = role.get('responsibilities', '').split('\n')
        
        # Build HTML table for the node (matching the user's reference image style)
        html_label = '<<TABLE BORDER="2" CELLBORDER="0" CELLSPACING="0" CELLPADDING="6" COLOR="#1e3a5f">\n'
        # Title row with blue background and underline
        html_label += f'  <TR><TD BGCOLOR="#1e3a5f"><FONT COLOR="white"><B><U>{name}</U></B></FONT></TD></TR>\n'
        if desc.strip():
            html_label += f'  <TR><TD ALIGN="CENTER" BGCOLOR="#f0f4f8">{desc}</TD></TR>\n'
        
        # Responsibilities with left alignment
        if any(r.strip() for r in resp_lines):
            html_label += '  <TR><TD ALIGN="LEFT" BGCOLOR="white">'
            for r in resp_lines:
                if r.strip():
                    html_label += f'{r.strip()}<BR ALIGN="LEFT"/>'
            html_label += '</TD></TR>\n'
            
        html_label += '</TABLE>>'
        
        dot += f'    node_{i} [label={html_label}];\n'
    
    # Build edges and group siblings for parallel rank
    children_by_parent = defaultdict(list)
    for i, role in enumerate(roles):
        parent_idx = role.get('parent_idx')
        if parent_idx is not None and 0 <= parent_idx < len(roles) and parent_idx != i:
            dot += f'    node_{parent_idx} -> node_{i};\n'
            children_by_parent[parent_idx].append(i)
    
    # Force same-rank for siblings (平行관계)
    for parent_idx, child_indices in children_by_parent.items():
        if len(child_indices) > 1:
            nodes_str = '; '.join(f'node_{c}' for c in child_indices)
            dot += f'    {{ rank=same; {nodes_str}; }}\n'
            
    dot += '}\n'
    encoded = urllib.parse.quote(dot)
    return f"https://quickchart.io/graphviz?format=png&graph={encoded}"
