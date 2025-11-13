# Git LFS PDF 변환 가이드

## 🚨 문제 발견

저장소의 모든 PDF 파일(114개)이 **Git LFS (Large File Storage)**에 저장되어 있습니다.

현재 상태:
- PDF 파일들이 LFS 포인터 파일로만 존재
- 실제 PDF 내용은 LFS 서버에 있음
- 변환 스크립트가 실제 PDF 파일에 접근할 수 없음

```bash
# 현재 PDF 파일 내용
$ head -3 "논문/파일.pdf"
version https://git-lfs.github.com/spec/v1
oid sha256:93508e9589fd42f765a9203ea547b2ca85f51210142018907be63e95a08ee035
size 5700608
```

---

## ✅ 해결 방법

### Option 1: Git LFS 설치 및 PDF 다운로드 (권장)

#### Step 1: Git LFS 설치

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install git-lfs
git lfs install
```

**macOS:**
```bash
brew install git-lfs
git lfs install
```

**Windows:**
```bash
# Chocolatey 사용
choco install git-lfs

# 또는 공식 웹사이트에서 다운로드
# https://git-lfs.github.com/
```

#### Step 2: 실제 PDF 파일 다운로드

```bash
# 모든 LFS 파일 다운로드
git lfs pull

# 완료 후 확인
file "논문/三國時代 湖南地域 住居·聚落의 地域性과 變動2012-이동희ㅇ.pdf"
# 출력: PDF document, version X.X
```

#### Step 3: PDF → 텍스트 변환

```bash
# 일괄 변환 실행
python3 scripts/convert_all_pdfs.py

# 결과 확인
find . -name "*.txt" | wc -l
```

---

### Option 2: 온라인 환경에서 작업

Git LFS를 설치할 수 없는 환경(예: Claude Code 웹 환경)에서는:

#### 2-1. 로컬에서 변환 후 푸시

```bash
# 로컬 컴퓨터에서:
git clone https://github.com/younga1234/20251112-3
cd 20251112-3

# Git LFS 설치 및 PDF 다운로드
git lfs install
git lfs pull

# PDF → 텍스트 변환
python3 scripts/convert_all_pdfs.py

# 변환된 텍스트 파일 커밋 & 푸시
git add **/*.txt
git commit -m "PDF 파일을 텍스트로 변환"
git push
```

#### 2-2. 필요한 PDF만 선택적으로 처리

```bash
# 특정 PDF만 다운로드
git lfs pull --include "논문/특정파일.pdf"

# 변환
python3 -c "
import PyPDF2
with open('논문/특정파일.pdf', 'rb') as f:
    pdf = PyPDF2.PdfReader(f)
    text = '\\n'.join([page.extract_text() for page in pdf.pages])
    with open('논문/특정파일.txt', 'w') as out:
        out.write(text)
"
```

---

### Option 3: Docker 사용 (LFS 없이)

Docker를 사용하여 실제 PDF 파일에 접근:

```bash
# Git LFS가 설치된 Docker 컨테이너에서 작업
docker run -it --rm -v "$(pwd):/repo" alpine/git sh

# 컨테이너 내부에서:
cd /repo
apk add git-lfs py3-pip
git lfs install
git lfs pull

# PDF 변환
pip install PyPDF2
python3 scripts/convert_all_pdfs.py
```

---

## 📋 변환 스크립트 사용법

### 모든 PDF 변환

```bash
python3 scripts/convert_all_pdfs.py
```

**기능:**
- 저장소의 모든 PDF 파일을 자동으로 찾아 변환
- 이미 변환된 파일은 건너뛰기 (스마트 캐싱)
- 변환 진행상황 실시간 표시
- 실패한 파일 목록 자동 생성

**예상 실행 시간:**
- 114개 PDF 파일 기준: 약 10-30분
- 파일 크기에 따라 다름

### 선택적 변환

특정 폴더만 변환:

```bash
# 논문 폴더만
cd 논문
python3 ../scripts/convert_all_pdfs.py
cd ..

# 장흥주변유적 폴더만
cd 장흥주변유적
python3 ../scripts/convert_all_pdfs.py
cd ..
```

### 병렬 처리 (빠른 변환)

```bash
# GNU Parallel 사용 (선택사항)
find . -name "*.pdf" | parallel -j 4 python3 scripts/convert_one_pdf.py {}
```

---

## 🔍 문제 해결

### 1. "EOF marker not found" 오류

**원인:** PDF가 손상되었거나 LFS 파일이 다운로드되지 않음

**해결:**
```bash
# LFS 파일 다시 다운로드
git lfs pull --force

# 특정 파일만 다시 가져오기
rm "논문/파일.pdf"
git checkout "논문/파일.pdf"
git lfs pull --include "논문/파일.pdf"
```

### 2. "Git LFS not installed" 오류

**해결:**
```bash
# Ubuntu/Debian
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs

# macOS
brew install git-lfs

# Windows
# https://git-lfs.github.com/ 에서 설치
```

### 3. 모든 PDF가 "ASCII text"로 표시됨

이것은 정상입니다! LFS 포인터 파일입니다.

```bash
# 해결: LFS 파일 다운로드
git lfs pull
```

### 4. 디스크 공간 부족

114개 PDF 파일의 총 크기 확인:

```bash
# LFS 파일 크기 확인
git lfs ls-files -s

# 필요한 공간: 약 1-3GB 예상
```

---

## 📊 변환 진행 상황 추적

### 변환 상태 확인

```bash
# 전체 PDF 수
find . -name "*.pdf" | wc -l

# 변환된 TXT 수
find . -name "*.txt" | wc -l

# 남은 PDF 수
comm -23 \
  <(find . -name "*.pdf" | sed 's/\.pdf$//' | sort) \
  <(find . -name "*.txt" | sed 's/\.txt$//' | sort) \
  | wc -l
```

### 변환 로그

```bash
# 변환 스크립트는 자동으로 로그 생성
tail -f /tmp/conversion_log.txt
```

---

## 🎯 권장 워크플로우

### 일회성 설정 (한 번만)

```bash
# 1. Git LFS 설치
sudo apt-get install git-lfs
git lfs install

# 2. PDF 파일 다운로드
git lfs pull

# 3. PyPDF2 설치
pip install PyPDF2

# 4. 모든 PDF 변환
python3 scripts/convert_all_pdfs.py

# 5. 변환된 파일 커밋
git add "**/*.txt"
git commit -m "모든 PDF를 텍스트로 변환"
git push
```

### 이후 작업 (변환 완료 후)

```bash
# PDF 대신 TXT 파일 읽기
cat "논문/파일.txt"

# Claude Code의 Read 도구로 .txt 파일 읽기 ✓
# - 에러 없음
# - 빠른 처리
# - 검색 가능
```

---

## 💡 추가 팁

### 1. .gitignore 업데이트

```bash
# .gitignore에 추가하여 TXT 파일 커밋하기
echo "!**/*.txt" >> .gitignore
```

### 2. Git Attributes 확인

```bash
# .gitattributes 파일 확인
cat .gitattributes

# PDF가 LFS로 설정되어 있는지 확인
# *.pdf filter=lfs diff=lfs merge=lfs -text
```

### 3. LFS 대역폭 확인

```bash
# GitHub LFS 사용량 확인
git lfs env
```

---

## 📞 추가 도움

- **Git LFS 공식 문서**: https://git-lfs.github.com/
- **GitHub LFS 가이드**: https://docs.github.com/en/repositories/working-with-files/managing-large-files
- **변환 스크립트**: `scripts/convert_all_pdfs.py`
- **PDF 처리 가이드**: `scripts/PDF_처리_가이드.md`

---

## ✅ 체크리스트

변환 전에 확인하세요:

- [ ] Git LFS 설치됨 (`git lfs version`)
- [ ] Git LFS 초기화됨 (`git lfs install`)
- [ ] PDF 파일 다운로드됨 (`git lfs pull`)
- [ ] PyPDF2 설치됨 (`pip show PyPDF2`)
- [ ] 충분한 디스크 공간 (3GB+)
- [ ] 변환 스크립트 실행 가능 (`chmod +x scripts/convert_all_pdfs.py`)

모두 확인했다면:

```bash
python3 scripts/convert_all_pdfs.py
```

변환이 완료되면 Claude Code에서 에러 없이 모든 PDF 내용을 텍스트로 읽을 수 있습니다! 🎉
