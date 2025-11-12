# 고고학 발굴조사 고찰 작성 자동화 파이프라인 - 사용 가이드

완전한 처음부터 끝까지 실행 가이드입니다.

## 목차
1. [사전 준비](#1-사전-준비)
2. [자료 수집 및 배치](#2-자료-수집-및-배치)
3. [파이프라인 실행](#3-파이프라인-실행)
4. [결과물 확인 및 활용](#4-결과물-확인-및-활용)
5. [문제 해결](#5-문제-해결)
6. [고급 활용](#6-고급-활용)

---

## 1. 사전 준비

### 1.1 Claude Code 환경 확인
```bash
# 현재 디렉터리 확인
pwd
# 출력 예: /home/user/20251112-1

# .claude/skills 폴더 존재 확인
ls -la .claude/skills
# 다음 7개 폴더가 있어야 함:
# - archaeology-orchestrator
# - data-normalizer
# - similarity-matcher
# - regulation-checker
# - discussion-drafter
# - tables-appendix
# - compliance-audit
```

### 1.2 프로젝트 폴더 구조 생성
```bash
# 필수 폴더 생성
mkdir -p 논문 발굴조사보고서 주변유적 output

# 폴더 구조 확인
tree -L 1
```

**올바른 구조**:
```
.
├── .claude/
│   └── skills/
│       ├── archaeology-orchestrator/
│       ├── data-normalizer/
│       └── ... (총 7개)
├── 논문/                    # 여기에 논문 PDF 배치
├── 발굴조사보고서/          # 여기에 보고서 PDF/HWP 배치
├── 주변유적/                # 여기에 주변 유적 자료 배치
├── output/                  # 자동 생성됨
└── README.md
```

---

## 2. 자료 수집 및 배치

### 2.1 논문/ 폴더
**목적**: 해당 시대·지역·유형 관련 학술 논문

**수집 방법**:
- 학술연구정보서비스(RISS): https://www.riss.kr
- DBpia: https://www.dbpia.co.kr
- 한국고고학회: http://www.archaeology.or.kr

**권장 수량**: 최소 5개, 이상적으로 10~20개

**검색 키워드 예시**:
```
- "청동기시대 주거지"
- "○○지역 선사시대"
- "무문토기 편년"
- "환상취락 구조"
```

**파일 배치**:
```bash
cp ~/Downloads/김철수_2020_청동기취락연구.pdf 논문/
cp ~/Downloads/이영희_2018_무문토기편년.pdf 논문/
...
```

### 2.2 발굴조사보고서/ 폴더
**목적**: 주변 지역(반경 20~50km) 발굴조사 보고서

**수집 방법**:
- 국가유산 협업포털: https://www.k-heritage.or.kr
- 한국문화재조사연구기관협회: http://www.jia.or.kr
- 조사기관 홈페이지

**권장 수량**: 최소 10개, 이상적으로 20~30개

**선정 기준**:
- 대상지로부터 반경 20~50km 이내
- 동일 또는 유사 시대 (청동기, 원삼국 등)
- 유사한 유구 유형 (주거지, 수혈 등)

**파일 배치**:
```bash
cp ~/Downloads/△△유적_발굴조사보고서_2018.pdf 발굴조사보고서/
cp ~/Downloads/□□유적_2019.hwp 발굴조사보고서/
...
```

### 2.3 주변유적/ 폴더
**목적**: 주변 유적 관련 보조 자료

**포함 자료**:
- 주변 유적 약식 보고서
- 신문 기사 (중요 발견 관련)
- 학회 발표 자료
- 문화재청 보도자료

**권장 수량**: 5~10개

**파일 배치**:
```bash
cp ~/Downloads/☆☆유적_약보고.pdf 주변유적/
cp ~/Downloads/◇◇유적_발표자료.pdf 주변유적/
...
```

### 2.4 자료 점검 체크리스트
```markdown
- [ ] 논문 폴더: 최소 5개 PDF 파일
- [ ] 발굴조사보고서 폴더: 최소 10개 PDF/HWP 파일
- [ ] 주변유적 폴더: 5개 이상 파일
- [ ] 모든 파일이 열리는지 확인 (암호화 없음)
- [ ] 파일명이 한글이어도 괜찮음
```

---

## 3. 파이프라인 실행

### 3.1 조사 정보 준비
다음 정보를 미리 메모장에 정리해두세요:

```yaml
조사명: "○○지구 도시개발사업 부지 내 유적 발굴조사"
조사기관: "○○문화재연구원"
조사기간: "2024년 3월 ~ 2024년 11월"
조사면적: "5,000㎡"

대상지_위치:
  주소: "○○시 △△동 123번지 일원"
  좌표:
    위도: 37.5665
    경도: 126.9780
  # 좌표는 Google Maps에서 확인 가능

비교_반경: 20  # km 단위

주요_시대:
  - "청동기시대 전기~후기"
  - "원삼국시대"

주요_유구:
  주거지:
    수량: 12기
    형태: "원형 5기, 방형 7기"
  수혈유구:
    수량: 34기
    형태: "원형 및 타원형"

주요_유물:
  토기:
    - "무문토기 구연부 26점"
    - "적색마연토기 18점"
  석기:
    - "석촉 12점"
    - "석도 5점"
    - "마제석검 1점"
  기타:
    - "철기류 4점"

특기사항:
  - "환상 배치 구조 확인"
  - "원형→방형 주거지 변화 관찰"
  - "C14 측정 1건 (B.C. 1050~920)"
```

### 3.2 파이프라인 실행
Claude Code에서 다음과 같이 입력:

```
archaeology-orchestrator 스킬을 사용하여 고찰을 작성해주세요.

조사 정보:
- 조사명: ○○지구 도시개발사업 부지 내 유적 발굴조사
- 조사기관: ○○문화재연구원
- 조사기간: 2024년 3월 ~ 2024년 11월
- 조사면적: 5,000㎡
- 대상지 좌표: 위도 37.5665, 경도 126.9780
- 비교 반경: 20km
- 주요 시대: 청동기시대, 원삼국시대
- 주요 유구: 주거지 12기 (원형 5, 방형 7), 수혈 34기
- 주요 유물: 무문토기 26점, 적색마연토기 18점, 석기 17점, 철기 4점
- 특기사항: 환상 배치 구조, 원형→방형 주거지 변화, C14 1건
```

### 3.3 진행 과정 모니터링
파이프라인 실행 중 각 단계별 출력:

```
🔄 STEP 1/6: data-normalizer 실행 중...
   📁 논문/ 폴더 스캔: 15개 파일 발견
   📁 발굴조사보고서/ 폴더 스캔: 25개 파일 발견
   📁 주변유적/ 폴더 스캔: 8개 파일 발견
   ⏳ 텍스트 추출 중... (예상 2~3분)
   [████████████████████] 100% (48/48 파일)
   ✅ 성공: 42개, ⚠️ 실패: 6개 (암호화 또는 손상)
   💾 output/normalized/documents.jsonl 생성 (12.5MB)
   💾 output/normalized/metadata.csv 생성 (125KB)
✓ STEP 1/6 완료 (2분 18초)

🔄 STEP 2/6: similarity-matcher 실행 중...
   🗺️ 반경 20km 내 유적 탐색...
   📊 18개 유적 발견, 유사도 계산 중...
   🏆 상위 10개 유적 선정
   💾 output/compare/nearby_ranked.csv 생성
   💾 output/compare/nearby_summaries.jsonl 생성
✓ STEP 2/6 완료 (1분 45초)

🔄 STEP 3/6: regulation-checker 실행 중...
   📋 규정 체크리스트 68개 항목 생성
   🔍 현재 자료 대비 결손 분석...
   ⚠️ 불충분 항목 5개 식별
   💾 output/compliance/checklist.md 생성
   💾 output/compliance/gaps.md 생성
✓ STEP 3/6 완료 (0분 32초)

🔄 STEP 4/6: discussion-drafter 실행 중...
   ✍️ I. 서론 작성 중...
   ✍️ II. 유구의 성격 및 기능 해석 작성 중...
   ✍️ III. 유물의 편년 및 계통 작성 중...
   ✍️ IV. 주변 유적과의 비교 분석 작성 중... (⭐ 핵심 섹션)
   ✍️ V. 역사·고고학적 의의 작성 중...
   ✍️ VI. 보존 및 활용 방안 작성 중...
   ✍️ VII. 향후 과제 및 제언 작성 중...
   ✍️ VIII. 결론 작성 중...
   📊 분량: 42쪽, 인용: 68개, 도면 언급: 15개
   💾 output/draft/discussion.md 생성 (185KB)
✓ STEP 4/6 완료 (4분 52초)

🔄 STEP 5/6: tables-appendix 실행 중...
   📊 표 1: 주변 유사 유적 비교표 생성
   📊 표 2: 유구 일람표 생성
   📊 표 3: 유물 관찰표 생성
   📚 참고문헌 42개 정리
   🌐 영문 초록 256단어 생성
   💾 output/draft/tables.md 생성
   💾 output/draft/references.md 생성
   💾 output/draft/appendix.md 생성
✓ STEP 5/6 완료 (1분 28초)

🔄 STEP 6/6: compliance-audit 실행 중...
   🔍 체크리스트 68개 항목 검증...
   ✅ 충족: 63개 (92%)
   ⚠️ 미흡: 5개
   🔧 개선안 생성 중...
   📝 Version 2 작성 중... (3개 항목 보완)
   📋 준수 보고서 작성 중...
   💾 output/final/discussion_v2.md 생성
   💾 output/final/compliance_report.md 생성
   💾 output/final/change_log.md 생성
✓ STEP 6/6 완료 (1분 55초)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 파이프라인 완료!
⏱️ 총 소요 시간: 12분 50초

📦 최종 산출물:
   📄 output/final/discussion_v2.md       (고찰 최종본, 42쪽)
   📊 output/draft/tables.md              (비교표 7개)
   📚 output/draft/references.md          (참고문헌 42개)
   📎 output/draft/appendix.md            (부록)
   📋 output/final/compliance_report.md   (검증 보고서)
   📝 output/final/change_log.md          (변경 이력)

🎉 "고찰작성" 완료! output/final/discussion_v2.md를 확인하세요.
```

---

## 4. 결과물 확인 및 활용

### 4.1 출력 폴더 구조
```bash
tree output/
```

```
output/
├── normalized/              # STEP 1 산출물
│   ├── documents.jsonl      # 전체 문서 내용 (12.5MB)
│   ├── metadata.csv         # 메타데이터 요약 (125KB)
│   └── extraction_log.txt   # 처리 로그
├── compare/                 # STEP 2 산출물
│   ├── nearby_ranked.csv    # 주변 유적 랭킹
│   ├── nearby_summaries.jsonl  # 유적별 요약
│   └── map_visualization.html  # 분포 지도 (선택)
├── compliance/              # STEP 3 산출물
│   ├── checklist.md         # 규정 체크리스트
│   ├── gaps.md              # 결손 항목 보고서
│   └── regulation_references.md
├── draft/                   # STEP 4, 5 산출물
│   ├── discussion.md        # 고찰 초안 (v1)
│   ├── tables.md            # 비교표·일람표
│   ├── appendix.md          # 부록
│   ├── references.md        # 참고문헌
│   └── abstract_en.md       # 영문 초록
└── final/                   # ⭐ STEP 6 최종 산출물
    ├── discussion_v2.md     # 고찰 최종본
    ├── compliance_report.md # 검증 보고서
    └── change_log.md        # 변경 이력
```

### 4.2 주요 파일 확인

#### (1) 고찰 최종본 (discussion_v2.md)
```bash
# 파일 열기
cat output/final/discussion_v2.md
# 또는 텍스트 에디터로 열기
```

**내용**:
```markdown
# 고찰(考察)

## I. 서론

○○지구 유적에 대한 이번 발굴조사는 [조사 배경]을 목적으로
○○문화재연구원에 의해 2024년 3월~11월에 걸쳐 실시되었다.
조사 결과, 총 5,000㎡ 내에서 청동기시대~원삼국시대에 해당하는
주거지 12기, 수혈유구 34기, 출토 유물 66점이 확인되었다.

주요 발견사항은 다음과 같다:
1. 환상 배치 구조: 중앙 광장을 중심으로 주거지가 원형으로 배치 [이영희(2018)]
2. 주거지 형태 변화: 원형(청동기)→방형(원삼국) 전환 [김철수(2020)]
3. 마제석검 출토: 사회적 계층화 시사 [박민수(2019)]

[표 1: 유구 종류별 수량]
| 유구 종류 | 수량 | 시대 추정 | 비고 |
|----------|------|----------|------|
| 주거지   | 12기 | 청동기~원삼국 | 원형 5, 방형 7 |
| 수혈유구 | 34기 | 청동기~원삼국 | 저장혈 추정 |

[...중략...]

## IV. 주변 유적과의 비교 ⭐

본 절에서는 대상지로부터 반경 20km 이내의 청동기~원삼국 유적 중
유사도가 높은 상위 10개 유적을 선정하여 비교 분석하였다.

[표 2: 주변 유사 유적 비교표]
| 연번 | 유적명 | 거리 | 시대 | 주요 유구 | 유사도 | 출처 |
|------|--------|------|------|-----------|--------|------|
| 1 | △△유적 | 5.2km | 청동기 전기 | 원형주거 8기 | 85.6 | ○○연구원(2018) |
| 2 | □□유적 | 12.8km | 청동기 후기 | 방형주거 15기 | 78.3 | △△대학(2019) |
[...10개 유적...]

### 1. 공간 분포
선정된 유적들은 모두 하안단구에 입지하며, ○○천 수계를 따라
5~15km 간격으로 분포한다 [지도 1]. 이는 청동기시대 취락이
수계를 중심으로 네트워크를 형성했음을 시사한다 [최○○(2017)].

### 2. 주거지 형태 비교
원형 주거지는 인근 △△유적, ☆☆유적과 직경·노지 위치·벽구 구조가
거의 일치하여 [도면 비교 12], 동일 문화권에 속했을 가능성이 높다...

[...계속...]

## VIII. 결론

○○지구 유적 발굴조사는 ○○지역 청동기~원삼국시대 취락의
실체를 구체적으로 밝혀낸 중요한 성과이다. 특히 환상 배치 구조,
주거지 형태 변화, 주변 유적과의 문화적 교류는 이 지역이
광역 네트워크 내에서 일정한 역할을 수행한 거점 취락이었음을 시사한다.

**주요 성과 요약**:
1. 청동기~원삼국 복합 취락 구조 확인
2. 환상 배치 및 주거지 형태 변화 실증
3. C14 연대 기준점 확보 (B.C. 1050~920)
4. 주변 유적과의 문화적 교류망 규명
5. 지역 취락 고고학 연구의 기초 자료 확보
```

#### (2) 검증 보고서 (compliance_report.md)
```bash
cat output/final/compliance_report.md
```

**주요 내용**:
```markdown
# 국가유산청 규정 준수 검증 보고서

## 종합 평가
- 전체 준수율: 92% (68개 항목 중 63개 충족)
- 고찰 섹션: 95% (40개 항목 중 38개 충족)
- 등급: **우수** ⭐⭐⭐⭐

## 정량 기준 검증
| 항목 | 필요 | 실제 | 충족 |
|------|------|------|------|
| 전체 분량 | 30~50쪽 | 42쪽 | ✓ |
| 본문 인용 | ≥50개 | 68개 | ✓ |
| 표 개수 | ≥5개 | 7개 | ✓ |
| 주변 유적 비교 | ≥5개 | 10개 | ✓ |
| 참고문헌 | ≥30개 | 42개 | ✓ |

## 최종 의견
본 고찰은 국가유산청 규정을 충실히 준수하며,
학술적 수준이 높습니다. 승인 의견: 발굴조사 보고서 발간에 적합.
```

### 4.3 활용 방법

#### 고찰 최종본 활용
```markdown
1. **보고서 본편에 삽입**
   - discussion_v2.md를 워드프로세서(HWP, Word)에 복사
   - 서식 조정 (글꼴, 줄간격 등)
   - 도면·사진 실물 삽입

2. **표 삽입**
   - tables.md의 표들을 해당 위치에 삽입
   - 표 번호를 본편 전체 흐름에 맞게 재조정

3. **참고문헌 삽입**
   - references.md를 보고서 말미에 삽입

4. **영문 초록 삽입**
   - abstract_en.md를 보고서 서두 또는 말미에 삽입
```

#### 검증 보고서 활용
```markdown
1. **내부 검토 자료**
   - 조사단 회의에서 품질 확인 자료로 활용
   - 미흡 항목 보완 계획 수립

2. **자문위원 제출**
   - 고찰 초안과 함께 검증 보고서 제출
   - 객관적 품질 평가 자료로 활용
```

---

## 5. 문제 해결

### 5.1 자료 추출 오류

#### 문제: "PDF를 읽을 수 없습니다" 오류
**원인**: PDF 암호화, 스캔 PDF (이미지), 파일 손상

**해결**:
```bash
# 암호화 PDF: 암호 해제 후 재배치
# 스캔 PDF: OCR 처리 또는 제외
# 손상 파일: 재다운로드 또는 제외

# 로그 확인
cat output/normalized/extraction_log.txt | grep "실패"
```

#### 문제: "HWP 파일 오류"
**원인**: 구버전 HWP (97, 2002 등)

**해결**:
```bash
# HWP → PDF 변환 (한글 프로그램 사용)
# 또는 hwp5txt 설치
sudo apt install hwp5txt
hwp5txt 파일.hwp > 파일.txt
```

### 5.2 메타데이터 추출 불완전

#### 문제: "좌표 정보가 없습니다"
**원인**: 보고서에 좌표 미기재 또는 다른 형식

**해결**:
```python
# similarity-matcher 설정 수정
# 지오코딩 활성화 (지명→좌표 자동 변환)
geocoding: true

# 또는 수동으로 metadata.csv 편집
# 파일 열기: output/normalized/metadata.csv
# 해당 행의 lat, lon 열에 좌표 입력
```

#### 문제: "시대 정보 추출 실패"
**원인**: 비표준 용어 사용 (예: "B.C. 1000년대" vs "청동기시대")

**해결**:
```python
# data-normalizer 설정 수정
# 키워드 추가
period_keywords:
  - "청동기"
  - "초기철기"
  - "B.C. 1000"  # 추가
  - "기원전"     # 추가
```

### 5.3 주변 유적 부족

#### 문제: "반경 20km 내 유적 5개 미만"
**원인**: 자료 부족, 지역 특성 (산간, 섬 등)

**해결**:
```
방법 1: 반경 자동 확대
- similarity-matcher는 5개 미만 시 자동으로 50km, 100km로 확대

방법 2: 시대 범위 확장
- "청동기시대"만 → "청동기~철기시대"로 확장

방법 3: 추가 자료 수집
- 발굴조사보고서/ 폴더에 더 많은 보고서 추가 후 재실행
```

### 5.4 고찰 품질 문제

#### 문제: "인용이 너무 적습니다 (30개 이하)"
**원인**: 수집 자료 부족

**해결**:
```
1. 논문/ 폴더에 논문 10개 이상 추가
2. data-normalizer 재실행
3. discussion-drafter 재실행
```

#### 문제: "주변 유적 비교가 부실합니다"
**원인**: nearby_summaries.jsonl에 요약이 불충분

**해결**:
```
1. similarity-matcher 재실행 (더 많은 유적 포함)
2. 또는 discussion.md를 수동 편집하여 비교 내용 보강
```

### 5.5 규정 준수 문제

#### 문제: "준수율 80% 미만"
**원인**: 필수 자료 부족 (C14, 도면, 과학 분석 등)

**해결**:
```markdown
1. gaps.md 파일 확인
   → 어떤 항목이 부족한지 파악

2. 조사단에 요청
   - 도면 파일 확보
   - C14 분석 결과 확보
   - 유구·유물 상세 데이터 확보

3. 대체 방안
   - C14 없음: 형식학적 편년으로 대체, 한계 명시
   - 과학 분석 없음: "향후 과제"에 포함
```

---

## 6. 고급 활용

### 6.1 개별 스킬만 실행

특정 단계만 재실행하고 싶을 때:

```bash
# STEP 1만: 자료 추가 후 재정규화
"data-normalizer 스킬을 실행해주세요"

# STEP 4만: 고찰 내용만 수정
"discussion-drafter 스킬을 실행해주세요"

# STEP 6만: 검증만 재실행
"compliance-audit 스킬을 실행해주세요"
```

### 6.2 파라미터 조정

#### 비교 반경 변경
```python
# similarity-matcher/SKILL.md 편집
default_radius: 50  # 20 → 50km로 변경
```

#### 인용 형식 변경
```python
# discussion-drafter/SKILL.md 편집
citation_format: "author_year"  # [저자(연도)]
# 또는
citation_format: "number"       # [1], [2] 형식
```

### 6.3 출력 형식 추가

#### PDF 생성 (Pandoc 사용)
```bash
# Pandoc 설치
sudo apt install pandoc texlive-xetex

# Markdown → PDF 변환
pandoc output/final/discussion_v2.md \
  -o output/final/discussion_v2.pdf \
  --pdf-engine=xelatex \
  -V mainfont="NanumGothic" \
  -V geometry:margin=2.5cm
```

#### Word 파일 생성
```bash
# Markdown → DOCX 변환
pandoc output/final/discussion_v2.md \
  -o output/final/discussion_v2.docx \
  --reference-doc=template.docx  # 서식 템플릿 (선택)
```

### 6.4 병렬 처리 (대용량 자료)

100개 이상 파일 처리 시:

```python
# data-normalizer/SKILL.md에 추가
parallel_processing: true
max_workers: 4  # CPU 코어 수에 맞게
batch_size: 10  # 한 번에 처리할 파일 수
```

### 6.5 자동화 스크립트

매번 동일한 설정으로 실행 시:

```bash
# run_pipeline.sh 생성
cat > run_pipeline.sh << 'EOF'
#!/bin/bash

# 자료 확인
echo "자료 파일 수 확인..."
논문_수=$(ls 논문/*.pdf | wc -l)
보고서_수=$(ls 발굴조사보고서/*.{pdf,hwp} 2>/dev/null | wc -l)

echo "논문: ${논문_수}개"
echo "보고서: ${보고서_수}개"

if [ $논문_수 -lt 5 ] || [ $보고서_수 -lt 10 ]; then
  echo "⚠️ 자료 부족! 최소 논문 5개, 보고서 10개 필요"
  exit 1
fi

# Claude Code 실행
echo "파이프라인 실행..."
claude code << 'CLAUDE_INPUT'
archaeology-orchestrator 스킬을 사용하여 고찰을 작성해주세요.

[사전 설정된 조사 정보...]
CLAUDE_INPUT

echo "✓ 완료!"
EOF

chmod +x run_pipeline.sh
./run_pipeline.sh
```

---

## 부록: 자주 묻는 질문 (FAQ)

### Q1: 파이프라인 실행 시간은 얼마나 걸리나요?
**A**: 자료 양에 따라 10~20분. 파일 50개 기준 약 12분.

### Q2: 인터넷 연결이 필요한가요?
**A**: 지오코딩(지명→좌표 변환) 사용 시 필요, 그 외 오프라인 가능.

### Q3: 여러 유적을 동시에 처리할 수 있나요?
**A**: 각 유적별로 별도 프로젝트 폴더 생성 후 개별 실행 권장.

### Q4: 생성된 고찰을 그대로 제출해도 되나요?
**A**: 초안이므로 반드시 전문가 검토 후 도면·사진 추가, 서식 조정 필요.

### Q5: 비용이 드나요?
**A**: Claude Code 사용료 외 추가 비용 없음. (오픈소스 도구 사용)

### Q6: 다른 시대(삼국, 고려, 조선)도 가능한가요?
**A**: 가능. 시대 키워드만 수정하면 됨.
```python
# regulation-checker/SKILL.md
period_keywords:
  - "삼국시대"
  - "고려시대"
  - "조선시대"
```

### Q7: 영문 보고서도 작성할 수 있나요?
**A**: 현재 한국어만 지원. 향후 버전에서 다국어 지원 예정.

### Q8: 오류가 나면 어떻게 하나요?
**A**:
1. 로그 파일 확인: `output/*/extraction_log.txt`
2. 해당 스킬의 `SKILL.md` 파일에서 "문제 해결" 섹션 참고
3. Claude Code에 오류 메시지 복사하여 질문

---

**이 가이드로 충분하지 않은 경우, 각 스킬의 SKILL.md 파일을 직접 확인하세요!**

- `.claude/skills/archaeology-orchestrator/SKILL.md`
- `.claude/skills/data-normalizer/SKILL.md`
- `.claude/skills/similarity-matcher/SKILL.md`
- `.claude/skills/regulation-checker/SKILL.md`
- `.claude/skills/discussion-drafter/SKILL.md`
- `.claude/skills/tables-appendix/SKILL.md`
- `.claude/skills/compliance-audit/SKILL.md`

**Happy Archaeology! 🏺**
