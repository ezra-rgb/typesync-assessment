<template>
  <div class="landing-page">
    <section class="hero">
      <div class="container">
        <h1>Discover Your Professional Archetype</h1>
        <p class="subtitle">
          Research-backed assessments to understand your work style and environmental demands
        </p>
      </div>
    </section>

    <section class="assessments">
      <div class="container">
        <div class="assessment-grid">
          <!-- AAS Card -->
          <div class="assessment-card">
            <div class="card-icon">🧠</div>
            <h2>AAS</h2>
            <p class="card-subtitle">Archetype Assessment Scale</p>
            <p class="card-description">
              Discover your natural professional profile and strengths across 7 core archetypes 
              that define workplace behavior and performance.
            </p>
            <ul class="card-features">
              <li>Scenario-based evaluation</li>
              <li>7 professional archetypes</li>
              <li>Personal profile insights</li>
              <li>Instant results visualization</li>
            </ul>
            <router-link to="/aas" class="btn-primary">
              Take AAS Assessment
            </router-link>
            <p class="card-time">⏱ ~8 minutes</p>
          </div>

          <!-- EAS-20 Card -->
          <div class="assessment-card">
            <div class="card-icon">🎯</div>
            <h2>EAS-20</h2>
            <p class="card-subtitle">Environmental Assessment Scale</p>
            <p class="card-description">
              Understand the demands and expectations of your work environment 
              across 7 key professional archetypes and contexts.
            </p>
            <ul class="card-features">
              <li>20 scenario-based questions</li>
              <li>Environmental demand mapping</li>
              <li>Context-specific insights</li>
              <li>Comprehensive results report</li>
            </ul>
            <router-link to="/eas20" class="btn-secondary">
              Take EAS-20 Assessment
            </router-link>
            <p class="card-time">⏱ ~10 minutes</p>
          </div>
        </div>
      </div>
    </section>

    <section class="archetypes-preview">
      <div class="container">
        <h2>The 7 Professional Archetypes</h2>
        <div class="archetypes-grid">
          <div class="archetype-item">
            <h3>Strategist</h3>
            <p>Long-term vision and pattern recognition</p>
          </div>
          <div class="archetype-item">
            <h3>Guardian</h3>
            <p>Risk management and quality assurance</p>
          </div>
          <div class="archetype-item">
            <h3>Innovator</h3>
            <p>Creative thinking and experimentation</p>
          </div>
          <div class="archetype-item">
            <h3>Coordinator</h3>
            <p>Team harmony and collaboration</p>
          </div>
          <div class="archetype-item">
            <h3>Analyst</h3>
            <p>Data-driven decision making</p>
          </div>
          <div class="archetype-item">
            <h3>Advocate</h3>
            <p>Communication and influence</p>
          </div>
          <div class="archetype-item">
            <h3>Executor</h3>
            <p>Task completion and delivery</p>
          </div>
        </div>
      </div>
    </section>

    <section class="info-section">
      <div class="container">
        <h2>How It Works</h2>
        <div class="steps">
          <div class="step">
            <div class="step-number">1</div>
            <h3>Take an Assessment</h3>
            <p>Choose EAS-20 or AAS and answer scenario-based questions</p>
          </div>
          <div class="step">
            <div class="step-number">2</div>
            <h3>Get Results</h3>
            <p>Instantly receive your archetype profile with radar visualization</p>
          </div>
          <div class="step">
            <div class="step-number">3</div>
            <h3>Share & Download</h3>
            <p>Get a shareable link and download your results as PDF or CSV</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'Home',
  data() {
    return {}
  }
}
</script>

<style scoped>
.landing-page {
  background: white;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Hero Section */
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4rem 0;
  text-align: center;
}

.hero h1 {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.subtitle {
  font-size: 1.1rem;
  opacity: 0.95;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* Assessments Grid */
.assessments {
  padding: 4rem 0;
  background: #f8f9fa;
}

.assessment-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.assessment-card {
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
}

.assessment-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}

.card-icon {
  font-size: 3.5rem;
  margin-bottom: 1rem;
  display: inline-block;
}

.assessment-card h2 {
  font-size: 1.8rem;
  color: #667eea;
  margin-bottom: 0.5rem;
  font-weight: 700;
}

.card-subtitle {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1rem;
  font-weight: 500;
}

.card-description {
  color: #555;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  flex-grow: 1;
  font-size: 0.95rem;
}

.card-features {
  list-style: none;
  padding: 0;
  margin-bottom: 1.5rem;
}

.card-features li {
  padding: 0.5rem 0 0.5rem 1.5rem;
  position: relative;
  color: #555;
  font-size: 0.9rem;
}

.card-features li::before {
  content: "✓";
  position: absolute;
  left: 0;
  color: #667eea;
  font-weight: bold;
  font-size: 1.1rem;
}

.btn-primary,
.btn-secondary {
  display: inline-block;
  padding: 0.9rem 2rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  text-align: center;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  font-size: 0.95rem;
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
  border-color: #667eea;
}

.card-time {
  margin-top: 1rem;
  font-size: 0.85rem;
  color: #999;
  text-align: center;
}

/* Archetypes Section */
.archetypes-preview {
  padding: 4rem 0;
  background: white;
}

.archetypes-preview h2 {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2.5rem;
  color: #333;
  font-weight: 700;
}

.archetypes-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 1.5rem;
}

.archetype-item {
  background: linear-gradient(135deg, #f0f3ff 0%, #e9ecef 100%);
  padding: 1.5rem;
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s ease;
  border-left: 4px solid #667eea;
}

.archetype-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
}

.archetype-item h3 {
  color: #667eea;
  margin-bottom: 0.5rem;
  font-size: 1rem;
  font-weight: 700;
}

.archetype-item p {
  font-size: 0.85rem;
  color: #666;
  line-height: 1.5;
}

/* Info Section */
.info-section {
  padding: 4rem 0;
  background: #f8f9fa;
}

.info-section h2 {
  text-align: center;
  font-size: 2rem;
  margin-bottom: 2.5rem;
  color: #333;
  font-weight: 700;
}

.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.step {
  text-align: center;
  padding: 1.5rem;
}

.step-number {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-radius: 50%;
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.step h3 {
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 1.1rem;
  font-weight: 700;
}

.step p {
  color: #666;
  line-height: 1.6;
  font-size: 0.95rem;
}

/* Responsive */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 1.8rem;
  }

  .subtitle {
    font-size: 1rem;
  }

  .assessment-grid {
    grid-template-columns: 1fr;
  }

  .archetypes-grid {
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  }

  .assessment-card h2 {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .hero {
    padding: 2rem 0;
  }

  .hero h1 {
    font-size: 1.5rem;
  }

  .assessments {
    padding: 2rem 0;
  }

  .archetypes-preview,
  .info-section {
    padding: 2rem 0;
  }

  .archetype-item {
    padding: 1rem;
  }
}
</style>