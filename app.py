function renderRankingChart(userAttendance) {
    const userCounts = {};
    for (const key in userAttendance) {
        const name = key.split('_')[1];
        if(name) userCounts[name] = (userCounts[name] || 0) + 1;
    }
    const sortedUsers = Object.entries(userCounts).sort((a, b) => b[1] - a[1]).slice(0, 10);
    
    const ctx = document.getElementById('rankingChart').getContext('2d');
    if (rankingChartInstance) rankingChartInstance.destroy();
    
    rankingChartInstance = new Chart(ctx, {
        type: 'bar', 
        // indexAxis를 'x'로 설정하거나 삭제하면 세로 막대그래프가 됩니다 (이름이 아래로 감)
        indexAxis: 'x', 
        data: {
            labels: sortedUsers.map(u => u[0]),
            datasets: [{ 
                label: '참석 횟수', 
                data: sortedUsers.map(u => u[1]), 
                backgroundColor: 'rgba(250, 204, 21, 0.85)', 
                borderRadius: 4 
            }]
        },
        options: { 
            responsive: true, 
            maintainAspectRatio: false, 
            plugins: { 
                legend: { display: false } 
            }, 
            scales: { 
                x: { 
                    display: true, // 이름을 표시하도록 설정 (이전 코드 오류 수정됨)
                    grid: { display: false },
                    ticks: {
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    }
                }, 
                y: { 
                    beginAtZero: true,
                    grid: { borderDash: [2, 2] } 
                } 
            } 
        }
    });
}
