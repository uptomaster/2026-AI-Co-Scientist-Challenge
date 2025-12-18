import time
import psutil

def run_workload(iterations):
    start = time.time()
    for _ in range(iterations):
        pass
    end = time.time()
    return end - start

# 부하 시나리오 정의
workloads = {
    "short_request": 10**6,     # 짧은 요청
    "long_request": 10**7,      # 긴 연산
}

results = {}

for name, iters in workloads.items():
    exec_time = run_workload(iters)
    cpu_usage = psutil.cpu_percent(interval=1)
    results[name] = (exec_time, cpu_usage)

# 결과 출력
for name, (t, cpu) in results.items():
    print(f"{name} | Time: {t:.2f}s | CPU Usage: {cpu}%")
