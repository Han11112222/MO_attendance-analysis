function renderRankingChart(userAttendance) {
    // 1. 데이터 집계 로직
    const userCounts = {};
    for (const key in userAttendance) {
        const name = key.split('_')[1];
        if(name) userCounts[name] = (userCounts[name] || 0) + 1;
    }
    // 상위 10명 추출
    const sortedUsers = Object.entries(userCounts).sort((a, b) => b[1] - a[1]).slice(0, 10);
    
    // 2. 캔버스 가져오기
    const ctx = document.getElementById('rankingChart').getContext('2d');
    
    // 기존 차트가 있으면 삭제 (오류 방지)
    if (rankingChartInstance) rankingChartInstance.destroy();
    
    // 3. 차트 생성 (세로 막대형)
    rankingChartInstance = new Chart(ctx, {
        type: 'bar', 
        // indexAxis 속성을 생략하면 기본적으로 '세로(x축이 바닥)' 그래프가 됩니다.
        data: {
            labels: sortedUsers.map(u => u[0]), // 여기에 이름이 들어갑니다
            datasets: [{ 
                label: '참석 횟수', 
                data: sortedUsers.map(u => u[1]), 
                backgroundColor: 'rgba(250, 204, 21, 0.85)', // 노란색
                borderRadius: 5,
                borderWidth: 1
            }]
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false, 
            plugins: { 
                legend: { display: false } // 범례 숨김
            }, 
            scales: { 
                x: { 
                    // [중요] X축(바닥) 설정
                    display: true, 
                    grid: { display: false },
                    ticks: {
                        autoSkip: false, // 이름이 겹쳐도 숨기지 않고 다 보여줌
                        maxRotation: 45, // 이름이 길면 비스듬히 45도 회전
                        minRotation: 45,
                        font: {
                            size: 11,
                            weight: 'bold',
                            family: 'Noto Sans KR'
                        },
                        color: '#334155' // 글자색 (진한 회색)
                    }
                }, 
                y: { 
                    beginAtZero: true,
                    grid: { borderDash: [2, 2] },
                    ticks: { stepSize: 1 } // y축 눈금 1단위 고정
                } 
            } 
        }
    });
}
