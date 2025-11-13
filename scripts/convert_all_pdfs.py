#!/usr/bin/env python3
"""
모든 PDF 파일을 텍스트로 일괄 변환하는 스크립트
"""

import os
import sys
from pathlib import Path

# PyPDF2 임포트 시도
try:
    import PyPDF2
    HAS_PYPDF2 = True
    print("✓ PyPDF2 사용 가능")
except ImportError:
    HAS_PYPDF2 = False
    print("✗ PyPDF2 없음")

def convert_pdf_to_text(pdf_path, txt_path):
    """PDF를 텍스트로 변환"""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            # 모든 페이지의 텍스트 추출
            text_content = []
            for i, page in enumerate(pdf_reader.pages, 1):
                text_content.append(f"\n{'='*60}\n")
                text_content.append(f"페이지 {i}/{len(pdf_reader.pages)}\n")
                text_content.append(f"{'='*60}\n\n")
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)
                else:
                    text_content.append("[이 페이지는 텍스트를 추출할 수 없습니다]\n")

            # 텍스트 파일로 저장
            full_text = ''.join(text_content)
            with open(txt_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(full_text)

            return True, len(pdf_reader.pages), len(full_text)

    except Exception as e:
        return False, 0, str(e)

def main():
    if not HAS_PYPDF2:
        print("\nPyPDF2가 설치되지 않았습니다.")
        print("설치 명령: pip install PyPDF2")
        return 1

    # 현재 디렉토리에서 모든 PDF 찾기
    pdf_files = list(Path('.').rglob('*.pdf'))
    total = len(pdf_files)

    print(f"\n총 {total}개의 PDF 파일을 찾았습니다.\n")
    print("변환을 시작합니다...\n")

    success_count = 0
    fail_count = 0
    failed_files = []

    for i, pdf_path in enumerate(pdf_files, 1):
        txt_path = pdf_path.with_suffix('.txt')

        # 이미 변환된 파일이 있고 최신인 경우 건너뛰기
        if txt_path.exists():
            pdf_mtime = os.path.getmtime(pdf_path)
            txt_mtime = os.path.getmtime(txt_path)
            if txt_mtime > pdf_mtime:
                print(f"[{i}/{total}] ⊘ 건너뜀: {pdf_path} (이미 변환됨)")
                success_count += 1
                continue

        print(f"[{i}/{total}] 변환 중: {pdf_path}")

        result, pages_or_error, chars = convert_pdf_to_text(pdf_path, txt_path)

        if result:
            print(f"          ✓ 완료: {pages_or_error}페이지, {chars:,}자 → {txt_path}")
            success_count += 1
        else:
            print(f"          ✗ 실패: {pages_or_error}")
            fail_count += 1
            failed_files.append((str(pdf_path), pages_or_error))

    # 결과 요약
    print("\n" + "="*60)
    print("변환 완료!")
    print("="*60)
    print(f"전체: {total}개")
    print(f"성공: {success_count}개")
    print(f"실패: {fail_count}개")

    if failed_files:
        print("\n실패한 파일:")
        for file_path, error in failed_files:
            print(f"  - {file_path}")
            print(f"    오류: {error}")

    print("\n✓ 이제 Claude Code에서 .txt 파일들을 안전하게 읽을 수 있습니다!")

    return 0 if fail_count == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
