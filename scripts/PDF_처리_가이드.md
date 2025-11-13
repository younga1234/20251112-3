# PDF 처리 가이드

Claude Code에서 PDF를 열 때 `invalid base64 data` 오류가 발생하는 경우 대비책입니다.

## 문제 원인

API Error 400: "The PDF specified was not valid" 오류는 다음과 같은 경우 발생합니다:
- PDF 파일이 손상됨
- PDF 파일 크기가 너무 큼 (Claude의 한계 초과)
- PDF가 암호화되어 있음
- Base64 인코딩 과정에서 오류 발생

## 해결 방법

### 🚀 빠른 시작

```bash
# 1. Bash 스크립트 사용 (추천 - 설치 불필요)
./scripts/pdf_helper.sh install        # 필요한 도구 설치
./scripts/pdf_helper.sh view "논문/파일.pdf" | less

# 2. Python 스크립트 사용 (더 많은 기능)
pip install PyPDF2 pdfplumber
./scripts/pdf_helper.py check          # 의존성 확인
./scripts/pdf_helper.py text "논문/파일.pdf"
```

---

## 📖 상세 사용법

### Option 1: Bash 스크립트 (pdf_helper.sh)

#### 설치
```bash
./scripts/pdf_helper.sh install
```

#### 명령어

**1. PDF 정보 확인**
```bash
./scripts/pdf_helper.sh info "논문/파일.pdf"
```

**2. PDF를 텍스트로 추출**
```bash
# 기본 (파일.txt로 저장)
./scripts/pdf_helper.sh text "논문/파일.pdf"

# 출력 파일 지정
./scripts/pdf_helper.sh text "논문/파일.pdf" output.txt
```

**3. PDF 내용 콘솔에 출력**
```bash
./scripts/pdf_helper.sh view "논문/파일.pdf"

# less로 페이징
./scripts/pdf_helper.sh view "논문/파일.pdf" | less

# 파일로 저장
./scripts/pdf_helper.sh view "논문/파일.pdf" > output.txt
```

**4. PDF 유효성 검사**
```bash
./scripts/pdf_helper.sh validate "논문/파일.pdf"
```

**5. 배치 검증 (전체 폴더)**
```bash
# 현재 디렉토리의 모든 PDF 검사
./scripts/pdf_helper.sh batch-validate

# 특정 폴더의 모든 PDF 검사
./scripts/pdf_helper.sh batch-validate ./논문
./scripts/pdf_helper.sh batch-validate ./장흥주변유적
```

---

### Option 2: Python 스크립트 (pdf_helper.py)

#### 설치
```bash
pip install PyPDF2 pdfplumber
./scripts/pdf_helper.py check
```

#### 명령어

**1. PDF 정보 확인**
```bash
./scripts/pdf_helper.py info "논문/파일.pdf"
```

**2. 텍스트 추출**
```bash
# pdfplumber 사용 (권장)
./scripts/pdf_helper.py text "논문/파일.pdf"

# PyPDF2 사용
./scripts/pdf_helper.py text "논문/파일.pdf" -m pypdf2

# 출력 파일 지정
./scripts/pdf_helper.py text "논문/파일.pdf" -o output.txt
```

**3. PDF 유효성 검사**
```bash
./scripts/pdf_helper.py validate "논문/파일.pdf"
```

**4. 배치 검증**
```bash
./scripts/pdf_helper.py batch-validate ./논문
```

---

## 🔍 실전 예제

### 예제 1: 논문 PDF 읽기

```bash
# 1단계: PDF가 유효한지 확인
./scripts/pdf_helper.sh validate "논문/三國時代 湖南地域 住居·聚落의 地域性과 變動2012-이동희ㅇ.pdf"

# 2단계: 텍스트로 추출
./scripts/pdf_helper.sh text "논문/三國時代 湖南地域 住居·聚落의 地域性과 變動2012-이동희ㅇ.pdf"

# 3단계: 추출된 텍스트 읽기
cat "논문/三國時代 湖南地域 住居·聚落의 地域性과 變動2012-이동희ㅇ.pdf.txt"
```

### 예제 2: 모든 PDF 일괄 검사

```bash
# 모든 논문 PDF 검증
./scripts/pdf_helper.sh batch-validate ./논문

# 문제가 있는 PDF 찾기
./scripts/pdf_helper.sh batch-validate ./논문 | grep FAIL
```

### 예제 3: PDF 정보 빠르게 확인

```bash
# 여러 PDF 정보 한 번에 확인
for pdf in 논문/*.pdf; do
    echo "=== $pdf ==="
    ./scripts/pdf_helper.sh info "$pdf"
    echo ""
done
```

### 예제 4: 대용량 PDF 처리

```bash
# 1. 먼저 파일 크기 확인
ls -lh "장흥주변유적/장흥 원도리유적-최종(저화질).pdf"

# 2. 텍스트로 변환 (Claude Code에서 읽기보다 빠름)
./scripts/pdf_helper.py text "장흥주변유적/장흥 원도리유적-최종(저화질).pdf"

# 3. 변환된 텍스트 파일을 Claude Code로 읽기
# Read 도구로 .txt 파일 읽기 (에러 없음!)
```

---

## 💡 권장 워크플로우

### Claude Code에서 PDF를 읽어야 할 때:

```bash
# ❌ 직접 Read 도구로 PDF 읽기 (에러 발생 가능)
# Read tool: "논문/파일.pdf"

# ✅ 1단계: 텍스트로 변환
./scripts/pdf_helper.sh text "논문/파일.pdf"

# ✅ 2단계: Read 도구로 .txt 파일 읽기
# Read tool: "논문/파일.txt"
```

### 자동화 스크립트 예제

모든 PDF를 텍스트로 변환:

```bash
#!/bin/bash
# convert_all_pdfs.sh

find ./논문 -name "*.pdf" -type f | while read pdf; do
    echo "처리 중: $pdf"
    ./scripts/pdf_helper.sh text "$pdf"
done

echo "완료! 이제 .txt 파일들을 읽을 수 있습니다."
```

---

## 🛠️ 문제 해결

### 문제: "command not found: pdftotext"
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler
```

### 문제: "ModuleNotFoundError: No module named 'PyPDF2'"
```bash
pip install PyPDF2 pdfplumber
```

### 문제: PDF가 암호화되어 있음
```bash
# 암호화 제거 (암호 필요)
qpdf --password=PASSWORD --decrypt input.pdf output.pdf
```

### 문제: PDF가 손상됨
```bash
# Ghostscript로 복구
gs -o recovered.pdf -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress damaged.pdf
```

---

## 📊 성능 비교

| 방법 | 속도 | 정확도 | 설치 |
|------|------|--------|------|
| Read 도구 (PDF 직접) | 빠름 | 낮음 | 불필요 |
| pdftotext | 매우 빠름 | 중간 | apt-get |
| PyPDF2 | 빠름 | 중간 | pip |
| pdfplumber | 중간 | 높음 | pip |

**권장**: pdftotext (Bash) 또는 pdfplumber (Python)

---

## 📝 요약

1. **PDF 오류 발생 시**: 먼저 `validate` 명령으로 확인
2. **대용량 PDF**: 텍스트로 변환 후 읽기
3. **배치 작업**: `batch-validate`로 전체 검증
4. **자동화**: 스크립트를 활용하여 워크플로우 개선

이제 PDF 관련 오류 없이 안전하게 작업할 수 있습니다! 🎉
