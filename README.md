# my-stock-team

종목명을 입력하면 애널리스트 에이전트들이 협업해 리서치를 수행하고, 그 결과를 **PPTX 리포트**로 내보내는 주식 분석용 Claude Code 플러그인입니다.

- 분석 관점: **가치투자(Value Investing)** — 기업의 내재가치·펀더멘털·안전마진 중심
- 사용 환경: [Claude Code](https://claude.com/claude-code)
- 성격: **실습용 더미 프로젝트** (투자 권유가 아니며 교육·학습 목적)

> ⚠️ 본 저장소의 산출물은 학습용 분석이며, 매수·매도 권유가 아닙니다.

## 동작 방식

종목 1건이 들어오면 메인(오케스트레이터)이 애널리스트 에이전트들에게 작업을 위임하고, 결과를 취합해 5부 구성 PPTX 리포트로 만듭니다.

```
종목명 입력
   │
   ├─ 입력 정규화 (종목명 → 6자리 코드 → DART corp_code)
   │
   ├─ 병렬 fan-out (서로 독립인 분석 동시 위임)
   │     ├─ fundamental-analyst   재무·실적·공시  (DART OpenAPI)
   │     ├─ market-tech-analyst   주가·추세·거래량 (FinanceDataReader)
   │     └─ daily-econ-indicators 금리·물가·환율   (매크로 지표)
   │
   ├─ 리스크 점검 (3개 결과에서 추출)
   ├─ 종합의견 (가치투자 관점 종합, 매수/매도 단정 없이 근거까지만)
   │
   └─ PPTX 출력 (report-pptx 스킬)
```

## 애널리스트 명단

| 에이전트 | 담당 | 데이터 소스 | 리포트 섹션 |
|----------|------|-------------|-------------|
| `fundamental-analyst` | 재무·실적·공시 | DART OpenAPI | 재무 |
| `market-tech-analyst` | 주가·추세·거래량 | FinanceDataReader | 차트 |
| `daily-econ-indicators` | 금리·물가·고용·환율 | 매크로 지표 | 시장 배경 |
| 리스크 / 리드 (공석) | 리스크·종합의견 | — | 리스크 · 종합의견 |

> 공석(리스크·리드)은 충원 전까지 메인 오케스트레이터가 규칙을 지키며 대행합니다.

## 리포트 구성 (5부)

1. **표지**
2. **재무**
3. **차트**
4. **리스크**
5. **종합의견**

- 문체는 "~입니다" 체로 통일
- 모든 수치에 **출처**와 **기준일** 병기
  - 재무: `(출처: DART, {연도}/{분기})`
  - 시세: `(출처: FinanceDataReader, 기준일: YYYY-MM-DD)`

## 디렉터리 구조

```
.
├── CLAUDE.md                  # 오케스트레이션 규칙 (프로젝트 지침)
├── .claude/
│   ├── agents/                # 애널리스트 에이전트 정의
│   ├── skills/report-pptx/    # Markdown 리서치 → PPTX 변환 스킬
│   ├── agent-memory/          # 에이전트별 영속 메모리
│   └── settings.local.json
├── templates/                 # 리포트 양식 / PPTX 템플릿
├── src/                       # 분석·데이터·리포트 코드
└── reports/                   # 생성된 리포트 (gitignore)
```

## 사전 준비

### 1. 시크릿 설정

`.env.local` 파일을 만들고 [DART OpenAPI](https://opendart.fss.or.kr) 키를 넣습니다. (이 파일은 `.gitignore`로 커밋되지 않습니다.)

```bash
# .env.local
DART_API_KEY=your_dart_api_key
DART_KEY=your_dart_api_key   # fundamental-analyst 호환용 별칭 (같은 키)
```

### 2. Python 라이브러리

```bash
pip3 install FinanceDataReader certifi python-pptx
```

> **macOS SSL 참고**: python.org 파이썬은 시스템 인증서를 못 찾아 FDR·DART 호출 시 SSL 검증이 실패할 수 있습니다. `certifi`로 컨텍스트를 지정하세요.
>
> ```python
> import ssl, certifi, functools
> ssl._create_default_https_context = functools.partial(
>     ssl.create_default_context, cafile=certifi.where())
> ```

## 사용 예시

Claude Code에서 종목명을 던지면 됩니다.

```
삼성전자 리서치 리포트 만들어줘
```

## 🌐 웹앱 (종목명 → PPTX 다운로드)

종목명만 입력하면 브라우저에서 바로 투자 리포트(PPTX)를 생성·다운로드하는 간단한 Flask 웹앱입니다. 에이전트 팀과 동일한 데이터 소스(DART·FinanceDataReader)에서 **실제 수치**를 받아 규칙 기반으로 5부 리포트를 채웁니다(LLM 미사용, 빠름).

```bash
pip3 install -r web/requirements.txt
python3 web/app.py
# → http://127.0.0.1:5000
```

- 입력: 종목명(예: `삼성전자`) 또는 6자리 코드(예: `005930`)
- 출력: `표지·재무·차트·리스크·종합의견` 5부 16:9 PPTX 다운로드
- 재무는 `.env.local`의 `DART_API_KEY` 필요(미설정 시 해당 섹션 "확인 불가")
- 매수·매도 의견/목표가 미제시, 출처·기준일 병기, 학습용 — 가드레일은 동일하게 적용

## 가드레일

- **매수·매도 단정 표현 금지** — 판단 근거까지만 제시 (목표가·매매 타이밍 제시 안 함)
- **출처 없는 수치 금지** — 확인 불가한 숫자는 "확인 불가"로 명시
- 리포트 끝에 **학습용 분석임을 명시**

## 라이선스

실습·학습용 프로젝트입니다.
