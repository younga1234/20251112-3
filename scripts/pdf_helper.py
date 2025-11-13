#!/usr/bin/env python3
"""
PDF 안전 처리 헬퍼 스크립트 (Python 버전)
"""

import argparse
import sys
import os
from pathlib import Path

try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False

try:
    import pdfplumber
    HAS_PDFPLUMBER = True
except ImportError:
    HAS_PDFPLUMBER = False


class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


def print_color(text, color):
    """색상 출력"""
    print(f"{color}{text}{Colors.NC}")


def check_dependencies():
    """의존성 확인"""
    missing = []
    if not HAS_PYPDF2:
        missing.append("PyPDF2")
    if not HAS_PDFPLUMBER:
        missing.append("pdfplumber")

    if missing:
        print_color(f"⚠ 다음 패키지를 설치하세요:", Colors.YELLOW)
        print(f"pip install {' '.join(missing)}")
        return False
    return True


def pdf_info(pdf_path):
    """PDF 정보 출력"""
    if not os.path.exists(pdf_path):
        print_color(f"✗ 파일을 찾을 수 없습니다: {pdf_path}", Colors.RED)
        return False

    print_color("=== PDF 정보 ===", Colors.GREEN)

    # 파일 크기
    file_size = os.path.getsize(pdf_path)
    print(f"파일 크기: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")

    # PyPDF2로 정보 추출
    if HAS_PYPDF2:
        try:
            with open(pdf_path, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                print(f"페이지 수: {len(pdf.pages)}")

                if pdf.metadata:
                    print("\n메타데이터:")
                    for key, value in pdf.metadata.items():
                        print(f"  {key}: {value}")

                # 암호화 확인
                if pdf.is_encrypted:
                    print_color("\n⚠ 암호화된 PDF입니다", Colors.YELLOW)

                print_color("\n✓ 유효한 PDF 파일", Colors.GREEN)
                return True

        except Exception as e:
            print_color(f"✗ PDF 읽기 실패: {e}", Colors.RED)
            return False

    return True


def pdf_extract_text(pdf_path, output_path=None, method='pdfplumber'):
    """PDF에서 텍스트 추출"""
    if not os.path.exists(pdf_path):
        print_color(f"✗ 파일을 찾을 수 없습니다: {pdf_path}", Colors.RED)
        return False

    if output_path is None:
        output_path = Path(pdf_path).with_suffix('.txt')

    text_content = []

    try:
        if method == 'pdfplumber' and HAS_PDFPLUMBER:
            print_color("pdfplumber로 텍스트 추출 중...", Colors.BLUE)
            with pdfplumber.open(pdf_path) as pdf:
                for i, page in enumerate(pdf.pages, 1):
                    print(f"\r페이지 {i}/{len(pdf.pages)} 처리 중...", end='')
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(f"\n=== Page {i} ===\n")
                        text_content.append(page_text)
                print()  # 줄바꿈

        elif method == 'pypdf2' and HAS_PYPDF2:
            print_color("PyPDF2로 텍스트 추출 중...", Colors.BLUE)
            with open(pdf_path, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                for i, page in enumerate(pdf.pages, 1):
                    print(f"\r페이지 {i}/{len(pdf.pages)} 처리 중...", end='')
                    text_content.append(f"\n=== Page {i} ===\n")
                    text_content.append(page.extract_text())
                print()  # 줄바꿈

        else:
            print_color("텍스트 추출 라이브러리가 없습니다", Colors.RED)
            return False

        # 파일로 저장
        full_text = ''.join(text_content)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(full_text)

        print_color(f"✓ 추출 완료: {output_path}", Colors.GREEN)
        print(f"총 문자 수: {len(full_text):,}")
        print(f"줄 수: {full_text.count(chr(10)):,}")

        return True

    except Exception as e:
        print_color(f"✗ 텍스트 추출 실패: {e}", Colors.RED)
        return False


def pdf_validate(pdf_path):
    """PDF 유효성 검사"""
    if not os.path.exists(pdf_path):
        print_color(f"✗ 파일을 찾을 수 없습니다: {pdf_path}", Colors.RED)
        return False

    print(f"검사 중: {pdf_path}")

    # PyPDF2로 검증
    if HAS_PYPDF2:
        try:
            with open(pdf_path, 'rb') as f:
                pdf = PyPDF2.PdfReader(f)
                _ = len(pdf.pages)  # 페이지 수 확인
                print_color("✓ 유효한 PDF 파일", Colors.GREEN)
                return True
        except Exception as e:
            print_color(f"✗ 유효하지 않은 PDF: {e}", Colors.RED)
            return False

    # pdfplumber로 검증
    if HAS_PDFPLUMBER:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                _ = len(pdf.pages)  # 페이지 수 확인
                print_color("✓ 유효한 PDF 파일", Colors.GREEN)
                return True
        except Exception as e:
            print_color(f"✗ 유효하지 않은 PDF: {e}", Colors.RED)
            return False

    print_color("PDF 검증 라이브러리가 없습니다", Colors.YELLOW)
    return False


def pdf_batch_validate(directory='.'):
    """디렉토리의 모든 PDF 검증"""
    print_color("=== PDF 배치 검증 ===", Colors.GREEN)
    print(f"디렉토리: {directory}\n")

    pdf_files = list(Path(directory).rglob('*.pdf'))
    total = len(pdf_files)
    valid = 0
    invalid = 0
    invalid_files = []

    for i, pdf_path in enumerate(pdf_files, 1):
        print(f"[{i}/{total}] {pdf_path} ... ", end='')

        try:
            if HAS_PYPDF2:
                with open(pdf_path, 'rb') as f:
                    pdf = PyPDF2.PdfReader(f)
                    _ = len(pdf.pages)
            elif HAS_PDFPLUMBER:
                with pdfplumber.open(pdf_path) as pdf:
                    _ = len(pdf.pages)
            else:
                print_color("SKIP", Colors.YELLOW)
                continue

            print_color("OK", Colors.GREEN)
            valid += 1

        except Exception as e:
            print_color(f"FAIL ({e})", Colors.RED)
            invalid += 1
            invalid_files.append(str(pdf_path))

    print()
    print_color("=== 결과 ===", Colors.GREEN)
    print(f"전체: {total}")
    print_color(f"유효: {valid}", Colors.GREEN)
    print_color(f"유효하지 않음: {invalid}", Colors.RED)

    if invalid_files:
        print("\n문제가 있는 파일:")
        for f in invalid_files:
            print(f"  - {f}")


def main():
    parser = argparse.ArgumentParser(
        description='PDF 안전 처리 헬퍼 스크립트',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
예시:
  %(prog)s info document.pdf
  %(prog)s text document.pdf
  %(prog)s text document.pdf -o output.txt
  %(prog)s validate document.pdf
  %(prog)s batch-validate ./논문
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='명령어')

    # info 명령
    parser_info = subparsers.add_parser('info', help='PDF 정보 출력')
    parser_info.add_argument('pdf', help='PDF 파일 경로')

    # text 명령
    parser_text = subparsers.add_parser('text', help='텍스트 추출')
    parser_text.add_argument('pdf', help='PDF 파일 경로')
    parser_text.add_argument('-o', '--output', help='출력 파일 경로')
    parser_text.add_argument('-m', '--method', choices=['pdfplumber', 'pypdf2'],
                             default='pdfplumber', help='추출 방법')

    # validate 명령
    parser_validate = subparsers.add_parser('validate', help='PDF 유효성 검사')
    parser_validate.add_argument('pdf', help='PDF 파일 경로')

    # batch-validate 명령
    parser_batch = subparsers.add_parser('batch-validate', help='배치 검증')
    parser_batch.add_argument('directory', nargs='?', default='.',
                              help='검사할 디렉토리 (기본: 현재 디렉토리)')

    # check 명령
    subparsers.add_parser('check', help='의존성 확인')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    if args.command == 'check':
        if check_dependencies():
            print_color("✓ 모든 의존성이 설치되어 있습니다", Colors.GREEN)
            return 0
        else:
            return 1

    if not check_dependencies():
        return 1

    if args.command == 'info':
        return 0 if pdf_info(args.pdf) else 1

    elif args.command == 'text':
        return 0 if pdf_extract_text(args.pdf, args.output, args.method) else 1

    elif args.command == 'validate':
        return 0 if pdf_validate(args.pdf) else 1

    elif args.command == 'batch-validate':
        pdf_batch_validate(args.directory)
        return 0

    return 0


if __name__ == '__main__':
    sys.exit(main())
