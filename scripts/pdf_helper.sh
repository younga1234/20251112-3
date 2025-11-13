#!/bin/bash
# PDF 안전 처리 헬퍼 스크립트

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 도구 설치 확인
check_tools() {
    local missing_tools=()

    command -v pdfinfo >/dev/null 2>&1 || missing_tools+=("poppler-utils")
    command -v pdftotext >/dev/null 2>&1 || missing_tools+=("poppler-utils")

    if [ ${#missing_tools[@]} -ne 0 ]; then
        echo -e "${YELLOW}필요한 도구를 설치합니다: ${missing_tools[*]}${NC}"
        sudo apt-get update && sudo apt-get install -y "${missing_tools[@]}"
    fi
}

# PDF 정보 확인
pdf_info() {
    local pdf_file="$1"

    if [ ! -f "$pdf_file" ]; then
        echo -e "${RED}파일을 찾을 수 없습니다: $pdf_file${NC}"
        return 1
    fi

    echo -e "${GREEN}=== PDF 정보 ===${NC}"
    pdfinfo "$pdf_file" 2>&1 || {
        echo -e "${RED}유효하지 않은 PDF 파일${NC}"
        return 1
    }

    echo ""
    echo -e "${GREEN}파일 크기:${NC} $(du -h "$pdf_file" | cut -f1)"
}

# PDF → 텍스트 추출
pdf_to_text() {
    local pdf_file="$1"
    local output_file="${2:-${pdf_file%.pdf}.txt}"

    if [ ! -f "$pdf_file" ]; then
        echo -e "${RED}파일을 찾을 수 없습니다: $pdf_file${NC}"
        return 1
    fi

    echo -e "${GREEN}텍스트 추출 중...${NC}"
    pdftotext "$pdf_file" "$output_file" 2>&1 && {
        echo -e "${GREEN}✓ 추출 완료: $output_file${NC}"
        echo -e "${GREEN}줄 수:${NC} $(wc -l < "$output_file")"
    } || {
        echo -e "${RED}텍스트 추출 실패${NC}"
        return 1
    }
}

# PDF → 콘솔 출력
pdf_view() {
    local pdf_file="$1"

    if [ ! -f "$pdf_file" ]; then
        echo -e "${RED}파일을 찾을 수 없습니다: $pdf_file${NC}"
        return 1
    fi

    pdftotext "$pdf_file" - 2>&1 || {
        echo -e "${RED}PDF 읽기 실패${NC}"
        return 1
    }
}

# PDF 유효성 검사
pdf_validate() {
    local pdf_file="$1"

    if [ ! -f "$pdf_file" ]; then
        echo -e "${RED}파일을 찾을 수 없습니다: $pdf_file${NC}"
        return 1
    fi

    echo -e "${GREEN}PDF 유효성 검사 중...${NC}"

    # pdfinfo로 검사
    if pdfinfo "$pdf_file" >/dev/null 2>&1; then
        echo -e "${GREEN}✓ 유효한 PDF 파일${NC}"
        return 0
    else
        echo -e "${RED}✗ 유효하지 않은 PDF 파일${NC}"
        return 1
    fi
}

# 배치 처리: 모든 PDF 검사
pdf_batch_validate() {
    local dir="${1:-.}"

    echo -e "${GREEN}=== PDF 배치 검증 ===${NC}"
    echo "디렉토리: $dir"
    echo ""

    local total=0
    local valid=0
    local invalid=0

    while IFS= read -r pdf_file; do
        ((total++))
        printf "검사 중 [%d]: %s ... " "$total" "$pdf_file"

        if pdfinfo "$pdf_file" >/dev/null 2>&1; then
            echo -e "${GREEN}OK${NC}"
            ((valid++))
        else
            echo -e "${RED}FAIL${NC}"
            ((invalid++))
        fi
    done < <(find "$dir" -name "*.pdf" -type f)

    echo ""
    echo -e "${GREEN}=== 결과 ===${NC}"
    echo "전체: $total"
    echo -e "${GREEN}유효: $valid${NC}"
    echo -e "${RED}유효하지 않음: $invalid${NC}"
}

# 사용법 출력
usage() {
    cat << EOF
PDF 안전 처리 헬퍼 스크립트

사용법:
    $0 <command> <pdf-file>

명령어:
    info <pdf>              PDF 파일 정보 출력
    text <pdf> [output]     PDF를 텍스트로 추출
    view <pdf>              PDF 내용을 콘솔에 출력
    validate <pdf>          PDF 유효성 검사
    batch-validate [dir]    디렉토리의 모든 PDF 검증 (기본: 현재 디렉토리)
    install                 필요한 도구 설치

예시:
    $0 info document.pdf
    $0 text document.pdf output.txt
    $0 view document.pdf | less
    $0 validate document.pdf
    $0 batch-validate ./논문

EOF
}

# 메인 로직
main() {
    local command="$1"
    shift

    case "$command" in
        install)
            check_tools
            ;;
        info)
            check_tools
            pdf_info "$@"
            ;;
        text)
            check_tools
            pdf_to_text "$@"
            ;;
        view)
            check_tools
            pdf_view "$@"
            ;;
        validate)
            check_tools
            pdf_validate "$@"
            ;;
        batch-validate)
            check_tools
            pdf_batch_validate "$@"
            ;;
        *)
            usage
            exit 1
            ;;
    esac
}

main "$@"
