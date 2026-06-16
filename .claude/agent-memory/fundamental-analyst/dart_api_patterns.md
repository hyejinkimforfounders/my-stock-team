---
name: dart-api-patterns
description: DART OpenAPI 호출 패턴, SSL 설정, 파라미터 코드 정리
metadata:
  type: reference
---

# DART OpenAPI 패턴 메모

## 환경 설정 (Python 3.14, macOS)
Python 3.14 환경에서 HTTPS SSL 검증 실패 발생 → certifi로 컨텍스트 강제 지정 필요:

```python
import ssl, certifi, functools
ssl._create_default_https_context = functools.partial(ssl.create_default_context, cafile=certifi.where())
# urlopen 직접 호출 시:
ctx = ssl.create_default_context(cafile=certifi.where())
with urllib.request.urlopen(url, context=ctx) as resp: ...
```

## API 키 로드
- 파일 위치: /Users/hyejin/Desktop/stock/.env.local
- 환경변수명: DART_KEY (= DART_API_KEY, 동일 값)

## fnlttSinglAcnt.json 파라미터
- URL: https://opendart.fss.or.kr/api/fnlttSinglAcnt.json
- 파라미터: crtfc_key, corp_code, bsns_year, reprt_code, fs_div
- reprt_code: 11011=사업보고서(연간), 11012=반기보고서, 11013=1분기, 11014=3분기
- fs_div: CFS=연결재무제표, OFS=별도재무제표

## 응답 구조 주의
- status='000' = 정상 (total_count=0이어도 list에 데이터 있음)
- list 배열에 연결/별도 두 세트 순서대로 포함됨 (연결 먼저)
- sj_div: BS=재무상태표, IS=손익계산서, CIS=포괄손익, CF=현금흐름, SCE=자본변동

## 주요 계정과목명
- 매출액: account_nm='매출액'
- 영업이익: account_nm='영업이익'
- 당기순이익: account_nm='당기순이익(손실)'
- 부채총계: account_nm='부채총계'
- 자본총계: account_nm='자본총계'
- 부채비율 계산: 부채총계/자본총계×100
