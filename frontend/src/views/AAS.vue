<template>
  <div class="aas-page">
    <div class="assessment-container" ref="container">
      <div class="progress-bar">
        <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
      </div>

      <h1>Workplace Alignment Assessment</h1>
      <p class="description">For each scenario, rate how much each response resonates with you.</p>
      <p class="progress-text">Question {{ currentQuestion + 1 }} of {{ scenarios.length }}</p>

      <form @submit.prevent="handleNext">
        <div class="scenario-card">
          <h3>Scenario {{ currentQuestion + 1 }}</h3>
          <p class="scenario-text">{{ scenarios[currentQuestion].description }}</p>
          <p class="instruction">Rate each response on the scale below:</p>

          <div class="options-container">
            <div
              v-for="(option, optionIdx) in scenarios[currentQuestion].options"
              :key="optionIdx"
              class="option-with-scale"
            >
              <p class="option-text">{{ optionIdx + 1 }}. {{ option }}</p>

              <div class="likert-scale">
                <label
                  v-for="score in [1, 2, 3, 4, 5]"
                  :key="score"
                  class="scale-item"
                >
                  <input
                    type="radio"
                    :name="`scenario_${currentQuestion}_option_${optionIdx}`"
                    :value="score"
                    v-model="responses[currentQuestion][optionIdx]"
                    required
                  />
                  <span class="score-label">{{ scoreLabels[score - 1] }}</span>
                </label>
              </div>
            </div>
          </div>
        </div>

        <div class="button-group">
          <button
            v-if="currentQuestion > 0"
            type="button"
            @click="previousQuestion"
            class="btn btn-secondary"
          >
            ← Previous
          </button>

          <button
            type="submit"
            :class="['btn', 'btn-primary', { 'btn-submit': currentQuestion === scenarios.length - 1 }]"
            :disabled="!isCurrentQuestionComplete"
          >
            {{ currentQuestion === scenarios.length - 1 ? 'Submit Assessment' : 'Next →' }}
          </button>
        </div>

        <p v-if="message" :class="['message', messageType]">
          {{ message }}
        </p>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const container = ref(null)
const currentQuestion = ref(0)
const responses = ref({})
const loading = ref(false)
const message = ref('')
const messageType = ref('success')

const scoreLabels = [
  'Strongly Disagree',
  'Disagree',
  'Neutral',
  'Agree',
  'Strongly Agree'
]

const scenarios = [
  {
    description: 'Your team faces a complex problem with multiple competing priorities. You tend to:',
    options: [
      'Step back and look for underlying patterns others might miss',
      'Document risks and create contingency plans',
      'Challenge assumptions and explore unconventional solutions',
      'Bring stakeholders together to build consensus',
      'Break it down into measurable components and analyze data',
      'Rally the team around a compelling vision for change',
      'Focus on execution and delivering quick results'
    ]
  },
  {
    description: 'When implementing change in your organization, your natural inclination is to:',
    options: [
      'Anticipate how it will ripple through the system',
      'Ensure stability during the transition period',
      'Question if this is the best way to do it',
      'Facilitate buy-in from different departments',
      'Measure impact through metrics and outcomes',
      'Inspire people about the possibilities ahead',
      'Get it done on schedule and within budget'
    ]
  },
  {
    description: 'In meetings, you are most likely to:',
    options: [
      'Connect dots between different ideas and perspectives',
      'Point out potential problems before they happen',
      'Suggest a completely new direction',
      'Make sure everyone\'s voice is heard',
      'Ask for evidence and request detailed analysis',
      'Paint a picture of where you\'re headed',
      'Keep discussion focused and move toward decisions'
    ]
  },
  {
    description: 'When facing uncertainty, you prefer to:',
    options: [
      'Model scenarios to understand possible futures',
      'Follow established procedures and best practices',
      'Experiment and learn by doing',
      'Seek input from diverse perspectives',
      'Gather more information and data',
      'Trust your instincts and conviction',
      'Move forward with a clear action plan'
    ]
  },
  {
    description: 'Your colleagues would say you are best at:',
    options: [
      'Seeing the big picture and long-term implications',
      'Preventing problems and maintaining standards',
      'Pushing boundaries and challenging the status quo',
      'Getting people to work together effectively',
      'Understanding the "why" behind decisions',
      'Motivating others toward ambitious goals',
      'Making things happen and getting results'
    ]
  },
  {
    description: 'When a project hits an obstacle, you typically:',
    options: [
      'Review what led to this point and adjust strategy',
      'Create a detailed mitigation plan',
      'See it as an opportunity to try something different',
      'Involve the team in finding the solution',
      'Analyze root causes systematically',
      'Find a way to turn it into a positive message',
      'Quickly solve it and keep moving forward'
    ]
  },
  {
    description: 'Your approach to building organizational culture is to:',
    options: [
      'Establish systems that support long-term resilience',
      'Maintain consistency and reinforce core values',
      'Challenge people to grow and evolve',
      'Create psychological safety and belonging',
      'Build trust through transparency and facts',
      'Articulate an inspiring future worth working toward',
      'Set clear expectations and hold people accountable'
    ]
  },
  {
    description: 'When mentoring others, you focus on helping them:',
    options: [
      'Think strategically and see connections',
      'Manage risks and make sound decisions',
      'Push their limits and try new approaches',
      'Develop strong relationships and influence',
      'Think analytically and solve problems',
      'Find their voice and lead authentically',
      'Build skills and deliver excellence'
    ]
  },
  {
    description: 'In your organization, you are known for:',
    options: [
      'Strategic foresight and pattern recognition',
      'Stability and reliability',
      'Disruptive innovation and creativity',
      'Collaboration and consensus building',
      'Rigorous thinking and attention to detail',
      'Passion and inspirational leadership',
      'Productivity and reliable delivery'
    ]
  },
  {
    description: 'When resources are limited, you prefer to:',
    options: [
      'Make choices that optimize long-term value',
      'Protect core functions and critical operations',
      'Invest in experimental initiatives',
      'Ensure all stakeholders feel valued',
      'Direct resources where data shows they\'ll have the most impact',
      'Find creative ways to inspire with less',
      'Maximize efficiency and output per resource'
    ]
  },
  {
    description: 'Your communication style is typically:',
    options: [
      'Thought-provoking and systemic',
      'Clear, direct, and reassuring',
      'Bold and challenging',
      'Inclusive and dialogue-based',
      'Precise and evidence-based',
      'Compelling and emotionally resonant',
      'Practical and results-focused'
    ]
  },
  {
    description: 'When facing ethical dilemmas, you tend to:',
    options: [
      'Consider systemic consequences and precedent',
      'Refer to established guidelines and procedures',
      'Question conventional wisdom on what\'s right',
      'Seek consensus on the right path forward',
      'Analyze all angles and relevant data',
      'Make the bold choice you believe in',
      'Find pragmatic solutions quickly'
    ]
  },
  {
    description: 'Your natural environment for doing your best work is:',
    options: [
      'Strategic planning and systems thinking',
      'Structured environments with clear processes',
      'Experimental labs and innovation spaces',
      'Collaborative teams and open forums',
      'Data centers and analytical environments',
      'Thought leadership and public visibility',
      'Fast-paced operations and deadline-driven projects'
    ]
  },
  {
    description: 'When learning something new, you prefer to:',
    options: [
      'Understand the frameworks and interconnections',
      'Master the fundamentals and best practices',
      'Challenge conventional approaches',
      'Learn alongside others and discuss',
      'Study case studies and deep-dive analysis',
      'Connect to a larger purpose and vision',
      'Get hands-on experience and apply it quickly'
    ]
  },
  {
    description: 'Your greatest professional satisfaction comes from:',
    options: [
      'Solving complex, multi-layered problems',
      'Protecting what matters and reducing risk',
      'Creating something that didn\'t exist before',
      'Building strong relationships and trust',
      'Understanding how things truly work',
      'Making a meaningful difference in people\'s lives',
      'Achieving ambitious goals and targets'
    ]
  },
  {
    description: 'In conflict situations, you typically:',
    options: [
      'Look for underlying interests and systemic issues',
      'Seek compromise that preserves stability',
      'Take a principled stance on what you believe',
      'Work to find common ground and understanding',
      'Present objective facts and analysis',
      'Appeal to shared values and vision',
      'Push for quick resolution and moving on'
    ]
  },
  {
    description: 'Your ideal role would involve:',
    options: [
      'Strategy, foresight, and systems design',
      'Risk management and compliance',
      'Research and development',
      'Stakeholder engagement and partnerships',
      'Research, analysis, and insight',
      'Vision setting and culture building',
      'Execution, operations, and delivery'
    ]
  },
  {
    description: 'When presenting to leadership, you emphasize:',
    options: [
      'Strategic implications and long-term value',
      'Risk mitigation and contingency planning',
      'Innovation potential and competitive advantage',
      'Stakeholder alignment and buy-in',
      'Data, evidence, and analytical rigor',
      'Transformational impact and purpose',
      'Results, timelines, and deliverables'
    ]
  },
  {
    description: 'Your approach to professional development is:',
    options: [
      'Building diverse expertise across domains',
      'Deepening expertise and technical mastery',
      'Staying at the leading edge of innovation',
      'Developing leadership and interpersonal skills',
      'Advancing analytical and research capabilities',
      'Enhancing communication and influence',
      'Improving efficiency and execution excellence'
    ]
  },
  {
    description: 'When evaluating organizational performance, you focus on:',
    options: [
      'Strategic alignment and long-term sustainability',
      'Operational stability and risk levels',
      'Innovation rate and market disruption',
      'Employee engagement and retention',
      'Process efficiency and quality metrics',
      'Cultural health and employee fulfillment',
      'Revenue, profit, and goal achievement'
    ]
  },
  {
    description: 'Your role in organizational decision-making is often to:',
    options: [
      'Provide strategic perspective and foresight',
      'Ensure risks are identified and managed',
      'Challenge assumptions and suggest alternatives',
      'Build coalition and collaborative support',
      'Provide rigorous analysis and evidence',
      'Inspire commitment and galvanize action',
      'Execute the decision and achieve results'
    ]
  }
]

// Initialize responses structure
const initializeResponses = () => {
  for (let i = 0; i < scenarios.length; i++) {
    if (!responses.value[i]) {
      responses.value[i] = {}
      for (let j = 0; j < 7; j++) {
        responses.value[i][j] = undefined
      }
    }
  }
}

initializeResponses()

const progressPercent = computed(() => {
  return ((currentQuestion.value + 1) / scenarios.length) * 100
})

const isCurrentQuestionComplete = computed(() => {
  const currentResponses = responses.value[currentQuestion.value]
  if (!currentResponses) return false
  return Object.values(currentResponses).every(val => val !== undefined && val !== '')
})

// Auto-scroll to top when question changes
const scrollToTop = async () => {
  await nextTick()
  if (container.value) {
    container.value.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

const previousQuestion = () => {
  if (currentQuestion.value > 0) {
    currentQuestion.value--
    scrollToTop()
  }
}

const handleNext = async () => {
  if (currentQuestion.value < scenarios.length - 1) {
    currentQuestion.value++
    scrollToTop()
  } else {
    await submitAssessment()
  }
}

const submitAssessment = async () => {
  try {
    loading.value = true

    // Build flat responses array and calculate archetype scores
    const flatResponses = []
    const archetypeScores = [0, 0, 0, 0, 0, 0, 0]

    for (let scenario = 0; scenario < scenarios.length; scenario++) {
      const scenarioResponses = responses.value[scenario]
      for (let option = 0; option < 7; option++) {
        const score = parseInt(scenarioResponses[option]) || 0
        flatResponses.push(score)
        archetypeScores[option] += score
      }
    }

    // Send payload WITHOUT assessment_id - backend will generate it
    const payload = {
      responses: flatResponses,
      scores: {
        Strategist: archetypeScores[0],
        Guardian: archetypeScores[1],
        Innovator: archetypeScores[2],
        Coordinator: archetypeScores[3],
        Analyst: archetypeScores[4],
        Advocate: archetypeScores[5],
        Executor: archetypeScores[6]
      }
    }

    console.log('Submitting AAS assessment:', payload)

    // Use relative URL - vite proxy handles it
    const response = await axios.post('/api/assessments/aas/submit', payload)

    if (response.data?.success && response.data?.assessment_id) {
      const assessmentId = response.data.assessment_id
      
      message.value = 'Assessment submitted successfully!'
      messageType.value = 'success'

      // Navigate to results with the backend-generated ID
      setTimeout(() => {
        router.push(`/results/${assessmentId}`)
      }, 1000)
    } else {
      throw new Error('Invalid response format')
    }
  } catch (error) {
    console.error('Assessment error:', error)
    message.value = error.message || 'Failed to submit assessment'
    messageType.value = 'error'
    scrollToTop()
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.aas-page {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem 1rem;
}

.assessment-container {
  background: white;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
  max-width: 800px;
  width: 100%;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 10px;
  margin-bottom: 2rem;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  transition: width 0.3s ease;
  border-radius: 10px;
}

h1 {
  color: #2d3748;
  margin-bottom: 0.5rem;
  font-size: 1.8em;
  text-align: center;
}

.description {
  color: #718096;
  text-align: center;
  margin-bottom: 0.5rem;
  font-size: 1rem;
}

.progress-text {
  color: #a0aec0;
  text-align: center;
  font-size: 0.9rem;
  margin-bottom: 2rem;
  font-weight: 500;
}

form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.scenario-card {
  background: #f7fafc;
  padding: 2rem;
  border-radius: 12px;
  border: 2px solid #e2e8f0;
  transition: all 0.3s ease;
}

.scenario-card:hover {
  border-color: #667eea;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
}

.scenario-card h3 {
  color: #667eea;
  margin-bottom: 0.5rem;
  font-size: 1.1em;
  font-weight: 600;
}

.scenario-text {
  color: #2d3748;
  margin-bottom: 1rem;
  font-size: 1.05em;
  line-height: 1.6;
  font-weight: 500;
}

.instruction {
  color: #718096;
  font-size: 0.9em;
  margin-bottom: 1.5rem;
  font-style: italic;
}

.options-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.option-with-scale {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  transition: all 0.2s ease;
}

.option-with-scale:hover {
  border-color: #667eea;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.08);
}

.option-text {
  color: #2d3748;
  margin-bottom: 1rem;
  font-weight: 500;
  font-size: 0.95em;
  line-height: 1.5;
}

.likert-scale {
  display: flex;
  justify-content: space-between;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.scale-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  transition: all 0.2s ease;
  flex: 1;
  min-width: 70px;
}

.scale-item:hover {
  background: rgba(102, 126, 234, 0.08);
}

.scale-item input[type='radio'] {
  cursor: pointer;
  width: 20px;
  height: 20px;
  accent-color: #667eea;
  margin: 0;
}

.scale-item input[type='radio']:checked {
  accent-color: #764ba2;
}

.score-label {
  font-size: 0.75rem;
  color: #4a5568;
  text-align: center;
  font-weight: 500;
  transition: all 0.2s ease;
  line-height: 1.2;
}

.scale-item input[type='radio']:checked ~ .score-label {
  color: #667eea;
  font-weight: 700;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: space-between;
  margin-top: 2rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  max-width: 200px;
}

.btn-primary {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #e2e8f0;
  color: #2d3748;
}

.btn-secondary:hover {
  background: #cbd5e0;
  transform: translateY(-2px);
}

.btn-submit {
  max-width: unset;
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

@media (max-width: 768px) {
  .assessment-container {
    padding: 1.5rem;
  }

  h1 {
    font-size: 1.5em;
  }

  .scenario-card {
    padding: 1.5rem;
  }

  .button-group {
    flex-direction: column-reverse;
  }

  .btn {
    max-width: unset;
  }

  .likert-scale {
    gap: 0.25rem;
  }

  .scale-item {
    min-width: 50px;
    padding: 0.25rem;
  }

  .score-label {
    font-size: 0.65rem;
  }
}
</style>