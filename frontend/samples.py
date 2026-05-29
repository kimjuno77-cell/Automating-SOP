# -*- coding: utf-8 -*-
"""
Sample SOP templates for quick-start.
Department mappings applied:
  장치팀 → 기술팀, 사업팀 → 기술팀, 영업팀 → 사업(영업)팀, 조달팀 → 구매팀
"""

SAMPLES = {
    "직접 입력 (빈 양식)": None,

    "별첨 3-1: JOB SPECIFICATION 작성": {
        "ref_no": "별첨 3-1",
        "title": "JOB SPECIFICATION 작성",
        "steps": [
            {
                "id": "S1", "activity": "JOB SPEC 작성\n관련자료 준비", "dept": "기계팀",
                "related_docs": [{"label": "BASIC DESIGN\nPACKAGE", "department": "기술팀", "classification": "정보제공"}],
                "points": "-관련자료 검토 방향 설정\n-검토 대상 항목 및 적용 항목 설정",
                "timing": "필요 시 최소 SPEC.\n작성 및 정리 2주 전",
                "input_data": "JOB SPEC. 작성 준비 기준",
                "output_data": "-",
                "standards": "기계 설계업무 절차서"
            },
            {
                "id": "S2", "activity": "JOB SPEC 작성 및 정리", "dept": "기술 담당자",
                "related_docs": [
                    {"label": "I.T.B", "department": "기술팀", "classification": "정보제공"},
                    {"label": "CONTRACT DOC.", "department": "기술팀", "classification": "정보제공"}
                ],
                "points": "-관련 장치 STANDARD SPEC. 검토\n-검토결과 문제점 해결",
                "timing": "필요시 최소 자체\n검토/검증/승인 3일 전",
                "input_data": "JOB SPEC. 작성 준비 기준",
                "output_data": "작성된 JOB SPEC LIST",
                "standards": "기계 설계업무 절차서"
            },
            {
                "id": "S3", "activity": "JOB SPEC\n검토/검증/승인", "dept": "기술 담당자",
                "related_docs": [{"label": "OWNER SPEC.\nREQUIREMENT", "department": "기술팀", "classification": "정보제공"}],
                "points": "-적용 타당성 검토\n-검토 결과 제기된 문제점 해결 가능여부\n협의 및 확인",
                "timing": "필요시 최소 사업주 승인 신청\n3일 전",
                "input_data": "기술 설계 출력문서 검토 LIST",
                "output_data": "설계검토 / 검증 기록서",
                "standards": "기술 설계 업무 수행 계획서"
            },
            {
                "id": "S4", "activity": "사업주 승인 신청", "dept": "기술팀",
                "related_docs": [{"label": "BEDD\n(물성치자료)", "department": "", "classification": "정보제공"}],
                "points": "-사업주 승인 절차 방향 설정\n-사업주 COMMENT 사항에 대한 대책 방안",
                "timing": "필요시 최소 사업주 승인 2주 전",
                "input_data": "사업주 문서 승인 신청 절차 기준",
                "output_data": "TRANSMITTAL SHEET",
                "standards": "문서 관리 절차서"
            },
            {
                "id": "S5", "activity": "사업주 승인", "dept": "기술팀",
                "related_docs": [{"label": "사업주 COMMENT\nFEED-BACK", "department": "", "classification": "정보제공"}],
                "points": "-사업주 COMMENT 반영 여부에 대한\n협의 및 결정",
                "timing": "필요시 최소 사업주 재 승인\n신청 2주 전",
                "input_data": "사업주 문서 승인 절차 기준",
                "output_data": "사업주 COMMENT 결과 보고서",
                "standards": "문서 관리 절차서"
            }
        ]
    },

    "별첨 3-2: JOB SPECIFICATION 작성 (설계외주)": {
        "ref_no": "별첨 3-2",
        "title": "JOB SPECIFICATION 작성",
        "steps": [
            {
                "id": "S1", "activity": "설계협력업체 건설\n참여 LIST 접수", "dept": "기술팀",
                "related_docs": [{"label": "업체 LIST 제출", "department": "EP 지원팀", "classification": "정보제공"}],
                "points": "-설계 술력 등록 LIST과의 및 관리\n-각 업체 품질 평가에 의한 현황 파악",
                "timing": "필요 시 최소입찰 설명 3일 전",
                "input_data": "협력업체 참여\n협력업체 품질 평가표",
                "output_data": "협력업체 선정기준 및\n품질 평가 자료",
                "standards": "플랜트 설계외주 처리 관리 절차서"
            },
            {
                "id": "S2", "activity": "JOB SPEC 작성 및 정리", "dept": "기술 담당자",
                "related_docs": [{"label": "입찰 참가 지원요청", "department": "EP 지원팀", "classification": "정보제공"}],
                "points": "-입찰 일정 통보\n-특기 사항 통보",
                "timing": "필요시 최소 입찰 설명 3일 전",
                "input_data": "입찰 정보철\n(입찰 관련 전체 내용)",
                "output_data": "업무 연락 및 입찰 참가 관련 서류",
                "standards": "플랜트 설계외주 처리 관리 절차서"
            },
            {
                "id": "S3", "activity": "설계용역 범위 설명", "dept": "EP 지원팀/기술팀",
                "related_docs": [{"label": "수행 PLANT 관련 지원\n설명", "department": "EP 지원팀", "classification": "정보제공"}],
                "points": "-설계용역 범위 설명\n-입찰 관련 특기사항 설명\n-입찰 관련 서류 배포",
                "timing": "필요시 최소 건적 자료 접수\n7일 전",
                "input_data": "입찰 및 건적 자료 접수 내용\n(입찰 자료)",
                "output_data": "-",
                "standards": "플랜트 설계외주 처리 관리 절차서"
            },
            {
                "id": "S4", "activity": "건적서 검토 및 평가", "dept": "기술 담당자",
                "related_docs": [{"label": "설계 협력업체의\n견적서(자료) 제출", "department": "", "classification": "정보제공"}],
                "points": "-건적 접수 자료 정리\n-응찰 업체 건적서 평가",
                "timing": "필요시 최소 응찰 결과 통보\n3일 전",
                "input_data": "건적 작성기준",
                "output_data": "건적 접수 및 평가 결과 자료",
                "standards": ""
            },
            {
                "id": "S5", "activity": "입찰 결과 통보", "dept": "EP 지원팀/기술팀",
                "related_docs": [],
                "points": "-장추 일정 통보\n-입찰 결과 특이사항 통보",
                "timing": "필요시 최소 업체 선정 3일 전",
                "input_data": "입찰 평가 기준",
                "output_data": "입찰 평가 결과 자료",
                "standards": "플랜트 설계외주 처리 관리 절차서"
            },
            {
                "id": "S6", "activity": "설계 협력 업체 선정", "dept": "EP 지원팀/기술팀",
                "related_docs": [],
                "points": "-계약 관련 업무 절차 및 관련 준비 사항\n파악 및 확인",
                "timing": "필요시 최소 선정 업체와의\n회의 3일 전",
                "input_data": "업체 선정 기준",
                "output_data": "-",
                "standards": "플랜트 설계외주 처리 관리 절차서"
            },
            {
                "id": "S7", "activity": "설계 용역 관련 기존\n협의 및 자료전달", "dept": "기술담당자",
                "related_docs": [{"label": "ENG'G DWG. 작성에\n대한 관련팀 자료접수", "department": "관련팀", "classification": "정보제공"}],
                "points": "-설계 용역 관련 자료 준비 및 발신\n-설계 관련 지침서 준비 확인",
                "timing": "필요시 최소 ENG'G DWG.\n작성 3일 전",
                "input_data": "설계 용역 범위 정리 및\n설계지침서",
                "output_data": "DESIGN CRITERIA",
                "standards": "플랜트 설계업무 절차서"
            },
            {
                "id": "S8", "activity": "ENG'G DWG.검수 및\n검토 승인", "dept": "기술담당자",
                "related_docs": [{"label": "관련팀의 ENG'G\nDWG.검토", "department": "관련팀", "classification": "정보제공"}],
                "points": "-설계 관련 문제점 검토\n-설계 관련 특이사항 및 누락사항 확인",
                "timing": "필요시 최소 ENG DWG.\n작성 2주 전",
                "input_data": "기술설계 출력문서 및 검토 LIST",
                "output_data": "기술 계획 결과 문서 및 도서",
                "standards": "기기 설계업무 절차서"
            },
            {
                "id": "S9", "activity": "ENG'G DWG.\n작성/검증/승인", "dept": "기술팀장",
                "related_docs": [],
                "points": "-설계관련 주요기기에 대한 기술적 검증\n-설계관련 HOLD STATUS 관리",
                "timing": "필요시 최소 ENG'G DWG.\n작성 3일 전",
                "input_data": "설계기기/관련기준 설계 검증서",
                "output_data": "설계 검토기록서\n설계 검증 기록서 HOLD STATUS",
                "standards": "기계 설계업무 절차서"
            },
            {
                "id": "S10", "activity": "ENG'G DWG. 송부", "dept": "기술팀/관련부서",
                "related_docs": [],
                "points": "-ENG'G DWG 사업주 승인 판비작업\n-승인관련 서류 준비",
                "timing": "필요시 최소 사업주 승인 2주 전",
                "input_data": "출력문서 관리 기준",
                "output_data": "설계 출력 문서 검토 LIST",
                "standards": "설계출력 문서 관리 절차서"
            },
            {
                "id": "S11", "activity": "사업주 승인 신청", "dept": "기술팀",
                "related_docs": [],
                "points": "-사업주 승인 관련 서류 검토 확인",
                "timing": "필요시 최소 사업주 승인 2주 전",
                "input_data": "사업주 문서 승인신청 절차 기준",
                "output_data": "TRANSMITTAL SHEET",
                "standards": "문서 관리 절차서"
            },
            {
                "id": "S12", "activity": "사업주 승인", "dept": "기술팀",
                "related_docs": [{"label": "사업주 COMMENT\nFEED-BACK", "department": "", "classification": "정보제공"}],
                "points": "-사업주 COMMENT 반영 여부에 대한\n협의 및 결정",
                "timing": "필요시 사업주 재 승인 신청\n2주 전",
                "input_data": "사업주 문서 승인 절차 기준",
                "output_data": "사업주 COMMENT 결과 보고서",
                "standards": "문서 관리 절차서"
            }
        ]
    },

    "별첨 3-3: LOADING DATA 작성": {
        "ref_no": "별첨 3-3",
        "title": "LOADING DATA 작성",
        "steps": [
            {
                "id": "S1", "activity": "유형별 관련 EQUIP.\nDATA SH'T REVIEW", "dept": "관련 담당자",
                "related_docs": [{"label": "EQUIP. DATA\nSH'T 제출", "department": "", "classification": "정보제공"}],
                "points": "-검토결과 제기된 문제점 해결\n-추가 INFORM DATA 접수 여부 확인",
                "timing": "최소 강도 계산 3일 전",
                "input_data": "EQUIPMENT DATA SHEET 관련\n검토 기준",
                "output_data": "-",
                "standards": "기계 설계업무 절차서"
            },
            {
                "id": "S2", "activity": "EQUIP. 별 S/W 준비 및\nDATA BASE 준비", "dept": "관련담당자",
                "related_docs": [],
                "points": "-EQUIPMENT 강도계산을 위한 자료준비\n및 TOOL 확인\n-설계 기준 CODE 및 STANDARD 확정",
                "timing": "최소 강도계산 3일 전",
                "input_data": "강도계산을 위한 기술 계산업무\n절차 기준",
                "output_data": "강도계산 TOOL 확보 CODE 및\nSTANDARD 확보",
                "standards": "기계 설계업무 절차서"
            },
            {
                "id": "S3", "activity": "EQUIP. 별 강도계산 수행", "dept": "관련담당자",
                "related_docs": [],
                "points": "-강도계산 결과에 대한 검토 및 검증\n-기타 DATA-BASE 및 건적자료를 이용한\nLOADING DATA 검토 및 검증",
                "timing": "LOADING DATA SHEET 작성\n3일 전",
                "input_data": "기술설계 출력 문서 검토 LIST",
                "output_data": "강도계산 OUTPUT",
                "standards": "기술 설계 업무 수행 계획서"
            },
            {
                "id": "S4", "activity": "EQUIP. LOADING DATA\n작성", "dept": "관련 담당자",
                "related_docs": [],
                "points": "-LOADING DATA 관련 FORMAT 확정\n-LOADING DATA 입력 작업",
                "timing": "최소 관련부서 송부 5일 전",
                "input_data": "LOADING DATA 작성 기준",
                "output_data": "LOADING DATA SHEET",
                "standards": "기계 설계업무 절차서"
            },
            {
                "id": "S5", "activity": "LOADING DATA 송부", "dept": "건축팀/토목팀",
                "related_docs": [],
                "points": "-관련 부서 송부를 위한 준비작업\n-송부 관련서류 준비",
                "timing": "최소 관련부서 요청 일자 1일\n이내",
                "input_data": "관련부서 LOADING DATA 송부\n공지",
                "output_data": "LOADING DATA SHEET",
                "standards": "기계 설계업무 절차서"
            }
        ]
    },

    "별첨 3-4: MATERIAL REQUISITION 작성": {
        "ref_no": "별첨 3-4",
        "title": "MATERIAL REQUISITION 작성",
        "steps": [
            {
                "id": "S1", "activity": "INQUIRY PACKAGE\nPLAN 작성", "dept": "기술팀",
                "related_docs": [{"label": "EQUIPMENT LIST\n접수", "department": "", "classification": "정보제공"}],
                "points": "-INQUIRY PACKAGE PLAN 작성 방향 설정\n검토\n-유형별 특성 재질 난이도에 따른 GROUP\nPLAN 작업",
                "timing": "최소 M/R작성 준비 작업 5일\n전",
                "input_data": "INQUIRY PKG PLAN 작성 기준",
                "output_data": "INQUIRY PKG PLAN",
                "standards": "플랜트 설계주관 업무 분장\n절차서"
            },
            {
                "id": "S2", "activity": "M/R 작성 관련 자료\n준비 작업", "dept": "기술 담당자",
                "related_docs": [
                    {"label": "EQUIPMENT DATA\nSHEET", "department": "공정팀", "classification": "정보제공"},
                    {"label": "REQ'D LOCAL\nREGULATION LIST", "department": "공정팀", "classification": "정보제공"},
                    {"label": "FLARE LOAD", "department": "공정팀", "classification": "정보제공"}
                ],
                "points": "-관련 자료 검토 방향 설정\n-M/R 작성 기준 검토",
                "timing": "최소 M/R 작업 및 정리 2주 전",
                "input_data": "M/R 작성 준비 절차 기준",
                "output_data": "-",
                "standards": "기계 설계업무 절차서"
            },
            {
                "id": "S3", "activity": "M/R 작성 및 정리", "dept": "기술 담당자",
                "related_docs": [],
                "points": "-관련 첨부 자료 검토 확정\n-기술적 내용 입력",
                "timing": "최소 M/R 승인 5일 전",
                "input_data": "M/R작성 및 정리 절차 기준",
                "output_data": "-",
                "standards": "기계 설계업무 절차서"
            },
            {
                "id": "S4", "activity": "M/R 작성\n검토/검증/승인", "dept": "기술팀장",
                "related_docs": [
                    {"label": "ENVIR/HEALTH/SAFETY", "department": "공정팀", "classification": "정보제공"},
                    {"label": "ELECT. EQUIP.\nINFORM", "department": "전기팀", "classification": "정보제공"},
                    {"label": "MOTOR INFORM\nDATA", "department": "기계팀", "classification": "정보제공"},
                    {"label": "INSPECTION GENERAL\nSPEC", "department": "검사팀", "classification": "정보제공"}
                ],
                "points": "-관련 내용 및 첨부 자료 검토/검증/확인\n-M/R 송부 기준 절차 검토",
                "timing": "최소 VENDOR 송부 3일 전",
                "input_data": "기술설계 출력문서 검토 LIST",
                "output_data": "M/R 작성 검토/검증/승인 결과\n자료",
                "standards": "기술 설계 업무 수행 계획서"
            },
            {
                "id": "S5", "activity": "M/R 송부", "dept": "기술팀/구매팀",
                "related_docs": [],
                "points": "-M/R 송부 기준 절차 확인\n-사업주 승인 VENDOR LIST 확인",
                "timing": "최소 VENDOR 송부 5일 전",
                "input_data": "M/R 송부 절차 기준",
                "output_data": "M/R PACKAGE",
                "standards": "문서관리 절차서"
            }
        ]
    },

    "별첨 3-5: TBA SHEET 작성": {
        "ref_no": "별첨 3-5",
        "title": "TBA SHEET 작성",
        "steps": [
            {
                "id": "S1", "activity": "VENDOR'S 견적서 접수", "dept": "기술팀",
                "related_docs": [{"label": "M/R VENDOR 송부", "department": "구매팀", "classification": "정보제공"}],
                "points": "-견적서 분류 작업\n-TBA 작업을 위한 관련 자료 준비",
                "timing": "최소 TBA 업무 수행 10일 전",
                "input_data": "TBA 업무 수행 기준",
                "output_data": "TBA 업무 수행업체 결정",
                "standards": "기계 설계 업무 절차서"
            },
            {
                "id": "S2", "activity": "TECH.CLARIF. LIST 작성", "dept": "기술팀",
                "related_docs": [],
                "points": "-기술적 사항 및 WORK SCOPE에 대한\n검토\n-DEVIATION & EXCEPTION 사항 검토",
                "timing": "최소 VENDOR 송부 3일 전",
                "input_data": "기술설계 출력문서 검토 LIST",
                "output_data": "TECHNICAL CLARIFICATION\nLIST",
                "standards": "기술 설계 업무 수행 계획서"
            },
            {
                "id": "S3", "activity": "TECH.CLARIF.LIST\nVENDOR 송부", "dept": "기술팀",
                "related_docs": [],
                "points": "-VENDOR별 송부 준비작업\n-VENDOR의 회신 통보 일정 확인",
                "timing": "최소 VENDOR의 회신 접수\n7일 전",
                "input_data": "문서 관리 기준",
                "output_data": "문서 수발 대장",
                "standards": "기계 설계업무 절차서"
            },
            {
                "id": "S4", "activity": "VENDORS 회신접수", "dept": "기술팀",
                "related_docs": [{"label": "EXPEDITING 업무", "department": "구매팀", "classification": "정보제공"}],
                "points": "-기술적 사항 및 WORK SCOPE관련 확인\n작업\n-COST IMPACT 관련 사항 검토",
                "timing": "최소 TBE SUMMARY SHEET\n작성 5일 전",
                "input_data": "문서 관리 기준",
                "output_data": "문서 수발 대장",
                "standards": "기계 설계 업무 절차서"
            },
            {
                "id": "S5", "activity": "VENDORS TECH.\nCLARIF. MTG", "dept": "기술팀/토목팀",
                "related_docs": [{"label": "회의 일정 조정 및\n통보", "department": "구매팀", "classification": "정보제공"}],
                "points": "-COST IMPACT 관련 검토 및 확인\n-WORK SCOPE 및 기술적 접토사항에 대한\n확인",
                "timing": "최소 VENDOR 선정 2주 전",
                "input_data": "회의 절차 기준",
                "output_data": "VENDOR와의 MEETING 회의록",
                "standards": "기계 설계 업무 절차서"
            },
            {
                "id": "S6", "activity": "TBE SUMMARY SH'T\n작성 및 송부", "dept": "기술팀/구매팀/기술팀",
                "related_docs": [],
                "points": "-VENDOR의 회신정리\n-기술적 사항 및 WORK SCOPE 정리",
                "timing": "최소 VENDOR와 TECH. MT'G\n5일 전",
                "input_data": "TBE SUMMARY SHEET 작성 기준",
                "output_data": "TBE SUMMARY SHEET",
                "standards": "기계 설계 업무 절차서"
            },
            {
                "id": "S7", "activity": "CBE SUMMARY SH'T\n작성 및 송부", "dept": "구매팀/토목팀/기술팀",
                "related_docs": [],
                "points": "-COMMERCIAL MEETING 참석\n-COST IMPACT 관련 사항 검토",
                "timing": "최소 VENDOR 선정 7일 전",
                "input_data": "CBE SUMMARY SHEET 작성 기준",
                "output_data": "CBE SUMMARY SHEET",
                "standards": "기자재 구매 업무 지침"
            },
            {
                "id": "S8", "activity": "VENDOR 선정", "dept": "구매팀/기술팀/기술팀",
                "related_docs": [{"label": "TBE&CBE를 고려한\n종합적 검토", "department": "구매팀/기술팀", "classification": "정보제공"}],
                "points": "-TBE & CBE 사항에 대한 관련 부서와의\n종합적 협의",
                "timing": "최소 VENDOR와의 KICK-OFF\nMEETING 7일 전",
                "input_data": "VENDOR 선정 기준",
                "output_data": "VENDOR 선정 결과 자료",
                "standards": "기계 설계 업무 절차서"
            }
        ]
    }
}

SAMPLE_NAMES = list(SAMPLES.keys())
