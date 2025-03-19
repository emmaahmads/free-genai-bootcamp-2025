<template>
  <div class="listening-speaking-container">
    <div class="listening-speaking-header">
      <h1>Practice Listening and Speaking</h1>
      <p>Improve your Malay listening comprehension and speaking skills with interactive exercises</p>
    </div>
    
    <div class="streamlit-container">
      <iframe 
        src="http://localhost:8502" 
        class="streamlit-frame" 
        allow="microphone; camera"
      ></iframe>
    </div>
    
    <div class="listening-speaking-info">
      <h2>About Listening and Speaking Practice</h2>
      <p>
        Effective communication in Malay requires strong listening and speaking skills. This module helps you:
      </p>
      <ul>
        <li>Understand native Malay speakers at different speeds</li>
        <li>Practice proper pronunciation and intonation</li>
        <li>Build confidence in real-world conversations</li>
        <li>Learn common phrases and expressions used in daily life</li>
      </ul>
      
      <div class="practice-tips">
        <h3>Practice Tips</h3>
        <div class="tips-grid">
          <div class="tip">
            <div class="tip-icon">🎧</div>
            <h4>Listen Actively</h4>
            <p>Focus on understanding the main ideas first, then details.</p>
          </div>
          <div class="tip">
            <div class="tip-icon">🔁</div>
            <h4>Repeat Often</h4>
            <p>Practice saying phrases multiple times to build muscle memory.</p>
          </div>
          <div class="tip">
            <div class="tip-icon">🗣️</div>
            <h4>Speak Aloud</h4>
            <p>Even when studying alone, speak at a normal volume.</p>
          </div>
          <div class="tip">
            <div class="tip-icon">📱</div>
            <h4>Record Yourself</h4>
            <p>Compare your pronunciation with native speakers.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ListeningSpeaking'
};
</script>

<style scoped>
.listening-speaking-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.listening-speaking-header {
  text-align: center;
  margin-bottom: 2rem;
}

.listening-speaking-header h1 {
  color: #0066cc;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.listening-speaking-header p {
  color: #666;
  font-size: 1.1rem;
}

.streamlit-container {
  background-color: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  margin-bottom: 2rem;
  min-height: 500px;
}

.streamlit-frame {
  width: 100%;
  height: 700px;
  border: none;
}

.listening-speaking-info {
  background-color: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.listening-speaking-info h2 {
  color: #0066cc;
  margin-top: 0;
  margin-bottom: 1rem;
}

.listening-speaking-info p {
  line-height: 1.6;
  margin-bottom: 1rem;
}

.listening-speaking-info ul {
  margin-bottom: 2rem;
  padding-left: 1.5rem;
}

.listening-speaking-info li {
  margin-bottom: 0.5rem;
  line-height: 1.5;
}

.practice-tips h3 {
  color: #0066cc;
  margin-bottom: 1.5rem;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
}

.tip {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
}

.tip-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.tip h4 {
  color: #0066cc;
  margin: 0.5rem 0;
}

.tip p {
  font-size: 0.9rem;
  margin: 0;
}

@media (max-width: 768px) {
  .listening-speaking-container {
    padding: 1rem;
  }
  
  .listening-speaking-header h1 {
    font-size: 2rem;
  }
  
  .streamlit-frame {
    height: 500px;
  }
  
  .tips-grid {
    grid-template-columns: 1fr;
  }
}
</style>
