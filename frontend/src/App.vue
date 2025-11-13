<template>
  <div id="app">
    <header class="main-header">
      <div class="container">
        <router-link to="/" class="logo">TypeSync</router-link>
        <nav>
          <router-link to="/">Home</router-link>
          <router-link to="/eas20">EAS-20</router-link>
          <router-link to="/aas">AAS</router-link>
        </nav>
      </div>
    </header>

    <main class="main-content">
      <router-view />
    </main>

    <footer class="main-footer">
      <p>&copy; 2025 TypeSync. All rights reserved.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
    'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
    sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #333;
}

#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  width: 100%;
}

/* Header */
.main-header {
  background: rgba(255, 255, 255, 0.97);
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 1000;
  backdrop-filter: blur(10px);
}

.main-header .container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.5rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-decoration: none;
  display: inline-block;
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05);
}

nav {
  display: flex;
  gap: 2.5rem;
  align-items: center;
}

nav a {
  text-decoration: none;
  color: #333;
  font-weight: 500;
  font-size: 0.95rem;
  transition: color 0.3s ease;
  position: relative;
}

nav a::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  transition: width 0.3s ease;
}

nav a:hover::after,
nav a.router-link-active::after {
  width: 100%;
}

nav a:hover,
nav a.router-link-active {
  color: #667eea;
}

/* Main Content */
.main-content {
  flex: 1;
  padding: 2rem 0;
}

/* Footer */
.main-footer {
  background: rgba(0, 0, 0, 0.85);
  color: white;
  text-align: center;
  padding: 2rem 0;
  margin-top: auto;
  font-size: 0.9rem;
}

.main-footer p {
  margin: 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-header .container {
    flex-direction: column;
    gap: 1rem;
  }

  nav {
    gap: 1.5rem;
    width: 100%;
    justify-content: center;
  }

  nav a {
    font-size: 0.9rem;
  }

  .main-content {
    padding: 1rem 0;
  }

  .main-footer {
    padding: 1.5rem 0;
  }
}

@media (max-width: 480px) {
  .logo {
    font-size: 1.3rem;
  }

  nav {
    gap: 1rem;
  }

  nav a {
    font-size: 0.85rem;
  }

  .main-content {
    padding: 0.5rem 0;
  }
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Scrollbar styling */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #667eea;
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: #764ba2;
}
</style>