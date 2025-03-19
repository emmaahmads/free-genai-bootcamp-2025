<template>
  <div class="jawi-container">
    <div class="jawi-header">
      <h1>Practice Jawi</h1>
      <p>Learn to read and write in the traditional Jawi script used for Malay language</p>
    </div>
    
    <div class="streamlit-container">
      <iframe 
        src="http://localhost:8501" 
        class="streamlit-frame" 
        allow="microphone; camera"
      ></iframe>
    </div>
    
    <div class="jawi-info">
      <h2>About Jawi Script</h2>
      <p>
        Jawi is an Arabic alphabet for writing the Malay language, used as an official script in Brunei and as an alternative script in Malaysia.
        Jawi was the standard script for the Malay language until the 20th century, when it was largely replaced by the Latin alphabet.
      </p>
      <div class="jawi-examples">
        <div class="example">
          <h3>Example Words</h3>
          <ul>
            <li><span class="latin">Selamat datang</span> → <span class="jawi">سلامت داتڠ</span></li>
            <li><span class="latin">Terima kasih</span> → <span class="jawi">تريما کاسيه</span></li>
            <li><span class="latin">Apa khabar</span> → <span class="jawi">اڤ خبر</span></li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PracticeJawi'
};
</script>

<style scoped>
.jawi-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.jawi-header {
  text-align: center;
  margin-bottom: 2rem;
}

.jawi-header h1 {
  color: #0066cc;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.jawi-header p {
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

.jawi-info {
  background-color: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.jawi-info h2 {
  color: #0066cc;
  margin-top: 0;
  margin-bottom: 1rem;
}

.jawi-info p {
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.jawi-examples {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  margin-top: 1.5rem;
}

.example {
  flex: 1;
  min-width: 250px;
}

.example h3 {
  color: #0066cc;
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.2rem;
}

.example ul {
  padding-left: 1.5rem;
}

.example li {
  margin-bottom: 0.75rem;
}

.latin {
  font-weight: bold;
}

.jawi {
  font-family: 'Scheherazade New', 'Amiri', serif;
  font-size: 1.4rem;
  direction: rtl;
  margin-right: 0.5rem;
}

@media (max-width: 768px) {
  .jawi-container {
    padding: 1rem;
  }
  
  .jawi-header h1 {
    font-size: 2rem;
  }
  
  .streamlit-frame {
    height: 500px;
  }
  
  .jawi-examples {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
