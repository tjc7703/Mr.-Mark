import sys
import re

def parse_time(logfile):
    with open(logfile) as f:
        lines = f.readlines()
    times = []
    for line in lines:
        m = re.search(r'\[\+\] Building ([0-9.]+)s', line)
        if m:
            times.append(float(m.group(1)))
    return times

def main():
    print("[빌드 병목 자동 분석 리포트]")
    for logfile in sys.argv[1:]:
        times = parse_time(logfile)
        if times:
            total = max(times)
            print(f"{logfile}: 총 빌드 시간 {total:.1f}초, 단계별 최대: {max(times):.1f}초, 평균: {sum(times)/len(times):.1f}초")
        else:
            print(f"{logfile}: 빌드 시간 정보 없음")

if __name__ == "__main__":
    main() 