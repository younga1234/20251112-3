# PDF Base64 오류 대비책 (요약)

## 🚨 문제
```
API Error: 400 {"type":"error","error":{"type":"invalid_request_error",
"message":"messages.2.content.0.pdf.source.base64.data: The PDF specified was not valid."}}
```

## ✅ 즉시 사용 가능한 해결책

### 방법 1: 웹 브라우저에서 PDF 읽기 (가장 빠름)
1. PDF 파일을 웹 브라우저로 열기
2. 필요한 내용을 복사해서 텍스트 파일로 저장
3. 텍스트 파일을 Claude Code로 읽기

### 방법 2: Docker 사용 (권장)
```bash
# PDF → 텍스트 변환 (설치 불필요)
docker run --rm -v "$(pwd):/data" alpine/pdftotext \
  /data/논문/파일.pdf /data/논문/파일.txt

# 변환된 텍스트 읽기
cat 논문/파일.txt
```

### 방법 3: 온라인 도구 사용
- https://www.ilovepdf.com/pdf_to_text (무료)
- https://pdftotext.com/ (무료)
- https://www.adobe.com/acrobat/online/pdf-to-text.html (무료)

### 방법 4: 작은 PDF만 읽기
```bash
# 파일 크기 확인 (5MB 이하만 안전)
ls -lh "논문/파일.pdf"

# 5MB 미만이면 Read 도구로 시도
# 5MB 이상이면 텍스트 변환 필수
```

---

## 🔧 로컬 환경 설정 (한 번만)

### Ubuntu/Debian 사용자
```bash
# poppler 설치
apt-get update && apt-get install -y poppler-utils

# 사용
pdftotext "논문/파일.pdf" "논문/파일.txt"
```

### macOS 사용자
```bash
# Homebrew로 설치
brew install poppler

# 사용
pdftotext "논문/파일.pdf" "논문/파일.txt"
```

### Windows 사용자
```powershell
# Chocolatey로 설치
choco install xpdf-utils

# 사용
pdftotext "논문\파일.pdf" "논문\파일.txt"
```

---

## 📋 워크플로우 예시

### 예시 1: 단일 PDF 처리
```bash
# Step 1: Docker로 텍스트 추출
docker run --rm -v "$(pwd):/data" alpine/pdftotext \
  /data/논문/三國時代\ 湖南地域\ 住居·聚落의\ 地域性과\ 變動2012-이동희ㅇ.pdf \
  /data/논문/三國時代\ 湖南地域\ 住居·聚落의\ 地域性과\ 變動2012-이동희ㅇ.txt

# Step 2: 텍스트 파일 확인
cat "논문/三國時代 湖南地域 住居·聚落의 地域性과 變動2012-이동희ㅇ.txt"

# Step 3: Claude Code의 Read 도구로 .txt 파일 읽기 ✓
```

### 예시 2: 배치 처리
```bash
#!/bin/bash
# convert_all_pdfs_docker.sh

find ./논문 -name "*.pdf" -type f | while IFS= read -r pdf; do
    txt="${pdf%.pdf}.txt"
    echo "변환 중: $pdf → $txt"

    docker run --rm -v "$(pwd):/data" alpine/pdftotext \
      "/data/$pdf" "/data/$txt"
done

echo "✓ 완료! 이제 .txt 파일들을 안전하게 읽을 수 있습니다."
```

### 예시 3: 선택적 처리
```bash
# 5MB 이상 PDF만 변환
find ./논문 -name "*.pdf" -size +5M | while read pdf; do
    echo "큰 파일 발견: $pdf"
    pdftotext "$pdf" "${pdf%.pdf}.txt"
done
```

---

## 💡 Best Practices

### ✅ DO (권장)
- PDF 크기가 5MB 이상이면 텍스트로 변환 후 읽기
- 변환된 .txt 파일을 Git에 커밋 (재사용 가능)
- Docker 사용 시 볼륨 마운트 경로 확인
- 한글 파일명은 따옴표로 감싸기

### ❌ DON'T (비권장)
- 10MB 이상 PDF를 Read 도구로 직접 읽기
- 암호화된 PDF를 변환 없이 시도
- 손상된 PDF 파일 무시

---

## 🎯 빠른 참조

| PDF 크기 | 방법 | 도구 |
|---------|------|------|
| < 1MB | Read 도구 직접 사용 | Claude Code |
| 1-5MB | 시도해보고 실패 시 변환 | pdftotext |
| 5-20MB | 무조건 텍스트 변환 | pdftotext |
| > 20MB | 필요한 부분만 추출 | 웹 브라우저 |

---

## 🔍 디버깅

### PDF가 읽히지 않을 때 체크리스트
- [ ] 파일이 실제로 존재하는가?
- [ ] 파일 크기가 적절한가? (< 5MB)
- [ ] 파일이 손상되지 않았는가?
- [ ] 파일이 암호화되지 않았는가?
- [ ] 파일명에 특수문자가 없는가?

### 테스트 명령어
```bash
# 1. 파일 존재 확인
ls -lh "논문/파일.pdf"

# 2. 파일 타입 확인
file "논문/파일.pdf"

# 3. Docker로 변환 시도
docker run --rm -v "$(pwd):/data" alpine/pdftotext \
  /data/논문/파일.pdf /data/논문/파일.txt

# 4. 결과 확인
head -20 "논문/파일.txt"
```

---

## 📞 추가 도움

- Docker 설치: https://docs.docker.com/get-docker/
- pdftotext 매뉴얼: `man pdftotext`
- 이슈 리포트: https://github.com/anthropics/claude-code/issues

**핵심 요약**: PDF를 직접 읽지 말고, 텍스트로 변환한 후 읽으세요! 🎉
