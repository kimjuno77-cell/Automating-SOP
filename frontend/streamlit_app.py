import streamlit as st
import requests
import json
import urllib.parse
import copy
import streamlit.components.v1 as components
from PIL import Image
import os
from samples import SAMPLES, SAMPLE_NAMES
from org_chart import build_org_chart_url
from master_map import build_master_map_url
import tab2_ui
import tab3_ui
import importlib
importlib.reload(tab2_ui)
importlib.reload(tab3_ui)
from tab2_ui import render_tab2
from tab3_ui import render_tab3

def open_explorer_folder(folder_path):
    try:
        norm_path = os.path.abspath(folder_path)
        if os.path.exists(norm_path):
            os.startfile(norm_path)
    except Exception as e:
        pass

# --- Configuration & Theme ---
st.set_page_config(
    page_title="SOP Auto-Generator | EMKO",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look & Theme Compatibility
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Outfit:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Global Header Style */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
    }
    
    /* Button Styling */
    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    /* Step card styling */
    .step-card {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #bae6fd;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 8px;
        position: relative;
    }
    @media (prefers-color-scheme: dark) {
        .step-card {
            background: linear-gradient(135deg, #0c4a6e 0%, #164e63 100%) !important;
            border-color: #0e7490 !important;
        }
    }
    
    .step-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 8px;
    }
    
    .step-number {
        background: linear-gradient(135deg, #0284c7, #0369a1);
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        flex-shrink: 0;
    }
    
    .step-title {
        font-weight: 600;
        font-size: 0.95rem;
        color: #0c4a6e;
    }
    @media (prefers-color-scheme: dark) {
        .step-title { color: #7dd3fc !important; }
    }
    
    /* Arrow connector between steps */
    .arrow-connector {
        text-align: center;
        font-size: 1.2rem;
        color: #0369a1;
        margin: -4px 0;
        line-height: 1;
    }
    @media (prefers-color-scheme: dark) {
        .arrow-connector { color: #38bdf8 !important; }
    }
    
    /* Flowchart container */
    .flowchart-container {
        border: 2px solid #cbd5e1;
        border-radius: 12px;
        padding: 16px;
        background: #ffffff;
        min-height: 400px;
    }
    @media (prefers-color-scheme: dark) {
        .flowchart-container {
            background: #1e293b !important;
            border-color: #475569 !important;
        }
    }
    
    /* Table header style */
    .table-header {
        background-color: #1e293b;
        color: white;
        padding: 10px 8px;
        border-radius: 5px;
        text-align: center;
        font-weight: bold;
        font-size: 0.85rem;
    }
    
    /* Insert button styling */
    .insert-btn button {
        font-size: 0.75rem !important;
        padding: 2px 8px !important;
        border-radius: 20px !important;
    }
    
    /* Light Mode Specifics */
    [data-theme="light"] .main {
        background: linear-gradient(135deg, #f8faff 0%, #eef2f7 100%);
    }
    [data-theme="light"] h1, [data-theme="light"] h2, [data-theme="light"] h3 {
        color: #1e293b;
    }
    
    /* Dark Mode Visibility Fixes */
    @media (prefers-color-scheme: dark) {
        .stMarkdown div p, .stMarkdown div h1, .stMarkdown div h2, .stMarkdown div h3, 
        label, .stWidgetLabel p, [data-testid="stWidgetLabel"] p {
            color: #ffffff !important;
            font-weight: 500;
        }
        .st-emotion-cache-pge3iw, .st-emotion-cache-1h9up9z p {
            color: #ffffff !important;
        }
        small, .stCaption {
            color: #cbd5e1 !important;
        }
        [data-testid="stSidebar"] {
            background-color: #0f172a !important;
        }
    }
    
    /* AI Polish Button Gradient */
    .ai-button button {
        background: linear-gradient(90deg, #6366f1 0%, #a855f7 100%) !important;
        color: white !important;
        border: none !important;
    }
    
    /* Expander Container Style */
    .stExpander {
        border-radius: 15px !important;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    @media (prefers-color-scheme: dark) {
        .stExpander {
            border-color: #334155 !important;
            background-color: #1e293b !important;
        }
    }

    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    if os.path.exists("EMKO Logo.png"):
        st.image("EMKO Logo.png", width=180)
    
    st.title("⚙️ 문서 설정")
    
    # --- Sample Template Selector ---
    st.markdown("#### 📑 샘플 양식 선택")
    if 'current_sample' not in st.session_state:
        st.session_state.current_sample = SAMPLE_NAMES[0]
    if 'form_key_suffix' not in st.session_state:
        st.session_state.form_key_suffix = 0
        
    # Default data for new tabs
    if 'org_roles' not in st.session_state:
        st.session_state.org_roles = [
            {"role_name": "환경사업본부사장", "role_desc": "환경사업본부 전체 관리 및 감독", "responsibilities": "", "parent_idx": None},
            {"role_name": "기술팀장", "role_desc": "팀 및 PROJECT 업무관리감독", "responsibilities": "- 설계업무 수행계획서 검토 및 승인\n- DESIGN PLAN 검토 및 승인\n- 설계 M/H 관리", "parent_idx": 0},
            {"role_name": "사업(영업)팀장", "role_desc": "사업 수주 및 영업 관리", "responsibilities": "- 사업수행 계획서 검토 및 승인\n- Project Master Schedule 관리", "parent_idx": 0},
            {"role_name": "품질보증팀장", "role_desc": "품질 관리 및 감독", "responsibilities": "- ISO 관련 업무 절차 관리\n- 설계 품질관리 이행 및 설계요원의 품질교육", "parent_idx": 0},
            {"role_name": "전계장팀장", "role_desc": "전기/계장 설계 관리", "responsibilities": "- 전기/계장 설계 업무 총괄\n- 관련 도면 검토 및 승인", "parent_idx": 0},
            {"role_name": "프로 (기술팀)", "role_desc": "기술팀 프로 엔지니어", "responsibilities": "- 설계 업무지시 및 관리\n- 설계 계산서 및 도면 검증\n- M/R 작성 및 검증", "parent_idx": 1},
            {"role_name": "엔지니어 (기술팀)", "role_desc": "기술팀 엔지니어", "responsibilities": "- 설계업무 수행\n- SPEC 작성\n- M/R 작성\n- V/P 검토", "parent_idx": 1},
            {"role_name": "프로 (사업팀)", "role_desc": "사업팀 프로", "responsibilities": "- 사업 관리 및 조정\n- 고객 커뮤니케이션", "parent_idx": 2},
            {"role_name": "프로 (전계장팀)", "role_desc": "전계장팀 프로", "responsibilities": "- 전기/계장 설계 수행\n- 관련 도면 작성 및 검증", "parent_idx": 4}
        ]
    if 'org_form_key' not in st.session_state:
        st.session_state.org_form_key = 0
    if 'master_steps' not in st.session_state:
        st.session_state.master_steps = [
            {
                "main_process": "Project Kick-Off Meeting",
                "pre_activity": "사업수행 계획서 검토",
                "post_activity": "장치 설계업무 수행계획서 작성",
                "incoming_data": [{"label": "자료 검토 요청", "department": "사업팀"}],
                "outgoing_data": [{"label": "자체 보관", "department": "-"}],
                "standards": "기계설계업무 절차서"
            }
        ]
    
    selected_sample = st.selectbox(
        "초안 작성에 활용할 샘플을 선택하세요",
        SAMPLE_NAMES,
        index=SAMPLE_NAMES.index(st.session_state.current_sample),
        key="sample_selector"
    )
    
    if selected_sample != st.session_state.current_sample:
        st.session_state.current_sample = selected_sample
        sample_data = SAMPLES.get(selected_sample)
        if sample_data is not None:
            st.session_state.steps = copy.deepcopy(sample_data["steps"])
            st.session_state.sample_ref_no = sample_data["ref_no"]
            st.session_state.sample_title = sample_data["title"]
        else:
            # 직접 입력: reset to empty single step
            st.session_state.steps = [{
                "id": "S1", "activity": "새 업무 활동", "dept": "부서명",
                "related_docs": [], "points": "", "timing": "",
                "input_data": "", "output_data": "", "standards": ""
            }]
            st.session_state.sample_ref_no = "별첨 3-"
            st.session_state.sample_title = ""
            
        # Increment the form key suffix to force Streamlit to recreate all widget keys
        st.session_state.form_key_suffix += 1
            
        st.rerun()
    
    st.markdown("---")
    
    # Use sample values as defaults for ref_no and title
    default_ref = st.session_state.get('sample_ref_no', '별첨 3-4')
    default_title = st.session_state.get('sample_title', 'MATERIAL REQUISITION 작성')
    ref_no = st.text_input("별첨 번호 (예: 별첨 3-4)", default_ref, key=f"ref_no_input_{st.session_state.form_key_suffix}")
    map_title = st.text_input("업무 명칭 (제목)", default_title, key=f"map_title_input_{st.session_state.form_key_suffix}")
    
    st.markdown("---")
    st.markdown("### 📁 로컬 저장 안내")
    st.info("💾 생성된 모든 보고서는 내 컴퓨터의 **다운로드(Downloads) 폴더**로 안전하게 자동 저장됩니다.")
    
    # Default path is Windows Downloads folder
    default_download_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    actual_save_dir = default_download_dir
    
    if st.button("📂 다운로드 폴더 열기", use_container_width=True):
        try:
            os.startfile(actual_save_dir)
            st.toast("📂 탐색기에서 다운로드 폴더를 열었습니다!", icon="📂")
        except Exception as e:
            st.error(f"폴더를 여는 중 오류 발생: {e}")

    st.markdown("---")
    st.markdown("### 📊 시스템 상태")
    st.info("백엔드 서버: Port 8000 (Active)")
    
    if st.button("🔄 모든 단계 초기화", type="secondary"):
        if 'steps' in st.session_state:
            del st.session_state.steps
        st.rerun()

# --- Main UI ---
st.title("📋 단위업무 Map 자동 생성기")
st.markdown("##### 업무 항목 입력 → 순서도 자동 생성 → Word 보고서 출력")

# Session State for File Generation Status
if 'file_generated' not in st.session_state:
    st.session_state.file_generated = False
    st.session_state.generated_path = ""
    st.session_state.generated_content = None
    st.session_state.generated_filename = ""
    st.session_state.html_generated_path = ""
    st.session_state.html_generated_content = None
    st.session_state.html_generated_filename = ""

# Session State for Unit Map Steps
if 'steps' not in st.session_state:
    st.session_state.steps = [
        {
            "id": "S1",
            "activity": "INQUIRY PACKAGE PLAN 작성",
            "dept": "장치팀",
            "related_docs": [{"label": "BASIC DESIGN PACKAGE", "department": "사업팀", "classification": "정보제공"}],
            "points": "-INQUIRY PACKAGE PLAN 작성 방향 설정 검토\n-유형별 특성 재질 난이도에 따른 GROUP PLAN 작업",
            "timing": "최소 M/R작성 준비 작업 5일 전",
            "input_data": "INQUIRY PK'G PLAN 작성 기준",
            "output_data": "INQUIRY PK'G PLAN",
            "standards": "플랜트 설계주관 업무 분장 절차서"
        },
        {
            "id": "S2",
            "activity": "M/R 작성 관련 자료\n준비 작업",
            "dept": "장치 담당자",
            "related_docs": [],
            "points": "-관련 자료 검토 방향 설정\n-M/R 작성 기준 검토",
            "timing": "최소 M/R 작업 및 정리 2주 전",
            "input_data": "M/R 작성 준비 절차 기준",
            "output_data": "-",
            "standards": "기계 설계업무 절차서"
        },
        {
            "id": "S3",
            "activity": "M/R 작성 및 정리",
            "dept": "장치 담당자",
            "related_docs": [],
            "points": "-관련 첨부 자료 검토 확정\n-기술적 내용 입력",
            "timing": "최소 M/R 승인 5일 전",
            "input_data": "M/R작성 및 정리 절차 기준",
            "output_data": "-",
            "standards": "기계 설계업무 절차서"
        },
        {
            "id": "S4",
            "activity": "M/R 작성\n검토/검증/승인",
            "dept": "장치팀장",
            "related_docs": [],
            "points": "-관련 내용 및 첨부 자료 검토/검증/확인\n-M/R 송부 기준 절차 확인",
            "timing": "최소 VENDOR 송부 3일 전",
            "input_data": "장치설계 출력문서 검토 LIST",
            "output_data": "M/R 작성 검토/검증/승인 결과 자료",
            "standards": "장치 설계 업무 수행 계획서"
        },
        {
            "id": "S5",
            "activity": "M/R 송부",
            "dept": "사업팀/조달팀",
            "related_docs": [],
            "points": "-M/R 송부 기준 절차 확인\n-사업주 승인 VENDOR LIST 확인",
            "timing": "최소 VENDOR 송부 5일 전",
            "input_data": "M/R 송부 절차 기준",
            "output_data": "M/R PACKAGE",
            "standards": "문서관리 절차서"
        }
    ]

def proofread_action(index):
    text = st.session_state.steps[index]['points']
    if not text:
        return
    
    # 로컬 교정 기능
    lines = text.split("\n")
    corrected_lines = []
    for line in lines:
        line = line.strip()
        if not line: continue
        if not line.startswith("- "):
            line = "- " + line
        if not line.endswith(".") and not line.endswith("함") and not line.endswith("임"):
            line = line + "함."
        corrected_lines.append(line)
        
    st.session_state.steps[index]['points'] = "\n".join(corrected_lines)
    st.toast("✨ 문장이 교정되었습니다!", icon='✅')

def add_step_at(position):
    """Insert a new step at the given position."""
    new_step = {
        "id": f"S{len(st.session_state.steps)+1}",
        "activity": "새 업무 활동",
        "dept": "부서명",
        "related_docs": [],
        "points": "",
        "timing": "",
        "input_data": "",
        "output_data": "",
        "standards": ""
    }
    st.session_state.steps.insert(position, new_step)
    _renumber_steps()

def delete_step(index):
    """Delete a step at the given index."""
    if len(st.session_state.steps) > 1:
        st.session_state.steps.pop(index)
        _renumber_steps()
    else:
        st.toast("⚠️ 최소 1개의 단계가 필요합니다.", icon='⚠️')

def move_step(index, direction):
    """Move a step up or down."""
    steps = st.session_state.steps
    if direction == "up" and index > 0:
        steps[index], steps[index - 1] = steps[index - 1], steps[index]
    elif direction == "down" and index < len(steps) - 1:
        steps[index], steps[index + 1] = steps[index + 1], steps[index]
    _renumber_steps()

def _renumber_steps():
    """Re-assign step IDs after add/delete/move."""
    for idx, step in enumerate(st.session_state.steps):
        step['id'] = f"S{idx + 1}"

def build_full_flowchart_url():
    """Build a complete vertical flowchart URL using QuickChart Graphviz API with a two-column layout."""
    steps = st.session_state.steps
    if not steps:
        return None
        
    dot = 'digraph G {\n'
    dot += '    rankdir=TB;\n'
    dot += '    splines=ortho;\n'
    dot += '    concentrate=true;\n'
    dot += '    nodesep=0.4;\n'
    dot += '    ranksep=0.3;\n'
    dot += '    bgcolor="transparent";\n'
    dot += '    pad=0.2;\n'
    dot += '    node [fontname="Malgun Gothic", fontsize=10];\n'
    dot += '    edge [fontname="Malgun Gothic", fontsize=9];\n'
    
    prev_step_id = None
    prev_global_doc_node = None
    
    for i, step in enumerate(steps):
        step_node = f"step_{i}"
        activity_clean = step['activity'].replace('\n', '\\n').replace('"', '\\"')
        dept_clean = step['dept'].replace('"', '\\"')
        
        # Step box on the right (filled light blue, solid bold blue border)
        dot += f'    {step_node} [label="{activity_clean}\\n({dept_clean})", shape=box, style="filled,rounded", fillcolor="#e0f2fe", color="#0369a1", fontcolor="#0c4a6e", penwidth=2.5, width=2.2];\n'
        
        # Related docs for this step
        rel_docs = step.get('related_docs', [])
        if rel_docs:
            doc_nodes = []
            info_docs = [d for d in rel_docs if d.get('classification', '정보제공') == "정보제공"]
            review_docs = [d for d in rel_docs if d.get('classification', '정보제공') == "검토요청"]
            
            # 정보제공 (Left -> Right)
            for j, doc in enumerate(info_docs):
                doc_node = f"doc_info_{i}_{j}"
                doc_label = doc['label'].replace('\n', '\\n').replace('"', '\\"')
                doc_dept = doc['department'].replace('"', '\\"')
                dot += f'    {doc_node} [label="{doc_label}\\n({doc_dept})", shape=box, style="dashed,filled", fillcolor="#f8fafc", color="#64748b", fontcolor="#334155", penwidth=1.5, width=2.0];\n'
                doc_nodes.append(doc_node)
                
            # 검토요청 (Right -> Left)
            for j, doc in enumerate(review_docs):
                doc_node = f"doc_rev_{i}_{j}"
                doc_label = doc['label'].replace('\n', '\\n').replace('"', '\\"')
                doc_dept = doc['department'].replace('"', '\\"')
                dot += f'    {doc_node} [label="{doc_label}\\n({doc_dept})", shape=box, style="dashed,filled", fillcolor="#f8fafc", color="#64748b", fontcolor="#334155", penwidth=1.5, width=2.0];\n'
                doc_nodes.append(doc_node)
                
            if doc_nodes:
                # Stack ALL of them vertically on the left across steps
                for doc_node in doc_nodes:
                    if prev_global_doc_node is not None:
                        dot += f'    {prev_global_doc_node} -> {doc_node} [style=invis];\n'
                    prev_global_doc_node = doc_node
                
                # Align middle document node horizontally with step node
                mid_idx = len(doc_nodes) // 2
                dot += f'    {{ rank=same; {doc_nodes[mid_idx]}; {step_node}; }}\n'
                
                # Draw connections
                for doc_node in doc_nodes:
                    if "info" in doc_node:
                        # 정보제공: Left to Right solid blue arrow
                        dot += f'    {doc_node} -> {step_node} [color="#0284c7", penwidth=1.5];\n'
                    else:
                        # 검토요청: Right to Left dashed gray arrow
                        dot += f'    {step_node} -> {doc_node} [style=dashed, color="#64748b", penwidth=1.5];\n'
                        
        if prev_step_id is not None:
            dot += f'    {prev_step_id} -> {step_node} [color="#334155", penwidth=1.5, arrowsize=0.8];\n'
            
        prev_step_id = step_node
        
    dot += '}'
    encoded = urllib.parse.quote(dot)
    url = f"https://quickchart.io/graphviz?format=png&graph={encoded}"
    return url

# =========================================
# TABS NAVIGATION
# =========================================
tab1, tab2, tab3 = st.tabs(["1. 단위업무 Map", "2. 조직 및 업무분장", "3. Business Master Map"])

with tab1:
    # =========================================
    # LAYOUT: Left = Input / Right = Flowchart
    # =========================================
    left_col, right_col = st.columns([3, 1.2])

    # ===========================
    # LEFT: Step Input Form
    # ===========================
    with left_col:
        st.markdown("### 📝 업무 항목 입력")
    
        # Top action: add step at the beginning
        if st.button("➕ 맨 위에 단계 삽입", key="insert_top", use_container_width=True):
            add_step_at(0)
            st.rerun()
    
        for i, step in enumerate(st.session_state.steps):
            # Step card with expander
            with st.expander(f"**{i+1}단계** — {step['activity']} ({step['dept']})", expanded=True):
                # Control buttons row
                ctrl_cols = st.columns([1, 1, 1, 1, 1, 1])
                with ctrl_cols[0]:
                    if st.button("⬆️", key=f"up_{i}", help="위로 이동", disabled=(i == 0)):
                        move_step(i, "up")
                        st.rerun()
                with ctrl_cols[1]:
                    if st.button("⬇️", key=f"down_{i}", help="아래로 이동", disabled=(i == len(st.session_state.steps) - 1)):
                        move_step(i, "down")
                        st.rerun()
                with ctrl_cols[2]:
                    if st.button("📋 복제", key=f"dup_{i}", help="이 단계를 복제"):
                        import copy
                        new_step = copy.deepcopy(step)
                        new_step['id'] = f"S{len(st.session_state.steps)+1}"
                        st.session_state.steps.insert(i + 1, new_step)
                        _renumber_steps()
                        st.rerun()
                with ctrl_cols[3]:
                    if st.button("➕ 아래 삽입", key=f"ins_{i}", help="이 단계 아래에 새 단계 삽입"):
                        add_step_at(i + 1)
                        st.rerun()
                with ctrl_cols[4]:
                    if st.button("✨ 교정", key=f"proof_{i}", help="AI 문체 교정"):
                        proofread_action(i)
                        st.rerun()
                with ctrl_cols[5]:
                    if st.button("🗑️ 삭제", key=f"del_{i}", help="이 단계 삭제", type="secondary"):
                        delete_step(i)
                        st.rerun()

                # --- Input fields (6 columns matching output) ---
                # Row 1: Activity + Department
                r1c1, r1c2 = st.columns(2)
                with r1c1:
                    step['activity'] = st.text_input("활동명", step['activity'], key=f"act_{i}_{st.session_state.form_key_suffix}")
                with r1c2:
                    step['dept'] = st.text_input("담당 부서", step['dept'], key=f"dept_{i}_{st.session_state.form_key_suffix}")
            
                # Row 2: 6 detail columns
                st.markdown("---")
                d_cols = st.columns([2, 1.5, 1.5, 1.5, 2])
                with d_cols[0]:
                    step['points'] = st.text_area("업무처리요점", step['points'], key=f"pts_{i}_{st.session_state.form_key_suffix}", height=100)
                with d_cols[1]:
                    step['timing'] = st.text_area("시기/주기", step['timing'], key=f"time_{i}_{st.session_state.form_key_suffix}", height=100)
                with d_cols[2]:
                    step['input_data'] = st.text_area("Input", step['input_data'], key=f"in_{i}_{st.session_state.form_key_suffix}", height=100)
                with d_cols[3]:
                    step['output_data'] = st.text_area("Output", step['output_data'], key=f"out_{i}_{st.session_state.form_key_suffix}", height=100)
                with d_cols[4]:
                    step['standards'] = st.text_area("관련문서/기준", step['standards'], key=f"std_{i}_{st.session_state.form_key_suffix}", height=100)
            
                # Related documents (optional)
                with st.container():
                    st.caption("📎 관련 문서 (선택사항)")
                    if 'related_docs' not in step:
                        # Migrate old key if any
                        step['related_docs'] = []
                        for old_doc in step.get('input_docs', []):
                            step['related_docs'].append({
                                "label": old_doc.get("label", ""),
                                "department": old_doc.get("department", ""),
                                "classification": old_doc.get("classification", "정보제공")
                            })
                        if 'input_docs' in step:
                            del step['input_docs']
                
                    for j, doc in enumerate(step.get('related_docs', [])):
                        dc1, dc2, dc3, dc4 = st.columns([2, 1.2, 1.2, 0.4])
                        with dc1:
                            step['related_docs'][j]['label'] = st.text_input(
                                "문서명", doc['label'], key=f"doc_label_{i}_{j}_{st.session_state.form_key_suffix}", label_visibility="collapsed"
                            )
                        with dc2:
                            step['related_docs'][j]['department'] = st.text_input(
                                "부서", doc['department'], key=f"doc_dept_{i}_{j}_{st.session_state.form_key_suffix}", label_visibility="collapsed"
                            )
                        with dc3:
                            step['related_docs'][j]['classification'] = st.selectbox(
                                "구분", ["정보제공", "검토요청"], index=0 if doc.get('classification', '정보제공') == "정보제공" else 1, key=f"doc_class_{i}_{j}_{st.session_state.form_key_suffix}", label_visibility="collapsed"
                            )
                        with dc4:
                            if st.button("✕", key=f"del_doc_{i}_{j}"):
                                step['related_docs'].pop(j)
                                st.rerun()
                
                    if st.button("➕ 관련 문서 추가", key=f"add_doc_{i}"):
                        if 'related_docs' not in step:
                            step['related_docs'] = []
                        step['related_docs'].append({"label": "새 관련문서", "department": "부서", "classification": "정보제공"})
                        st.rerun()

            # Arrow between steps
            if i < len(st.session_state.steps) - 1:
                st.markdown('<div class="arrow-connector">▼</div>', unsafe_allow_html=True)
    
        # Bottom: Add step at end
        st.markdown("")
        if st.button("➕ 새로운 업무 단계 추가 (맨 아래)", key="add_bottom", use_container_width=True, type="primary"):
            add_step_at(len(st.session_state.steps))
            st.rerun()


    # ===========================
    # RIGHT: Preview & List (Sticky)
    # ===========================
    with right_col:
        # Add an invisible marker to target this specific column with Javascript
        st.markdown('<div id="right-col-marker"></div>', unsafe_allow_html=True)
    
        st.markdown("### 👁️ 미리보기")
    
        st.markdown("##### 📌 업무 Process")
        flowchart_url = build_full_flowchart_url()
        if flowchart_url:
            try:
                st.image(flowchart_url, use_container_width=True)
            except Exception:
                st.warning("순서도 생성 중 오류가 발생했습니다.")
        else:
            st.info("업무 단계를 추가하면 순서도가 자동으로 생성됩니다.")
    
        st.markdown("---")
        st.markdown("##### 📊 현재 단계 목록")
        for i, step in enumerate(st.session_state.steps):
            dept_badge = f"({step['dept']})"
            st.markdown(f"**{i+1}.** {step['activity']} {dept_badge}")

        # Inject Javascript to forcefully make this column sticky
        components.html("""
            <script>
            // Use a small timeout to ensure DOM is fully rendered
            setTimeout(() => {
                const doc = parent.document;
                const marker = doc.getElementById('right-col-marker');
                if (marker) {
                    // Find the closest column container
                    const column = marker.closest('[data-testid="column"]');
                    if (column) {
                        column.style.position = 'sticky';
                        column.style.top = '4rem';
                        column.style.height = 'calc(100vh - 5rem)';
                        column.style.overflowY = 'auto';
                        column.style.overflowX = 'hidden';
                    
                        if (column.parentElement) {
                            column.parentElement.style.alignItems = 'flex-start';
                            column.parentElement.style.overflow = 'visible';
                        }
                    }
                }
            }, 500);
            </script>
        """, height=0)


    # =========================================
    # BOTTOM: Preview Table + Word Export
    # =========================================
    st.markdown("---")
    st.markdown("### 📄 최종 출력 미리보기")

    # Beautiful Document Title Block matching Reference Word Format
    st.markdown(f"""
        <style>
        .preview-header-container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 25px;
            width: 100%;
            background-color: transparent;
            padding: 5px 0;
        }}
        .preview-ref-box {{
            border: 1.5px solid #475569;
            padding: 8px 16px;
            font-weight: 700;
            font-size: 0.95rem;
            color: #1e293b;
            background-color: #f8fafc;
            border-radius: 6px;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            text-align: center;
        }}
        .preview-title-box {{
            border: 4px double #1e293b;
            padding: 10px 40px;
            font-weight: 800;
            font-size: 1.4rem;
            text-align: center;
            color: #0f172a;
            background-color: #ffffff;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            border-radius: 6px;
            margin: 0 auto;
        }}
        .preview-spacer {{
            width: 100px;
        }}
        @media (prefers-color-scheme: dark) {{
            .preview-ref-box {{
                border-color: #94a3b8;
                color: #f1f5f9;
                background-color: #334155;
            }}
            .preview-title-box {{
                border-color: #cbd5e1;
                color: #ffffff;
                background-color: #1e293b;
            }}
        }}
        </style>
    
        <div class="preview-header-container">
            <div class="preview-ref-box">
                {ref_no}
            </div>
            <div class="preview-title-box">
                단위업무 Map - {map_title}
            </div>
            <div class="preview-spacer"></div>
        </div>
    """, unsafe_allow_html=True)

    # Table Header & Custom Style — 2-column Process layout with single full flowchart
    num_steps = len(st.session_state.steps)
    full_flowchart_url = build_full_flowchart_url()

    steps_html = ""
    for i, step in enumerate(st.session_state.steps):
        points_clean = step['points'].replace('\n', '<br>')
        timing_clean = step['timing'].replace('\n', '<br>')
        input_clean = step['input_data'].replace('\n', '<br>')
        output_clean = step['output_data'].replace('\n', '<br>')
        std_clean = step['standards'].replace('\n', '<br>')
    
        # First row: add flowchart cell with rowspan spanning all step rows
        if i == 0:
            flowchart_td = f'<td colspan="2" rowspan="{num_steps}" style="text-align: center; vertical-align: middle; background-color: #ffffff; padding: 8px; border-left: 1px solid #cbd5e1; border-right: 1px solid #cbd5e1; border-top: none; border-bottom: 1px solid #cbd5e1;"><img src="{full_flowchart_url}" style="width: 100%; height: auto;" /></td>'
            steps_html += f"<tr>{flowchart_td}" \
                          f"<td style='border: 1px solid #cbd5e1; padding: 12px; vertical-align: middle;'>{points_clean}</td>" \
                          f"<td style='border: 1px solid #cbd5e1; padding: 12px; text-align: center; vertical-align: middle;'>{timing_clean}</td>" \
                          f"<td style='border: 1px solid #cbd5e1; padding: 12px; vertical-align: middle;'>{input_clean}</td>" \
                          f"<td style='border: 1px solid #cbd5e1; padding: 12px; vertical-align: middle;'>{output_clean}</td>" \
                          f"<td style='border: 1px solid #cbd5e1; padding: 12px; vertical-align: middle;'>{std_clean}</td>" \
                          f"</tr>"
        else:
            # Subsequent rows: no process column (already spanned)
            steps_html += f"<tr>" \
                          f"<td style='border: 1px solid #cbd5e1; padding: 12px; vertical-align: middle;'>{points_clean}</td>" \
                          f"<td style='border: 1px solid #cbd5e1; padding: 12px; text-align: center; vertical-align: middle;'>{timing_clean}</td>" \
                          f"<td style='border: 1px solid #cbd5e1; padding: 12px; vertical-align: middle;'>{input_clean}</td>" \
                          f"<td style='border: 1px solid #cbd5e1; padding: 12px; vertical-align: middle;'>{output_clean}</td>" \
                          f"<td style='border: 1px solid #cbd5e1; padding: 12px; vertical-align: middle;'>{std_clean}</td>" \
                          f"</tr>"

    preview_table_html = f"""<div style="width: 100%;">
    <style>
    .sop-preview-table {{
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        font-size: 0.88rem;
        font-family: 'Malgun Gothic', sans-serif;
        color: #334155;
    }}
    .sop-preview-table th {{
        background-color: #1e293b;
        color: white;
        border: 1px solid #cbd5e1;
        padding: 12px;
        font-weight: 700;
        text-align: center;
    }}
    .sop-preview-table td {{
        border: 1px solid #cbd5e1;
        padding: 12px;
        vertical-align: middle;
        line-height: 1.5;
    }}
    @media (prefers-color-scheme: dark) {{
        .sop-preview-table {{
            color: #cbd5e1;
        }}
        .sop-preview-table th {{
            background-color: #334155;
            border-color: #475569;
        }}
        .sop-preview-table td {{
            border-color: #475569;
            background-color: #1e293b;
        }}
    }}
    </style>
    <table class="sop-preview-table">
        <thead>
            <tr>
                <th colspan="2" style="width: 40%;">업무 Process</th>
                <th rowspan="2" style="width: 18%;">업무처리요점</th>
                <th rowspan="2" style="width: 9%;">시기/주기</th>
                <th rowspan="2" style="width: 10%;">Input</th>
                <th rowspan="2" style="width: 10%;">Output</th>
                <th rowspan="2" style="width: 13%;">관련문서/기준</th>
            </tr>
            <tr>
                <th style="width: 20%;">고객/관련문서</th>
                <th style="width: 20%;">업무팀</th>
            </tr>
        </thead>
        <tbody>
            {steps_html}
        </tbody>
    </table>
    <br>
    </div>"""

    st.markdown(preview_table_html, unsafe_allow_html=True)

    # Generate Button
    if st.button("🚀 최종 보고서 (Word & HTML) 생성 및 로컬 저장", use_container_width=True, type="primary"):
        import sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from app.schemas import UnitMap
        from app.generator import generate_unit_map_docx, generate_unit_map_html
        
        try:
            # Clean filename
            safe_title = map_title.replace(' ', '_').replace('/', '_').replace('\\', '_')
            docx_filename = f"UnitMap_{safe_title}.docx"
            html_filename = f"UnitMap_{safe_title}.html"
            
            # Use current dir or outputs if actual_save_dir fails
            try:
                os.makedirs(actual_save_dir, exist_ok=True)
                output_dir = actual_save_dir
            except Exception:
                output_dir = "outputs"
                os.makedirs(output_dir, exist_ok=True)
                
            docx_save_path = os.path.join(output_dir, docx_filename)
            html_save_path = os.path.join(output_dir, html_filename)
            
            unit_map = UnitMap(title=map_title, ref_no=ref_no, steps=st.session_state.steps)
            
            generate_unit_map_docx(unit_map, docx_save_path, output_dir)
            generate_unit_map_html(unit_map, html_save_path)
            
            with open(docx_save_path, "rb") as f:
                docx_content = f.read()
            with open(html_save_path, "rb") as f:
                html_content = f.read()
                
            # Store in session state to persist
            st.session_state.file_generated = True
            st.session_state.generated_path = docx_save_path
            st.session_state.generated_content = docx_content
            st.session_state.generated_filename = docx_filename
        
            st.session_state.html_generated_path = html_save_path
            st.session_state.html_generated_content = html_content
            st.session_state.html_generated_filename = html_filename
        
            st.toast("🎉 보고서(Word & HTML) 생성 완료!", icon="✅")
        except Exception as e:
            import traceback
            st.error(f"보고서 생성 중 오류 발생: {e}")

    # Display Generation Results if generated
    if st.session_state.file_generated:
        st.markdown("---")
        st.success(
            f"🎉 **Word 보고서 및 HTML 보고서가 로컬 컴퓨터에 성공적으로 저장되었습니다!**\n\n"
            f"*   **💾 로컬 저장 폴더:** `{actual_save_dir}`\n"
            f"*   **📄 생성된 Word 파일:** `{st.session_state.generated_filename}`\n"
            f"*   **🌐 생성된 HTML 파일:** `{st.session_state.html_generated_filename}`\n\n"
            f"지정된 다운로드 폴더로 자동 저장되었으므로 다운로드 폴더에서 즉시 찾으실 수 있습니다."
        )
    
        # Action buttons row 1: Open Folder
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("📂 다운로드 폴더 열기", key="open_folder_bottom", use_container_width=True):
                try:
                    os.startfile(actual_save_dir)
                    st.toast("📂 탐색기에서 다운로드 폴더를 열었습니다!", icon="📂")
                except Exception as e:
                    st.error(f"폴더를 여는 중 오류 발생: {e}")
                
        # Action buttons row 2: Re-downloads
        dl_col1, dl_col2 = st.columns(2)
        with dl_col1:
            st.download_button(
                label="📥 웹 브라우저를 통해 Word 재다운로드",
                data=st.session_state.generated_content,
                file_name=st.session_state.generated_filename,
                use_container_width=True,
                key="download_btn_docx",
                on_click=open_explorer_folder,
                args=(actual_save_dir,)
            )
        with dl_col2:
            st.download_button(
                label="📥 웹 브라우저를 통해 HTML 재다운로드",
                data=st.session_state.html_generated_content,
                file_name=st.session_state.html_generated_filename,
                use_container_width=True,
                key="download_btn_html",
                on_click=open_explorer_folder,
                args=(actual_save_dir,)
            )

    # Footer
    st.markdown(
        "<div style='text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 50px;'>"
        "© 2026 EMKO SOP Automation System | Table-Style Intelligent UI"
        "</div>",
        unsafe_allow_html=True
    )

with tab2:
    render_tab2()

with tab3:
    render_tab3()
 
 

