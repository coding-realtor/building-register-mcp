"""Data models for 건축HUB 건축물대장정보 API."""

from typing import Optional, List
from pydantic import BaseModel, Field


class BrTitleItem(BaseModel):
    """건축물대장 표제부 항목."""

    mgm_bldrgst_pk: Optional[str] = Field(None, description="관리 건축물대장 PK")
    법정동코드: Optional[str] = Field(None, alias="bjdong_cd", description="법정동코드")
    법정동명: Optional[str] = Field(None, alias="bjdong_nm", description="법정동명")
    블록: Optional[str] = Field(None, alias="block", description="블록")
    건물명: Optional[str] = Field(None, alias="bld_nm", description="건물명")
    에너지효율등급: Optional[str] = Field(None, alias="enrg_efcnc_grade", description="에너지효율등급")
    에너지절감율: Optional[str] = Field(None, alias="enrg_saving_rate", description="에너지절감율")
    에너지EPI점수: Optional[str] = Field(None, alias="enrg_epi_score", description="에너지EPI점수")
    지상층수: Optional[str] = Field(None, alias="grnd_flr_cnt", description="지상층수")
    호수: Optional[str] = Field(None, alias="ho", description="호수")
    건폐율: Optional[str] = Field(None, alias="bc_rat", description="건폐율")
    지하층수: Optional[str] = Field(None, alias="ugrnd_flr_cnt", description="지하층수")
    지번: Optional[str] = Field(None, alias="ji", description="지번")
    대장구분코드: Optional[str] = Field(None, alias="regstr_gb_cd", description="대장구분코드")
    대장구분명: Optional[str] = Field(None, alias="regstr_gb_cd_nm", description="대장구분명")
    대장종류코드: Optional[str] = Field(None, alias="regstr_kind_cd", description="대장종류코드")
    대장종류명: Optional[str] = Field(None, alias="regstr_kind_cd_nm", description="대장종류명")
    로트: Optional[str] = Field(None, alias="lot", description="로트")
    메인건물명: Optional[str] = Field(None, alias="main_bld_nm", description="메인건물명")
    주부속구분코드: Optional[str] = Field(None, alias="main_atcht_gb_cd", description="주부속구분코드")
    주부속구분명: Optional[str] = Field(None, alias="main_atcht_gb_cd_nm", description="주부속구분명")
    주구조코드: Optional[str] = Field(None, alias="strct_cd", description="주구조코드")
    주구조명: Optional[str] = Field(None, alias="strct_cd_nm", description="주구조명")
    주용도코드: Optional[str] = Field(None, alias="main_purps_cd", description="주용도코드")
    주용도명: Optional[str] = Field(None, alias="main_purps_cd_nm", description="주용도명")
    기타용도: Optional[str] = Field(None, alias="etc_purps", description="기타용도")
    지붕구조코드: Optional[str] = Field(None, alias="roof_cd", description="지붕구조코드")
    지붕구조명: Optional[str] = Field(None, alias="roof_cd_nm", description="지붕구조명")
    기타지붕: Optional[str] = Field(None, alias="etc_roof", description="기타지붕")
    세대수: Optional[str] = Field(None, alias="hhld_cnt", description="세대수")
    가구수: Optional[str] = Field(None, alias="fmly_cnt", description="가구수")
    대지면적: Optional[str] = Field(None, alias="plat_area", description="대지면적(㎡)")
    건축면적: Optional[str] = Field(None, alias="arch_area", description="건축면적(㎡)")
    용적률산정연면적: Optional[str] = Field(None, alias="vlat_rat_estm_totarea", description="용적률산정연면적(㎡)")
    연면적: Optional[str] = Field(None, alias="tot_area", description="연면적(㎡)")
    용적률: Optional[str] = Field(None, alias="vlat_rat", description="용적률")
    인허가일: Optional[str] = Field(None, alias="pmsn_date", description="인허가일")
    착공일: Optional[str] = Field(None, alias="stcns_date", description="착공일")
    사용승인일: Optional[str] = Field(None, alias="use_aprv_date", description="사용승인일")
    허가번호일련번호: Optional[str] = Field(None, alias="pmsn_no_yn", description="허가번호일련번호")
    시도코드: Optional[str] = Field(None, alias="sido_cd", description="시도코드")
    시도명: Optional[str] = Field(None, alias="sido_nm", description="시도명")
    시군구코드: Optional[str] = Field(None, alias="sgg_cd", description="시군구코드")
    시군구명: Optional[str] = Field(None, alias="sgg_nm", description="시군구명")
    도로명대지위치: Optional[str] = Field(None, alias="new_plat_plc", description="도로명대지위치")
    도로명: Optional[str] = Field(None, alias="road_nm", description="도로명")
    도로명시군구코드: Optional[str] = Field(None, alias="road_nm_sgg_cd", description="도로명시군구코드")
    도로명코드: Optional[str] = Field(None, alias="road_nm_cd", description="도로명코드")
    도로명지하여부코드: Optional[str] = Field(None, alias="udrtrd_yn", description="도로명지하여부코드")
    도로명건물본번: Optional[str] = Field(None, alias="road_nm_main_bun", description="도로명건물본번")
    도로명건물부번: Optional[str] = Field(None, alias="road_nm_sub_bun", description="도로명건물부번")
    도로명우편번호: Optional[str] = Field(None, alias="road_nm_postno", description="도로명우편번호")
    도로명건물명: Optional[str] = Field(None, alias="road_nm_bld_nm", description="도로명건물명")
    주차대수기계식: Optional[str] = Field(None, alias="pkng_cnt_mech", description="주차대수(기계식)")
    주차대수옥내자주식: Optional[str] = Field(None, alias="pkng_cnt_insdelev", description="주차대수(옥내자주식)")
    주차대수옥외자주식: Optional[str] = Field(None, alias="pkng_cnt_outsideauto", description="주차대수(옥외자주식)")
    생성일자: Optional[str] = Field(None, alias="crtn_day", description="생성일자")

    class Config:
        populate_by_name = True


class BrBasisOulnItem(BaseModel):
    """건축물대장 기본개요 항목."""

    mgm_bldrgst_pk: Optional[str] = Field(None, description="관리 건축물대장 PK")
    법정동코드: Optional[str] = Field(None, alias="bjdong_cd", description="법정동코드")
    법정동명: Optional[str] = Field(None, alias="bjdong_nm", description="법정동명")
    블록: Optional[str] = Field(None, alias="block", description="블록")
    건물명: Optional[str] = Field(None, alias="bld_nm", description="건물명")
    지번: Optional[str] = Field(None, alias="ji", description="지번")
    대장구분코드: Optional[str] = Field(None, alias="regstr_gb_cd", description="대장구분코드")
    대장구분명: Optional[str] = Field(None, alias="regstr_gb_cd_nm", description="대장구분명")
    대장종류코드: Optional[str] = Field(None, alias="regstr_kind_cd", description="대장종류코드")
    대장종류명: Optional[str] = Field(None, alias="regstr_kind_cd_nm", description="대장종류명")
    로트: Optional[str] = Field(None, alias="lot", description="로트")
    주부속구분코드: Optional[str] = Field(None, alias="main_atcht_gb_cd", description="주부속구분코드")
    주부속구분명: Optional[str] = Field(None, alias="main_atcht_gb_cd_nm", description="주부속구분명")
    대지위치: Optional[str] = Field(None, alias="plat_plc", description="대지위치")
    시도코드: Optional[str] = Field(None, alias="sido_cd", description="시도코드")
    시도명: Optional[str] = Field(None, alias="sido_nm", description="시도명")
    시군구코드: Optional[str] = Field(None, alias="sgg_cd", description="시군구코드")
    시군구명: Optional[str] = Field(None, alias="sgg_nm", description="시군구명")
    지역코드: Optional[str] = Field(None, alias="locatadd_nm", description="지역코드")
    지역명: Optional[str] = Field(None, alias="지역명", description="지역명")
    지구코드: Optional[str] = Field(None, alias="지구코드", description="지구코드")
    지구명: Optional[str] = Field(None, alias="지구명", description="지구명")
    구역코드: Optional[str] = Field(None, alias="구역코드", description="구역코드")
    구역명: Optional[str] = Field(None, alias="구역명", description="구역명")
    생성일자: Optional[str] = Field(None, alias="crtn_day", description="생성일자")

    class Config:
        populate_by_name = True


class BrFlrOulnItem(BaseModel):
    """건축물대장 층별개요 항목."""

    mgm_bldrgst_pk: Optional[str] = Field(None, description="관리 건축물대장 PK")
    법정동코드: Optional[str] = Field(None, alias="bjdong_cd", description="법정동코드")
    법정동명: Optional[str] = Field(None, alias="bjdong_nm", description="법정동명")
    층구분코드: Optional[str] = Field(None, alias="flr_gb_cd", description="층구분코드")
    층구분명: Optional[str] = Field(None, alias="flr_gb_cd_nm", description="층구분명")
    층번호: Optional[str] = Field(None, alias="flr_no", description="층번호")
    구조코드: Optional[str] = Field(None, alias="strct_cd", description="구조코드")
    구조명: Optional[str] = Field(None, alias="strct_cd_nm", description="구조명")
    기타구조: Optional[str] = Field(None, alias="etc_strct", description="기타구조")
    주용도코드: Optional[str] = Field(None, alias="main_purps_cd", description="주용도코드")
    주용도명: Optional[str] = Field(None, alias="main_purps_cd_nm", description="주용도명")
    기타용도: Optional[str] = Field(None, alias="etc_purps", description="기타용도")
    면적: Optional[str] = Field(None, alias="area", description="면적(㎡)")
    시도코드: Optional[str] = Field(None, alias="sido_cd", description="시도코드")
    시군구코드: Optional[str] = Field(None, alias="sgg_cd", description="시군구코드")
    생성일자: Optional[str] = Field(None, alias="crtn_day", description="생성일자")

    class Config:
        populate_by_name = True


class BrExposPubuseAreaItem(BaseModel):
    """건축물대장 전유공용면적 항목."""

    mgm_bldrgst_pk: Optional[str] = Field(None, description="관리 건축물대장 PK")
    법정동코드: Optional[str] = Field(None, alias="bjdong_cd", description="법정동코드")
    층구분코드: Optional[str] = Field(None, alias="flr_gb_cd", description="층구분코드")
    층구분명: Optional[str] = Field(None, alias="flr_gb_cd_nm", description="층구분명")
    층번호: Optional[str] = Field(None, alias="flr_no", description="층번호")
    전유공용구분코드: Optional[str] = Field(None, alias="expos_pubuse_gb_cd", description="전유공용구분코드")
    전유공용구분명: Optional[str] = Field(None, alias="expos_pubuse_gb_cd_nm", description="전유공용구분명")
    구조코드: Optional[str] = Field(None, alias="strct_cd", description="구조코드")
    구조명: Optional[str] = Field(None, alias="strct_cd_nm", description="구조명")
    기타구조: Optional[str] = Field(None, alias="etc_strct", description="기타구조")
    주용도코드: Optional[str] = Field(None, alias="main_purps_cd", description="주용도코드")
    주용도명: Optional[str] = Field(None, alias="main_purps_cd_nm", description="주용도명")
    면적: Optional[str] = Field(None, alias="area", description="면적(㎡)")
    시도코드: Optional[str] = Field(None, alias="sido_cd", description="시도코드")
    시군구코드: Optional[str] = Field(None, alias="sgg_cd", description="시군구코드")
    생성일자: Optional[str] = Field(None, alias="crtn_day", description="생성일자")

    class Config:
        populate_by_name = True


class BrHsprcItem(BaseModel):
    """건축물대장 주택가격 항목."""

    mgm_bldrgst_pk: Optional[str] = Field(None, description="관리 건축물대장 PK")
    법정동코드: Optional[str] = Field(None, alias="bjdong_cd", description="법정동코드")
    법정동명: Optional[str] = Field(None, alias="bjdong_nm", description="법정동명")
    건물명: Optional[str] = Field(None, alias="bld_nm", description="건물명")
    호명칭: Optional[str] = Field(None, alias="ho_nm", description="호명칭")
    공시가격: Optional[str] = Field(None, alias="hsprc", description="공시가격(원)")
    기준년도: Optional[str] = Field(None, alias="stdr_year", description="기준년도")
    시도코드: Optional[str] = Field(None, alias="sido_cd", description="시도코드")
    시군구코드: Optional[str] = Field(None, alias="sgg_cd", description="시군구코드")
    생성일자: Optional[str] = Field(None, alias="crtn_day", description="생성일자")

    class Config:
        populate_by_name = True


class BrExposItem(BaseModel):
    """건축물대장 전유부 항목."""

    mgm_bldrgst_pk: Optional[str] = Field(None, description="관리 건축물대장 PK")
    법정동코드: Optional[str] = Field(None, alias="bjdong_cd", description="법정동코드")
    법정동명: Optional[str] = Field(None, alias="bjdong_nm", description="법정동명")
    건물명: Optional[str] = Field(None, alias="bld_nm", description="건물명")
    동명칭: Optional[str] = Field(None, alias="dong_nm", description="동명칭")
    호명칭: Optional[str] = Field(None, alias="ho_nm", description="호명칭")
    주부속구분코드: Optional[str] = Field(None, alias="main_atcht_gb_cd", description="주부속구분코드")
    주부속구분명: Optional[str] = Field(None, alias="main_atcht_gb_cd_nm", description="주부속구분명")
    시도코드: Optional[str] = Field(None, alias="sido_cd", description="시도코드")
    시군구코드: Optional[str] = Field(None, alias="sgg_cd", description="시군구코드")
    생성일자: Optional[str] = Field(None, alias="crtn_day", description="생성일자")

    class Config:
        populate_by_name = True


class BrWclfItem(BaseModel):
    """건축물대장 오수정화시설 항목."""

    mgm_bldrgst_pk: Optional[str] = Field(None, description="관리 건축물대장 PK")
    법정동코드: Optional[str] = Field(None, alias="bjdong_cd", description="법정동코드")
    오수정화형식코드: Optional[str] = Field(None, alias="wclf_kind_cd", description="오수정화형식코드")
    오수정화형식명: Optional[str] = Field(None, alias="wclf_kind_cd_nm", description="오수정화형식명")
    용량: Optional[str] = Field(None, alias="cap", description="용량")
    용량단위코드: Optional[str] = Field(None, alias="cap_unit_cd", description="용량단위코드")
    용량단위명: Optional[str] = Field(None, alias="cap_unit_cd_nm", description="용량단위명")
    시도코드: Optional[str] = Field(None, alias="sido_cd", description="시도코드")
    시군구코드: Optional[str] = Field(None, alias="sgg_cd", description="시군구코드")
    생성일자: Optional[str] = Field(None, alias="crtn_day", description="생성일자")

    class Config:
        populate_by_name = True


class BrRecapTitleItem(BaseModel):
    """건축물대장 총괄표제부 항목."""

    mgm_bldrgst_pk: Optional[str] = Field(None, description="관리 건축물대장 PK")
    법정동코드: Optional[str] = Field(None, alias="bjdong_cd", description="법정동코드")
    법정동명: Optional[str] = Field(None, alias="bjdong_nm", description="법정동명")
    블록: Optional[str] = Field(None, alias="block", description="블록")
    건물명: Optional[str] = Field(None, alias="bld_nm", description="건물명")
    에너지절감율: Optional[str] = Field(None, alias="enrg_saving_rate", description="에너지절감율")
    에너지효율등급: Optional[str] = Field(None, alias="enrg_efcnc_grade", description="에너지효율등급")
    인텔리전트건물등급: Optional[str] = Field(None, alias="itgn_bld_grade", description="인텔리전트건물등급")
    지번: Optional[str] = Field(None, alias="ji", description="지번")
    주용도코드: Optional[str] = Field(None, alias="main_purps_cd", description="주용도코드")
    주용도명: Optional[str] = Field(None, alias="main_purps_cd_nm", description="주용도명")
    기타용도: Optional[str] = Field(None, alias="etc_purps", description="기타용도")
    지상층수: Optional[str] = Field(None, alias="grnd_flr_cnt", description="지상층수")
    지하층수: Optional[str] = Field(None, alias="ugrnd_flr_cnt", description="지하층수")
    로트: Optional[str] = Field(None, alias="lot", description="로트")
    건폐율: Optional[str] = Field(None, alias="bc_rat", description="건폐율")
    대지면적: Optional[str] = Field(None, alias="plat_area", description="대지면적(㎡)")
    건축면적: Optional[str] = Field(None, alias="arch_area", description="건축면적(㎡)")
    연면적: Optional[str] = Field(None, alias="tot_area", description="연면적(㎡)")
    용적률: Optional[str] = Field(None, alias="vlat_rat", description="용적률")
    세대수: Optional[str] = Field(None, alias="hhld_cnt", description="세대수")
    가구수: Optional[str] = Field(None, alias="fmly_cnt", description="가구수")
    사용승인일: Optional[str] = Field(None, alias="use_aprv_date", description="사용승인일")
    시도코드: Optional[str] = Field(None, alias="sido_cd", description="시도코드")
    시도명: Optional[str] = Field(None, alias="sido_nm", description="시도명")
    시군구코드: Optional[str] = Field(None, alias="sgg_cd", description="시군구코드")
    시군구명: Optional[str] = Field(None, alias="sgg_nm", description="시군구명")
    도로명대지위치: Optional[str] = Field(None, alias="new_plat_plc", description="도로명대지위치")
    도로명: Optional[str] = Field(None, alias="road_nm", description="도로명")
    주차대수기계식: Optional[str] = Field(None, alias="pkng_cnt_mech", description="주차대수(기계식)")
    주차대수옥내자주식: Optional[str] = Field(None, alias="pkng_cnt_insdelev", description="주차대수(옥내자주식)")
    주차대수옥외자주식: Optional[str] = Field(None, alias="pkng_cnt_outsideauto", description="주차대수(옥외자주식)")
    생성일자: Optional[str] = Field(None, alias="crtn_day", description="생성일자")

    class Config:
        populate_by_name = True


class BrAtchJibunItem(BaseModel):
    """건축물대장 부속지번 항목."""

    mgm_bldrgst_pk: Optional[str] = Field(None, description="관리 건축물대장 PK")
    법정동코드: Optional[str] = Field(None, alias="bjdong_cd", description="법정동코드")
    법정동명: Optional[str] = Field(None, alias="bjdong_nm", description="법정동명")
    부속대장구분코드: Optional[str] = Field(None, alias="atcht_gb_cd", description="부속대장구분코드")
    부속대장구분명: Optional[str] = Field(None, alias="atcht_gb_cd_nm", description="부속대장구분명")
    지번: Optional[str] = Field(None, alias="ji", description="지번")
    지번주소: Optional[str] = Field(None, alias="plat_plc", description="지번주소")
    시도코드: Optional[str] = Field(None, alias="sido_cd", description="시도코드")
    시군구코드: Optional[str] = Field(None, alias="sgg_cd", description="시군구코드")
    생성일자: Optional[str] = Field(None, alias="crtn_day", description="생성일자")

    class Config:
        populate_by_name = True


class BrJijiguItem(BaseModel):
    """건축물대장 지역지구구역 항목."""

    mgm_bldrgst_pk: Optional[str] = Field(None, description="관리 건축물대장 PK")
    법정동코드: Optional[str] = Field(None, alias="bjdong_cd", description="법정동코드")
    지역지구구역구분코드: Optional[str] = Field(None, alias="jijig_gb_cd", description="지역지구구역구분코드")
    지역지구구역구분명: Optional[str] = Field(None, alias="jijig_gb_cd_nm", description="지역지구구역구분명")
    지역지구구역코드: Optional[str] = Field(None, alias="jigu_cd", description="지역지구구역코드")
    지역지구구역명: Optional[str] = Field(None, alias="jigu_cd_nm", description="지역지구구역명")
    대표여부: Optional[str] = Field(None, alias="reprst_yn", description="대표여부")
    시도코드: Optional[str] = Field(None, alias="sido_cd", description="시도코드")
    시군구코드: Optional[str] = Field(None, alias="sgg_cd", description="시군구코드")
    생성일자: Optional[str] = Field(None, alias="crtn_day", description="생성일자")

    class Config:
        populate_by_name = True


class SearchResponse(BaseModel):
    """API 응답 공통 모델."""

    items: List[dict]
    page_no: int
    num_of_rows: int
    total_count: int
