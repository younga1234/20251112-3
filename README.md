# 고고학 발굴조사 고찰 작성 자동화 파이프라인

> "고찰작성" 한 문장으로 국가유산청 규정에 부합하는 발굴조사 보고서 고찰 섹션을 자동 생성

Claude Code Skills를 활용한 고고학 발굴조사 보고서 고찰 작성 자동화 시스템입니다.

## 주요 기능

### 🚀 완전 자동화된 6단계 파이프라인
1. **자료 수집·정규화**: 논문, 보고서, 주변 유적 자료 자동 추출
2. **주변 유적 매칭**: 공간·시대·유형 기반 유사 유적 자동 탐색
3. **규정 체크리스트**: 국가유산청 규정 68개 항목 자동 검증
4. **고찰 초안 작성**: 8개 섹션, 30~50쪽 분량 자동 생성
5. **표·부록 생성**: 비교표, 일람표, 참고문헌 자동 정리
6. **준수 검증**: 품질 검증 후 개선된 버전 2 자동 생성

### ✨ 핵심 강점
- 📚 **학술적 엄밀성**: 모든 주장에 근거 문헌 자동 인용 [저자(연도)]
- 📊 **체계적 비교**: 주변 유적 10개 이상 자동 비교 분석
- ✅ **규정 완벽 준수**: 국가유산청 규정 68개 항목 자동 검증
- ⚡ **시간 절약**: 수일~수주 작업을 10~15분으로 단축
- 🔄 **재사용 가능**: 스킬 기반 모듈화로 다른 프로젝트에도 적용

## 설치 및 설정

### 1. Claude Code Skills 폴더 구조
```
.claude/
└── skills/
    ├── archaeology-orchestrator/  # 마스터 오케스트레이터
    ├── data-normalizer/           # 자료 정규화
    ├── similarity-matcher/        # 유사 유적 매칭
    ├── regulation-checker/        # 규정 체크리스트
    ├── discussion-drafter/        # 고찰 작성
    ├── tables-appendix/           # 표·부록 생성
    └── compliance-audit/          # 준수 검증
```

### 2. 자료 폴더 준비
```bash
# 프로젝트 루트에 3개 폴더 생성
mkdir -p 논문 발굴조사보고서 주변유적 output

# 각 폴더에 관련 자료 배치
# 논문/           : 학술 논문 PDF (최소 5개)
# 발굴조사보고서/ : 주변 지역 보고서 PDF/HWP (최소 10개)
# 주변유적/       : 주변 유적 관련 자료
```

### 3. Python 패키지 설치 (선택)
```bash
pip install pandas numpy matplotlib seaborn
pip install PyPDF2 pdfplumber  # PDF 처리
pip install olefile            # HWP 처리
```

## 빠른 시작

### 방법 1: 한 번에 실행 (추천)
Claude Code에서:
```
archaeology-orchestrator 스킬을 사용하여 고찰을 작성해주세요.

조사 정보:
- 조사명: ○○지구 유적 발굴조사
- 조사기관: ○○문화재연구원
- 조사기간: 2024.03~2024.11
- 대상지 좌표: 위도 37.5665, 경도 126.9780
- 시대: 청동기시대, 원삼국시대
- 주요 유구: 주거지 12기, 수혈 34기
- 주요 유물: 무문토기, 석기, 적색마연토기
```

### 방법 2: 단계별 실행
```
# 1단계
data-normalizer 스킬 실행

# 2단계
similarity-matcher 스킬 실행

# ... 이하 순차 실행
```

## 사용 예시

### 입력
```
3개 폴더에 자료 배치:
- 논문/: 15개 PDF
- 발굴조사보고서/: 25개 PDF/HWP
- 주변유적/: 8개 파일

조사 정보 입력: 위 형식 참고
```

### 출력 (약 12분 후)
```
output/
├── final/
│   ├── discussion_v2.md         ⭐ 고찰 최종본 (42쪽)
│   ├── compliance_report.md     📋 검증 보고서 (준수율 92%)
│   └── change_log.md            📝 변경 이력
├── draft/
│   ├── tables.md                📊 비교표 7개
│   ├── references.md            📚 참고문헌 42개
│   └── appendix.md              📎 부록
└── ... (중간 산출물)
```

## 출력물 활용

### 1. 고찰 최종본 (discussion_v2.md)
- 발굴조사 보고서 "고찰" 섹션으로 바로 사용 가능
- 8개 필수 구성: 성과 종합, 유구 분석, 유물 편년, 주변 비교, 의의, 보존, 향후 과제, 결론
- 42쪽, 68개 인용, 15개 도면 언급

### 2. 비교표 (tables.md)
- 주변 유사 유적 비교표
- 유구·유물 일람표
- 시대별 분포표
- 보고서 본문 또는 부록에 삽입

### 3. 참고문헌 (references.md)
- 가나다순 정리
- 단행본, 논문, 보고서, 기타 분류
- 보고서 말미에 삽입

### 4. 검증 보고서 (compliance_report.md)
- 규정 준수율 확인
- 미흡 항목 보완 가이드
- 내부 검토 자료로 활용

## 고급 활용

### 커스터마이징
각 스킬의 `SKILL.md` 파일을 편집하여:
- 비교 반경 조정 (20km → 50km)
- 인용 형식 변경
- 출력 형식 추가 (PDF, DOCX 등)

### 재실행
자료 추가 후 특정 스킬만 재실행 가능:
```
# 논문 5개 추가 수집 후
data-normalizer 재실행

# 고찰 내용만 다시 생성
discussion-drafter 재실행
```

### 병렬 처리
대용량 자료(100개 이상 파일) 처리 시 병렬 처리 활성화:
```python
# data-normalizer 설정 조정
parallel: true
max_workers: 4
```

## 문제 해결

### Q: "좌표 정보가 없습니다" 오류
**A**: 보고서에 좌표 미기재 시 지명으로 지오코딩 시도 또는 수동 입력

### Q: 주변 유적이 5개 미만
**A**: 비교 반경 자동 확대 (20→50→100km) 또는 시대 범위 확장

### Q: C14 연대 측정 자료 없음
**A**: 형식학적 편년으로 대체, 고찰에서 한계 명시

### Q: 참고문헌과 본문 인용 불일치
**A**: compliance-audit에서 자동 수정, 또는 references.md 수동 편집

더 많은 문제 해결은 각 스킬의 `SKILL.md` 파일 참고

## 스킬 상세 설명

### 1. archaeology-orchestrator
- **역할**: 전체 파이프라인 제어
- **입력**: 조사 정보
- **출력**: 6단계 순차 실행

### 2. data-normalizer
- **역할**: 자료 수집 및 메타데이터 추출
- **기술**: PDF/HWP 텍스트 추출, 정규식 메타데이터 파싱
- **출력**: documents.jsonl, metadata.csv

### 3. similarity-matcher
- **역할**: 주변 유사 유적 탐색 및 랭킹
- **알고리즘**: Haversine 거리 + Jaccard 유사도
- **출력**: nearby_ranked.csv, nearby_summaries.jsonl

### 4. regulation-checker
- **역할**: 국가유산청 규정 체크리스트 생성
- **근거**: 발굴조사의 방법 및 절차 등에 관한 규정
- **출력**: checklist.md, gaps.md

### 5. discussion-drafter
- **역할**: 고찰 8개 섹션 작성
- **분량**: 30~50쪽
- **출력**: discussion.md (v1)

### 6. tables-appendix
- **역할**: 비교표, 일람표, 참고문헌 생성
- **출력**: tables.md, appendix.md, references.md

### 7. compliance-audit
- **역할**: 규정 준수 검증 및 개선
- **검증**: 68개 항목, 정량 기준 7개, 인용 무결성
- **출력**: discussion_v2.md, compliance_report.md

## 기술 스택

- **Claude Code Skills**: 스킬 기반 모듈화
- **Python**: 데이터 처리 (pandas, numpy)
- **정규식**: 메타데이터 추출
- **지리 계산**: Haversine 공식
- **자연어 처리**: 텍스트 요약, 인용 추출

## 라이센스 및 저작권

### 스킬 소스코드
MIT License - 자유롭게 사용·수정·배포 가능

### 자료 및 산출물
- 수집한 보고서·논문: 원저작자 저작권 존중
- 생성된 고찰: 조사기관 소유, 내부 분석용
- 최종 보고서 발간 시 국가유산청 규정 준수 필수

## 기여 및 개선

### 버그 리포트
Claude Code에 이슈 설명 또는 로그 파일 첨부

### 기능 제안
- 도면 자동 생성
- 다국어 지원 (영어, 일본어)
- 웹 UI
- 클라우드 협업

### 풀 리퀘스트
개선된 SKILL.md 파일 공유

## 로드맵

### v1.0 (현재)
- ✅ 6단계 파이프라인 완성
- ✅ 국가유산청 규정 준수
- ✅ 주변 유적 자동 비교

### v1.1 (계획)
- [ ] 도면 자동 생성 (matplotlib)
- [ ] Excel 출력 (openpyxl)
- [ ] PDF 보고서 생성 (pandoc)

### v2.0 (구상)
- [ ] 웹 UI (Streamlit)
- [ ] 다국어 지원
- [ ] 클라우드 스토리지 연동

## 참고 자료

- [국가유산청](https://www.heritage.go.kr)
- [국가유산 협업포털](https://www.k-heritage.or.kr)
- [Claude Code Skills 공식 문서](https://code.claude.com/docs/en/skills)
- [발굴조사 업무 처리지침](https://...)

## 지원

문제나 질문이 있으면:
1. 각 스킬의 `SKILL.md` 파일 참고
2. `output/*/extraction_log.txt` 로그 확인
3. Claude Code에 직접 문의

---

**Archaeology Report Pipeline v1.0.0**
고고학 발굴조사 보고서 작성의 미래

"고찰작성" 한 문장으로 수주 작업을 10분으로 단축하세요.
