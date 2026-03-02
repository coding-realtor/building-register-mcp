# 🏢 Korea Building Register MCP

[English](#english) | [한국어](#한국어)

---

## English

Ask Claude about Korean building register data — powered by data.go.kr's Building Register API.

Provides **12 tools** for querying building register (건축물대장) information including title sheets, floor details, exclusive-use areas, house prices, zoning, and more.

### Supported Tools

| Tool | Description |
|------|-------------|
| `smart_building_lookup` | 🏢 Smart lookup — auto-detects general vs. collective buildings |
| `search_bjdong_code` | Search region codes (sigungu_cd, bjdong_cd) by name |
| `get_building_title_info` | Title sheet (표제부) — area, structure, usage, etc. |
| `get_building_recap_title_info` | Summary title sheet (총괄표제부) |
| `get_building_basis_ouln_info` | Basic outline (기본개요) |
| `get_building_floor_ouln_info` | Floor outline (층별개요) |
| `get_building_expos_info` | Exclusive-use units (전유부) |
| `get_building_expos_pubuse_area_info` | Exclusive/common area details (전유공용면적) |
| `get_building_house_price_info` | Official house prices (주택가격) |
| `get_building_wclf_info` | Sewage treatment facilities (오수정화시설) |
| `get_building_atch_jibun_info` | Attached land lots (부속지번) |
| `get_building_jijigu_info` | Zoning districts (지역지구구역) |

### Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- API key from [공공데이터포털 (data.go.kr)](https://www.data.go.kr)
  - Apply for: [건축HUB 건축물대장정보 서비스](https://www.data.go.kr/data/15044713/openapi.do)

### Quick Start: Claude Desktop (stdio)

1. **Clone this repository**

```bash
git clone https://github.com/coding-realtor/building-register-mcp.git
cd building-register-mcp
```

2. **Open the Claude Desktop config file**

```bash
# macOS
open "$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Windows
notepad %APPDATA%\Claude\claude_desktop_config.json
```

3. **Add the entry below under `mcpServers`**

```json
{
  "mcpServers": {
    "building-register": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "/path/to/building-register-mcp",
        "data-go-mcp-building-register"
      ],
      "env": {
        "BUILDING_REGISTER_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

> Replace `/path/to/building-register-mcp` with the actual path where you cloned the repository.

4. **Restart Claude Desktop**

Setup is complete when you can see the `building-register` server in the tool list.

### Usage Example

```
Tell me about the building at 서울 종로구 청운동 89-3
```

Claude will automatically:
1. Look up the region code via `search_bjdong_code`
2. Call `smart_building_lookup` to fetch building details
3. Present the results in a readable table

---

## 한국어

Claude에게 건축물대장 정보를 물어보세요 — 공공데이터포털 건축물대장정보 API 기반 MCP 서버입니다.

건축물대장 **표제부, 층별개요, 전유부, 주택가격, 지역지구구역** 등을 조회하는 **12개 도구**를 제공합니다.

### 제공 도구 (Tools)

| Tool 명 | 설명 |
|---------|------|
| `smart_building_lookup` | 🏢 스마트 조회 — 일반/집합건축물 자동 판별 |
| `search_bjdong_code` | 지역명으로 시군구코드·법정동코드 검색 |
| `get_building_title_info` | 건축물대장 **표제부** (대지면적, 건축면적, 용적률 등) |
| `get_building_recap_title_info` | 건축물대장 **총괄표제부** |
| `get_building_basis_ouln_info` | 건축물대장 **기본개요** |
| `get_building_floor_ouln_info` | 건축물대장 **층별개요** |
| `get_building_expos_info` | 건축물대장 **전유부** (동/호 정보) |
| `get_building_expos_pubuse_area_info` | 건축물대장 **전유공용면적** |
| `get_building_house_price_info` | 건축물대장 **주택가격** (공시가격) |
| `get_building_wclf_info` | 건축물대장 **오수정화시설** |
| `get_building_atch_jibun_info` | 건축물대장 **부속지번** |
| `get_building_jijigu_info` | 건축물대장 **지역지구구역** |

### 사전 준비

- [uv](https://docs.astral.sh/uv/getting-started/installation/) 설치
- [공공데이터포털](https://www.data.go.kr)에서 API 키 발급
  - 신청 대상: [건축HUB 건축물대장정보 서비스](https://www.data.go.kr/data/15044713/openapi.do)

### 빠른 시작: Claude Desktop (stdio)

1. **레포지토리 클론**

```bash
git clone https://github.com/coding-realtor/building-register-mcp.git
cd building-register-mcp
```

2. **Claude Desktop 설정 파일 열기**

```bash
# macOS
open "$HOME/Library/Application Support/Claude/claude_desktop_config.json"

# Windows
notepad %APPDATA%\Claude\claude_desktop_config.json
```

3. **`mcpServers` 항목에 아래 내용 추가**

```json
{
  "mcpServers": {
    "building-register": {
      "command": "uv",
      "args": [
        "run",
        "--directory", "C:\\path\\to\\building-register-mcp",
        "data-go-mcp-building-register"
      ],
      "env": {
        "BUILDING_REGISTER_API_KEY": "여기에_API_키_입력"
      }
    }
  }
}
```

> `C:\\path\\to\\building-register-mcp` 부분을 실제 클론한 경로로 변경하세요.

4. **Claude Desktop 재시작**

도구 목록에 `building-register` 서버가 표시되면 설정 완료입니다.

### 사용 예시 (Claude에서)

```
서울 종로구 청운동 89-3 건물의 건축물대장 조회해줘
```

```
강남구 역삼동 736번지 건물의 주택 공시가격을 알려줘
```

```
송파구 잠실동 40번지 아파트의 동/호 목록을 보여줘
```

Claude가 자동으로:
1. `search_bjdong_code`로 시군구/법정동 코드를 검색
2. `smart_building_lookup`으로 건축물 정보를 조회
3. 결과를 보기 좋은 표로 정리하여 보여줍니다

### Gemini CLI / 기타 MCP 클라이언트

Gemini CLI 등 다른 MCP 클라이언트에서도 동일하게 사용할 수 있습니다.
설정 파일의 MCP 서버 항목에 위와 같은 형식으로 추가하세요.

### 로컬 테스트

```bash
# 서버 직접 실행
uv run data-go-mcp-building-register
```

## 라이센스

Apache-2.0 — 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.
