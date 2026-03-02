"""법정동 코드 조회를 위한 로컬 텍스트 검색 도구"""
from __future__ import annotations

from pathlib import Path
from typing import Any, TypedDict

# resources 폴더의 region_codes.txt를 바라보도록 경로 지정
REGION_FILE = Path(__file__).parent / "resources" / "region_codes.txt"

class RegionMatch(TypedDict):
    """A single match result."""
    code: str  # 10자리 원본 코드
    name: str

class RegionResult(TypedDict, total=False):
    """Return type of search_region_code."""
    sigungu_cd: str  # 시군구코드 5자리 (건축물대장 API 조회용)
    bjdong_cd: str   # 법정동코드 5자리 (건축물대장 API 조회용)
    full_name: str
    matches: list[RegionMatch]
    error: str
    message: str

def _load_region_rows() -> list[tuple[str, str]]:
    """텍스트 파일에서 (법정동코드, 지역명) 리스트를 로드"""
    rows: list[tuple[str, str]] = []
    with REGION_FILE.open(encoding="utf-8") as f:
        next(f)  # skip header (첫째 줄 헤더 건너뛰기)
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            code, name, status = parts[0], parts[1], parts[2]
            if status == "존재":  # 현재 존재하는 법정동만 리스트업
                rows.append((code, name))
    return rows

def search_region_code(query: str) -> dict[str, Any]:
    """자유 형식의 지역 이름(예: '강동구 고덕동')을 입력받아 코드를 검색"""
    query = query.strip()
    if not query:
        return {"error": "invalid_input", "message": "지역 이름을 입력해주세요."}

    try:
        rows = _load_region_rows()
    except FileNotFoundError:
        return {"error": "file_not_found", "message": "'region_codes.txt' 데이터 파일을 찾을 수 없습니다."}

    # "강동구 고덕동" -> ["강동구", "고덕동"]
    tokens = query.split()
    
    # 모든 조건(토큰)을 포함하는 지역명(name) 필터링
    matched = [(code, name) for code, name in rows if all(tok in name for tok in tokens)]

    if not matched:
        return {"error": "no_match", "message": f"'{query}'에 해당하는 지역이 없습니다."}

    # 정렬: 
    # 일반적인 상황에서는 이름이 더 간결하면서 매치되는 가장 짧은 결과가 지역 매칭의 타겟일 확률이 높음.
    # 단, 여러개가 매칭될 경우, (예: 고덕동 매칭시 경기도 평택시 고덕동과 서울 강동구 고덕동이 나올 수 있으나, 
    # 사용자가 '고덕동'만 쳤을 때를 대비. 일단 문자열 길이 순으로 오름차순 정렬하여 가장 직관적인 지역명 선호.
    matched.sort(key=lambda x: len(x[1]))

    matches: list[RegionMatch] = [{"code": c, "name": n} for c, n in matched]

    # 제일 먼저 매칭된 가장 구체적인 지역 데이터 픽
    best_code, best_name = matched[0]

    # 건축물대장 API는 앞 5자리가 sigungu_cd (시군구코드), 뒤 5자리가 bjdong_cd (법정동코드) 임
    sigungu_cd = best_code[:5]
    bjdong_cd = best_code[5:10]

    return {
        "sigungu_cd": sigungu_cd,
        "bjdong_cd": bjdong_cd,
        "full_name": best_name,
        "matches": matches[:10], # 매치 결과가 너무 길면 상위 10개만 리턴
    }
