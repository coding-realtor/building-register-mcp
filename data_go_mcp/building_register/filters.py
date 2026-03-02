"""API 응답 데이터 정제 모듈.

공공데이터 API 원본 응답에서 불필요한 필드를 제거하고,
AI 컨텍스트 윈도우 절약을 위해 핵심 정보만 추출합니다.

선별 기준:
  1. 코드값 제거 — 이름(~Nm) 필드가 있으면 코드(~Cd) 필드는 버림
  2. 내부 식별코드 제거 — sigunguCd, bjdongCd, platGbCd 등 이미 알고있는 조회 파라미터
  3. 빈 값 제거 — " ", "", 0, None 등 정보가 없는 필드 전부 제거
  4. 중복 주소 제거 — platPlc(지번주소)와 newPlatPlc(도로명주소) 중 하나만 유지하거나 둘 다 유지하되 도로명 관련 세부코드는 제거
  5. 관리용 필드 제거 — rnum, crtnDay, bylotCnt 등
"""

from typing import Dict, Any, List, Optional

GLOBAL_REMOVE_FIELDS = {
    "rnum",
    "platGbCd",
    "sigunguCd",
    "bjdongCd",
    "crtnDay",
    "bylotCnt",
    "naRoadCd",
    "naBjdongCd",
    "naUgrndCd",
    "naMainBun",
    "naSubBun",
    "splotNm",
    "block",
    "lot",
    "jiyukCd",
    "jiguCd",
    "guyukCd",
    "jiyukCdNm",
    "jiguCdNm",
    "guyukCdNm",
}

TITLE_KEEP_FIELDS = {
    "mgmBldrgstPk",
    "mgmUpBldrgstPk",
    "platPlc",
    "newPlatPlc",
    "bldNm",
    "mainAtchGbCdNm",
    "dongNm",
    "mainPurpsCdNm",
    "etcPurps",
    "strctCdNm",
    "roofCdNm",
    "grndFlrCnt",
    "ugrndFlrCnt",
    "platArea",
    "archArea",
    "totArea",
    "bcRat",
    "vlatRat",
    "vlatRatEstmTotarea",
    "hhldCnt",
    "fmlyCnt",
    "hoCnt",
    "pmsDay",
    "stcnsDay",
    "useAprDay",
    "enrgEfcnGrade",
    "enrgEfcnRt",
    "gnBldGrade",
    "gnBldCert",
    "itgBldGrade",
    "itgBldCert",
    "rserthqkDsgnApplyYn",
    "rserthqkAblty",
    "pkngtYpCdNm",
    "indrMechUtcnt",
    "indrMechArea",
    "oudrMechUtcnt",
    "oudrMechArea",
    "indrAutoUtcnt",
    "indrAutoArea",
    "oudrAutoUtcnt",
    "oudrAutoArea",
    "regstrGbCdNm",
    "regstrKindCdNm",
}

RECAP_TITLE_KEEP_FIELDS = {
    "mgmBldrgstPk",
    "platPlc",
    "newPlatPlc",
    "bldNm",
    "mainPurpsCdNm",
    "etcPurps",
    "grndFlrCnt",
    "ugrndFlrCnt",
    "platArea",
    "archArea",
    "totArea",
    "bcRat",
    "vlatRat",
    "hhldCnt",
    "fmlyCnt",
    "hoCnt",
    "useAprDay",
    "enrgEfcnGrade",
    "enrgSavingRt",
    "gnBldGrade",
    "itgBldGrade",
    "pkngtYpCdNm",
    "indrMechUtcnt",
    "indrAutoUtcnt",
    "oudrMechUtcnt",
    "oudrAutoUtcnt",
    "regstrGbCdNm",
    "regstrKindCdNm",
}

BASIS_OULN_KEEP_FIELDS = {
    "mgmBldrgstPk",
    "platPlc",
    "newPlatPlc",
    "bldNm",
    "mainAtchGbCdNm",
    "regstrGbCdNm",
    "regstrKindCdNm",
}

FLOOR_KEEP_FIELDS = {
    "mgmBldrgstPk",
    "flrGbCdNm",
    "flrNo",
    "strctCdNm",
    "etcStrct",
    "mainPurpsCdNm",
    "etcPurps",
    "area",
}

EXPOS_PUBUSE_AREA_KEEP_FIELDS = {
    "mgmBldrgstPk",
    "flrGbCdNm",
    "flrNo",
    "exposPubuseGbCdNm",
    "strctCdNm",
    "etcStrct",
    "mainPurpsCdNm",
    "etcPurps",
    "area",
}

EXPOS_KEEP_FIELDS = {
    "mgmBldrgstPk",
    "mgmUpBldrgstPk",
    "platPlc",
    "newPlatPlc",
    "bldNm",
    "dongNm",
    "hoNm",
    "mainAtchGbCdNm",
    "regstrGbCdNm",
    "regstrKindCdNm",
}

HSPRC_KEEP_FIELDS = {
    "mgmBldrgstPk",
    "bldNm",
    "hoNm",
    "hsprc",
    "stdrYear",
}

WCLF_KEEP_FIELDS = {
    "mgmBldrgstPk",
    "wclfKindCdNm",
    "cap",
    "capUnitCdNm",
}

ATCH_JIBUN_KEEP_FIELDS = {
    "mgmBldrgstPk",
    "platPlc",
    "newPlatPlc",
    "bjdongNm",
    "atchGbCdNm",
    "ji",
    "bun",
}

JIJIGU_KEEP_FIELDS = {
    "mgmBldrgstPk",
    "jijiguGbCdNm",
    "jijiguCdNm",
    "reprstYn",
}

FIELD_RENAME_MAP = {
    "mgmBldrgstPk": "관리PK",
    "mgmUpBldrgstPk": "상위PK",
    "platPlc": "소재지_지번",
    "newPlatPlc": "소재지_도로명",
    "bldNm": "건물명",
    "dongNm": "동명칭",
    "hoNm": "호명칭",
    "mainAtchGbCdNm": "주부속구분",
    "mainPurpsCdNm": "주용도",
    "etcPurps": "기타용도",
    "strctCdNm": "구조",
    "etcStrct": "기타구조",
    "roofCdNm": "지붕구조",
    "grndFlrCnt": "지상층수",
    "ugrndFlrCnt": "지하층수",
    "platArea": "대지면적_㎡",
    "archArea": "건축면적_㎡",
    "totArea": "연면적_㎡",
    "vlatRatEstmTotarea": "용적률산정연면적_㎡",
    "bcRat": "건폐율_%",
    "vlatRat": "용적률_%",
    "hhldCnt": "세대수",
    "fmlyCnt": "가구수",
    "hoCnt": "호수",
    "pmsDay": "허가일",
    "stcnsDay": "착공일",
    "useAprDay": "사용승인일",
    "enrgEfcnGrade": "에너지효율등급",
    "enrgEfcnRt": "에너지절감율",
    "enrgSavingRt": "에너지절감율",
    "gnBldGrade": "친환경건축물등급",
    "gnBldCert": "친환경건축물인증",
    "itgBldGrade": "인텔리전트건물등급",
    "itgBldCert": "인텔리전트건물인증",
    "rserthqkDsgnApplyYn": "내진설계적용여부",
    "rserthqkAblty": "내진능력",
    "pkngtYpCdNm": "주차형태",
    "indrMechUtcnt": "옥내기계식_대수",
    "indrMechArea": "옥내기계식_면적",
    "oudrMechUtcnt": "옥외기계식_대수",
    "oudrMechArea": "옥외기계식_면적",
    "indrAutoUtcnt": "옥내자주식_대수",
    "indrAutoArea": "옥내자주식_면적",
    "oudrAutoUtcnt": "옥외자주식_대수",
    "oudrAutoArea": "옥외자주식_면적",
    "regstrGbCdNm": "대장구분",
    "regstrKindCdNm": "대장종류",
    "flrGbCdNm": "층구분",
    "flrNo": "층번호",
    "area": "면적_㎡",
    "exposPubuseGbCdNm": "전유공용구분",
    "hsprc": "공시가격_원",
    "stdrYear": "기준년도",
    "wclfKindCdNm": "오수정화형식",
    "cap": "용량",
    "capUnitCdNm": "용량단위",
    "atchGbCdNm": "부속대장구분",
    "bjdongNm": "법정동명",
    "ji": "지번",
    "bun": "번",
    "jijiguGbCdNm": "지역지구구역구분",
    "jijiguCdNm": "지역지구구역명",
    "reprstYn": "대표여부",
}


def _is_empty(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, str):
        stripped = value.strip()
        return stripped == "" or stripped == "0" or stripped == "0.0"
    if isinstance(value, (int, float)):
        return value == 0
    return False


def _filter_item(item: Dict[str, Any], keep_fields: set) -> Dict[str, Any]:
    result = {}
    for key, value in item.items():
        if key in GLOBAL_REMOVE_FIELDS:
            continue
        if keep_fields and key not in keep_fields:
            continue
        if _is_empty(value):
            continue
        display_key = FIELD_RENAME_MAP.get(key, key)
        result[display_key] = value
    return result


def filter_title_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [r for item in items if (r := _filter_item(item, TITLE_KEEP_FIELDS))]


def filter_recap_title_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [r for item in items if (r := _filter_item(item, RECAP_TITLE_KEEP_FIELDS))]


def filter_basis_ouln_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [r for item in items if (r := _filter_item(item, BASIS_OULN_KEEP_FIELDS))]


def filter_floor_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [r for item in items if (r := _filter_item(item, FLOOR_KEEP_FIELDS))]


def filter_expos_pubuse_area_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [r for item in items if (r := _filter_item(item, EXPOS_PUBUSE_AREA_KEEP_FIELDS))]


def filter_expos_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [r for item in items if (r := _filter_item(item, EXPOS_KEEP_FIELDS))]


def filter_hsprc_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [r for item in items if (r := _filter_item(item, HSPRC_KEEP_FIELDS))]


def filter_wclf_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [r for item in items if (r := _filter_item(item, WCLF_KEEP_FIELDS))]


def filter_atch_jibun_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [r for item in items if (r := _filter_item(item, ATCH_JIBUN_KEEP_FIELDS))]


def filter_jijigu_items(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [r for item in items if (r := _filter_item(item, JIJIGU_KEEP_FIELDS))]


def filter_response(
    response: Dict[str, Any],
    filter_fn,
) -> Dict[str, Any]:
    filtered_items = filter_fn(response.get("items", []))
    return {
        "items": filtered_items,
        "total_count": response.get("total_count", 0),
        "page_no": response.get("page_no", 1),
        "num_of_rows": response.get("num_of_rows", 100),
    }
