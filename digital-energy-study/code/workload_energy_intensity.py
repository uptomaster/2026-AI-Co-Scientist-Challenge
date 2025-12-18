import time
import psutil
import statistics

# ============================================================
# Energy Model Parameters
# ------------------------------------------------------------
# 본 연구에서는 전형적인 서버 노드를 가정한 선형 전력 모델을 사용한다.
# P_IDLE : 서버 유휴 상태에서의 전력 소비 (W)
# P_MAX  : 서버 최대 부하 시 전력 소비 (W)
# 해당 값들은 선행 서버 에너지 모델 연구를 참고한 가정값이다.
# ============================================================
P_IDLE = 50    # W (Idle power)
P_MAX = 150   # W (Max power)

# 각 실험 조건에 대해 반복 수행 횟수
# 단일 측정값의 변동성을 줄이기 위한 통계적 평균 처리 목적
REPEAT = 5

def run_workload(iterations):
    """
    지정된 반복 횟수(iterations)에 대해 단순 연산 부하를 수행하고,
    해당 부하 동안의 실행 시간과 CPU 사용률을 측정한다.

    CPU 사용률은 시스템 전체가 아닌,
    본 실험 프로세스(psutil.Process()) 단위로 측정하여
    정보 처리 부하와의 시간적 대응성을 확보한다.
    """

    # 현재 프로세스 객체 생성
    process = psutil.Process()

    # cpu_percent 측정 초기화
    # 이전 측정값의 영향을 제거하기 위함
    process.cpu_percent(None)

    # 부하 수행 시작 시점
    start = time.time()

    # 단순 반복 연산을 통해 CPU 연산 부하 생성
    for _ in range(iterations):
        pass

    # 부하 수행 종료 시점에서의 CPU 사용률 측정
    cpu_usage = process.cpu_percent(None)

    end = time.time()

    # 실행 시간과 CPU 사용률 반환
    return end - start, cpu_usage

def calculate_energy(exec_time, cpu_usage):
    """
    실행 시간과 CPU 사용률을 기반으로 에너지 소비량을 계산한다.

    에너지 모델:
        E = (P_IDLE + u * (P_MAX - P_IDLE)) * t

    where:
        u : CPU 사용률 (0~1)
        t : 실행 시간 (초)
    """

    u = cpu_usage / 100.0
    power = P_IDLE + u * (P_MAX - P_IDLE)
    energy = power * exec_time

    return energy

# ============================================================
# Workload Definitions
# ------------------------------------------------------------
# 정보 처리 부하 유형(short / long)과
# 각 부하의 강도(low / mid / high)를 정의
#
# short  : 검색과 같은 짧은 정보 처리 요청을 모사
# long   : 추론·분석과 같은 상대적으로 무거운 처리 요청을 모사
# ============================================================
workloads = {
    "short_low": 5 * 10**5,
    "short_mid": 10**6,
    "short_high": 2 * 10**6,
    "long_low": 5 * 10**6,
    "long_mid": 10**7,
    "long_high": 2 * 10**7,
}

# 결과 출력 헤더
print("Workload | Time(s) | CPU(%) | Energy(J) | J/request")

# 각 부하 조건에 대해 실험 수행
for name, iters in workloads.items():

    # 반복 실험 결과 저장 리스트
    times = []
    cpus = []
    energies = []

    # 동일 조건에서 REPEAT 횟수만큼 반복 실험 수행
    for _ in range(REPEAT):
        exec_time, cpu_usage = run_workload(iters)
        energy = calculate_energy(exec_time, cpu_usage)

        times.append(exec_time)
        cpus.append(cpu_usage)
        energies.append(energy)

    # 평균값 계산
    avg_time = statistics.mean(times)
    avg_cpu = statistics.mean(cpus)
    avg_energy = statistics.mean(energies)

    # 단위 요청당 에너지 소비량 계산
    energy_per_req = avg_energy / iters

    # 결과 출력
    print(
        f"{name:10s} | "
        f"{avg_time:6.2f} | "
        f"{avg_cpu:6.1f} | "
        f"{avg_energy:8.2f} | "
        f"{energy_per_req:.6f}"
    )
