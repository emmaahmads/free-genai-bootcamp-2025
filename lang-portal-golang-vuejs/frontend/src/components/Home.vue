<template>
  <div class="home-container">
    <header class="header">
      <div class="logo-container">
        <h1 class="logo">MalayMaster</h1>
        <p class="tagline">Your Journey to Malay Language Mastery</p>
      </div>
      <nav class="main-nav">
        <router-link to="/" class="nav-link active">Home</router-link>
        <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
        <router-link to="/study-activities" class="nav-link">Study Activities</router-link>
        <a href="#" class="nav-link">Resources</a>
        <a href="#" class="nav-link">Community</a>
      </nav>
    </header>

    <section class="hero">
      <div class="hero-content">
        <h2>Selamat Datang ke MalayMaster!</h2>
        <p>Begin your journey to learn Bahasa Melayu with our interactive platform designed for learners of all levels.</p>
        <div class="cta-buttons">
          <router-link to="/dashboard" class="cta-button primary">Start Learning</router-link>
          <a href="#features" class="cta-button secondary">Explore Features</a>
        </div>
      </div>
      <div class="hero-image">
        <img src="https://placehold.co/600x400/e6f7ff/0066cc?text=Malay+Learning" alt="Malay Learning" />
      </div>
    </section>

    <section id="features" class="features">
      <h2 class="section-title">Learning Apps & Features</h2>
      <div class="feature-cards">
        <!-- <div class="feature-card">
          <div class="feature-icon">📚</div>
          <h3>Vocabulary Builder</h3>
          <p>Expand your Malay vocabulary with our spaced repetition system.</p>
          <router-link to="/ollama-chat" class="feature-link">Start Learning</router-link>
        </div> -->
        
        <div class="feature-card">
          <div class="feature-icon">💬</div>
          <h3>Malay Chatbox</h3>
          <p>Practice your Malay language skills with our AI conversation partner.</p>
          <router-link to="/malay-chatbox" class="feature-link">Start Chatting</router-link>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">🗣️</div>
          <h3>Pronunciation Practice</h3>
          <p>Perfect your accent with audio examples and speech recognition.</p>
          <a href="#" class="feature-link">Coming Soon</a>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">✍️</div>
          <h3>Grammar Exercises</h3>
          <p>Master Malay grammar rules through interactive exercises.</p>
          <router-link to="/study-activities" class="feature-link">Practice Now</router-link>
        </div>
        
        <div class="feature-card">
          <div class="feature-icon">💬</div>
          <h3>Conversation Practice</h3>
          <p>Practice real-life conversations with our AI conversation partner.</p>
          <a href="#" class="feature-link">Coming Soon</a>
        </div>
      </div>
    </section>

    <section class="progress-tracker">
      <h2 class="section-title">Track Your Progress</h2>
      <p class="section-description">Monitor your learning journey with detailed analytics and progress tracking.</p>
      <div class="progress-image">
        <img src="https://placehold.co/800x400/f0f9ff/0066cc?text=Progress+Dashboard" alt="Progress Dashboard" />
      </div>
      <router-link to="/dashboard" class="cta-button primary">View Your Dashboard</router-link>
    </section>

    <section class="cultural-insights">
      <h2 class="section-title">Cultural Insights</h2>
      <div class="cultural-content">
        <div class="cultural-text">
          <p>Learning a language is more than just words and grammar. Discover the rich culture, traditions, and history behind Bahasa Melayu.</p>
          <ul class="cultural-list">
            <li>Traditional customs and celebrations</li>
            <li>Malaysian and Indonesian cultural differences</li>
            <li>Historical context of the Malay language</li>
            <li>Modern usage and regional dialects</li>
          </ul>
          <a href="#" class="feature-link">Explore Cultural Content</a>
        </div>
        <div class="cultural-image">
          <img src="https://placehold.co/500x300/fff5e6/cc7700?text=Malay+Culture" alt="Malay Culture" />
        </div>
      </div>
    </section>

    <footer class="footer">
      <div class="footer-content">
        <div class="footer-logo">
          <h2>MalayMaster</h2>
          <p>Your Journey to Malay Language Mastery</p>
        </div>
        <div class="footer-links">
          <div class="footer-column">
            <h3>Learning</h3>
            <ul>
              <li><router-link to="/dashboard">Dashboard</router-link></li>
              <li><router-link to="/study-activities">Study Activities</router-link></li>
              <li><a href="#">Resources</a></li>
              <li><a href="#">Dictionary</a></li>
            </ul>
          </div>
          <div class="footer-column">
            <h3>Community</h3>
            <ul>
              <li><a href="#">Forums</a></li>
              <li><a href="#">Language Partners</a></li>
              <li><a href="#">Events</a></li>
            </ul>
          </div>
          <div class="footer-column">
            <h3>About</h3>
            <ul>
              <li><a href="#">Our Method</a></li>
              <li><a href="#">Team</a></li>
              <li><a href="#">Contact Us</a></li>
            </ul>
          </div>
        </div>
      </div>
      <div class="copyright">
        <p>&copy; 2025 MalayMaster. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'Home',
};
</script>

<style scoped>
.home-container {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
  line-height: 1.6;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 5%;
  background-color: #ffffff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.logo {
  font-size: 2rem;
  font-weight: 700;
  color: #0066cc;
  margin: 0;
}

.tagline {
  margin: 0;
  font-size: 0.9rem;
  color: #666;
}

.main-nav {
  display: flex;
  gap: 1.5rem;
}

.nav-link {
  text-decoration: none;
  color: #555;
  font-weight: 500;
  padding: 0.5rem 0.75rem;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.nav-link:hover, .nav-link.active {
  color: #0066cc;
  background-color: #f0f7ff;
}

.hero {
  display: flex;
  align-items: center;
  padding: 4rem 5%;
  background: linear-gradient(135deg, #e6f7ff 0%, #f0f9ff 100%);
}

.hero-content {
  flex: 1;
  padding-right: 2rem;
}

.hero-content h2 {
  font-size: 2.5rem;
  color: #0066cc;
  margin-bottom: 1rem;
}

.hero-content p {
  font-size: 1.2rem;
  margin-bottom: 2rem;
  color: #555;
}

.hero-image {
  flex: 1;
}

.hero-image img {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.cta-buttons {
  display: flex;
  gap: 1rem;
}

.cta-button {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.3s ease;
}

.cta-button.primary {
  background-color: #0066cc;
  color: white;
}

.cta-button.primary:hover {
  background-color: #0055aa;
  transform: translateY(-2px);
}

.cta-button.secondary {
  background-color: white;
  color: #0066cc;
  border: 1px solid #0066cc;
}

.cta-button.secondary:hover {
  background-color: #f0f7ff;
  transform: translateY(-2px);
}

.features {
  padding: 4rem 5%;
  background-color: #ffffff;
}

.section-title {
  text-align: center;
  font-size: 2rem;
  color: #0066cc;
  margin-bottom: 2rem;
}

.section-description {
  text-align: center;
  max-width: 800px;
  margin: 0 auto 3rem;
  color: #666;
  font-size: 1.1rem;
}

.feature-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
}

.feature-card {
  background-color: #f8fbff;
  border-radius: 8px;
  padding: 2rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.feature-card h3 {
  font-size: 1.3rem;
  color: #0066cc;
  margin-bottom: 0.75rem;
}

.feature-link {
  display: inline-block;
  margin-top: 1rem;
  color: #0066cc;
  text-decoration: none;
  font-weight: 600;
}

.feature-link:hover {
  text-decoration: underline;
}

.progress-tracker {
  padding: 4rem 5%;
  background-color: #f0f9ff;
  text-align: center;
}

.progress-image {
  margin: 2rem auto;
  max-width: 800px;
}

.progress-image img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.cultural-insights {
  padding: 4rem 5%;
  background-color: #ffffff;
}

.cultural-content {
  display: flex;
  align-items: center;
  gap: 3rem;
}

.cultural-text {
  flex: 1;
}

.cultural-image {
  flex: 1;
}

.cultural-image img {
  width: 100%;
  border-radius: 8px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.cultural-list {
  margin: 1.5rem 0;
  padding-left: 1.5rem;
}

.cultural-list li {
  margin-bottom: 0.5rem;
  color: #555;
}

.footer {
  background-color: #003366;
  color: white;
  padding: 3rem 5% 1.5rem;
}

.footer-content {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.footer-logo h2 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
}

.footer-logo p {
  margin: 0;
  font-size: 0.9rem;
  opacity: 0.8;
}

.footer-links {
  display: flex;
  gap: 3rem;
}

.footer-column h3 {
  font-size: 1.1rem;
  margin-bottom: 1rem;
  color: #66b3ff;
}

.footer-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-column li {
  margin-bottom: 0.5rem;
}

.footer-column a {
  color: white;
  text-decoration: none;
  opacity: 0.8;
  transition: opacity 0.3s ease;
}

.footer-column a:hover {
  opacity: 1;
}

.copyright {
  text-align: center;
  padding-top: 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  font-size: 0.9rem;
  opacity: 0.7;
}

@media (max-width: 900px) {
  .hero, .cultural-content {
    flex-direction: column;
  }
  
  .hero-content, .cultural-text {
    padding-right: 0;
    margin-bottom: 2rem;
  }
  
  .footer-content {
    flex-direction: column;
    gap: 2rem;
  }
  
  .footer-links {
    flex-wrap: wrap;
    gap: 2rem;
  }
}

@media (max-width: 600px) {
  .header {
    flex-direction: column;
    text-align: center;
  }
  
  .main-nav {
    margin-top: 1rem;
    flex-wrap: wrap;
    justify-content: center;
  }
  
  .feature-cards {
    grid-template-columns: 1fr;
  }
}
</style>
