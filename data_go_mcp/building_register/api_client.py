"""API client for 건축HUB 건축물대장정보 API."""

import os
import json
from typing import Optional, Dict, Any
import httpx
from urllib.parse import urlencode, quote


class BuildingRegisterClient:
    """Client for 건축HUB 건축물대장정보 API."""

    BASE_URL = "https://apis.data.go.kr/1613000/BldRgstHubService"

    def __init__(self):
        self.api_key = os.getenv("BUILDING_REGISTER_API_KEY")
        if not self.api_key:
            raise ValueError(
                "BUILDING_REGISTER_API_KEY environment variable is required. "
                "Get your API key from https://www.data.go.kr"
            )
        self.client = httpx.AsyncClient(timeout=30.0)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    def _build_url(self, endpoint: str, params: Dict[str, Any]) -> str:
        base_params = {
            "serviceKey": self.api_key,
            "_type": "json",
        }
        base_params.update(params)
        filtered = {k: str(v) for k, v in base_params.items() if v is not None and str(v).strip() != ""}
        query_string = urlencode(filtered, safe="%+=", quote_via=quote)
        return f"{self.BASE_URL}/{endpoint}?{query_string}"

    def _parse_response(self, response_text: str, page_no: int, num_of_rows: int) -> Dict[str, Any]:
        data = json.loads(response_text)
        body = data.get("response", {}).get("body", {})
        total_count = int(body.get("totalCount", 0))
        items_raw = body.get("items", {})

        if isinstance(items_raw, dict):
            items = items_raw.get("item", [])
        else:
            items = []

        if isinstance(items, dict):
            items = [items]

        return {
            "items": items,
            "page_no": page_no,
            "num_of_rows": num_of_rows,
            "total_count": total_count,
        }

    async def get_title_info(
        self,
        sigungu_cd: Optional[str] = None,
        bjdong_cd: Optional[str] = None,
        plat_gb_cd: Optional[str] = None,
        bun: Optional[str] = None,
        ji: Optional[str] = None,
        mgm_bldrgst_pk: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 100,
    ) -> Dict[str, Any]:
        """건축물대장 표제부 조회."""
        params = {
            "sigunguCd": sigungu_cd,
            "bjdongCd": bjdong_cd,
            "platGbCd": plat_gb_cd,
            "bun": bun,
            "ji": ji,
            "mgmBldrgstPk": mgm_bldrgst_pk,
            "pageNo": page_no,
            "numOfRows": num_of_rows,
        }
        url = self._build_url("getBrTitleInfo", params)
        response = await self.client.get(url)
        response.raise_for_status()
        return self._parse_response(response.text, page_no, num_of_rows)

    async def get_basis_ouln_info(
        self,
        sigungu_cd: Optional[str] = None,
        bjdong_cd: Optional[str] = None,
        plat_gb_cd: Optional[str] = None,
        bun: Optional[str] = None,
        ji: Optional[str] = None,
        mgm_bldrgst_pk: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 100,
    ) -> Dict[str, Any]:
        """건축물대장 기본개요 조회."""
        params = {
            "sigunguCd": sigungu_cd,
            "bjdongCd": bjdong_cd,
            "platGbCd": plat_gb_cd,
            "bun": bun,
            "ji": ji,
            "mgmBldrgstPk": mgm_bldrgst_pk,
            "pageNo": page_no,
            "numOfRows": num_of_rows,
        }
        url = self._build_url("getBrBasisOulnInfo", params)
        response = await self.client.get(url)
        response.raise_for_status()
        return self._parse_response(response.text, page_no, num_of_rows)

    async def get_flr_ouln_info(
        self,
        sigungu_cd: Optional[str] = None,
        bjdong_cd: Optional[str] = None,
        plat_gb_cd: Optional[str] = None,
        bun: Optional[str] = None,
        ji: Optional[str] = None,
        mgm_bldrgst_pk: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 100,
    ) -> Dict[str, Any]:
        """건축물대장 층별개요 조회."""
        params = {
            "sigunguCd": sigungu_cd,
            "bjdongCd": bjdong_cd,
            "platGbCd": plat_gb_cd,
            "bun": bun,
            "ji": ji,
            "mgmBldrgstPk": mgm_bldrgst_pk,
            "pageNo": page_no,
            "numOfRows": num_of_rows,
        }
        url = self._build_url("getBrFlrOulnInfo", params)
        response = await self.client.get(url)
        response.raise_for_status()
        return self._parse_response(response.text, page_no, num_of_rows)

    async def get_expos_pubuse_area_info(
        self,
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
        """건축물대장 전유공용면적 조회.

        mgmBldrgstPk는 이 API의 공식 파라미터가 아니므로 사용하지 않음.
        dongNm/hoNm은 서버사이드 필터링 지원. hoNm은 접미사 '호'를 제거하여 전달.
        서버 결과가 없으면 클라이언트사이드 필터링으로 폴백.
        """
        normalized_dong = dong_nm.strip() if dong_nm else None
        normalized_ho = ho_nm.strip().rstrip("호") if ho_nm else None

        params = {
            "sigunguCd": sigungu_cd,
            "bjdongCd": bjdong_cd,
            "platGbCd": plat_gb_cd,
            "bun": bun,
            "ji": ji,
            "dongNm": normalized_dong,
            "hoNm": normalized_ho,
            "pageNo": page_no,
            "numOfRows": num_of_rows,
        }
        url = self._build_url("getBrExposPubuseAreaInfo", params)
        response = await self.client.get(url)
        response.raise_for_status()
        result = self._parse_response(response.text, page_no, num_of_rows)

        if result["items"] or not (dong_nm or ho_nm):
            return result

        has_address = sigungu_cd and bjdong_cd
        if not has_address:
            return result

        fetch_size = 100
        current_page = 1
        matched = []
        total_count = 0

        while True:
            fallback_params = {
                "sigunguCd": sigungu_cd,
                "bjdongCd": bjdong_cd,
                "platGbCd": plat_gb_cd,
                "bun": bun,
                "ji": ji,
                "pageNo": current_page,
                "numOfRows": fetch_size,
            }
            url = self._build_url("getBrExposPubuseAreaInfo", fallback_params)
            response = await self.client.get(url)
            response.raise_for_status()
            page_result = self._parse_response(response.text, current_page, fetch_size)

            if current_page == 1:
                total_count = page_result["total_count"]

            items = page_result["items"]
            if not items:
                break

            for item in items:
                item_dong = item.get("dongNm", "").strip()
                item_ho = item.get("hoNm", "").strip()
                search_dong = dong_nm.strip().rstrip("동") if dong_nm else None
                search_ho = ho_nm.strip().rstrip("호") if ho_nm else None
                dong_match = (
                    not dong_nm
                    or item_dong == dong_nm.strip()
                    or item_dong.rstrip("동") == search_dong
                    or item_dong == search_dong
                )
                ho_match = (
                    not ho_nm
                    or item_ho == ho_nm.strip()
                    or item_ho.rstrip("호") == search_ho
                    or item_ho == search_ho
                )
                if dong_match and ho_match:
                    matched.append(item)

            fetched_so_far = current_page * fetch_size
            if fetched_so_far >= total_count:
                break

            current_page += 1

        return {
            "items": matched,
            "page_no": page_no,
            "num_of_rows": num_of_rows,
            "total_count": len(matched),
            "note": f"API 서버 필터 매칭 실패로 전체 {total_count}건 중 클라이언트 필터링 적용",
        }

    async def get_hsprc_info(
        self,
        sigungu_cd: Optional[str] = None,
        bjdong_cd: Optional[str] = None,
        plat_gb_cd: Optional[str] = None,
        bun: Optional[str] = None,
        ji: Optional[str] = None,
        mgm_bldrgst_pk: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 100,
    ) -> Dict[str, Any]:
        """건축물대장 주택가격 조회."""
        params = {
            "sigunguCd": sigungu_cd,
            "bjdongCd": bjdong_cd,
            "platGbCd": plat_gb_cd,
            "bun": bun,
            "ji": ji,
            "mgmBldrgstPk": mgm_bldrgst_pk,
            "pageNo": page_no,
            "numOfRows": num_of_rows,
        }
        url = self._build_url("getBrHsprcInfo", params)
        response = await self.client.get(url)
        response.raise_for_status()
        return self._parse_response(response.text, page_no, num_of_rows)

    async def get_expos_info(
        self,
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
        """건축물대장 전유부 조회. dong_nm/ho_nm은 클라이언트 사이드 필터링."""
        base_params = {
            "sigunguCd": sigungu_cd,
            "bjdongCd": bjdong_cd,
            "platGbCd": plat_gb_cd,
            "bun": bun,
            "ji": ji,
            "mgmBldrgstPk": mgm_bldrgst_pk,
        }

        need_filter = dong_nm or ho_nm

        if not need_filter:
            params = {**base_params, "pageNo": page_no, "numOfRows": num_of_rows}
            url = self._build_url("getBrExposInfo", params)
            response = await self.client.get(url)
            response.raise_for_status()
            return self._parse_response(response.text, page_no, num_of_rows)

        fetch_size = 100
        current_page = 1
        matched = []
        total_count = 0

        while True:
            params = {**base_params, "pageNo": current_page, "numOfRows": fetch_size}
            url = self._build_url("getBrExposInfo", params)
            response = await self.client.get(url)
            response.raise_for_status()
            result = self._parse_response(response.text, current_page, fetch_size)

            if current_page == 1:
                total_count = result["total_count"]

            items = result["items"]
            if not items:
                break

            for item in items:
                item_dong = item.get("dongNm", "").strip()
                item_ho = item.get("hoNm", "").strip()
                search_dong = dong_nm.strip().rstrip("동") if dong_nm else None
                search_ho = ho_nm.strip().rstrip("호") if ho_nm else None
                dong_match = (
                    not dong_nm
                    or item_dong == dong_nm.strip()
                    or item_dong.rstrip("동") == search_dong
                    or item_dong == search_dong
                )
                ho_match = (
                    not ho_nm
                    or item_ho == ho_nm.strip()
                    or item_ho.rstrip("호") == search_ho
                    or item_ho == search_ho
                )
                if dong_match and ho_match:
                    matched.append(item)

            fetched_so_far = current_page * fetch_size
            if fetched_so_far >= total_count:
                break

            current_page += 1

        return {
            "items": matched,
            "page_no": page_no,
            "num_of_rows": num_of_rows,
            "total_count": len(matched),
            "note": f"API 서버사이드 필터 미지원으로 전체 {total_count}건 중 클라이언트 필터링 적용",
        }


    async def get_wclf_info(
        self,
        sigungu_cd: Optional[str] = None,
        bjdong_cd: Optional[str] = None,
        plat_gb_cd: Optional[str] = None,
        bun: Optional[str] = None,
        ji: Optional[str] = None,
        mgm_bldrgst_pk: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 100,
    ) -> Dict[str, Any]:
        """건축물대장 오수정화시설 조회."""
        params = {
            "sigunguCd": sigungu_cd,
            "bjdongCd": bjdong_cd,
            "platGbCd": plat_gb_cd,
            "bun": bun,
            "ji": ji,
            "mgmBldrgstPk": mgm_bldrgst_pk,
            "pageNo": page_no,
            "numOfRows": num_of_rows,
        }
        url = self._build_url("getBrWclfInfo", params)
        response = await self.client.get(url)
        response.raise_for_status()
        return self._parse_response(response.text, page_no, num_of_rows)

    async def get_recap_title_info(
        self,
        sigungu_cd: Optional[str] = None,
        bjdong_cd: Optional[str] = None,
        plat_gb_cd: Optional[str] = None,
        bun: Optional[str] = None,
        ji: Optional[str] = None,
        mgm_bldrgst_pk: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 100,
    ) -> Dict[str, Any]:
        """건축물대장 총괄표제부 조회."""
        params = {
            "sigunguCd": sigungu_cd,
            "bjdongCd": bjdong_cd,
            "platGbCd": plat_gb_cd,
            "bun": bun,
            "ji": ji,
            "mgmBldrgstPk": mgm_bldrgst_pk,
            "pageNo": page_no,
            "numOfRows": num_of_rows,
        }
        url = self._build_url("getBrRecapTitleInfo", params)
        response = await self.client.get(url)
        response.raise_for_status()
        return self._parse_response(response.text, page_no, num_of_rows)

    async def get_atch_jibun_info(
        self,
        sigungu_cd: Optional[str] = None,
        bjdong_cd: Optional[str] = None,
        plat_gb_cd: Optional[str] = None,
        bun: Optional[str] = None,
        ji: Optional[str] = None,
        mgm_bldrgst_pk: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 100,
    ) -> Dict[str, Any]:
        """건축물대장 부속지번 조회."""
        params = {
            "sigunguCd": sigungu_cd,
            "bjdongCd": bjdong_cd,
            "platGbCd": plat_gb_cd,
            "bun": bun,
            "ji": ji,
            "mgmBldrgstPk": mgm_bldrgst_pk,
            "pageNo": page_no,
            "numOfRows": num_of_rows,
        }
        url = self._build_url("getBrAtchJibunInfo", params)
        response = await self.client.get(url)
        response.raise_for_status()
        return self._parse_response(response.text, page_no, num_of_rows)

    async def get_jijigu_info(
        self,
        sigungu_cd: Optional[str] = None,
        bjdong_cd: Optional[str] = None,
        plat_gb_cd: Optional[str] = None,
        bun: Optional[str] = None,
        ji: Optional[str] = None,
        mgm_bldrgst_pk: Optional[str] = None,
        page_no: int = 1,
        num_of_rows: int = 100,
    ) -> Dict[str, Any]:
        """건축물대장 지역지구구역 조회."""
        params = {
            "sigunguCd": sigungu_cd,
            "bjdongCd": bjdong_cd,
            "platGbCd": plat_gb_cd,
            "bun": bun,
            "ji": ji,
            "mgmBldrgstPk": mgm_bldrgst_pk,
            "pageNo": page_no,
            "numOfRows": num_of_rows,
        }
        url = self._build_url("getBrJijiguInfo", params)
        response = await self.client.get(url)
        response.raise_for_status()
        return self._parse_response(response.text, page_no, num_of_rows)
