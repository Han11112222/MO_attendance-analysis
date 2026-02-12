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
        // 💡 가로 막대형(y)에서 세로 막대형으로 변경하여 하단에 이름이 나오게 합니다.
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
            responsive: True, 
            maintainAspectRatio: False, 
            plugins: { 
                legend: { display: False } 
            }, 
            scales: { 
                x: { 
                    display: True, // 💡 이름을 표시하기 위해 True로 설정
                    grid: { display: False },
                    ticks: {
                        font: {
                            size: 12,
                            weight: 'bold'
                        }
                    }
                }, 
                y: { 
                    beginAtZero: True,
                    grid: { borderDash: [2, 2] } 
                } 
            } 
        }
    });
}
