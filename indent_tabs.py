import sys

with open('frontend/streamlit_app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

idx = 0
for i, line in enumerate(lines):
    if line.strip() == '# LAYOUT: Left = Input / Right = Flowchart':
        idx = i - 1
        break

if idx > 0:
    prefix = lines[:idx]
    suffix = lines[idx:]
    
    tab_code = [
        '# =========================================\n',
        '# TABS NAVIGATION\n',
        '# =========================================\n',
        'tab1, tab2, tab3 = st.tabs(["1. 단위업무 Map", "2. 조직 및 업무분장", "3. Business Master Map"])\n\n',
        'with tab1:\n'
    ]
    
    indented_suffix = ['    ' + line if line.strip() else line for line in suffix]
    
    # Add placeholders for tab2 and tab3 at the end
    tab2_code = [
        '\nwith tab2:\n',
        '    st.markdown("### 👥 조직 및 업무분장 Work Flow")\n',
        '    st.info("조직도 및 각 조직별 업무분장을 입력하고 순서도를 생성하는 기능이 추가될 예정입니다.")\n'
    ]
    
    tab3_code = [
        '\nwith tab3:\n',
        '    st.markdown("### 🏢 Department(Team) Business Master Map")\n',
        '    st.info("타 부서와의 Input/Output 관계를 포함한 마스터 맵을 생성하는 기능이 추가될 예정입니다.")\n'
    ]
    
    with open('frontend/streamlit_app.py', 'w', encoding='utf-8') as f:
        f.writelines(prefix + tab_code + indented_suffix + tab2_code + tab3_code)
        
    print('Successfully indented and wrapped in tabs')
else:
    print('Could not find the target line')
