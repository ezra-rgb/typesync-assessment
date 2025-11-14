<template>
  <div class="results-page">
    <div class="container">
      <div class="results-header">
        <h1>Your Assessment Results</h1>
        <p class="results-subtitle">{{ assessmentType }} - Completed {{ formattedDate }}</p>
      </div>

      <div v-if="loading" class="loading">
        <p>Loading your results...</p>
      </div>

      <div v-else-if="error" class="error-message">
        <p>{{ error }}</p>
        <router-link to="/" class="btn-primary">Return Home</router-link>
      </div>

      <div v-else class="results-content">
        <!-- Radar Chart Section -->
        <section class="chart-section">
          <h2>Archetype Profile</h2>
          <div class="chart-container">
            <canvas ref="radarChart" id="radarChart"></canvas>
          </div>
        </section>

        <!-- Scores Grid -->
        <section class="scores-section">
          <h2>Detailed Scores</h2>
          <div class="scores-grid">
            <div 
              v-for="(score, archetype) in scores" 
              :key="archetype"
              class="score-card"
              :style="{ borderLeftColor: getArchetypeColor(archetype) }"
            >
              <h3>{{ archetype }}</h3>
              <div class="score-display">
                <div class="percentage">{{ score }}%</div>
                <div class="score-bar">
                  <div class="score-fill" :style="{ width: score + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Share & Download Section -->
        <section class="actions-section">
          <h2>Share & Download</h2>
          <div class="actions-grid">
            <!-- Shareable Link -->
            <div class="action-card">
              <h3>📎 Shareable Link</h3>
              <p>Share your results with others:</p>
              <div class="share-input">
                <input 
                  type="text" 
                  :value="shareableUrl" 
                  readonly
                  class="share-url"
                >
                <button @click="copyLink" class="btn-copy">
                  {{ copyStatus }}
                </button>
              </div>
            </div>

            <!-- Download Options -->
            <div class="action-card">
              <h3>📥 Download Results</h3>
              <p>Save your results for future reference:</p>
              <div class="download-buttons">
                <button @click="downloadPDF" class="btn-download btn-pdf">
                  Download PDF
                </button>
                <button @click="downloadCSV" class="btn-download btn-csv">
                  Download CSV
                </button>
              </div>
            </div>
          </div>
        </section>

        <!-- Navigation -->
        <section class="navigation-section">
          <router-link to="/" class="btn-secondary">
            Return Home
          </router-link>
          <router-link 
            v-if="assessmentType === 'EAS-20'" 
            to="/aas" 
            class="btn-primary"
          >
            Take AAS Assessment
          </router-link>
          <router-link 
            v-if="assessmentType === 'AAS'" 
            to="/eas20" 
            class="btn-primary"
          >
            Take EAS-20 Assessment
          </router-link>
        </section>
      </div>
    </div>
  </div>
</template>

<script>
import Chart from 'chart.js/auto'
import axios from 'axios'

export default {
  name: 'Results',
  data() {
    return {
      assessmentId: null,
      assessmentType: 'Assessment',
      scores: {},
      responses: [],
      createdAt: null,
      loading: true,
      error: null,
      copyStatus: 'Copy Link',
      chart: null,
      archetype_colors: {
        'Strategist': '#FF6B6B',
        'Guardian': '#4ECDC4',
        'Innovator': '#45B7D1',
        'Coordinator': '#96CEB4',
        'Analyst': '#FFEAA7',
        'Advocate': '#DDA15E',
        'Executor': '#BC6C25'
      }
    }
  },
  computed: {
    shareableUrl() {
      if (!this.assessmentId) return ''
      return `${window.location.origin}/results/${this.assessmentId}`
    },
    formattedDate() {
      if (!this.createdAt) return ''
      return new Date(this.createdAt).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      })
    }
  },
  methods: {
    async fetchResults() {
  try {
    this.loading = true
    this.error = null

    // Use full backend URL directly
    const response = await axios.get(
      `https://typesync-backend-ipca.onrender.com/api/results/${this.assessmentId}`
    )

    const data = response.data
    this.assessmentType = data.type || 'Assessment'
    this.scores = data.scores || {}
    this.responses = data.responses || []
    this.createdAt = data.created_at || new Date().toISOString()

    this.$nextTick(() => {
      this.initializeChart()
    })
  } catch (err) {
    console.error('Error fetching results:', err)
    this.fetchFromLocalStorage()
  } finally {
    this.loading = false
  }
},

    fetchFromLocalStorage() {
      try {
        const storedResults = JSON.parse(
          localStorage.getItem(`results_${this.assessmentId}`)
        )
        
        if (!storedResults) {
          this.error = 'Results not found. Please complete an assessment first.'
          return
        }

        this.assessmentType = storedResults.type || 'Assessment'
        this.scores = storedResults.scores || {}
        this.responses = storedResults.responses || []
        this.createdAt = storedResults.createdAt || new Date().toISOString()

        // Initialize chart
        this.$nextTick(() => {
          this.initializeChart()
        })
      } catch (err) {
        this.error = 'Unable to load results. Please try again.'
      }
    },

    initializeChart() {
      const ctx = this.$refs.radarChart
      if (!ctx) return

      const labels = Object.keys(this.scores)
      const data = Object.values(this.scores)
      const colors = labels.map(label => this.archetype_colors[label] || '#667eea')

      this.chart = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: labels,
          datasets: [{
            label: this.assessmentType,
            data: data,
            borderColor: '#667eea',
            backgroundColor: 'rgba(102, 126, 234, 0.1)',
            borderWidth: 2,
            pointBackgroundColor: colors,
            pointBorderColor: '#fff',
            pointBorderWidth: 2,
            pointRadius: 5,
            pointHoverRadius: 7
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          scales: {
            r: {
              beginAtZero: true,
              max: 100,
              ticks: {
                stepSize: 20
              },
              grid: {
                color: 'rgba(0, 0, 0, 0.1)'
              }
            }
          },
          plugins: {
            legend: {
              display: true,
              labels: {
                font: { size: 12 },
                padding: 15
              }
            },
            tooltip: {
              backgroundColor: 'rgba(0, 0, 0, 0.8)',
              padding: 12,
              titleFont: { size: 14 },
              bodyFont: { size: 12 }
            }
          }
        }
      })
    },

    getArchetypeColor(archetype) {
      return this.archetype_colors[archetype] || '#667eea'
    },

    copyLink() {
      navigator.clipboard.writeText(this.shareableUrl)
      this.copyStatus = '✓ Copied!'
      setTimeout(() => {
        this.copyStatus = 'Copy Link'
      }, 2000)
    },

    async downloadPDF() {
  try {
    const html2pdf = (await import('html2pdf.js')).default
    const element = document.querySelector('.results-content')
    const opt = {
      margin: 10,
      filename: `TypeSync-${this.assessmentType}-${this.assessmentId}.pdf`,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2, useCORS: true },
      jsPDF: { orientation: 'portrait', unit: 'mm', format: 'a4' }
    }
    html2pdf().set(opt).from(element).save()
  } catch (error) {
    console.error('PDF generation error:', error)
    alert('Failed to generate PDF')
  }
},


    downloadCSV() {
      const headers = ['Archetype', 'Score (%)', 'Level']
      const rows = Object.entries(this.scores).map(([archetype, score]) => {
        let level = 'Low'
        if (score >= 66) level = 'High'
        else if (score >= 33) level = 'Medium'
        return [archetype, score, level]
      })

      let csvContent = 'data:text/csv;charset=utf-8,'
      csvContent += headers.join(',') + '\n'
      rows.forEach(row => {
        csvContent += row.join(',') + '\n'
      })

      const encodedUri = encodeURI(csvContent)
      const link = document.createElement('a')
      link.setAttribute('href', encodedUri)
      link.setAttribute('download', `TypeSync-${this.assessmentType}-${this.assessmentId}.csv`)
      link.click()
    }
  },
  mounted() {
    this.assessmentId = this.$route.params.id
    this.fetchResults()
  },
  beforeUnmount() {
    if (this.chart) {
      this.chart.destroy()
    }
  }
}
</script>

<style scoped>
.results-page {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  padding: 2rem 0;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

.results-header {
  text-align: center;
  margin-bottom: 3rem;
  padding: 2rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
}

.results-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.results-subtitle {
  color: #666;
  font-size: 1rem;
}

.loading,
.error-message {
  text-align: center;
  padding: 2rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
}

.error-message {
  color: #e74c3c;
  border-left: 4px solid #e74c3c;
}

.error-message .btn-primary {
  margin-top: 1rem;
}

.results-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

/* Chart Section */
.chart-section {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
}

.chart-section h2 {
  margin-bottom: 1.5rem;
  color: #333;
  font-size: 1.5rem;
}

.chart-container {
  position: relative;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Scores Section */
.scores-section {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
}

.scores-section h2 {
  margin-bottom: 1.5rem;
  color: #333;
  font-size: 1.5rem;
}

.scores-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}

.score-card {
  border-left: 4px solid #667eea;
  padding: 1.5rem;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.score-card:hover {
  transform: translateX(5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.score-card h3 {
  color: #333;
  margin-bottom: 1rem;
  font-weight: 600;
}

.score-display {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.percentage {
  font-size: 1.8rem;
  font-weight: 700;
  color: #667eea;
  min-width: 60px;
}

.score-bar {
  flex: 1;
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.score-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transition: width 0.3s ease;
}

/* Actions Section */
.actions-section {
  background: white;
  padding: 2rem;
  border-radius: 15px;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
}

.actions-section h2 {
  margin-bottom: 1.5rem;
  color: #333;
  font-size: 1.5rem;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}

.action-card {
  border: 1px solid #e9ecef;
  padding: 1.5rem;
  border-radius: 10px;
  background: #f8f9fa;
}

.action-card h3 {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
}

.action-card p {
  color: #666;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.share-input {
  display: flex;
  gap: 0.5rem;
}

.share-url {
  flex: 1;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  background: white;
}

.btn-copy {
  padding: 0.75rem 1.5rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-copy:hover {
  background: #764ba2;
  transform: scale(1.05);
}

.download-buttons {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.btn-download {
  flex: 1;
  min-width: 120px;
  padding: 0.75rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  font-size: 0.9rem;
}

.btn-pdf {
  background: #667eea;
  color: white;
}

.btn-pdf:hover {
  background: #5568d3;
}

.btn-csv {
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-csv:hover {
  background: #667eea;
  color: white;
}

/* Navigation Section */
.navigation-section {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  margin-top: 2rem;
}

.btn-primary,
.btn-secondary {
  padding: 0.9rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  text-align: center;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.btn-primary:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.btn-secondary {
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
}

.btn-secondary:hover {
  background: #667eea;
  color: white;
}

@media (max-width: 768px) {
  .results-header h1 {
    font-size: 1.8rem;
  }

  .scores-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .share-input {
    flex-direction: column;
  }

  .download-buttons {
    flex-direction: column;
  }

  .btn-download {
    width: 100%;
  }
}
</style>