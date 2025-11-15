<template>
  <div class="intro-page">
    <!-- Hero Section -->
    <div class="hero">
      <div class="container">
        
        <h1>👋 Welcome to the TypeSync Pilot Programme</h1>
        
        <div class="content-section">
          <p class="intro-text">
            We're TypeSync, and we're on a mission to revolutionise how people find work that actually fits them not just on paper, but in reality.
          </p>
          
          <p class="intro-text">
            Right now, we're building something pretty special: a science backed assessment named the <strong>Environmental Model of Performance (EMP)</strong>. More to come on this later but in a nutshell, we are using social cognitive theory and environmental analysis to predict how well you'll thrive in different environments or roles.
          </p>
          
          <p class="intro-text">
            Think of it as your personal career GPS, built on rigorous behavioural science.
          </p>
        </div>
      </div>
    </div>

    <!-- What You're About to Try -->
    <div class="section what-section">
      <div class="container">
        <h2>🎮 What You're About to Try (and Why It Matters)</h2>
        
        <p class="section-text">
          The test you are about to take allows us to understand the relationship your job has with your strengths under pressure. This is just for fun, but it's also real science that helps us show how you naturally respond to different workplace stressors. If this theory works (and we believe it will), it could transform how organisations build teams and how people find roles that truly fit.
        </p>
        
        <p class="section-text">
          You'll answer 20 real-world scenario questions. No abstract personality confusion, just real world questions about real 'work' scenarios that reveal how you actually respond under pressure.
        </p>
      </div>
    </div>

    <!-- How to Get Best Results -->
    <div class="section tips-section">
      <div class="container">
        <h2>✨ How to Get the Best Results</h2>
        
        <ul class="tips-list">
          <li><strong>Be honest, not aspirational.</strong> Choose what you'd <em>actually</em> do, not what sounds impressive. The key is understanding your true responses.</li>
          <li><strong>Go with your gut.</strong> Your first instinct is usually the truest.</li>
          <li><strong>Take your time.</strong> This isn't a race, quality and understanding beats speed.</li>
          <li><strong>Enjoy the process!</strong> You're helping us build something groundbreaking (and you'll get cool insights about yourself).</li>
        </ul>
      </div>
    </div>

    <!-- Data Privacy -->
    <div class="section privacy-section">
      <div class="container">
        <h2>🔒 About Your Data</h2>
        
        <p class="section-text">
          No personal data is collected during the test. The only thing we know is your answers and an assessment ID. As we do not store any identifying information, it is important you <strong>take a screenshot or download your test results</strong> via PDF or CSV at the end. The assessment ID you are given allows us to identify and delete your test data if you ever require it.
        </p>
      </div>
    </div>

    <!-- CTA Button -->
    <div class="cta-section">
      <div class="container">
        <router-link to="/home" class="btn btn-primary btn-lg">
          Let's Go! Enter TypeSync →
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Intro'
}
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

.intro-page {
  width: 100%;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
  width: 100%;
}

/* Hero Section */
.hero {
  padding: 4rem 0;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.logo {
  max-width: 280px;
  height: auto;
  margin-bottom: 2rem;
  display: block;
}

.hero h1 {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 2rem;
  line-height: 1.3;
}

.content-section {
  max-width: 700px;
  margin: 0 auto;
}

.intro-text {
  font-size: 1.1rem;
  line-height: 1.8;
  margin-bottom: 1.5rem;
  opacity: 0.95;
}

/* Content Sections */
.section {
  padding: 3rem 0;
  background: white;
  border-bottom: 1px solid #e5e7eb;
}

.section h2 {
  font-size: 1.8rem;
  color: #1f2937;
  margin-bottom: 1.5rem;
  font-weight: 700;
}

.section-text {
  font-size: 1rem;
  line-height: 1.8;
  color: #4b5563;
  margin-bottom: 1.2rem;
}

/* Tips List */
.tips-list {
  list-style: none;
  display: grid;
  gap: 1.2rem;
}

.tips-list li {
  font-size: 1rem;
  line-height: 1.7;
  color: #4b5563;
  padding: 1.2rem;
  background: #f9fafb;
  border-left: 4px solid #667eea;
  border-radius: 4px;
}

.tips-list strong {
  color: #1f2937;
  display: block;
  margin-bottom: 0.3rem;
}

/* Privacy Section */
.privacy-section {
  background: #f0f4ff;
  border-left: 4px solid #667eea;
}

/* CTA Section */
.cta-section {
  padding: 3rem 0;
  text-align: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Buttons */
.btn {
  padding: 14px 32px;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-decoration: none;
  display: inline-block;
}

.btn-primary {
  background: white;
  color: #667eea;
}

.btn-primary:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.btn-lg {
  padding: 16px 40px;
  font-size: 1.1rem;
}

/* Responsive */
@media (max-width: 768px) {
  .hero h1 {
    font-size: 1.8rem;
  }

  .logo {
    max-width: 200px;
  }

  .section h2 {
    font-size: 1.4rem;
  }

  .intro-text,
  .section-text {
    font-size: 0.95rem;
  }

  .hero,
  .cta-section {
    padding: 2rem 0;
  }

  .section {
    padding: 2rem 0;
  }
}
</style>
