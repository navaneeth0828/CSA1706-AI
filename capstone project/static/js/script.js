document.addEventListener("DOMContentLoaded", function () {
    // 1. Prediction Form Handler
    const predictForm = document.getElementById("predict-form");
    if (predictForm) {
        predictForm.addEventListener("submit", function (e) {
            e.preventDefault();
            
            const reviewInput = document.getElementById("review-input");
            const productSelect = document.getElementById("product-select");
            const resultSection = document.getElementById("result-section");
            const submitBtn = document.getElementById("submit-btn");
            const btnText = document.getElementById("btn-text");
            const btnSpinner = document.getElementById("btn-spinner");
            
            const reviewText = reviewInput.value.trim();
            const selectedProduct = productSelect.value;
            
            if (!reviewText || !selectedProduct) return;
            
            // Show loading state
            submitBtn.disabled = true;
            btnText.textContent = "Analyzing...";
            btnSpinner.classList.remove("d-none");
            resultSection.classList.add("d-none");
            
            fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ 
                    review: reviewText,
                    product: selectedProduct
                })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Prediction request failed.");
                }
                return response.json();
            })
            .then(data => {
                // Hide loading state
                submitBtn.disabled = false;
                btnText.textContent = "Analyze Sentiment";
                btnSpinner.classList.add("d-none");
                
                if (data.error) {
                    alert("Error: " + data.error);
                    return;
                }
                
                // Display Results
                const sentimentResult = document.getElementById("sentiment-result");
                const confidenceResult = document.getElementById("confidence-result");
                const confidenceBar = document.getElementById("confidence-bar");
                const resultCard = document.getElementById("result-card");
                
                sentimentResult.className = "badge-sentiment";
                let badgeClass = "";
                let emoji = "";
                
                if (data.sentiment === "Positive") {
                    badgeClass = "badge-pos";
                    emoji = "😊";
                    resultCard.style.borderLeft = "5px solid #15803d";
                } else if (data.sentiment === "Neutral") {
                    badgeClass = "badge-neu";
                    emoji = "😐";
                    resultCard.style.borderLeft = "5px solid #a16207";
                } else {
                    badgeClass = "badge-neg";
                    emoji = "😞";
                    resultCard.style.borderLeft = "5px solid #b91c1c";
                }
                
                sentimentResult.classList.add(badgeClass);
                sentimentResult.innerHTML = `<span>${data.sentiment} ${emoji}</span>`;
                
                confidenceResult.textContent = `${data.confidence}%`;
                confidenceBar.style.width = `${data.confidence}%`;
                
                confidenceBar.className = "progress-bar";
                if (data.sentiment === "Positive") {
                    confidenceBar.classList.add("bg-success");
                } else if (data.sentiment === "Neutral") {
                    confidenceBar.classList.add("bg-warning");
                } else {
                    confidenceBar.classList.add("bg-danger");
                }
                
                resultSection.classList.remove("d-none");
                resultSection.scrollIntoView({ behavior: "smooth", block: "nearest" });
                
                // Clear inputs
                reviewInput.value = "";
                productSelect.selectedIndex = 0;
                
                // Prepend to History Table (5 columns)
                const historyBody = document.getElementById("history-table-body");
                const noHistoryRow = document.getElementById("no-history-row");
                
                if (historyBody) {
                    if (noHistoryRow) {
                        noHistoryRow.remove();
                    }
                    
                    const now = new Date();
                    const timestampStr = now.getFullYear() + '-' + 
                        String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                        String(now.getDate()).padStart(2, '0') + ' ' + 
                        String(now.getHours()).padStart(2, '0') + ':' + 
                        String(now.getMinutes()).padStart(2, '0') + ':' + 
                        String(now.getSeconds()).padStart(2, '0');
                    
                    let historyBadgeClass = "";
                    if (data.sentiment === "Positive") historyBadgeClass = "badge-pos";
                    else if (data.sentiment === "Neutral") historyBadgeClass = "badge-neu";
                    else historyBadgeClass = "badge-neg";
                    
                    const newRow = document.createElement("tr");
                    newRow.innerHTML = `
                        <td class="text-truncate ps-3" style="max-width: 180px;" title="${escapeHtml(data.review)}">${escapeHtml(data.review)}</td>
                        <td class="text-truncate text-secondary" style="max-width: 140px;" title="${escapeHtml(data.product)}">${escapeHtml(data.product)}</td>
                        <td><span class="badge-sentiment ${historyBadgeClass}" style="font-size: 0.8rem; padding: 0.25rem 0.6rem;">${data.sentiment}</span></td>
                        <td class="font-monospace">${data.confidence}%</td>
                        <td class="text-muted small pe-3">${timestampStr}</td>
                    `;
                    
                    historyBody.insertBefore(newRow, historyBody.firstChild);
                    
                    if (historyBody.children.length > 10) {
                        historyBody.removeChild(historyBody.lastChild);
                    }
                }
            })
            .catch(error => {
                submitBtn.disabled = false;
                btnText.textContent = "Analyze Sentiment";
                btnSpinner.classList.add("d-none");
                console.error(error);
                alert("An error occurred during sentiment analysis.");
            });
        });
    }

    // 2. Clear History Handler
    const clearHistoryBtn = document.getElementById("clear-history-btn");
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener("click", function () {
            if (!confirm("Are you sure you want to clear the prediction history?")) {
                return;
            }
            
            fetch("/clear_history", {
                method: "POST"
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === "success") {
                    const historyBody = document.getElementById("history-table-body");
                    if (historyBody) {
                        historyBody.innerHTML = `
                            <tr id="no-history-row">
                                <td colspan="5" class="text-center text-muted py-4">No prediction history yet. Try analyzing a review above!</td>
                            </tr>
                        `;
                    }
                } else {
                    alert("Error: " + data.message);
                }
            })
            .catch(err => {
                console.error(err);
                alert("Failed to clear history.");
            });
        });
    }
});

// HTML escaping utility
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, function(m) { return map[m]; });
}

// 3. Dashboard Chart Rendering
window.renderDashboardCharts = function (datasetStats, dbStats) {
    const pieCtx = document.getElementById("sentimentPieChart");
    if (pieCtx) {
        new Chart(pieCtx, {
            type: 'doughnut',
            data: {
                labels: ['Positive', 'Neutral', 'Negative'],
                datasets: [{
                    data: [
                        datasetStats.positive_count,
                        datasetStats.neutral_count,
                        datasetStats.negative_count
                    ],
                    backgroundColor: ['#22c55e', '#eab308', '#ef4444'],
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: { family: 'Inter', size: 12 },
                            usePointStyle: true,
                            padding: 15
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const val = context.raw;
                                const pct = ((val / total) * 100).toFixed(1);
                                return ` ${context.label}: ${val} (${pct}%)`;
                            }
                        }
                    }
                },
                cutout: '65%'
            }
        });
    }

    const barCtx = document.getElementById("predictionsBarChart");
    if (barCtx) {
        new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: ['Positive', 'Neutral', 'Negative'],
                datasets: [{
                    label: 'User Predictions logged in DB',
                    data: [
                        dbStats.pos_count,
                        dbStats.neu_count,
                        dbStats.neg_count
                    ],
                    backgroundColor: ['#4ade80', '#fef08a', '#fca5a5'],
                    borderColor: ['#15803d', '#a16207', '#b91c1c'],
                    borderWidth: 1.5,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            font: { family: 'Inter' }
                        },
                        grid: {
                            color: '#f1f5f9'
                        }
                    },
                    x: {
                        ticks: {
                            font: { family: 'Inter' }
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
};

// 4. Product Analysis Page Chart Rendering
window.renderProductAnalysisCharts = function (sentimentData, ratingData) {
    const pieCtx = document.getElementById("productSentimentPie");
    if (pieCtx) {
        new Chart(pieCtx, {
            type: 'pie',
            data: {
                labels: ['Positive', 'Neutral', 'Negative'],
                datasets: [{
                    data: [sentimentData.pos, sentimentData.neu, sentimentData.neg],
                    backgroundColor: ['#22c55e', '#eab308', '#ef4444'],
                    borderWidth: 1,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            font: { family: 'Inter', size: 11 },
                            usePointStyle: true,
                            padding: 10
                        }
                    }
                }
            }
        });
    }

    const barCtx = document.getElementById("productRatingBar");
    if (barCtx) {
        new Chart(barCtx, {
            type: 'bar',
            data: {
                labels: ['1★', '2★', '3★', '4★', '5★'],
                datasets: [{
                    label: 'Reviews Count',
                    data: ratingData,
                    backgroundColor: '#4f46e5',
                    borderRadius: 3
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            font: { family: 'Inter' }
                        },
                        grid: {
                            color: '#f1f5f9'
                        }
                    },
                    x: {
                        ticks: {
                            font: { family: 'Inter' }
                        },
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
};
