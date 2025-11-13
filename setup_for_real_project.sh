#!/bin/bash
# 실제 프로젝트 데이터 통합을 위한 설정 스크립트
# 사용법: ./setup_for_real_project.sh [GitHub_저장소_경로]

set -e  # 오류 시 중단

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "고고학 발굴조사 고찰 작성 파이프라인"
echo "실제 프로젝트 데이터 통합 설정"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# GitHub 저장소 경로 확인
GITHUB_REPO=${1:-"https://github.com/younga1234/up.git"}
TARGET_DIR=${2:-"$HOME/archaeology-project"}

echo "설정 정보:"
echo "  GitHub 저장소: $GITHUB_REPO"
echo "  설치 경로: $TARGET_DIR"
echo ""

# 1. 저장소 클론 또는 업데이트
if [ -d "$TARGET_DIR" ]; then
  echo "📁 기존 폴더 발견: $TARGET_DIR"
  read -p "덮어쓰시겠습니까? (y/N): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  기존 폴더 삭제 중..."
    rm -rf "$TARGET_DIR"
  else
    echo "❌ 중단되었습니다."
    exit 0
  fi
fi

echo "📥 GitHub 저장소 클론 중..."
git clone "$GITHUB_REPO" "$TARGET_DIR"
cd "$TARGET_DIR"

echo "✓ 클론 완료"
echo ""

# 2. 스킬 폴더 복사
echo "📋 Claude Code Skills 복사 중..."
if [ -d "/home/user/20251112-1/.claude/skills" ]; then
  cp -r /home/user/20251112-1/.claude .
  echo "✓ 스킬 7개 복사 완료"
else
  echo "⚠️  스킬 폴더를 찾을 수 없습니다: /home/user/20251112-1/.claude/skills"
  echo "   수동으로 복사해주세요."
fi
echo ""

# 3. 필요한 폴더 생성
echo "📁 자료 폴더 생성 중..."
mkdir -p 논문 발굴조사보고서 주변유적 output

echo "✓ 폴더 생성 완료:"
echo "  - 논문/"
echo "  - 발굴조사보고서/"
echo "  - 주변유적/"
echo "  - output/"
echo ""

# 4. 기존 자료 확인 및 이동 제안
echo "📊 기존 자료 확인 중..."

if [ -d "장흥주변유적" ]; then
  echo "✓ '장흥주변유적' 폴더 발견"
  FILE_COUNT=$(find 장흥주변유적 -type f | wc -l)
  echo "  파일 수: $FILE_COUNT"

  echo ""
  read -p "이 폴더를 '주변유적/'으로 복사하시겠습니까? (Y/n): " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    cp -r 장흥주변유적/* 주변유적/ 2>/dev/null || true
    echo "✓ 복사 완료"
  fi
fi

if [ -d "data" ]; then
  echo "✓ 'data' 폴더 발견"

  PDF_COUNT=$(find data -type f -name "*.pdf" 2>/dev/null | wc -l)
  HWP_COUNT=$(find data -type f -name "*.hwp" 2>/dev/null | wc -l)

  echo "  PDF 파일: $PDF_COUNT"
  echo "  HWP 파일: $HWP_COUNT"

  if [ $PDF_COUNT -gt 0 ] || [ $HWP_COUNT -gt 0 ]; then
    echo ""
    echo "data/ 폴더의 파일을 분류해야 합니다:"
    echo "  - 논문 → 논문/"
    echo "  - 발굴조사보고서 → 발굴조사보고서/"
    echo "  - 기타 → 주변유적/"
    echo ""
    read -p "자동 분류를 시도하시겠습니까? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      echo "🔄 자동 분류 중..."

      # PDF 파일 분류
      for file in data/*.pdf data/**/*.pdf 2>/dev/null; do
        [ -f "$file" ] || continue
        basename=$(basename "$file")

        if [[ "$basename" =~ (논문|학위|연구|학보|journal) ]]; then
          cp "$file" 논문/ && echo "  → 논문/: $basename"
        elif [[ "$basename" =~ (발굴|조사|보고서|report) ]]; then
          cp "$file" 발굴조사보고서/ && echo "  → 발굴조사보고서/: $basename"
        else
          cp "$file" 주변유적/ && echo "  → 주변유적/: $basename"
        fi
      done

      # HWP 파일 분류
      for file in data/*.hwp data/**/*.hwp 2>/dev/null; do
        [ -f "$file" ] || continue
        basename=$(basename "$file")

        if [[ "$basename" =~ (발굴|조사|보고서) ]]; then
          cp "$file" 발굴조사보고서/ && echo "  → 발굴조사보고서/: $basename"
        else
          cp "$file" 주변유적/ && echo "  → 주변유적/: $basename"
        fi
      done

      echo "✓ 자동 분류 완료"
    else
      echo "⚠️  나중에 수동으로 분류해주세요."
    fi
  fi
fi

echo ""

# 5. 최종 상태 확인
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "설정 완료!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📊 현재 상태:"
echo "  프로젝트 경로: $TARGET_DIR"
echo "  논문: $(find 논문 -type f 2>/dev/null | wc -l)개 파일"
echo "  발굴조사보고서: $(find 발굴조사보고서 -type f 2>/dev/null | wc -l)개 파일"
echo "  주변유적: $(find 주변유적 -type f 2>/dev/null | wc -l)개 파일"
echo ""

# 6. 다음 단계 안내
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "다음 단계"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. 자료 확인 및 추가:"
echo "   cd $TARGET_DIR"
echo "   ls 논문/"
echo "   ls 발굴조사보고서/"
echo "   ls 주변유적/"
echo ""
echo "2. 조사 정보 준비:"
echo "   - 조사명"
echo "   - 조사기관, 조사기간"
echo "   - 대상지 좌표 (Google Maps에서 확인)"
echo "   - 주요 시대, 유구, 유물"
echo ""
echo "3. Claude Code에서 실행:"
echo '   archaeology-orchestrator 스킬을 사용하여 고찰을 작성해주세요.'
echo ""
echo "자세한 사용법:"
echo "  cat INTEGRATION_GUIDE_실제프로젝트.md"
echo ""
echo "Happy Archaeology! 🏺"
