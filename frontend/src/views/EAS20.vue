<template>
  <div class="eas20-container">
    <div class="eas20-header">
      <h1>Environment Assessment Scale (EAS-20)</h1>
      <p class="subtitle">Workplace Environmental Demands Assessment</p>
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>
      <p class="progress-text">{{ currentItem + 1 }} of 20 items</p>
    </div>

    <div class="eas20-main" v-if="!showResults">
      <div class="question-section">
        <div class="question-number">{{ currentItem + 1 }}.</div>
        <div class="question-text">{{ currentQuestion.text }}</div>
      </div>

      <div class="rating-scale">
        <div class="scale-instruction">
          Rate how much this describes your current work environment:
        </div>

        <div class="rating-options">
          <button
            v-for="(label, idx) in ratingLabels"
            :key="idx"
            class="rating-btn"
            :class="{ active: responses[currentItem] === idx + 1 }"
            @click="selectRating(idx + 1)"
          >
            <div class="rating-value">{{ idx + 1 }}</div>
            <div class="rating-label">{{ label }}</div>
          </button>
        </div>
      </div>

      <div class="navigation-buttons">
        <button class="btn btn-secondary" @click="previousQuestion" :disabled="currentItem === 0">
          ← Previous
        </button>

        <button
          v-if="currentItem < 19"
          class="btn btn-primary"
          @click="nextQuestion"
          :disabled="responses[currentItem] === null"
        >
          Next →
        </button>

        <button v-else class="btn btn-success" @click="submitAssessment" :disabled="!isAllAnswered">
          Submit Assessment
        </button>
      </div>

      <div class="answered-summary">
        <span>{{ answeredCount }} of 20 answered</span>
      </div>

      <p v-if="message" :class="['message', messageType]">
        {{ message }}
      </p>
    </div>

    <div v-else class="eas20-results">
      <div class="results-header">
        <h2>Your Environmental Profile</h2>
        <p>How your workplace demands align with the 7 S.E.M.P. archetypes</p>
      </div>

      <div class="radar-chart-section">
        <h3>{{ radarTitle }}</h3>
        <div class="radar-container">
          <canvas id="easRadarChart"></canvas>
        </div>
      </div>

      <div class="results-charts">
        <h3>Environmental Demand Breakdown</h3>
        <div v-for="archetype in archetypes" :key="archetype.name" class="archetype-result">
          <div class="result-label">{{ archetype.name }}</div>
          <div class="result-bar-container">
            <div
              class="result-bar"
              :style="{
                width: (scores[archetype.name] || 0) + '%',
                backgroundColor: archetype.color,
              }"
            ></div>
          </div>
          <div class="result-score">{{ (scores[archetype.name] || 0).toFixed(0) }}%</div>
        </div>
      </div>

      <div class="archetype-summary">
        <div class="summary-section">
          <h3>Primary Environmental Demand</h3>
          <p class="primary-archetype">{{ primaryArchetype }}</p>
          <p class="summary-description">{{ getArchetypeDescription(primaryArchetype) }}</p>
        </div>

        <div class="summary-section">
          <h3>Secondary Environmental Demands</h3>
          <div v-if="secondaryArchetypes.length > 0" class="secondary-archetypes">
            <p v-for="archetype in secondaryArchetypes" :key="archetype">• {{ archetype }}</p>
          </div>
          <p v-else class="no-secondary">No secondary demands identified</p>
        </div>
      </div>

      <div class="raw-data">
        <h3>Complete Scoring Data</h3>
        <div class="data-table">
          <div class="data-row header">
            <div class="data-cell">Archetype</div>
            <div class="data-cell">Raw Score</div>
            <div class="data-cell">Max Score</div>
            <div class="data-cell">Percentage</div>
          </div>
          <div v-for="archetype in archetypes" :key="archetype.name" class="data-row">
            <div class="data-cell">{{ archetype.name }}</div>
            <div class="data-cell">{{ rawScores[archetype.name] || 0 }}</div>
            <div class="data-cell">{{ archetype.maxScore }}</div>
            <div class="data-cell">{{ (scores[archetype.name] || 0).toFixed(1) }}%</div>
          </div>
        </div>
      </div>

      <div class="results-actions">
        <button class="btn btn-secondary" @click="resetAssessment">Take Assessment Again</button>
        <button class="btn btn-primary" @click="downloadResults">Download Data (CSV)</button>
      </div>

      <div class="disclaimer">
        <p>
          <strong>Important Disclaimer:</strong> The EAS-20 is a pre-validated research instrument
          and has not undergone formal empirical validation. Results are for developmental and
          exploratory purposes only, not for operational decision-making.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { Chart } from 'chart.js/auto'
import { useRouter } from 'vue-router'

export default {
  name: 'EAS20Assessment',
  setup() {
    const router = useRouter()
    return { router }
  },
  data() {
    return {
      currentItem: 0,
      responses: new Array(20).fill(null),
      showResults: false,
      ratingLabels: ['Not at all', 'Slightly', 'Moderately', 'Considerably', 'Very much'],
      questions: [
        {
          text: 'Work in this role frequently requires rapid identification of hidden patterns and anticipation of future developments',
          domain: 'Strategist',
        },
        {
          text: 'This environment demands long-term strategic thinking and complex planning across multiple variables',
          domain: 'Strategist',
        },
        {
          text: 'Success here depends on the ability to synthesize information from diverse sources to predict outcomes',
          domain: 'Strategist',
        },
        {
          text: 'Managing uncertainty and maintaining safety in unpredictable situations is a core part of this environment',
          domain: 'Guardian',
        },
        {
          text: 'This workplace requires constant vigilance and attention to potential risks or threats',
          domain: 'Guardian',
        },
        {
          text: 'Protecting resources, people, or processes from harm is a critical responsibility in this role',
          domain: 'Guardian',
        },
        {
          text: 'This environment actively encourages experimentation and the generation of novel solutions',
          domain: 'Innovator',
        },
        {
          text: 'Success requires breaking conventional approaches and implementing creative ideas',
          domain: 'Innovator',
        },
        {
          text: 'This workplace rewards those who challenge existing methods and pioneer new approaches',
          domain: 'Innovator',
        },
        {
          text: 'This role involves frequent negotiation and resolution of conflicts between different parties',
          domain: 'Coordinator',
        },
        {
          text: 'Success depends on the ability to organize diverse groups and align competing interests',
          domain: 'Coordinator',
        },
        {
          text: 'This environment requires managing complex interdependencies between teams or departments',
          domain: 'Coordinator',
        },
        {
          text: 'This work environment demands systematic analysis and logical problem-solving approaches',
          domain: 'Analyst',
        },
        {
          text: 'Success requires breaking down complex problems into component parts for detailed examination',
          domain: 'Analyst',
        },
        {
          text: 'This role involves extensive data interpretation and evidence-based decision making',
          domain: 'Analyst',
        },
        {
          text: 'This environment requires building strong relationships and influencing others through persuasion',
          domain: 'Advocate',
        },
        {
          text: "Success depends on understanding others' perspectives and communicating effectively across diverse groups",
          domain: 'Advocate',
        },
        {
          text: 'This role involves representing interests and negotiating on behalf of others or the organization',
          domain: 'Advocate',
        },
        {
          text: 'This environment demands reliable execution of tasks under tight deadlines and high pressure',
          domain: 'Executor',
        },
        {
          text: 'Success requires consistent delivery of results through persistence and methodical implementation',
          domain: 'Executor',
        },
      ],
      archetypes: [
        { name: 'Strategist', color: '#8B5CF6', maxScore: 15 },
        { name: 'Guardian', color: '#DC2626', maxScore: 15 },
        { name: 'Innovator', color: '#06B6D4', maxScore: 15 },
        { name: 'Coordinator', color: '#10B981', maxScore: 15 },
        { name: 'Analyst', color: '#F59E0B', maxScore: 15 },
        { name: 'Advocate', color: '#EC4899', maxScore: 15 },
        { name: 'Executor', color: '#3B82F6', maxScore: 10 },
      ],
      scores: {},
      rawScores: {},
      primaryArchetype: '',
      secondaryArchetypes: [],
      radarChart: null,
      message: '',
      messageType: 'success',
    }
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentItem]
    },
    progressPercent() {
      return ((this.currentItem + 1) / 20) * 100
    },
    answeredCount() {
      return this.responses.filter((r) => r !== null).length
    },
    isAllAnswered() {
      return this.responses.every((r) => r !== null)
    },
    radarTitle() {
      return 'Environmental Demand Profile'
    },
  },
  methods: {
    selectRating(rating) {
      this.responses[this.currentItem] = rating
    },
    nextQuestion() {
      if (this.currentItem < 19 && this.responses[this.currentItem] !== null) {
        this.currentItem++
      }
    },
    previousQuestion() {
      if (this.currentItem > 0) {
        this.currentItem--
      }
    },
    async submitAssessment() {
      if (!this.isAllAnswered) return

      try {
        // Send payload WITHOUT assessment_id - backend will generate it
        const payload = {
          responses: this.responses,
          domain_scores: this.calculateDomainScores(),
        }

        console.log('Submitting EAS-20 assessment:', payload)

        // Use relative URL - vite proxy handles it
        const response = await axios.post('/api/assessments/eas20/save', payload)

        if (response.data?.success && response.data?.assessment_id) {
          const assessmentId = response.data.assessment_id
          console.log('✅ EAS-20 saved with ID:', assessmentId)

          this.calculateScores()
          this.showResults = true
          this.$nextTick(() => {
            this.renderRadarChart()
          })
        } else {
          throw new Error('Invalid response format')
        }
      } catch (error) {
        console.error('Assessment error:', error)
        this.message = error.message || 'Failed to submit assessment'
        this.messageType = 'error'
      }
    },
    calculateScores() {
      const domainMapping = {
        Strategist: [0, 1, 2],
        Guardian: [3, 4, 5],
        Innovator: [6, 7, 8],
        Coordinator: [9, 10, 11],
        Analyst: [12, 13, 14],
        Advocate: [15, 16, 17],
        Executor: [18, 19],
      }

      for (const archetype of this.archetypes) {
        const itemIndices = domainMapping[archetype.name] || []
        const rawSum = itemIndices.reduce((sum, idx) => sum + (this.responses[idx] || 0), 0)
        const percentage = (rawSum / archetype.maxScore) * 100
        this.rawScores[archetype.name] = rawSum
        this.scores[archetype.name] = Math.min(100, percentage)
      }

      // Find primary archetype
      let maxScore = -1
      for (const archetype of this.archetypes) {
        if (this.scores[archetype.name] > maxScore) {
          maxScore = this.scores[archetype.name]
          this.primaryArchetype = archetype.name
        }
      }

      // Find secondary archetypes (>= 70%)
      this.secondaryArchetypes = []
      for (const archetype of this.archetypes) {
        if (archetype.name !== this.primaryArchetype && this.scores[archetype.name] >= 70) {
          this.secondaryArchetypes.push(archetype.name)
        }
      }
      this.secondaryArchetypes.sort((a, b) => this.scores[b] - this.scores[a])
    },
    renderRadarChart() {
      const ctx = document.getElementById('easRadarChart')
      if (!ctx) return

      if (this.radarChart) {
        this.radarChart.destroy()
      }

      const labels = ['Strategist', 'Guardian', 'Innovator', 'Coordinator', 'Analyst', 'Advocate', 'Executor']

      const datasets = [
        {
          label: 'EAS Environment',
          data: labels.map((a) => this.scores[a] || 0),
          borderColor: '#DC2626',
          backgroundColor: 'rgba(220, 38, 38, 0.1)',
          borderWidth: 2,
          pointBackgroundColor: '#DC2626',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: '#DC2626',
        },
      ]

      this.radarChart = new Chart(ctx, {
        type: 'radar',
        data: {
          labels: labels,
          datasets: datasets,
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          scales: {
            r: {
              beginAtZero: true,
              max: 100,
              ticks: {
                stepSize: 20,
              },
            },
          },
          plugins: {
            legend: {
              display: true,
              position: 'top',
            },
          },
        },
      })
    },
    getArchetypeDescription(name) {
      const descriptions = {
        Strategist:
          'Your environment emphasizes pattern recognition, long-term planning, and anticipation of future developments.',
        Guardian:
          'Your environment emphasizes vigilance, risk management, and maintaining safety in uncertain situations.',
        Innovator:
          'Your environment emphasizes experimentation, creativity, and challenging conventional approaches.',
        Coordinator:
          'Your environment emphasizes conflict resolution, organizing groups, and managing interdependencies.',
        Analyst:
          'Your environment emphasizes systematic analysis, logical problem-solving, and data interpretation.',
        Advocate:
          'Your environment emphasizes relationship-building, persuasion, and stakeholder negotiation.',
        Executor:
          'Your environment emphasizes reliable execution, deadline adherence, and consistent delivery under pressure.',
      }
      return descriptions[name] || ''
    },
    resetAssessment() {
      this.currentItem = 0
      this.responses = new Array(20).fill(null)
      this.showResults = false
      this.scores = {}
      this.rawScores = {}
      this.primaryArchetype = ''
      this.secondaryArchetypes = []
    },
    calculateDomainScores() {
      const domainMapping = {
        Strategist: [0, 1, 2],
        Guardian: [3, 4, 5],
        Innovator: [6, 7, 8],
        Coordinator: [9, 10, 11],
        Analyst: [12, 13, 14],
        Advocate: [15, 16, 17],
        Executor: [18, 19],
      }

      const domainScores = {}

      for (const [domain, questionIndices] of Object.entries(domainMapping)) {
        const validResponses = questionIndices
          .map(index => this.responses[index])
          .filter(response => response !== null)

        if (validResponses.length > 0) {
          const average = validResponses.reduce((sum, val) => sum + val, 0) / validResponses.length
          domainScores[domain] = Math.round((average / 5) * 100)
        } else {
          domainScores[domain] = 0
        }
      }

      return domainScores
    },
    downloadResults() {
      const csv = this.generateCSV()
      const blob = new Blob([csv], { type: 'text/csv' })
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'EAS20_Results.csv'
      a.click()
    },
    generateCSV() {
      let csv = 'EAS-20 Assessment Results\n'
      csv += `Assessment Date,${new Date().toLocaleString()}\n`
      csv += `Primary Archetype,${this.primaryArchetype}\n`
      csv += `\nArchetype Scores:\n`
      csv += 'Archetype,Raw Score,Max Score,Percentage\n'
      for (const archetype of this.archetypes) {
        csv += `${archetype.name},${this.rawScores[archetype.name] || 0},${archetype.maxScore},${(this.scores[archetype.name] || 0).toFixed(1)}%\n`
      }
      csv += `\nAll Responses:\n`
      csv += 'Item #,Domain,Question,Rating\n'
      for (let i = 0; i < this.questions.length; i++) {
        csv += `${i + 1},"${this.questions[i].domain}","${this.questions[i].text}",${this.responses[i]}\n`
      }
      return csv
    },
  },
}
</script>

<style scoped>
.eas20-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

.eas20-header {
  text-align: center;
  margin-bottom: 40px;
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.eas20-header h1 {
  margin: 0 0 10px 0;
  color: #1a202c;
  font-size: 28px;
  font-weight: 600;
}

.subtitle {
  color: #718096;
  font-size: 16px;
  margin: 0 0 20px 0;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  margin: 15px 0;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #8b5cf6, #ec4899);
  transition: width 0.3s ease;
}

.progress-text {
  color: #4a5568;
  font-size: 14px;
  margin: 10px 0 0 0;
}

.eas20-main {
  background: white;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.question-section {
  margin-bottom: 40px;
  padding: 30px;
  background: #f7fafc;
  border-left: 4px solid #8b5cf6;
  border-radius: 4px;
}

.question-number {
  display: inline-block;
  font-size: 20px;
  font-weight: 700;
  color: #8b5cf6;
  margin-right: 10px;
}

.question-text {
  font-size: 18px;
  color: #2d3748;
  line-height: 1.6;
  margin: 10px 0;
  font-weight: 500;
}

.rating-scale {
  margin: 40px 0;
}

.scale-instruction {
  font-size: 14px;
  color: #4a5568;
  margin-bottom: 20px;
  font-weight: 500;
}

.rating-options {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.rating-btn {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 70px;
  height: 90px;
  padding: 10px;
  border: 2px solid #cbd5e0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.rating-btn:hover {
  border-color: #8b5cf6;
  background: #f7fafc;
  transform: translateY(-2px);
}

.rating-btn.active {
  border-color: #8b5cf6;
  background: #ede9fe;
  color: #7c3aed;
}

.rating-value {
  font-size: 24px;
  font-weight: 700;
  margin-bottom: 5px;
}

.rating-label {
  font-size: 11px;
  text-align: center;
  line-height: 1.2;
}

.navigation-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin: 40px 0 30px 0;
  flex-wrap: wrap;
}

.btn {
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 600;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
}

.btn-primary {
  background: #8b5cf6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #7c3aed;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
}

.btn-secondary {
  background: #cbd5e0;
  color: #2d3748;
}

.btn-secondary:hover:not(:disabled) {
  background: #a0aec0;
  transform: translateY(-2px);
}

.btn-success {
  background: #10b981;
  color: white;
}

.btn-success:hover:not(:disabled) {
  background: #059669;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
}

.btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.answered-summary {
  text-align: center;
  color: #718096;
  font-size: 14px;
  padding: 15px;
  background: #f7fafc;
  border-radius: 4px;
}

.message {
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
  font-weight: 500;
  margin-top: 1rem;
}

.message.success {
  background: rgba(34, 197, 94, 0.1);
  color: #16a34a;
}

.message.error {
  background: rgba(220, 38, 38, 0.1);
  color: #dc2626;
}

.eas20-results {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

.results-header {
  background: linear-gradient(135deg, #8b5cf6, #ec4899);
  color: white;
  padding: 40px;
  text-align: center;
}

.results-header h2 {
  margin: 0 0 10px 0;
  font-size: 28px;
}

.results-header p {
  margin: 0;
  opacity: 0.95;
  font-size: 16px;
}

.radar-chart-section {
  padding: 40px;
  background: white;
  text-align: center;
}

.radar-chart-section h3 {
  margin: 0 0 20px 0;
  color: #2d3748;
  font-size: 20px;
  font-weight: 600;
}

.radar-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.results-charts {
  padding: 40px;
  background: #f7fafc;
}

.results-charts h3 {
  margin: 0 0 30px 0;
  color: #2d3748;
  font-size: 18px;
  font-weight: 600;
  text-align: center;
}

.archetype-result {
  display: grid;
  grid-template-columns: 120px 1fr 80px;
  gap: 20px;
  align-items: center;
  margin-bottom: 20px;
}

.result-label {
  font-weight: 600;
  color: #2d3748;
  font-size: 14px;
}

.result-bar-container {
  height: 30px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.result-bar {
  height: 100%;
  transition: width 0.6s ease;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding-right: 10px;
  color: white;
  font-weight: 600;
  font-size: 12px;
}

.result-score {
  text-align: right;
  font-weight: 700;
  color: #2d3748;
  font-size: 16px;
  min-width: 60px;
}

.archetype-summary {
  padding: 40px;
  background: white;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
}

.summary-section h3 {
  color: #2d3748;
  margin: 0 0 15px 0;
  font-size: 16px;
}

.primary-archetype {
  font-size: 24px;
  font-weight: 700;
  color: #8b5cf6;
  margin: 0 0 15px 0;
}

.summary-description {
  color: #4a5568;
  line-height: 1.6;
  margin: 0;
  font-size: 14px;
}

.secondary-archetypes p {
  margin: 8px 0;
  color: #4a5568;
  font-size: 14px;
}

.no-secondary {
  color: #a0aec0;
  font-style: italic;
  margin: 0;
}

.raw-data {
  padding: 40px;
  background: #f7fafc;
}

.raw-data h3 {
  margin: 0 0 20px 0;
  color: #2d3748;
  font-size: 16px;
}

.data-table {
  border: 1px solid #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
}

.data-row {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;
  border-bottom: 1px solid #e2e8f0;
}

.data-row.header {
  background: #edf2f7;
  font-weight: 700;
}

.data-row.header .data-cell {
  color: #2d3748;
}

.data-cell {
  padding: 12px;
  color: #4a5568;
  font-size: 13px;
}

.results-actions {
  padding: 30px 40px;
  background: white;
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

.disclaimer {
  padding: 20px 40px 40px 40px;
  background: #fef3c7;
  color: #92400e;
  font-size: 12px;
  border-left: 4px solid #f59e0b;
}

.disclaimer p {
  margin: 0;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .eas20-container {
    padding: 20px 10px;
  }

  .eas20-main {
    padding: 20px;
  }

  .rating-options {
    gap: 8px;
  }

  .rating-btn {
    width: 60px;
    height: 80px;
    font-size: 12px;
  }

  .rating-value {
    font-size: 18px;
  }

  .archetype-result {
    grid-template-columns: 100px 1fr 70px;
    gap: 15px;
  }

  .archetype-summary {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .data-row {
    grid-template-columns: 1fr;
  }

  .data-row.header {
    display: none;
  }
}
</style>