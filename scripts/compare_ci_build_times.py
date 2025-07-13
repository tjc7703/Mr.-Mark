import glob
import re

print("[CI/CD별 빌드 속도 비교 리포트]")
print("플랫폼, 빌드시간(초)")
for logfile in glob.glob("ci_build_*.log"):
    platform = logfile.replace("ci_build_","").replace(".log","")
    with open(logfile) as f:
        content = f.read()
    m = re.search(r'Total build time: ([0-9.]+)s', content)
    if m:
        print(f"{platform}, {m.group(1)}")
    else:
        print(f"{platform}, 정보 없음") 