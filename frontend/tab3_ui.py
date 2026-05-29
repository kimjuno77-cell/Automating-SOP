import streamlit as st
from master_map import build_master_map_url
import copy

def render_tab3():
    left_col, right_col = st.columns([3, 1.2])
    
    with left_col:
        st.markdown("### 📝 Department Master Map 입력")
        if st.button("➕ 맨 위에 단계 삽입", key="add_m_top"):
            st.session_state.master_steps.insert(0, {"main_process": "새 프로세스", "pre_activity": "", "post_activity": "", "incoming_data": [], "outgoing_data": [], "standards": ""})
            st.rerun()
            
        for i, step in enumerate(st.session_state.master_steps):
            with st.expander(f"**{i+1}.** {step.get('main_process', '새 프로세스')}", expanded=True):
                ctrl = st.columns(4)
                if ctrl[0].button("⬆️", key=f"mup_{i}") and i > 0:
                    st.session_state.master_steps[i], st.session_state.master_steps[i-1] = st.session_state.master_steps[i-1], st.session_state.master_steps[i]
                    st.rerun()
                if ctrl[1].button("⬇️", key=f"mdown_{i}") and i < len(st.session_state.master_steps) - 1:
                    st.session_state.master_steps[i], st.session_state.master_steps[i+1] = st.session_state.master_steps[i+1], st.session_state.master_steps[i]
                    st.rerun()
                if ctrl[2].button("➕ 아래 삽입", key=f"mins_{i}"):
                    st.session_state.master_steps.insert(i+1, {"main_process": "새 프로세스", "pre_activity": "", "post_activity": "", "incoming_data": [], "outgoing_data": [], "standards": ""})
                    st.rerun()
                if ctrl[3].button("🗑️ 삭제", key=f"mdel_{i}"):
                    st.session_state.master_steps.pop(i)
                    st.rerun()
                    
                step['main_process'] = st.text_input("Main Process", step.get('main_process', ''), key=f"m_mp_{i}")
                
                c1, c2 = st.columns(2)
                with c1:
                    step['pre_activity'] = st.text_area("사전 Activity", step.get('pre_activity', ''), key=f"m_pre_{i}")
                    st.caption("📥 Incoming Data")
                    for j, inc in enumerate(step.get('incoming_data', [])):
                        ic1, ic2, ic3 = st.columns([2, 1, 0.5])
                        inc['label'] = ic1.text_input("자료명", inc['label'], key=f"m_inc_l_{i}_{j}", label_visibility="collapsed")
                        inc['department'] = ic2.text_input("부서", inc['department'], key=f"m_inc_d_{i}_{j}", label_visibility="collapsed")
                        if ic3.button("✕", key=f"m_inc_del_{i}_{j}"):
                            step['incoming_data'].pop(j)
                            st.rerun()
                    if st.button("➕ 추가", key=f"m_inc_add_{i}"):
                        step.setdefault('incoming_data', []).append({"label": "자료명", "department": "부서"})
                        st.rerun()

                with c2:
                    step['post_activity'] = st.text_area("사후 Activity", step.get('post_activity', ''), key=f"m_post_{i}")
                    st.caption("📤 Outgoing Data")
                    for j, out in enumerate(step.get('outgoing_data', [])):
                        oc1, oc2, oc3 = st.columns([2, 1, 0.5])
                        out['label'] = oc1.text_input("자료명", out['label'], key=f"m_out_l_{i}_{j}", label_visibility="collapsed")
                        out['department'] = oc2.text_input("부서", out['department'], key=f"m_out_d_{i}_{j}", label_visibility="collapsed")
                        if oc3.button("✕", key=f"m_out_del_{i}_{j}"):
                            step['outgoing_data'].pop(j)
                            st.rerun()
                    if st.button("➕ 추가", key=f"m_out_add_{i}"):
                        step.setdefault('outgoing_data', []).append({"label": "자료명", "department": "부서"})
                        st.rerun()
                
                step['standards'] = st.text_input("관련문서/기준", step.get('standards', ''), key=f"m_std_{i}")
                
        if st.button("➕ 맨 아래 추가", key="add_m_bottom"):
            st.session_state.master_steps.append({"main_process": "새 프로세스", "pre_activity": "", "post_activity": "", "incoming_data": [], "outgoing_data": [], "standards": ""})
            st.rerun()

    with right_col:
        st.markdown("### 👁️ Master Map 미리보기")
        url = build_master_map_url()
        if url:
            try:
                st.image(url, use_container_width=True)
            except Exception:
                st.warning("순서도 생성 중 오류가 발생했습니다.")
