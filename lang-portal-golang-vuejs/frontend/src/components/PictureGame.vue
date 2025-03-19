<template>
  <div class="picture-game-container">
    <div class="picture-game-header">
      <h1>Picture Game</h1>
      <p>Interactive picture game based on your chosen outcomes</p>
    </div>
    
    <div class="streamlit-container">
      <iframe 
        src="http://localhost:8503" 
        class="streamlit-frame" 
        allow="microphone; camera"
      ></iframe>
    </div>
    
    <div class="picture-game-info">
      <h2>How to Play</h2>
      <p>
        This interactive picture game helps you practice Malay vocabulary and sentence construction in a fun, 
        engaging way. The game adapts to your learning goals and provides immediate feedback.
      </p>
      
      <div class="game-features">
        <div class="feature">
          <div class="feature-icon">🎯</div>
          <h3>Choose Your Focus</h3>
          <p>Select vocabulary categories or specific grammar structures you want to practice.</p>
        </div>
        
        <div class="feature">
          <div class="feature-icon">🖼️</div>
          <h3>Picture Prompts</h3>
          <p>Describe images in Malay or answer questions about what you see.</p>
        </div>
        
        <div class="feature">
          <div class="feature-icon">🔄</div>
          <h3>Adaptive Difficulty</h3>
          <p>The game adjusts to your skill level, becoming more challenging as you improve.</p>
        </div>
        
        <div class="feature">
          <div class="feature-icon">📊</div>
          <h3>Track Progress</h3>
          <p>See your improvement over time with detailed performance statistics.</p>
        </div>
      </div>
      
      <div class="game-tips">
        <h3>Tips for Success</h3>
        <ul>
          <li>Start with familiar vocabulary categories to build confidence</li>
          <li>Use complete sentences when describing pictures</li>
          <li>Don't worry about making mistakes - they're part of learning!</li>
          <li>Try to incorporate new vocabulary you've learned in other exercises</li>
          <li>Challenge yourself with timed rounds once you're comfortable</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PictureGame'
};
</script>

<style scoped>
.picture-game-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.picture-game-header {
  text-align: center;
  margin-bottom: 2rem;
}

.picture-game-header h1 {
  color: #0066cc;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.picture-game-header p {
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

.picture-game-info {
  background-color: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.picture-game-info h2 {
  color: #0066cc;
  margin-top: 0;
  margin-bottom: 1rem;
}

.picture-game-info p {
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.game-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.feature {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
}

.feature-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

.feature h3 {
  color: #0066cc;
  margin: 0.5rem 0;
}

.feature p {
  font-size: 0.9rem;
  margin: 0;
}

.game-tips {
  background-color: #f0f9ff;
  border-radius: 8px;
  padding: 1.5rem;
  margin-top: 2rem;
}

.game-tips h3 {
  color: #0066cc;
  margin-top: 0;
  margin-bottom: 1rem;
}

.game-tips ul {
  padding-left: 1.5rem;
  margin-bottom: 0;
}

.game-tips li {
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .picture-game-container {
    padding: 1rem;
  }
  
  .picture-game-header h1 {
    font-size: 2rem;
  }
  
  .streamlit-frame {
    height: 500px;
  }
  
  .game-features {
    grid-template-columns: 1fr;
  }
}
</style>
