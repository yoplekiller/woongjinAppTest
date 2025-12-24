"""
중앙 로깅 시스템
실무용: 파일 저장, 콘솔 출력, 레벨별 필터링
"""
from typing import Optional
import logging
import os
from datetime import datetime
from config.app_config import AppConfig


class TestLogger:
    """테스트 로거 싱글톤"""

    _instance: Optional['TestLogger'] = None
    _logger: Optional[logging.Logger] = None

    def __new__(cls) -> 'TestLogger':
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._logger is None:
            self._setup_logger()

    def _setup_logger(self) -> None:
        """로거 초기 설정"""
        # 로그 디렉토리 생성
        log_dir = "./logs"
        os.makedirs(log_dir, exist_ok=True)

        # 로거 생성
        self._logger = logging.getLogger("AppiumTest")
        self._logger.setLevel(logging.DEBUG)

        # 기존 핸들러 제거 (중복 방지)
        if self._logger.handlers:
            self._logger.handlers.clear()

        # 포맷 설정
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # 파일 핸들러 - 전체 로그
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_handler = logging.FileHandler(
            f"{log_dir}/test_{timestamp}.log",
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

        # 파일 핸들러 - 에러만
        error_handler = logging.FileHandler(
            f"{log_dir}/error_{timestamp}.log",
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self._logger.addHandler(error_handler)

        # 콘솔 핸들러
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(levelname)-8s | %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self._logger.addHandler(console_handler)

        self._logger.info("=" * 80)
        self._logger.info("테스트 로거 초기화 완료")
        self._logger.info("=" * 80)

    def get_logger(self) -> logging.Logger:
        """로거 인스턴스 반환"""
        return self._logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    로거 가져오기

    Usage:
        from utils.logger import get_logger
        logger = get_logger(__name__)
        logger.info("테스트 시작")
    """
    test_logger = TestLogger()
    logger = test_logger.get_logger()

    if name:
        return logger.getChild(name)
    return logger
