# PDF 에러 없이 읽기 - 완벽 가이드

Claude Code에서 PDF를 열 때 `invalid base64 data` 오류가 발생하는 문제에 대한 종합 솔루션입니다.

---

## 🚨 현재 상황

**문제:**
```
API Error: 400 {"type":"error","error":{"type":"invalid_request_error",
"message":"messages.2.content.0.pdf.source.base64.data: The PDF specified was not valid."}}
```

**원인:**
1. PDF 파일이 Git LFS에 저장되어 실제 파일이 아님
2. 114개의 PDF 파일 모두 LFS 포인터로만 존재
3. Claude Code가 포인터 파일을 읽어서 base64 변환 실패

---

## ✅ 해결책 요약

| 상황 | 해결 방법 | 시간 |
|-----|----------|------|
| **로컬 환경 (권장)** | Git LFS 설치 → PDF 다운로드 → 텍스트 변환 | 15-30분 |
| **온라인 환경** | 온라인 도구 또는 Docker 사용 | 5-10분/파일 |
| **임시 방법** | 필요한 PDF만 선택적으로 처리 | 1-2분/파일 |

---

## 🚀 빠른 시작 (로컬 환경)

### 1단계: Git LFS 설치

```bash
# Ubuntu/Debian
sudo apt-get install git-lfs
git lfs install

# macOS
brew install git-lfs
git lfs install

# Windows
choco install git-lfs
```

### 2단계: PDF 파일 다운로드

```bash
# 모든 PDF 다운로드 (1-3GB)
git lfs pull

# 검증
file "논문/三國時代 湖南地域 住居·聚落의 地域性과 變動2012-이동희ㅇ.pdf"
# 출력: PDF document (정상)
```

### 3단계: 일괄 변환

```bash
# PyPDF2 설치
pip install PyPDF2

# 모든 PDF → 텍스트 변환
python3 scripts/convert_all_pdfs.py

# 결과
# ✓ 성공: 114개
# ✓ 이제 .txt 파일로 안전하게 읽기 가능
```

### 4단계: 변환된 파일 커밋

```bash
# 변환된 텍스트 파일 커밋
git add "**/*.txt"
git commit -m "모든 PDF를 텍스트로 변환 (Claude Code 호환)"
git push
```

---

## 📚 상세 가이드

### 각 상황별 가이드

1. **`Git_LFS_PDF_변환_가이드.md`** - Git LFS 설정 및 일괄 변환
   - LFS 설치 및 설정
   - 114개 PDF 일괄 처리
   - 문제 해결

2. **`PDF_처리_가이드.md`** - PDF 개별 처리 도구
   - Bash 스크립트 (`pdf_helper.sh`)
   - Python 스크립트 (`pdf_helper.py`)
   - 명령어 예시

3. **`PDF_오류_대비책.md`** - 빠른 참조 가이드
   - 즉시 사용 가능한 해결책
   - Docker/온라인 도구
   - 크기별 권장 방법

---

## 🛠️ 도구 목록

### 1. `convert_all_pdfs.py` (일괄 변환)

```bash
python3 scripts/convert_all_pdfs.py
```

**기능:**
- 114개 PDF 자동 변환
- 스마트 캐싱 (이미 변환된 파일 건너뛰기)
- 실시간 진행 상황 표시
- 실패 파일 자동 추적

### 2. `pdf_helper.sh` (개별 처리 - Bash)

```bash
# PDF 정보 확인
./scripts/pdf_helper.sh info "논문/파일.pdf"

# 텍스트 추출
./scripts/pdf_helper.sh text "논문/파일.pdf"

# 배치 검증
./scripts/pdf_helper.sh batch-validate ./논문
```

### 3. `pdf_helper.py` (개별 처리 - Python)

```bash
# PDF 정보
python3 scripts/pdf_helper.py info "논문/파일.pdf"

# 텍스트 추출
python3 scripts/pdf_helper.py text "논문/파일.pdf"
```

---

## 💡 임시 해결책 (Git LFS 없이)

### Option A: 온라인 도구

1. https://www.ilovepdf.com/pdf_to_text
2. https://pdftotext.com/
3. https://www.adobe.com/acrobat/online/pdf-to-text.html

### Option B: Docker

```bash
docker run --rm -v "$(pwd):/data" alpine/pdftotext \
  /data/논문/파일.pdf /data/논문/파일.txt
```

### Option C: 필요한 PDF만

```bash
# 특정 PDF만 LFS에서 가져오기
git lfs pull --include "논문/특정파일.pdf"

# 변환
./scripts/pdf_helper.sh text "논문/특정파일.pdf"
```

---

## 📊 변환 진행 상황

### 현재 상태 확인

```bash
# 전체 PDF 수
find . -name "*.pdf" -type f | wc -l
# 결과: 114

# 변환 완료된 TXT 수
find . -name "*.txt" -type f | wc -l

# 변환율 계산
echo "scale=2; $(find . -name "*.txt" | wc -l) / 114 * 100" | bc
```

### 폴더별 통계

```bash
# 논문 폴더
ls 논문/*.pdf | wc -l
ls 논문/*.txt | wc -l

# 장흥주변유적 폴더
ls 장흥주변유적/*.pdf | wc -l
ls 장흥주변유적/*.txt | wc -l

# 보성주변유적 폴더
ls 보성주변유적/*.pdf | wc -l
ls 보성주변유적/*.txt | wc -l
```

---

## 🎯 워크플로우 예시

### 예시 1: 새 논문 추가

```bash
# 1. PDF 추가
cp ~/Downloads/새논문.pdf 논문/

# 2. Git LFS 추적
git lfs track "논문/새논문.pdf"

# 3. 텍스트 변환
./scripts/pdf_helper.sh text "논문/새논문.pdf"

# 4. 커밋
git add "논문/새논문.*" .gitattributes
git commit -m "논문 추가: 새논문"
git push
```

### 예시 2: 특정 논문 내용 확인

```bash
# Git LFS에서 가져오기
git lfs pull --include "논문/파일.pdf"

# 텍스트 변환
./scripts/pdf_helper.sh text "논문/파일.pdf"

# 내용 읽기
cat "논문/파일.txt" | less

# 또는 Claude Code Read 도구로 읽기 ✓
```

### 예시 3: 전체 변환 (최초 1회)

```bash
# 모든 준비
git lfs install
git lfs pull
pip install PyPDF2

# 일괄 변환
python3 scripts/convert_all_pdfs.py

# 결과 커밋
git add "**/*.txt"
git commit -m "전체 PDF 텍스트 변환"
git push

# 이후 작업: .txt 파일만 사용 ✓
```

---

## 🔍 문제 해결

### Q1: "EOF marker not found" 오류

**A:** LFS 파일이 다운로드되지 않았습니다.

```bash
git lfs pull --force
```

### Q2: "ASCII text" 로 표시됨

**A:** 정상입니다. LFS 포인터 파일입니다.

```bash
# 실제 PDF 다운로드 필요
git lfs pull
```

### Q3: 변환이 너무 느림

**A:** 병렬 처리 사용

```bash
# 4개 동시 처리
find . -name "*.pdf" | parallel -j 4 \
  python3 -c "import sys; from convert_all_pdfs import convert_pdf_to_text; convert_pdf_to_text(sys.argv[1], sys.argv[1].replace('.pdf', '.txt'))" {}
```

### Q4: 디스크 공간 부족

**A:** 필요한 폴더만 처리

```bash
# 논문만 변환
cd 논문
python3 ../scripts/convert_all_pdfs.py
cd ..

# 필요 없는 PDF 제거
git lfs prune
```

---

## 📈 예상 결과

변환 완료 후:

```
저장소 구조:
├── 논문/
│   ├── 파일1.pdf (LFS)
│   ├── 파일1.txt ✓ (새로 생성)
│   ├── 파일2.pdf (LFS)
│   └── 파일2.txt ✓ (새로 생성)
├── 장흥주변유적/
│   ├── 유적1.pdf (LFS)
│   ├── 유적1.txt ✓
│   └── ...
└── scripts/
    ├── convert_all_pdfs.py
    ├── pdf_helper.sh
    └── pdf_helper.py

총 파일:
- PDF: 114개 (Git LFS)
- TXT: 114개 (일반 파일)
```

**장점:**
- ✅ Claude Code에서 .txt 파일 에러 없이 읽기
- ✅ 검색 가능 (grep, Ctrl+F)
- ✅ 빠른 로딩
- ✅ 버전 관리 용이

---

## 🎉 완료 체크리스트

변환이 완료되면:

- [ ] `find . -name "*.txt" | wc -l` = 114
- [ ] Claude Code Read 도구로 텍스트 파일 읽기 성공
- [ ] 변환된 파일 커밋 완료
- [ ] PDF 오류 없이 작업 가능

축하합니다! 이제 PDF 관련 오류 없이 안전하게 작업할 수 있습니다! 🎊

---

## 📞 추가 지원

- **가이드**: 이 폴더의 다른 `.md` 파일 참조
- **스크립트**: `scripts/` 폴더의 도구들 활용
- **Git LFS 문서**: https://git-lfs.github.com/
