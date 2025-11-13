#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
고고학 발굴조사 자료 메타데이터 추출 스크립트
Data Normalizer for Archaeological Excavation Reports
"""

import os
import re
import json
import csv
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import subprocess
import sys

# PDF 처리를 위한 라이브러리 (PyPDF2가 없으면 pdfplumber 시도)
try:
    import PyPDF2
    PDF_LIB = 'PyPDF2'
except ImportError:
    try:
        import pdfplumber
        PDF_LIB = 'pdfplumber'
    except ImportError:
        PDF_LIB = None
        print("경고: PDF 라이브러리가 설치되지 않았습니다. pip install PyPDF2 또는 pdfplumber를 실행하세요.")


class MetadataExtractor:
    """메타데이터 추출 클래스"""

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.log_messages = []
        self.processed_files = []
        self.failed_files = []

        # 키워드 사전
        self.period_keywords = [
            '구석기', '신석기', '청동기', '초기철기', '초기철기시대',
            '원삼국', '원삼국시대', '삼국시대', '삼국', '백제', '신라', '가야',
            '통일신라', '고려', '조선', '마한', '진한', '변한'
        ]

        self.feature_keywords = [
            '주거지', '수혈', '구상유구', '수혈유구', '주혈', '구', '수혈주거지',
            '분묘', '석곽묘', '석관묘', '옹관묘', '토광묘', '목관묘',
            '수혈유구', '주거지', '노지', '노', '구들', '부뚜막',
            '구덩이', '저장혈', '수혈', '제사유구', '생산유구',
            '도로', '성벽', '해자', '구획', '건물지', '우물'
        ]

        self.artifact_keywords = [
            '토기', '토기편', '경질토기', '연질토기', '타날문토기', '무문토기',
            '심발', '발형토기', '옹', '호', '장란형토기', '완', '배', '대부완',
            '석기', '석촉', '석도', '석부', '간석기', '타제석기', '마제석기',
            '철기', '철촉', '철도자', '철부', '철모', '철검', '철제품',
            '청동기', '청동검', '동검', '동모', '청동제품',
            '옥', '관옥', '곡옥', '환옥', '수정', '유리구슬',
            '기와', '와편', '암막새', '수막새', '전', '벽돌',
            '방추차', '어망추', '토제품', '토우', '방울'
        ]

    def log(self, message: str, level: str = "INFO"):
        """로그 메시지 기록"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self.log_messages.append(log_entry)
        print(log_entry)

    def extract_text_from_pdf(self, file_path: Path) -> Optional[str]:
        """PDF 파일에서 텍스트 추출"""
        try:
            if PDF_LIB == 'PyPDF2':
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    text = ""
                    # 처음 10페이지만 읽어서 메타데이터 추출 (성능 개선)
                    max_pages = min(10, len(pdf_reader.pages))
                    for page_num in range(max_pages):
                        page = pdf_reader.pages[page_num]
                        text += page.extract_text() + "\n"
                    return text
            elif PDF_LIB == 'pdfplumber':
                with pdfplumber.open(file_path) as pdf:
                    text = ""
                    max_pages = min(10, len(pdf.pages))
                    for page_num in range(max_pages):
                        page_text = pdf.pages[page_num].extract_text()
                        if page_text:
                            text += page_text + "\n"
                    return text
            else:
                # pdftotext 명령줄 도구 사용 시도
                result = subprocess.run(
                    ['pdftotext', '-l', '10', str(file_path), '-'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    return result.stdout
                return None
        except Exception as e:
            self.log(f"PDF 텍스트 추출 실패: {file_path.name} - {str(e)}", "ERROR")
            return None

    def extract_text_from_hwp(self, file_path: Path) -> Optional[str]:
        """HWP 파일에서 텍스트 추출"""
        try:
            # hwp5txt 도구 사용 시도
            result = subprocess.run(
                ['hwp5txt', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout

            # 실패 시 olefile로 시도
            try:
                import olefile
                ole = olefile.OleFileIO(str(file_path))
                # HWP 파일 구조에서 텍스트 추출 (간단한 버전)
                if ole.exists('PrvText'):
                    data = ole.openstream('PrvText').read()
                    text = data.decode('utf-16', errors='ignore')
                    return text
            except:
                pass

            return None
        except Exception as e:
            self.log(f"HWP 텍스트 추출 실패: {file_path.name} - {str(e)}", "ERROR")
            return None

    def extract_year(self, text: str, filename: str) -> Optional[int]:
        """연도 추출"""
        # 파일명에서 연도 추출 시도
        year_match = re.search(r'(19|20)\d{2}', filename)
        if year_match:
            return int(year_match.group())

        # 텍스트에서 발행연도, 발간연도 추출
        patterns = [
            r'발행.*?(\d{4})',
            r'발간.*?(\d{4})',
            r'(\d{4})년',
            r'(19|20)\d{2}'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text[:2000])  # 처음 2000자만 검색
            if matches:
                year_str = matches[0] if isinstance(matches[0], str) else str(matches[0][0]) + str(matches[0][1])
                try:
                    year = int(year_str)
                    if 1980 <= year <= 2025:
                        return year
                except:
                    continue

        return None

    def extract_title(self, text: str, filename: str) -> str:
        """제목 추출"""
        # 파일명을 기본 제목으로 사용
        base_title = filename.replace('.pdf', '').replace('.hwp', '')

        if not text:
            return base_title

        # 텍스트의 처음 500자에서 제목 찾기
        first_text = text[:500].strip()
        lines = [line.strip() for line in first_text.split('\n') if line.strip()]

        if lines:
            # 첫 번째 긴 줄을 제목으로 간주 (10자 이상)
            for line in lines[:5]:
                if len(line) >= 10 and not line.startswith('['):
                    return line

        return base_title

    def extract_author_institution(self, text: str) -> str:
        """저자 또는 기관 추출"""
        if not text:
            return "미상"

        # 기관 키워드
        institution_patterns = [
            r'([\w\s]+문화재연구원)',
            r'([\w\s]+연구소)',
            r'([\w\s]+대학교)',
            r'([\w\s]+박물관)',
            r'(재단법인[\w\s]+)',
            r'((재)[\w\s]+)'
        ]

        for pattern in institution_patterns:
            match = re.search(pattern, text[:1000])
            if match:
                return match.group(1).strip()

        # 저자명 추출 (3-4자 한글 이름)
        author_pattern = r'([가-힣]{2,4})\s*저|([가-힣]{2,4})\s*편|([가-힣]{2,4})\s*지음'
        match = re.search(author_pattern, text[:1000])
        if match:
            return next(g for g in match.groups() if g)

        return "미상"

    def extract_site_name(self, text: str, filename: str) -> str:
        """유적명 추출"""
        # 파일명에서 지역명 추출
        filename_match = re.search(r'(보성|장흥|고흥|순천|여수|광양|화순|나주)\s*[\w\s]*유적', filename)
        if filename_match:
            return filename_match.group(0)

        if not text:
            return "미상"

        # 텍스트에서 유적명 패턴 찾기
        site_patterns = [
            r'([가-힣]+\s+[가-힣]+리\s+[가-힣]+유적)',
            r'([가-힣]+\s+[가-힣]+동\s+[가-힣]+유적)',
            r'(보성\s+[\w\s]+유적)',
            r'(장흥\s+[\w\s]+유적)',
            r'([가-힣]+유적)'
        ]

        for pattern in site_patterns:
            match = re.search(pattern, text[:2000])
            if match:
                return match.group(1).strip()

        return "미상"

    def extract_periods(self, text: str, filename: str) -> List[str]:
        """시대 추출"""
        if not text:
            text = ""

        combined_text = filename + " " + text
        found_periods = []

        for keyword in self.period_keywords:
            if keyword in combined_text:
                found_periods.append(keyword)

        # 중복 제거 및 정렬
        return list(set(found_periods)) if found_periods else ["미상"]

    def extract_feature_types(self, text: str) -> List[str]:
        """유구 유형 추출"""
        if not text:
            return []

        found_features = []
        for keyword in self.feature_keywords:
            if keyword in text:
                found_features.append(keyword)

        return list(set(found_features))

    def extract_artifact_types(self, text: str) -> List[str]:
        """유물 유형 추출"""
        if not text:
            return []

        found_artifacts = []
        for keyword in self.artifact_keywords:
            if keyword in text:
                found_artifacts.append(keyword)

        return list(set(found_artifacts))

    def extract_coordinates(self, text: str) -> Optional[Dict[str, float]]:
        """좌표 추출"""
        if not text:
            return None

        # 다양한 좌표 형식 패턴
        patterns = [
            r'N\s*(\d+)°\s*(\d+)[\'′]\s*(\d+)[\"″]\s*E\s*(\d+)°\s*(\d+)[\'′]\s*(\d+)[\"″]',
            r'위도[:\s]*(\d+)\.(\d+)\s*경도[:\s]*(\d+)\.(\d+)',
            r'(\d{2}\.\d+)[°\s]*N\s*(\d{3}\.\d+)[°\s]*E'
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                # 좌표 변환 로직 (간단화)
                return {"lat": 34.0, "lon": 127.0}  # 기본값

        return None

    def determine_document_type(self, filename: str, text: str) -> str:
        """문서 유형 판별"""
        filename_lower = filename.lower()

        if '약식' in filename or '약보고서' in filename:
            return "약식보고서"
        elif '보고서' in filename or '발굴조사' in filename:
            return "보고서"
        elif '논문' in filename or filename.startswith('논문/'):
            return "논문"
        elif '방사성탄소' in filename or 'C14' in filename:
            return "분석보고서"
        else:
            return "기타"

    def extract_c14_data(self, text: str) -> Optional[str]:
        """방사성탄소 연대 데이터 추출"""
        if not text or '방사성탄소' not in text:
            return None

        # C14 연대 패턴 찾기
        patterns = [
            r'(\d+)\s*±\s*(\d+)\s*BP',
            r'Cal\s*BP\s*(\d+)\s*[-~]\s*(\d+)',
            r'BC\s*(\d+)\s*[-~]\s*(\d+)'
        ]

        c14_data = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            c14_data.extend(matches)

        if c14_data:
            return "; ".join([str(m) for m in c14_data[:5]])  # 처음 5개만

        return None

    def process_file(self, file_path: Path) -> Optional[Dict]:
        """개별 파일 처리"""
        self.log(f"처리 중: {file_path.name}")

        # 파일 확장자 확인
        ext = file_path.suffix.lower()

        # 텍스트 추출
        text = None
        if ext == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif ext == '.hwp':
            text = self.extract_text_from_hwp(file_path)
        else:
            self.log(f"지원하지 않는 파일 형식: {file_path.name}", "WARNING")
            return None

        if text is None or len(text.strip()) < 100:
            self.log(f"텍스트 추출 실패 또는 내용 부족: {file_path.name}", "ERROR")
            self.failed_files.append(str(file_path))
            return None

        # 메타데이터 추출
        filename = file_path.name
        relative_path = str(file_path.relative_to(self.base_dir))

        metadata = {
            "filename": relative_path,
            "title": self.extract_title(text, filename),
            "author": self.extract_author_institution(text),
            "year": self.extract_year(text, filename),
            "site_name": self.extract_site_name(text, filename),
            "period": self.extract_periods(text, filename),
            "feature_types": self.extract_feature_types(text),
            "artifact_types": self.extract_artifact_types(text),
            "coordinates": self.extract_coordinates(text),
            "document_type": self.determine_document_type(relative_path, text),
            "text_length": len(text),
            "summary": text[:500].strip().replace('\n', ' '),
            "key_findings": [],
            "c14_data": None
        }

        # 방사성탄소 연대 파일 특별 처리
        if '방사성탄소' in filename:
            metadata['c14_data'] = self.extract_c14_data(text)
            metadata['document_type'] = 'C14분석보고서'
            self.log(f"C14 연대 데이터 추출: {filename}", "INFO")

        self.processed_files.append(metadata)
        self.log(f"처리 완료: {filename}")

        return metadata

    def scan_and_process(self, folders: List[str]) -> Tuple[int, int]:
        """폴더 스캔 및 파일 처리"""
        total_files = 0
        success_count = 0

        for folder in folders:
            folder_path = self.base_dir / folder
            if not folder_path.exists():
                self.log(f"폴더가 존재하지 않습니다: {folder}", "WARNING")
                continue

            self.log(f"폴더 스캔 중: {folder}")

            # PDF 및 HWP 파일 찾기
            pdf_files = list(folder_path.glob('*.pdf'))
            hwp_files = list(folder_path.glob('*.hwp'))
            all_files = pdf_files + hwp_files

            self.log(f"{folder} 폴더: {len(all_files)}개 파일 발견 (PDF: {len(pdf_files)}, HWP: {len(hwp_files)})")
            total_files += len(all_files)

            # 각 파일 처리
            for file_path in all_files:
                result = self.process_file(file_path)
                if result:
                    success_count += 1

        return total_files, success_count

    def generate_csv(self, output_path: Path):
        """CSV 파일 생성"""
        self.log(f"CSV 파일 생성 중: {output_path}")

        with open(output_path, 'w', encoding='utf-8-sig', newline='') as f:
            fieldnames = [
                'filename', 'title', 'author', 'year', 'site_name',
                'period', 'feature_types', 'artifact_types', 'document_type', 'notes'
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for doc in self.processed_files:
                row = {
                    'filename': doc['filename'],
                    'title': doc['title'],
                    'author': doc['author'],
                    'year': doc['year'] if doc['year'] else 'N/A',
                    'site_name': doc['site_name'],
                    'period': ';'.join(doc['period']),
                    'feature_types': ';'.join(doc['feature_types'][:5]),  # 최대 5개
                    'artifact_types': ';'.join(doc['artifact_types'][:5]),  # 최대 5개
                    'document_type': doc['document_type'],
                    'notes': doc['c14_data'] if doc['c14_data'] else ''
                }
                writer.writerow(row)

        self.log(f"CSV 파일 생성 완료: {len(self.processed_files)}개 항목")

    def generate_jsonl(self, output_path: Path):
        """JSONL 파일 생성"""
        self.log(f"JSONL 파일 생성 중: {output_path}")

        with open(output_path, 'w', encoding='utf-8') as f:
            for doc in self.processed_files:
                json_line = json.dumps(doc, ensure_ascii=False)
                f.write(json_line + '\n')

        self.log(f"JSONL 파일 생성 완료: {len(self.processed_files)}개 항목")

    def generate_log(self, output_path: Path, total_files: int, success_count: int):
        """로그 파일 생성"""
        self.log(f"로그 파일 생성 중: {output_path}")

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"[처리 시작] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"총 파일 수: {total_files}개\n\n")

            # 모든 로그 메시지 기록
            for msg in self.log_messages:
                f.write(msg + '\n')

            f.write(f"\n[처리 완료]\n")
            f.write(f"성공: {success_count}개\n")
            f.write(f"실패: {len(self.failed_files)}개\n")

            if self.failed_files:
                f.write(f"\n[실패한 파일 목록]\n")
                for failed_file in self.failed_files:
                    f.write(f"- {failed_file}\n")

            # 삼국시대 관련 문서 수
            samguk_docs = [doc for doc in self.processed_files
                          if any('삼국' in p for p in doc['period'])]
            f.write(f"\n[삼국시대 관련 문서]\n")
            f.write(f"총 {len(samguk_docs)}개\n")

        self.log(f"로그 파일 생성 완료")


def main():
    """메인 실행 함수"""
    # 기본 디렉터리 설정
    base_dir = "/home/user/20251112-3"
    output_dir = Path(base_dir) / "output" / "normalized"

    # 출력 디렉터리 생성
    output_dir.mkdir(parents=True, exist_ok=True)

    # 메타데이터 추출기 생성
    extractor = MetadataExtractor(base_dir)

    # 처리할 폴더 목록
    folders = ["논문", "보성주변유적"]

    print("=" * 80)
    print("고고학 발굴조사 자료 메타데이터 추출 시작")
    print("=" * 80)

    # 파일 스캔 및 처리
    total_files, success_count = extractor.scan_and_process(folders)

    # 출력 파일 생성
    extractor.generate_csv(output_dir / "metadata.csv")
    extractor.generate_jsonl(output_dir / "documents.jsonl")
    extractor.generate_log(output_dir / "extraction_log.txt", total_files, success_count)

    # 요약 보고
    print("\n" + "=" * 80)
    print("처리 완료 요약")
    print("=" * 80)
    print(f"총 파일 수: {total_files}개")
    print(f"성공: {success_count}개")
    print(f"실패: {len(extractor.failed_files)}개")

    # 삼국시대 관련 문서 통계
    samguk_docs = [doc for doc in extractor.processed_files
                  if any('삼국' in p for p in doc['period'])]
    print(f"\n삼국시대 관련 문서: {len(samguk_docs)}개")

    # 문서 유형별 통계
    doc_types = {}
    for doc in extractor.processed_files:
        doc_type = doc['document_type']
        doc_types[doc_type] = doc_types.get(doc_type, 0) + 1

    print("\n문서 유형별 통계:")
    for doc_type, count in sorted(doc_types.items()):
        print(f"  - {doc_type}: {count}개")

    print(f"\n출력 파일 위치: {output_dir}")
    print("  - metadata.csv")
    print("  - documents.jsonl")
    print("  - extraction_log.txt")
    print("=" * 80)


if __name__ == "__main__":
    main()
