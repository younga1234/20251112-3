#!/bin/bash
# PDF 일괄 변환 실행 스크립트
# 로컬 환경에서 실행하세요!

set -e

echo "========================================="
echo "  PDF → 텍스트 일괄 변환 스크립트"
echo "========================================="
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Step 1: Git LFS 확인
echo -e "${BLUE}[1/5] Git LFS 확인 중...${NC}"
if ! command -v git-lfs &> /dev/null; then
    echo -e "${RED}✗ Git LFS가 설치되지 않았습니다.${NC}"
    echo ""
    echo "설치 방법:"
    echo "  Ubuntu/Debian: sudo apt-get install git-lfs"
    echo "  macOS:         brew install git-lfs"
    echo "  Windows:       choco install git-lfs"
    echo ""
    exit 1
fi
echo -e "${GREEN}✓ Git LFS 설치됨${NC}"

# Step 2: Git LFS 초기화
echo -e "${BLUE}[2/5] Git LFS 초기화 중...${NC}"
git lfs install
echo -e "${GREEN}✓ Git LFS 초기화 완료${NC}"

# Step 3: PDF 파일 다운로드
echo -e "${BLUE}[3/5] PDF 파일 다운로드 중... (시간이 걸릴 수 있습니다)${NC}"
git lfs pull
echo -e "${GREEN}✓ PDF 파일 다운로드 완료${NC}"

# Step 4: PyPDF2 확인
echo -e "${BLUE}[4/5] PyPDF2 확인 중...${NC}"
if ! python3 -c "import PyPDF2" 2>/dev/null; then
    echo -e "${YELLOW}PyPDF2가 설치되지 않았습니다. 설치 중...${NC}"
    pip install PyPDF2
fi
echo -e "${GREEN}✓ PyPDF2 준비됨${NC}"

# Step 5: PDF 변환 실행
echo -e "${BLUE}[5/5] PDF 변환 실행 중...${NC}"
python3 scripts/convert_all_pdfs.py

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}  변환 완료!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "다음 명령으로 변환된 파일을 커밋하세요:"
echo ""
echo -e "${YELLOW}  git add \"**/*.txt\"${NC}"
echo -e "${YELLOW}  git commit -m \"PDF 파일 텍스트 변환\"${NC}"
echo -e "${YELLOW}  git push${NC}"
echo ""
