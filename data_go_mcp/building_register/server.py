"""MCP server for 건축HUB 건축물대장정보 API."""

from typing import Optional, Dict, Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from .api_client import BuildingRegisterClient
from .region import search_region_code
from .filters import (
    filter_response,
    filter_title_items,
    filter_recap_title_items,
    filter_basis_ouln_items,
    filter_floor_items,
    filter_expos_pubuse_area_items,
    filter_expos_items,
    filter_hsprc_items,
    filter_wclf_items,
    filter_atch_jibun_items,
    filter_jijigu_items,
)

load_dotenv()

mcp = FastMCP("건축물대장정보")

COMMON_PARAM_DOCS = """
    Args:
        sigungu_cd: 시군구코드 (5자리, 예: 11110 = 서울 종로구)
        bjdong_cd: 법정동코드 (5자리, 예: 10100)
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록)
        bun: 번 (4자리, 예: 0001)
        ji: 지 (4자리, 예: 0000)
        mgm_bldrgst_pk: 관리건축물대장PK (직접 PK를 알고 있을 때 사용)
        page_no: 페이지 번호 (기본값: 1)
        num_of_rows: 한 페이지 결과 수 (기본값: 100)
"""


@mcp.tool()
async def get_building_title_info(
    sigungu_cd: Optional[str] = None,
    bjdong_cd: Optional[str] = None,
    plat_gb_cd: Optional[str] = None,
    bun: Optional[str] = None,
    ji: Optional[str] = None,
    mgm_bldrgst_pk: Optional[str] = None,
    page_no: int = 1,
    num_of_rows: int = 100,
) -> Dict[str, Any]:
    """
    건축물대장 표제부를 조회합니다.

    🚨 [중요/MCP 지침] 🚨
    이 툴을 포함한 모든 건축물대장 API 호출 시에는 search_bjdong_code 에서 검색한 
    올바른 시군구코드(sigungu_cd)와 법정동코드(bjdong_cd)를 절대 틀리지 않게 기입해야 합니다.
    만약 조회 결과가 없다고 해서 터미널로 대화 로그(transcript)를 뒤지는 행동은 금지되어 있습니다.

    건축물의 지번주소 및 새주소, 주/부속구분, 대지면적, 건축면적, 건폐율, 용적율,
    구조, 용도, 지붕구조, 주차대수 등의 표제부 정보를 제공합니다.

    Args:
        sigungu_cd: 시군구코드 (5자리, 예: 11110 = 서울 종로구)
        bjdong_cd: 법정동코드 (5자리, 예: 10100)
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록)
        bun: 번 (4자리, 예: 0001)
        ji: 지 (4자리, 예: 0000)
        mgm_bldrgst_pk: 관리건축물대장PK
        page_no: 페이지 번호 (기본값: 1)
        num_of_rows: 한 페이지 결과 수 (기본값: 100)

    Returns:
        Dictionary containing:
        - items: 표제부 정보 목록 (건물명, 대지면적, 건축면적, 연면적, 건폐율, 용적률, 구조, 용도, 사용승인일 등)
        - page_no: 현재 페이지 번호
        - num_of_rows: 페이지당 결과 수
        - total_count: 전체 결과 수
    """
    async with BuildingRegisterClient() as client:
        try:
            raw = await client.get_title_info(
                sigungu_cd=sigungu_cd,
                bjdong_cd=bjdong_cd,
                plat_gb_cd=plat_gb_cd,
                bun=bun,
                ji=ji,
                mgm_bldrgst_pk=mgm_bldrgst_pk,
                page_no=page_no,
                num_of_rows=num_of_rows,
            )
            return filter_response(raw, filter_title_items)
        except Exception as e:
            return {"error": str(e), "items": [], "page_no": page_no, "num_of_rows": num_of_rows, "total_count": 0}


@mcp.tool()
async def get_building_basis_ouln_info(
    sigungu_cd: Optional[str] = None,
    bjdong_cd: Optional[str] = None,
    plat_gb_cd: Optional[str] = None,
    bun: Optional[str] = None,
    ji: Optional[str] = None,
    mgm_bldrgst_pk: Optional[str] = None,
    page_no: int = 1,
    num_of_rows: int = 100,
) -> Dict[str, Any]:
    """
    건축물대장 기본개요를 조회합니다.

    대장종류, 대장구분, 지번주소 및 새주소, 지역/지구/구역 등의 기본정보를 제공합니다.

    Args:
        sigungu_cd: 시군구코드 (5자리, 예: 11110 = 서울 종로구)
        bjdong_cd: 법정동코드 (5자리, 예: 10100)
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록)
        bun: 번 (4자리, 예: 0001)
        ji: 지 (4자리, 예: 0000)
        mgm_bldrgst_pk: 관리건축물대장PK
        page_no: 페이지 번호 (기본값: 1)
        num_of_rows: 한 페이지 결과 수 (기본값: 100)

    Returns:
        Dictionary containing:
        - items: 기본개요 정보 목록 (대장종류, 대장구분, 지번주소, 지역/지구/구역 등)
        - page_no: 현재 페이지 번호
        - num_of_rows: 페이지당 결과 수
        - total_count: 전체 결과 수
    """
    async with BuildingRegisterClient() as client:
        try:
            raw = await client.get_basis_ouln_info(
                sigungu_cd=sigungu_cd,
                bjdong_cd=bjdong_cd,
                plat_gb_cd=plat_gb_cd,
                bun=bun,
                ji=ji,
                mgm_bldrgst_pk=mgm_bldrgst_pk,
                page_no=page_no,
                num_of_rows=num_of_rows,
            )
            return filter_response(raw, filter_basis_ouln_items)
        except Exception as e:
            return {"error": str(e), "items": [], "page_no": page_no, "num_of_rows": num_of_rows, "total_count": 0}


@mcp.tool()
async def get_building_floor_ouln_info(
    sigungu_cd: Optional[str] = None,
    bjdong_cd: Optional[str] = None,
    plat_gb_cd: Optional[str] = None,
    bun: Optional[str] = None,
    ji: Optional[str] = None,
    mgm_bldrgst_pk: Optional[str] = None,
    page_no: int = 1,
    num_of_rows: int = 100,
) -> Dict[str, Any]:
    """
    건축물대장 층별개요를 조회합니다.

    🚨 [중요/MCP 지침] 🚨
    1. 집합건축물(아파트, 오피스텔, 상가 등 여러 동이 있는 건물)의 경우,
       주소(sigungu_cd+bjdong_cd+bun+ji)로만 조회하면 해당 대지 위 모든 동의
       층별 정보가 혼재되어 반환됩니다.
       반드시 mgm_bldrgst_pk를 지정하여 특정 동의 층별 정보만 조회하세요.
    2. mgm_bldrgst_pk는 smart_building_lookup 또는 get_building_title_info의
       응답에서 "관리PK" 필드로 확인할 수 있습니다.
    3. 값을 잊었거나 빈 결과가 나오면, 터미널(grep 등)로 과거 대화 로그를 무단 검색하지 말고
       정상적으로 표제부 API를 올바른 코드로 다시 호출하여 찾으세요.

    건축물의 층구분, 층번호, 층의 구조, 용도, 면적 등의 층별 정보를 제공합니다.

    Args:
        sigungu_cd: 시군구코드 (5자리, 예: 11110 = 서울 종로구)
        bjdong_cd: 법정동코드 (5자리, 예: 10100)
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록)
        bun: 번 (4자리, 예: 0001)
        ji: 지 (4자리, 예: 0000)
        mgm_bldrgst_pk: 관리건축물대장PK (집합건축물은 필수 — 없으면 다른 동 데이터 혼재)
        page_no: 페이지 번호 (기본값: 1)
        num_of_rows: 한 페이지 결과 수 (기본값: 100)

    Returns:
        Dictionary containing:
        - items: 층별개요 정보 목록 (층구분, 층번호, 구조, 용도, 면적 등)
        - page_no: 현재 페이지 번호
        - num_of_rows: 페이지당 결과 수
        - total_count: 전체 결과 수
    """
    async with BuildingRegisterClient() as client:
        try:
            raw = await client.get_flr_ouln_info(
                sigungu_cd=sigungu_cd,
                bjdong_cd=bjdong_cd,
                plat_gb_cd=plat_gb_cd,
                bun=bun,
                ji=ji,
                mgm_bldrgst_pk=mgm_bldrgst_pk,
                page_no=page_no,
                num_of_rows=num_of_rows,
            )
            return filter_response(raw, filter_floor_items)
        except Exception as e:
            return {"error": str(e), "items": [], "page_no": page_no, "num_of_rows": num_of_rows, "total_count": 0}


@mcp.tool()
async def get_building_expos_pubuse_area_info(
    sigungu_cd: Optional[str] = None,
    bjdong_cd: Optional[str] = None,
    plat_gb_cd: Optional[str] = None,
    bun: Optional[str] = None,
    ji: Optional[str] = None,
    mgm_bldrgst_pk: Optional[str] = None,
    dong_nm: Optional[str] = None,
    ho_nm: Optional[str] = None,
    page_no: int = 1,
    num_of_rows: int = 100,
) -> Dict[str, Any]:
    """
    건축물대장 전유공용면적을 조회합니다.

    전유/공용면적의 층구분, 층번호, 전유/공용구분, 구조, 용도 등의 정보를 제공합니다.

    Args:
        sigungu_cd: 시군구코드 (5자리, 예: 11110 = 서울 종로구)
        bjdong_cd: 법정동코드 (5자리, 예: 10100)
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록)
        bun: 번 (4자리, 예: 0001)
        ji: 지 (4자리, 예: 0000)
        mgm_bldrgst_pk: 관리건축물대장PK
        dong_nm: 동명칭
        ho_nm: 호명칭
        page_no: 페이지 번호 (기본값: 1)
        num_of_rows: 한 페이지 결과 수 (기본값: 100)

    Returns:
        Dictionary containing:
        - items: 전유공용면적 정보 목록 (층구분, 층번호, 전유/공용구분, 구조, 용도, 면적 등)
        - page_no: 현재 페이지 번호
        - num_of_rows: 페이지당 결과 수
        - total_count: 전체 결과 수
    """
    async with BuildingRegisterClient() as client:
        try:
            raw = await client.get_expos_pubuse_area_info(
                sigungu_cd=sigungu_cd,
                bjdong_cd=bjdong_cd,
                plat_gb_cd=plat_gb_cd,
                bun=bun,
                ji=ji,
                mgm_bldrgst_pk=mgm_bldrgst_pk,
                dong_nm=dong_nm,
                ho_nm=ho_nm,
                page_no=page_no,
                num_of_rows=num_of_rows,
            )
            return filter_response(raw, filter_expos_pubuse_area_items)
        except Exception as e:
            return {"error": str(e), "items": [], "page_no": page_no, "num_of_rows": num_of_rows, "total_count": 0}


@mcp.tool()
async def get_building_house_price_info(
    sigungu_cd: Optional[str] = None,
    bjdong_cd: Optional[str] = None,
    plat_gb_cd: Optional[str] = None,
    bun: Optional[str] = None,
    ji: Optional[str] = None,
    mgm_bldrgst_pk: Optional[str] = None,
    page_no: int = 1,
    num_of_rows: int = 100,
) -> Dict[str, Any]:
    """
    건축물대장 주택가격을 조회합니다.

    건축물대장 대상 주택의 공시가격 정보를 제공합니다.

    Args:
        sigungu_cd: 시군구코드 (5자리, 예: 11110 = 서울 종로구)
        bjdong_cd: 법정동코드 (5자리, 예: 10100)
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록)
        bun: 번 (4자리, 예: 0001)
        ji: 지 (4자리, 예: 0000)
        mgm_bldrgst_pk: 관리건축물대장PK
        page_no: 페이지 번호 (기본값: 1)
        num_of_rows: 한 페이지 결과 수 (기본값: 100)

    Returns:
        Dictionary containing:
        - items: 주택가격 정보 목록 (건물명, 호명칭, 공시가격, 기준년도 등)
        - page_no: 현재 페이지 번호
        - num_of_rows: 페이지당 결과 수
        - total_count: 전체 결과 수
    """
    async with BuildingRegisterClient() as client:
        try:
            raw = await client.get_hsprc_info(
                sigungu_cd=sigungu_cd,
                bjdong_cd=bjdong_cd,
                plat_gb_cd=plat_gb_cd,
                bun=bun,
                ji=ji,
                mgm_bldrgst_pk=mgm_bldrgst_pk,
                page_no=page_no,
                num_of_rows=num_of_rows,
            )
            return filter_response(raw, filter_hsprc_items)
        except Exception as e:
            return {"error": str(e), "items": [], "page_no": page_no, "num_of_rows": num_of_rows, "total_count": 0}


@mcp.tool()
async def get_building_expos_info(
    sigungu_cd: Optional[str] = None,
    bjdong_cd: Optional[str] = None,
    plat_gb_cd: Optional[str] = None,
    bun: Optional[str] = None,
    ji: Optional[str] = None,
    mgm_bldrgst_pk: Optional[str] = None,
    dong_nm: Optional[str] = None,
    ho_nm: Optional[str] = None,
    page_no: int = 1,
    num_of_rows: int = 100,
) -> Dict[str, Any]:
    """
    건축물대장 전유부를 조회합니다.

    건축물대장 전유부의 지번주소 및 새주소, 동/호명칭 등의 정보를 제공합니다.
    dong_nm과 ho_nm으로 특정 동/호를 직접 필터링할 수 있습니다.

    Args:
        sigungu_cd: 시군구코드 (5자리, 예: 11110 = 서울 종로구)
        bjdong_cd: 법정동코드 (5자리, 예: 10100)
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록)
        bun: 번 (4자리, 예: 0001)
        ji: 지 (4자리, 예: 0000)
        mgm_bldrgst_pk: 관리건축물대장PK
        dong_nm: 동명칭 (예: "126동") - 특정 동으로 필터링
        ho_nm: 호명칭 (예: "1704호") - 특정 호로 필터링
        page_no: 페이지 번호 (기본값: 1)
        num_of_rows: 한 페이지 결과 수 (기본값: 100)

    Returns:
        Dictionary containing:
        - items: 전유부 정보 목록 (건물명, 동명칭, 호명칭, 주부속구분 등)
        - page_no: 현재 페이지 번호
        - num_of_rows: 페이지당 결과 수
        - total_count: 전체 결과 수
    """
    async with BuildingRegisterClient() as client:
        try:
            raw = await client.get_expos_info(
                sigungu_cd=sigungu_cd,
                bjdong_cd=bjdong_cd,
                plat_gb_cd=plat_gb_cd,
                bun=bun,
                ji=ji,
                mgm_bldrgst_pk=mgm_bldrgst_pk,
                dong_nm=dong_nm,
                ho_nm=ho_nm,
                page_no=page_no,
                num_of_rows=num_of_rows,
            )
            return filter_response(raw, filter_expos_items)
        except Exception as e:
            return {"error": str(e), "items": [], "page_no": page_no, "num_of_rows": num_of_rows, "total_count": 0}


@mcp.tool()
async def get_building_wclf_info(
    sigungu_cd: Optional[str] = None,
    bjdong_cd: Optional[str] = None,
    plat_gb_cd: Optional[str] = None,
    bun: Optional[str] = None,
    ji: Optional[str] = None,
    mgm_bldrgst_pk: Optional[str] = None,
    page_no: int = 1,
    num_of_rows: int = 100,
) -> Dict[str, Any]:
    """
    건축물대장 오수정화시설을 조회합니다.

    건축물과 관련된 오수정화시설의 오수정화형식, 용량, 용량단위 등의 정보를 제공합니다.

    Args:
        sigungu_cd: 시군구코드 (5자리, 예: 11110 = 서울 종로구)
        bjdong_cd: 법정동코드 (5자리, 예: 10100)
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록)
        bun: 번 (4자리, 예: 0001)
        ji: 지 (4자리, 예: 0000)
        mgm_bldrgst_pk: 관리건축물대장PK
        page_no: 페이지 번호 (기본값: 1)
        num_of_rows: 한 페이지 결과 수 (기본값: 100)

    Returns:
        Dictionary containing:
        - items: 오수정화시설 정보 목록 (오수정화형식, 용량, 용량단위 등)
        - page_no: 현재 페이지 번호
        - num_of_rows: 페이지당 결과 수
        - total_count: 전체 결과 수
    """
    async with BuildingRegisterClient() as client:
        try:
            raw = await client.get_wclf_info(
                sigungu_cd=sigungu_cd,
                bjdong_cd=bjdong_cd,
                plat_gb_cd=plat_gb_cd,
                bun=bun,
                ji=ji,
                mgm_bldrgst_pk=mgm_bldrgst_pk,
                page_no=page_no,
                num_of_rows=num_of_rows,
            )
            return filter_response(raw, filter_wclf_items)
        except Exception as e:
            return {"error": str(e), "items": [], "page_no": page_no, "num_of_rows": num_of_rows, "total_count": 0}


@mcp.tool()
async def get_building_recap_title_info(
    sigungu_cd: Optional[str] = None,
    bjdong_cd: Optional[str] = None,
    plat_gb_cd: Optional[str] = None,
    bun: Optional[str] = None,
    ji: Optional[str] = None,
    mgm_bldrgst_pk: Optional[str] = None,
    page_no: int = 1,
    num_of_rows: int = 100,
) -> Dict[str, Any]:
    """
    건축물대장 총괄표제부를 조회합니다.

    총괄표제부의 지번주소 및 새주소, 대지면적, 건축면적, 연면적, 건폐율, 용적율,
    용도, 주차방식 및 주차대수, 부속건축물의 면적, 허가관리기관, 에너지관련 등급 등의 정보를 제공합니다.

    Args:
        sigungu_cd: 시군구코드 (5자리, 예: 11110 = 서울 종로구)
        bjdong_cd: 법정동코드 (5자리, 예: 10100)
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록)
        bun: 번 (4자리, 예: 0001)
        ji: 지 (4자리, 예: 0000)
        mgm_bldrgst_pk: 관리건축물대장PK
        page_no: 페이지 번호 (기본값: 1)
        num_of_rows: 한 페이지 결과 수 (기본값: 100)

    Returns:
        Dictionary containing:
        - items: 총괄표제부 정보 목록 (대지면적, 건축면적, 연면적, 건폐율, 용적률, 주차대수, 에너지효율등급 등)
        - page_no: 현재 페이지 번호
        - num_of_rows: 페이지당 결과 수
        - total_count: 전체 결과 수
    """
    async with BuildingRegisterClient() as client:
        try:
            raw = await client.get_recap_title_info(
                sigungu_cd=sigungu_cd,
                bjdong_cd=bjdong_cd,
                plat_gb_cd=plat_gb_cd,
                bun=bun,
                ji=ji,
                mgm_bldrgst_pk=mgm_bldrgst_pk,
                page_no=page_no,
                num_of_rows=num_of_rows,
            )
            return filter_response(raw, filter_recap_title_items)
        except Exception as e:
            return {"error": str(e), "items": [], "page_no": page_no, "num_of_rows": num_of_rows, "total_count": 0}


@mcp.tool()
async def get_building_atch_jibun_info(
    sigungu_cd: Optional[str] = None,
    bjdong_cd: Optional[str] = None,
    plat_gb_cd: Optional[str] = None,
    bun: Optional[str] = None,
    ji: Optional[str] = None,
    mgm_bldrgst_pk: Optional[str] = None,
    page_no: int = 1,
    num_of_rows: int = 100,
) -> Dict[str, Any]:
    """
    건축물대장 부속지번을 조회합니다.

    건축물과 관련된 부속지번의 지번주소 및 새주소, 부속대장구분 등의 정보를 제공합니다.

    Args:
        sigungu_cd: 시군구코드 (5자리, 예: 11110 = 서울 종로구)
        bjdong_cd: 법정동코드 (5자리, 예: 10100)
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록)
        bun: 번 (4자리, 예: 0001)
        ji: 지 (4자리, 예: 0000)
        mgm_bldrgst_pk: 관리건축물대장PK
        page_no: 페이지 번호 (기본값: 1)
        num_of_rows: 한 페이지 결과 수 (기본값: 100)

    Returns:
        Dictionary containing:
        - items: 부속지번 정보 목록 (지번주소, 부속대장구분, 법정동명 등)
        - page_no: 현재 페이지 번호
        - num_of_rows: 페이지당 결과 수
        - total_count: 전체 결과 수
    """
    async with BuildingRegisterClient() as client:
        try:
            raw = await client.get_atch_jibun_info(
                sigungu_cd=sigungu_cd,
                bjdong_cd=bjdong_cd,
                plat_gb_cd=plat_gb_cd,
                bun=bun,
                ji=ji,
                mgm_bldrgst_pk=mgm_bldrgst_pk,
                page_no=page_no,
                num_of_rows=num_of_rows,
            )
            return filter_response(raw, filter_atch_jibun_items)
        except Exception as e:
            return {"error": str(e), "items": [], "page_no": page_no, "num_of_rows": num_of_rows, "total_count": 0}


@mcp.tool()
async def get_building_jijigu_info(
    sigungu_cd: Optional[str] = None,
    bjdong_cd: Optional[str] = None,
    plat_gb_cd: Optional[str] = None,
    bun: Optional[str] = None,
    ji: Optional[str] = None,
    mgm_bldrgst_pk: Optional[str] = None,
    page_no: int = 1,
    num_of_rows: int = 100,
) -> Dict[str, Any]:
    """
    건축물대장 지역지구구역을 조회합니다.

    건축물과 관련된 지역/지구/구역의 구분 및 명칭, 대표여부 등의 정보를 제공합니다.

    Args:
        sigungu_cd: 시군구코드 (5자리, 예: 11110 = 서울 종로구)
        bjdong_cd: 법정동코드 (5자리, 예: 10100)
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 2: 블록)
        bun: 번 (4자리, 예: 0001)
        ji: 지 (4자리, 예: 0000)
        mgm_bldrgst_pk: 관리건축물대장PK
        page_no: 페이지 번호 (기본값: 1)
        num_of_rows: 한 페이지 결과 수 (기본값: 100)

    Returns:
        Dictionary containing:
        - items: 지역지구구역 정보 목록 (지역지구구역구분, 지역지구구역명, 대표여부 등)
        - page_no: 현재 페이지 번호
        - num_of_rows: 페이지당 결과 수
        - total_count: 전체 결과 수
    """
    async with BuildingRegisterClient() as client:
        try:
            raw = await client.get_jijigu_info(
                sigungu_cd=sigungu_cd,
                bjdong_cd=bjdong_cd,
                plat_gb_cd=plat_gb_cd,
                bun=bun,
                ji=ji,
                mgm_bldrgst_pk=mgm_bldrgst_pk,
                page_no=page_no,
                num_of_rows=num_of_rows,
            )
            return filter_response(raw, filter_jijigu_items)
        except Exception as e:
            return {"error": str(e), "items": [], "page_no": page_no, "num_of_rows": num_of_rows, "total_count": 0}


@mcp.tool()
async def search_bjdong_code(query: str) -> Dict[str, Any]:
    """
    건축물대장 API 조회용 시군구코드(sigungu_cd) 및 법정동코드(bjdong_cd)를 지역명(예: 강동구 고덕동)으로 검색하여 빠르게 찾습니다.
    사용자의 주소 관련 질의에 대해 본 API를 호출하기 전에 코드를 획득하기 위해 반드시 이 툴을 먼저 사용하세요.
    """
    return search_region_code(query)


@mcp.tool()
async def smart_building_lookup(
    sigungu_cd: str,
    bjdong_cd: str,
    bun: str,
    ji: str = "0000",
    plat_gb_cd: str = "0",
) -> Dict[str, Any]:
    """
    🏢 건축물대장 스마트 조회 — 주소 하나로 건축물 전체 개요를 자동으로 파악합니다.

    이 도구는 사용자가 건축물대장을 조회할 때 가장 먼저 호출해야 하는 핵심 도구입니다.
    search_bjdong_code로 코드를 얻은 뒤 이 도구를 호출하세요.

    [자동 처리 흐름]
    1. 기본개요를 조회하여 일반건축물 vs 집합건축물 자동 판별
    2. 일반건축물: 표제부 + 층별 정보를 한번에 조회하여 반환 (데이터 적음)
    3. 집합건축물: 총괄표제부 요약 + 표제부(동 목록)를 조회하되,
       전유부(5,000건 이상 가능)는 조회하지 않고 "동/호 선택 안내"를 반환

    [반환 후 AI 행동 지침]
    - 일반건축물: 바로 결과를 사용자에게 표로 보여주세요.
    - 집합건축물: 총괄표제부 요약과 동 목록을 보여준 뒤,
      "어느 동/호의 상세정보를 조회할까요?" 라고 사용자에게 물어보세요.
      사용자가 동/호를 지정하면 get_building_expos_info (전유부) 또는
      get_building_expos_pubuse_area_info (전유공용면적) 를 해당 동/호로 호출하세요.

    Args:
        sigungu_cd: 시군구코드 (5자리, search_bjdong_code로 조회)
        bjdong_cd: 법정동코드 (5자리, search_bjdong_code로 조회)
        bun: 번 (4자리, 예: 0843)
        ji: 지 (4자리, 기본값: 0000)
        plat_gb_cd: 대지구분코드 (0: 대지, 1: 산, 기본값: 0)
    """
    async with BuildingRegisterClient() as client:
        try:
            basis_raw = await client.get_basis_ouln_info(
                sigungu_cd=sigungu_cd,
                bjdong_cd=bjdong_cd,
                plat_gb_cd=plat_gb_cd,
                bun=bun,
                ji=ji,
                num_of_rows=5,
            )
            basis = filter_response(basis_raw, filter_basis_ouln_items)
            basis_items = basis.get("items", [])

            if not basis_items:
                return {"error": "해당 주소로 등록된 건축물대장이 없습니다.", "items": []}

            first = basis_items[0]
            register_type = first.get("대장구분", "")
            is_collective = register_type == "집합"

            result: Dict[str, Any] = {
                "건축물유형": "집합건축물" if is_collective else "일반건축물",
                "기본개요": basis_items[0],
            }

            if is_collective:
                recap_raw = await client.get_recap_title_info(
                    sigungu_cd=sigungu_cd,
                    bjdong_cd=bjdong_cd,
                    plat_gb_cd=plat_gb_cd,
                    bun=bun,
                    ji=ji,
                    num_of_rows=5,
                )
                recap = filter_response(recap_raw, filter_recap_title_items)

                title_raw = await client.get_title_info(
                    sigungu_cd=sigungu_cd,
                    bjdong_cd=bjdong_cd,
                    plat_gb_cd=plat_gb_cd,
                    bun=bun,
                    ji=ji,
                    num_of_rows=100,
                )
                title = filter_response(title_raw, filter_title_items)

                dong_list = []
                for idx, item in enumerate(title.get("items", []), 1):
                    dong_info = {
                        k: v for k, v in item.items()
                        if k in ("관리PK", "건물명", "동명칭", "주부속구분", "주용도", "구조", "지상층수", "세대수", "호수", "연면적_㎡")
                    }
                    if dong_info:
                        dong_info["번호"] = idx
                        dong_nm = dong_info.get("동명칭", "")
                        purps = dong_info.get("주용도", "")
                        if not dong_nm and purps:
                            dong_info["표시명"] = purps
                        dong_list.append(dong_info)

                result["총괄표제부"] = recap.get("items", [])
                result["동_목록"] = dong_list
                result["동_수"] = len(dong_list)
                result["전유부_총건수"] = title_raw.get("total_count", 0)
                result["안내"] = (
                    "집합건축물입니다. 위 동 목록에서 원하는 동/호를 선택하면 "
                    "전유부(세부호실) 또는 전유공용면적을 조회해 드립니다. "
                    "동명칭이 없는 건물(상가동 등)은 '표시명'으로 구분됩니다. "
                    "예: '101동 1504호 상세정보 조회해줘' 또는 '근린생활시설 층별 조회해줘'"
                )

            else:
                title_raw = await client.get_title_info(
                    sigungu_cd=sigungu_cd,
                    bjdong_cd=bjdong_cd,
                    plat_gb_cd=plat_gb_cd,
                    bun=bun,
                    ji=ji,
                    num_of_rows=100,
                )
                title = filter_response(title_raw, filter_title_items)

                floor_raw = await client.get_flr_ouln_info(
                    sigungu_cd=sigungu_cd,
                    bjdong_cd=bjdong_cd,
                    plat_gb_cd=plat_gb_cd,
                    bun=bun,
                    ji=ji,
                    num_of_rows=100,
                )
                floor = filter_response(floor_raw, filter_floor_items)

                result["표제부"] = title.get("items", [])
                result["층별개요"] = floor.get("items", [])

            return result

        except Exception as e:
            return {"error": str(e)}


@mcp.prompt()
def get_building_summary(address: str) -> str:
    """건축물대장 스마트 조회"""
    return f"""'{address}'의 건축물대장을 조회해주세요.

[조회 절차]
1. search_bjdong_code로 시군구코드와 법정동코드를 검색하세요.
2. smart_building_lookup 도구를 호출하세요 (자동으로 일반/집합 판별).
3. 결과를 가독성 좋은 마크다운 표(Table)로 정리하세요.
4. 집합건축물인 경우: 총괄표제부 요약 + 동 목록 표를 보여주고,
   "어느 동/호의 상세정보를 조회할까요?"라고 물어보세요.
5. 일반건축물인 경우: 표제부 + 층별개요를 바로 표로 보여주세요.

[출력 규칙]
- 불필요한 원본 데이터(JSON)는 출력하지 마세요.
- 표제부 58건 이상이면 전부 나열하지 말고 동별로 요약하세요.
- 전유부(5,000건 이상 가능)는 사용자가 동/호를 지정할 때까지 절대 호출하지 마세요.
"""


def main():
    """Main entry point."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

