<template>
  <div class="typesync-assessment">
    <div v-if="!assessmentStarted && !showResults" class="landing-page">
      <div class="hero-section">
        <div class="container">
          <h1>Discover Your Work Style</h1>
          <p class="subtitle">Science-based assessment using real workplace scenarios to predict your fit across 15+ roles</p>
          
          <div class="value-props">
            <div class="prop-card">
              <div class="prop-icon">🎯</div>
              <h3>Real Scenarios</h3>
              <p>No generic personality questions. Every scenario mirrors actual work situations you'll face.</p>
            </div>
            <div class="prop-card">
              <div class="prop-icon">📊</div>
              <h3>Role Fit Analysis</h3>
              <p>See your predicted fit across Project Manager, Sales, Engineering, and 12+ other roles.</p>
            </div>
            <div class="prop-card">
              <div class="prop-icon">💡</div>
              <h3>Actionable Insights</h3>
              <p>Understand where you'll thrive, struggle, and how to develop.</p>
            </div>
          </div>

          <div class="assessment-details">
            <span>⏱️ 12-15 minutes</span>
            <span>📝 20 scenarios</span>
            <span>📊 5 dimensions</span>
            <span>🎯 15 role matches</span>
          </div>

          <button @click="startAssessment" class="btn btn-primary btn-lg">Start Assessment</button>
        </div>
      </div>
    </div>

    <div v-if="assessmentStarted && !showResults" class="assessment-container">
      <div class="assessment-header">
        <div class="progress-section">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: progress + '%' }"></div>
          </div>
          <span class="progress-text">Question {{ currentScenarioIndex + 1 }} of 20</span>
        </div>
      </div>

      <div class="scenario-content">
        <div class="scenario-dimension">
          <span class="dimension-badge" :style="{ backgroundColor: getDimensionColor(currentScenario.dimension) }">
            {{ getDimensionIcon(currentScenario.dimension) }} {{ getDimensionName(currentScenario.dimension) }}
          </span>
        </div>

        <div class="scenario-card">
          <p class="scenario-text">{{ currentScenario.scenario }}</p>
          <p class="scenario-question">{{ currentScenario.question }}</p>

          <div class="options-grid">
            <button
              v-for="(option, index) in currentScenario.options"
              :key="index"
              @click="selectAnswer(option.score)"
              class="option-card"
            >
              {{ option.text }}
            </button>
          </div>
        </div>

        <div class="navigation">
          <button 
            v-if="currentScenarioIndex > 0"
            @click="previousScenario"
            class="btn btn-secondary"
          >
            ← Previous
          </button>
          <div class="spacer"></div>
          <button 
            v-if="currentScenarioIndex < 19"
            @click="nextScenario"
            class="btn btn-secondary"
            :disabled="!hasAnsweredCurrent"
          >
            Next →
          </button>
          <button 
            v-else
            @click="completeAssessment"
            class="btn btn-primary"
            :disabled="!hasAnsweredCurrent"
          >
            See Results
          </button>
        </div>
      </div>
    </div>

    <div v-if="showResults" class="results-container">
      <section class="profile-section">
        <h2>Your Work Style Profile</h2>
        <div class="dimensions-grid">
          <div 
            v-for="(dim, key) in dimensions"
            :key="key"
            class="dimension-card"
          >
            <div class="dim-header">
              <span class="dim-icon">{{ dim.icon }}</span>
              <h3>{{ dim.name }}</h3>
            </div>
            <div class="dim-score">{{ scores[key] }}%</div>
            <div class="dim-bar">
              <div class="dim-fill" :style="{ width: scores[key] + '%', backgroundColor: dim.color }"></div>
            </div>
            <p class="dim-desc">{{ getScoreInterpretation(key, scores[key]) }}</p>
          </div>
        </div>
      </section>

      <section class="fit-section">
        <h2>Your Role Fit Analysis</h2>
        
        <div class="fit-grid">
          <div 
            v-for="role in roleFits.slice(0, 5)"
            :key="role.roleKey"
            class="fit-card"
            :class="getFitCategory(role.fit).color"
          >
            <div class="fit-header">
              <h3>{{ role.roleName }}</h3>
              <span class="fit-score">{{ role.fit }}%</span>
            </div>
            <span class="fit-label">{{ getFitCategory(role.fit).label }}</span>
            <p class="fit-explanation">{{ getFitExplanation(role) }}</p>
          </div>
        </div>
      </section>

      <section class="actions-section">
        <button @click="resetAssessment" class="btn btn-secondary">🔄 Retake Assessment</button>
      </section>
    </div>
  </div>
</template>

<script>
import { ref, computed } from 'vue'

const dimensions = {
  drive: { name: 'Drive & Delivery', icon: '🎯', color: '#2563eb' },
  adaptability: { name: 'Adaptability & Innovation', icon: '🚀', color: '#059669' },
  collaboration: { name: 'Collaboration & Influence', icon: '🤝', color: '#dc2626' },
  composure: { name: 'Composure & Resilience', icon: '🛡️', color: '#7c3aed' },
  analysis: { name: 'Analysis & Learning', icon: '🧠', color: '#ea580c' }
}

const scenarios = [
  { id: 1, dimension: 'drive', scenario: "Your project deadline is in 2 weeks. You've completed 60% and new requirements just arrived.", question: 'How likely are you to...', options: [ { text: 'Immediately create a new plan and prioritize ruthlessly', score: 4 }, { text: 'Assess impact and adjust the plan as needed', score: 3 }, { text: 'Present concerns about feasibility to the team', score: 2 }, { text: 'Focus on current tasks and hope it works out', score: 1 } ] },
  { id: 2, dimension: 'drive', scenario: "You notice your colleague is falling behind on their part of the project.", question: 'What do you do?', options: [ { text: 'Step in proactively to help them catch up', score: 4 }, { text: 'Mention it in the next team meeting', score: 3 }, { text: 'Let them figure it out independently', score: 2 }, { text: 'Do nothing unless directly impacted', score: 1 } ] },
  { id: 3, dimension: 'drive', scenario: "You receive critical feedback on your work that stings a bit.", question: 'Your response?', options: [ { text: 'Thank them, dig deep to understand, and fix it immediately', score: 4 }, { text: 'Ask clarifying questions and make improvements', score: 3 }, { text: 'Take it under consideration but move on', score: 2 }, { text: 'Dismiss it or get defensive', score: 1 } ] },
  { id: 4, dimension: 'drive', scenario: "You finish a task early. Your manager hasn't assigned new work yet.", question: 'What do you do?', options: [ { text: 'Identify the next priority and start without being asked', score: 4 }, { text: 'Ask your manager what to work on next', score: 3 }, { text: 'Take a break and wait for direction', score: 2 }, { text: 'Chat with colleagues or scroll social media', score: 1 } ] },
  { id: 5, dimension: 'adaptability', scenario: "Your company announces a major restructuring and role changes are coming.", question: 'Your immediate thought?', options: [ { text: 'This is an opportunity to learn and try new things', score: 4 }, { text: 'It is a change, but I can adapt and make it work', score: 3 }, { text: 'I am a bit concerned about the uncertainty', score: 2 }, { text: 'I am very unsettled by this disruption', score: 1 } ] },
  { id: 6, dimension: 'adaptability', scenario: "A client requests a feature that challenges your current approach completely.", question: 'How do you respond?', options: [ { text: 'Get excited - let us rethink the whole thing', score: 4 }, { text: 'Explore how we could adapt our approach', score: 3 }, { text: 'Explain why our current approach is better', score: 2 }, { text: 'Push back on the request', score: 1 } ] },
  { id: 7, dimension: 'adaptability', scenario: "You are asked to lead a project in an unfamiliar area of business.", question: 'Your reaction?', options: [ { text: 'Absolutely! I love learning new domains', score: 4 }, { text: 'I will do it and pick up what I need along the way', score: 3 }, { text: 'I would prefer someone with experience in this area', score: 2 }, { text: 'I am not comfortable with this', score: 1 } ] },
  { id: 8, dimension: 'adaptability', scenario: "A system you rely on breaks and there is no quick fix available.", question: 'What do you do?', options: [ { text: 'Figure out a creative workaround and innovate', score: 4 }, { text: 'Find alternative solutions and adapt', score: 3 }, { text: 'Wait for IT support to fix it', score: 2 }, { text: 'Get frustrated - this disrupts everything', score: 1 } ] },
  { id: 9, dimension: 'collaboration', scenario: "You need buy-in from skeptical stakeholders for your idea.", question: 'How do you approach this?', options: [ { text: 'Build relationships first, understand their concerns, then present persuasively', score: 4 }, { text: 'Present your idea clearly and address objections', score: 3 }, { text: 'Push the idea and hope it gains traction', score: 2 }, { text: 'Accept their skepticism and move on', score: 1 } ] },
  { id: 10, dimension: 'collaboration', scenario: "There is conflict between two team members affecting project progress.", question: 'Do you?', options: [ { text: 'Step in, help them understand each other, and rebuild the relationship', score: 4 }, { text: 'Talk to both separately and find middle ground', score: 3 }, { text: 'Alert the manager and let them handle it', score: 2 }, { text: 'Stay out of it - it is not your problem', score: 1 } ] },
  { id: 11, dimension: 'collaboration', scenario: "You have a great idea but it requires input from multiple departments.", question: 'What do you do?', options: [ { text: 'Organize a meeting and facilitate cross-team collaboration', score: 4 }, { text: 'Talk to key people from each department', score: 3 }, { text: 'Send a detailed email and hope they respond', score: 2 }, { text: 'Develop it independently as much as possible', score: 1 } ] },
  { id: 12, dimension: 'collaboration', scenario: "A colleague is hesitant about a decision you want to make.", question: 'How do you respond?', options: [ { text: 'Listen deeply, understand their perspective, find a solution together', score: 4 }, { text: 'Explain your reasoning and consider their input', score: 3 }, { text: 'Respectfully disagree and move forward', score: 2 }, { text: 'Proceed without their agreement', score: 1 } ] },
  { id: 13, dimension: 'composure', scenario: "Everything goes wrong on a critical day - multiple systems down, clients upset.", question: 'How do you handle it?', options: [ { text: 'Stay calm, take action, help the team stay focused', score: 4 }, { text: 'Feel stressed but manage it and work through the issues', score: 3 }, { text: 'Feel very overwhelmed but try to push through', score: 2 }, { text: 'Panic or freeze under the pressure', score: 1 } ] },
  { id: 14, dimension: 'composure', scenario: "You make a significant mistake that impacts the team.", question: 'What happens?', options: [ { text: 'Own it immediately, apologize, fix it, and learn from it', score: 4 }, { text: 'Feel bad, acknowledge it, and work on solutions', score: 3 }, { text: 'Feel very ashamed and struggle to move past it', score: 2 }, { text: 'Get defensive or blame external factors', score: 1 } ] },
  { id: 15, dimension: 'composure', scenario: "Your manager criticizes your work publicly in a meeting.", question: 'Your response?', options: [ { text: 'Listen without defensiveness, ask for specific feedback after', score: 4 }, { text: 'Feel embarrassed but accept the feedback', score: 3 }, { text: 'Feel very hurt and struggle the rest of the day', score: 2 }, { text: 'Get angry or emotional in the moment', score: 1 } ] },
  { id: 16, dimension: 'composure', scenario: "You have been working 12-hour days for weeks with no end in sight.", question: 'How do you sustain yourself?', options: [ { text: 'Maintain perspective, take care of myself, find moments of peace', score: 4 }, { text: 'Push through but feel the strain', score: 3 }, { text: 'Feel exhausted and burned out', score: 2 }, { text: 'Feel broken and unable to continue', score: 1 } ] },
  { id: 17, dimension: 'analysis', scenario: "You are given data showing your approach is not working.", question: 'What do you do?', options: [ { text: 'Dig into the data, understand why, redesign the approach', score: 4 }, { text: 'Review the data and make adjustments', score: 3 }, { text: 'Question the validity of the data', score: 2 }, { text: 'Ignore it and continue as planned', score: 1 } ] },
  { id: 18, dimension: 'analysis', scenario: "A complex problem lands on your desk with no obvious solution.", question: 'How do you approach it?', options: [ { text: 'Break it down systematically, research, test hypotheses', score: 4 }, { text: 'Analyze the key factors and work toward solutions', score: 3 }, { text: 'Try obvious fixes and see what sticks', score: 2 }, { text: 'Avoid it or push it to someone else', score: 1 } ] },
  { id: 19, dimension: 'analysis', scenario: "You are in a field that is rapidly evolving with new tools and methods.", question: 'What is your relationship to learning?', options: [ { text: 'Actively study new developments and experiment with them', score: 4 }, { text: 'Keep up with key updates and gradually adopt new methods', score: 3 }, { text: 'Learn when necessary but do not seek it out', score: 2 }, { text: 'Stick with what you know and avoid new complexity', score: 1 } ] },
  { id: 20, dimension: 'analysis', scenario: "You need to make a decision with incomplete information.", question: 'How do you proceed?', options: [ { text: 'Gather what data you can, analyze scenarios, make informed decision', score: 4 }, { text: 'Get available information and make a reasonable call', score: 3 }, { text: 'Make a gut feeling decision', score: 2 }, { text: 'Wait until you have more information', score: 1 } ] }
]

const roleLibrary = {
  project_manager: { name: 'Project Manager', demands: { drive: 85, adaptability: 55, collaboration: 75, composure: 70, analysis: 65 }, critical: ['drive', 'collaboration'] },
  software_engineer: { name: 'Software Engineer', demands: { drive: 70, adaptability: 75, collaboration: 55, composure: 60, analysis: 90 }, critical: ['analysis', 'adaptability'] },
  sales_executive: { name: 'Sales Executive', demands: { drive: 75, adaptability: 70, collaboration: 90, composure: 80, analysis: 55 }, critical: ['collaboration', 'composure'] },
  data_analyst: { name: 'Data Analyst', demands: { drive: 75, adaptability: 60, collaboration: 50, composure: 55, analysis: 95 }, critical: ['analysis', 'drive'] },
  hr_business_partner: { name: 'HR Business Partner', demands: { drive: 70, adaptability: 65, collaboration: 85, composure: 75, analysis: 60 }, critical: ['collaboration', 'composure'] },
  marketing_manager: { name: 'Marketing Manager', demands: { drive: 70, adaptability: 85, collaboration: 75, composure: 65, analysis: 70 }, critical: ['adaptability', 'collaboration'] },
  operations_coordinator: { name: 'Operations Coordinator', demands: { drive: 90, adaptability: 45, collaboration: 65, composure: 70, analysis: 60 }, critical: ['drive', 'composure'] },
  innovation_manager: { name: 'Innovation Manager', demands: { drive: 60, adaptability: 95, collaboration: 80, composure: 70, analysis: 75 }, critical: ['adaptability', 'collaboration'] },
  customer_support: { name: 'Customer Support Specialist', demands: { drive: 65, adaptability: 55, collaboration: 70, composure: 80, analysis: 50 }, critical: ['composure', 'collaboration'] },
  financial_analyst: { name: 'Financial Analyst', demands: { drive: 85, adaptability: 50, collaboration: 55, composure: 65, analysis: 90 }, critical: ['analysis', 'drive'] },
  product_manager: { name: 'Product Manager', demands: { drive: 75, adaptability: 80, collaboration: 85, composure: 75, analysis: 80 }, critical: ['collaboration', 'analysis'] },
  executive_assistant: { name: 'Executive Assistant', demands: { drive: 90, adaptability: 65, collaboration: 70, composure: 85, analysis: 55 }, critical: ['drive', 'composure'] },
  ux_designer: { name: 'UX Designer', demands: { drive: 70, adaptability: 90, collaboration: 75, composure: 65, analysis: 70 }, critical: ['adaptability', 'collaboration'] },
  qa_specialist: { name: 'Quality Assurance Specialist', demands: { drive: 90, adaptability: 45, collaboration: 60, composure: 70, analysis: 75 }, critical: ['analysis', 'drive'] },
  change_consultant: { name: 'Change Management Consultant', demands: { drive: 70, adaptability: 85, collaboration: 90, composure: 80, analysis: 75 }, critical: ['collaboration', 'adaptability'] }
}

export default {
  name: 'TypeSyncSecret',
  setup() {
    const responses = ref([])
    const currentScenarioIndex = ref(0)
    const scores = ref({})
    const roleFits = ref([])
    const assessmentStarted = ref(false)
    const showResults = ref(false)

    const currentScenario = computed(() => scenarios[currentScenarioIndex.value] || {})
    const progress = computed(() => ((currentScenarioIndex.value + 1) / scenarios.length) * 100)
    const hasAnsweredCurrent = computed(() => responses.value.some(r => r.scenarioId === currentScenario.value.id))

    const selectAnswer = (score) => {
      const existingIndex = responses.value.findIndex(r => r.scenarioId === currentScenario.value.id)
      if (existingIndex >= 0) {
        responses.value[existingIndex].score = score
      } else {
        responses.value.push({ scenarioId: currentScenario.value.id, score })
      }
    }

    const nextScenario = () => {
      if (currentScenarioIndex.value < scenarios.length - 1) {
        currentScenarioIndex.value++
      }
    }

    const previousScenario = () => {
      if (currentScenarioIndex.value > 0) {
        currentScenarioIndex.value--
      }
    }

    const calculateScores = () => {
      const dimensionScores = {}
      Object.keys(dimensions).forEach(dim => {
        const dimScenarios = scenarios.filter(s => s.dimension === dim)
        const dimResponses = responses.value.filter(r => dimScenarios.some(s => s.id === r.scenarioId))
        const average = dimResponses.reduce((sum, r) => sum + r.score, 0) / dimResponses.length
        dimensionScores[dim] = Math.round(average * 25)
      })
      scores.value = dimensionScores
      calculateRoleFits()
    }

    const calculateRoleFits = () => {
      const fits = Object.entries(roleLibrary).map(([key, role]) => {
        let totalFit = 0, totalWeight = 0
        Object.keys(dimensions).forEach(dim => {
          const personScore = scores.value[dim] || 0
          const roleScore = role.demands[dim] || 0
          const fit = Math.max(0, 100 - Math.abs(personScore - roleScore))
          const weight = role.critical.includes(dim) ? 1.5 : 1.0
          totalFit += fit * weight
          totalWeight += weight
        })
        return { roleKey: key, roleName: role.name, fit: Math.round(totalFit / totalWeight), critical: role.critical }
      })
      roleFits.value = fits.sort((a, b) => b.fit - a.fit)
    }

    const completeAssessment = () => {
      calculateScores()
      showResults.value = true
      assessmentStarted.value = false
    }

    const resetAssessment = () => {
      responses.value = []
      currentScenarioIndex.value = 0
      scores.value = {}
      roleFits.value = []
      assessmentStarted.value = false
      showResults.value = false
    }

    const startAssessment = () => {
      assessmentStarted.value = true
    }

    const getDimensionName = (key) => dimensions[key]?.name || ''
    const getDimensionIcon = (key) => dimensions[key]?.icon || ''
    const getDimensionColor = (key) => dimensions[key]?.color || '#666'
    
    const getScoreInterpretation = (key, score) => {
      if (score >= 80) return 'Exceptional strength'
      if (score >= 60) return 'Strong capability'
      if (score >= 40) return 'Balanced approach'
      return 'Development opportunity'
    }

    const getFitExplanation = (role) => {
      const fit = role.fit
      if (fit >= 85) return 'Strong alignment. You would thrive in this role.'
      if (fit >= 70) return 'Good match. Consider developing skills.'
      if (fit >= 55) return 'Mixed alignment.'
      return 'Limited alignment.'
    }

    const getFitCategory = (fit) => {
      if (fit >= 85) return { label: 'Excellent Fit', color: 'green' }
      if (fit >= 70) return { label: 'Good Fit', color: 'amber' }
      if (fit >= 55) return { label: 'Moderate Fit', color: 'orange' }
      return { label: 'Limited Fit', color: 'red' }
    }

    return { 
      scenarios, dimensions, responses, currentScenarioIndex, currentScenario, scores, roleFits, 
      assessmentStarted, showResults, hasAnsweredCurrent, progress, selectAnswer, nextScenario, 
      previousScenario, completeAssessment, startAssessment, resetAssessment, getDimensionName, 
      getDimensionIcon, getDimensionColor, getScoreInterpretation, getFitExplanation, getFitCategory 
    }
  }
}
</script>

<style scoped>
.typesync-assessment { width: 100%; min-height: 100vh; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem 0; }
.container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; width: 100%; }
.landing-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; }
.hero-section { text-align: center; color: white; }
.hero-section h1 { font-size: 3.5rem; font-weight: 800; margin-bottom: 1rem; line-height: 1.2; }
.subtitle { font-size: 1.5rem; margin-bottom: 3rem; opacity: 0.9; max-width: 600px; margin-left: auto; margin-right: auto; }
.value-props { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; margin-bottom: 3rem; }
.prop-card { background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); padding: 2rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.2); }
.prop-icon { font-size: 3rem; margin-bottom: 1rem; }
.prop-card h3 { font-size: 1.3rem; margin-bottom: 0.5rem; }
.assessment-details { display: flex; justify-content: center; gap: 3rem; margin-bottom: 3rem; font-size: 1.1rem; }
.btn { padding: 12px 28px; border: none; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: all 0.3s ease; }
.btn-primary { background: white; color: #667eea; }
.btn-primary:hover { transform: scale(1.05); }
.btn-secondary { background: rgba(255, 255, 255, 0.2); color: white; border: 1px solid rgba(255, 255, 255, 0.3); }
.btn-lg { padding: 16px 40px; font-size: 1.2rem; }
.assessment-container { max-width: 900px; margin: 0 auto; background: white; border-radius: 16px; padding: 3rem; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2); min-height: 80vh; display: flex; flex-direction: column; }
.progress-bar { width: 100%; height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden; margin-bottom: 1rem; }
.progress-fill { height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); transition: width 0.3s ease; }
.progress-text { display: block; text-align: center; color: #666; font-size: 0.9rem; }
.scenario-card { background: #f9fafb; padding: 2rem; border-radius: 12px; margin-bottom: 2rem; border-left: 4px solid #667eea; }
.scenario-text { font-size: 1.2rem; font-weight: 600; margin-bottom: 1rem; color: #1f2937; line-height: 1.6; }
.options-grid { display: grid; gap: 1rem; }
.option-card { padding: 1rem; border: 2px solid #e5e7eb; border-radius: 8px; background: white; text-align: left; cursor: pointer; transition: all 0.3s ease; font-size: 0.95rem; }
.option-card:hover { border-color: #667eea; background: #f0f4ff; }
.navigation { display: flex; justify-content: space-between; gap: 1rem; margin-top: 3rem; }
.spacer { flex: 1; }
.results-container { max-width: 1000px; margin: 0 auto; background: white; border-radius: 16px; padding: 3rem; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2); }
.results-container section { margin-bottom: 3rem; }
.results-container h2 { font-size: 2rem; margin-bottom: 2rem; color: #1f2937; }
.dimensions-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 2rem; }
.dimension-card { padding: 1.5rem; border: 2px solid #e5e7eb; border-radius: 12px; }
.dim-header { display: flex; align-items: center; gap: 1rem; margin-bottom: 1rem; }
.dim-icon { font-size: 2rem; }
.dim-header h3 { font-size: 1rem; color: #1f2937; }
.dim-score { font-size: 2rem; font-weight: 800; color: #667eea; margin-bottom: 0.5rem; }
.dim-bar { width: 100%; height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden; margin-bottom: 1rem; }
.dim-fill { height: 100%; transition: width 0.5s ease; }
.fit-grid { display: grid; gap: 2rem; }
.fit-card { padding: 2rem; border: 2px solid #e5e7eb; border-radius: 12px; transition: all 0.3s ease; }
.fit-card.green { border-color: #10b981; background: #f0fdf4; }
.fit-card.amber { border-color: #f59e0b; background: #fffbf0; }
.fit-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; }
.fit-header h3 { font-size: 1.3rem; color: #1f2937; }
.fit-score { font-size: 1.5rem; font-weight: 800; color: #667eea; }
.fit-label { display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 0.8rem; font-weight: 600; margin-bottom: 1rem; background: rgba(102, 126, 234, 0.1); color: #667eea; }
.fit-explanation { color: #666; line-height: 1.6; }
.actions-section { display: flex; gap: 1rem; justify-content: center; padding-top: 2rem; border-top: 2px solid #e5e7eb; }
.dimension-badge { display: inline-block; padding: 8px 16px; border-radius: 20px; color: white; font-weight: 600; font-size: 0.9rem; }
.scenario-question { color: #666; margin-bottom: 2rem; font-style: italic; }
@media (max-width: 768px) {
  .hero-section h1 { font-size: 2rem; }
  .assessment-container { padding: 1.5rem; }
}
</style>
