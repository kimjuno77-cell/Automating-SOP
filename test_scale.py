"""Test: verify the image scale calculation produces correct fit_w."""
import sys
sys.path.insert(0, 'frontend')
from org_chart_docx import _fetch_chart_image

roles = [
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

# Simulate the streamlit session state
import streamlit as st
st.session_state = {"org_roles": roles}

result = _fetch_chart_image(roles)
if result:
    img_bytes, w, h = result
    print(f"Image size: {w}x{h} pixels")
    print(f"Image size at 150 DPI: {w/150:.1f} x {h/150:.1f} inches")
    
    # Landscape A4 page
    max_w = 10.51  # inches (29.7cm - 3cm margins)
    max_h = 5.59   # inches (21cm - 3cm margins - 1.5 title)
    
    img_w_in = w / 150.0
    img_h_in = h / 150.0
    
    scale_w = max_w / img_w_in
    scale_h = max_h / img_h_in
    scale = min(scale_w, scale_h, 1.0)
    
    fit_w = img_w_in * scale
    fit_w = min(fit_w, max_w)
    fit_h = img_h_in * scale
    
    print(f"scale_w={scale_w:.3f}, scale_h={scale_h:.3f}, scale={scale:.3f}")
    print(f"fit_w={fit_w:.2f} inches (max={max_w:.2f})")
    print(f"fit_h={fit_h:.2f} inches (max={max_h:.2f})")
    print(f"Fits page: width={fit_w <= max_w}, height={fit_h <= max_h}")
else:
    print("Failed to fetch image")
