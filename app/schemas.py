from pydantic import BaseModel
from typing import List, Optional

class RelatedDocument(BaseModel):
    label: str
    department: str
    classification: str = "정보제공" # "정보제공" 또는 "검토요청"

class UnitMapStep(BaseModel):
    id: str
    activity: str             # 업무팀 활동 (오른쪽 박스)
    dept: str                 # 담당 부서 (예: 장치팀)
    related_docs: List[RelatedDocument] # 고객/관련문서 (왼쪽 박스들)
    points: str               # 업무처리요점
    timing: str               # 시기/주기
    input_data: str           # Input
    output_data: str          # Output
    standards: str            # 관련문서/기준

class UnitMap(BaseModel):
    title: str
    ref_no: str               # 별첨 번호 (예: 별첨 3-4)
    steps: List[UnitMapStep]

# ==========================================
# 2. 조직 및 업무분장 (Org Chart & Responsibilities)
# ==========================================
class OrgRole(BaseModel):
    id: str
    role_name: str
    role_desc: str
    responsibilities: str
    parent_id: Optional[str] = None # For hierarchy

class OrgChart(BaseModel):
    title: str
    ref_no: str
    roles: List[OrgRole]

# ==========================================
# 3. Department Business Master Map
# ==========================================
class IncomingData(BaseModel):
    label: str
    department: str

class OutgoingData(BaseModel):
    label: str
    department: str

class MasterMapStep(BaseModel):
    id: str
    main_process: str
    pre_activity: str
    post_activity: str
    incoming_data: List[IncomingData]
    outgoing_data: List[OutgoingData]
    standards: str

class MasterMap(BaseModel):
    title: str
    ref_no: str
    steps: List[MasterMapStep]
