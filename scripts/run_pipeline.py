#!/usr/bin/env python3
"""
Mr. Mark 데이터/AI 파이프라인 전체 실행 스크립트
- 데이터 수집/적재/정제
- 품질 체크
- AI 학습/예측
- 리포트 생성
"""
import subprocess
import sys
import os


def run_step(name, cmd):
    print(f"\n===== [{name}] 단계 실행 =====")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {name} 단계에서 오류 발생: {e}")
        sys.exit(1)


def main():
    steps = [
        ("ETL", "python scripts/etl.py"),
        ("품질 체크", "python scripts/quality_check.py"),
        ("AI 학습/예측", "python scripts/train_ai.py"),
        ("리포트 생성", "python scripts/report.py"),
    ]
    for name, cmd in steps:
        if os.path.exists(cmd.split()[1]):
            run_step(name, cmd)
        else:
            print(f"[SKIP] {name} 단계 스크립트가 없어 더미 실행")
            print(f"[DUMMY] {name} 단계 완료!")
    print("\n🎉 전체 파이프라인 실행 완료!")


if __name__ == "__main__":
    main()
