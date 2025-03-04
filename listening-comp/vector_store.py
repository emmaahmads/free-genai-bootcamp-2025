import chromadb
from chromadb.utils import embedding_functions
import json
import os
import time
import hashlib
import pickle
import numpy as np
from typing import Dict, List, Optional
import requests
from dotenv import load_dotenv

class HuggingFaceEmbeddingFunction(embedding_functions.EmbeddingFunction):
    def __init__(self, model_id="sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize Hugging Face embedding function"""
        load_dotenv()
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise ValueError("HUGGINGFACE_API_KEY not found in environment variables")
        
        self.model_id = model_id
        self.api_url = f"https://api-inference.huggingface.co/models/{model_id}"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Default embedding dimensions for common models
        self.embedding_dimensions = {
            "sentence-transformers/all-MiniLM-L6-v2": 384,
            "sentence-transformers/all-mpnet-base-v2": 768,
            "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2": 384
        }
        self.default_dimension = 384  # Fallback dimension
        
        # Setup cache directory
        self.cache_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "data/embedding_cache"
        )
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Load cache if exists
        self.cache = self._load_cache()
        
        # Retry settings
        self.max_retries = 3
        self.base_delay = 2  # seconds

    def _get_cache_path(self):
        """Get path to the cache file"""
        return os.path.join(self.cache_dir, f"{self.model_id.replace('/', '_')}_cache.pkl")

    def _load_cache(self):
        """Load embedding cache from disk"""
        cache_path = self._get_cache_path()
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading embedding cache: {str(e)}")
        return {}

    def _save_cache(self):
        """Save embedding cache to disk"""
        cache_path = self._get_cache_path()
        try:
            with open(cache_path, 'wb') as f:
                pickle.dump(self.cache, f)
        except Exception as e:
            print(f"Error saving embedding cache: {str(e)}")

    def _get_text_hash(self, text):
        """Create a hash for the text to use as cache key"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def _fallback_embedding(self, text):
        """Generate a deterministic fallback embedding when API is unavailable"""
        # Create a simple hash-based embedding that's consistent for the same text
        text_hash = self._get_text_hash(text)
        
        # Use the hash to seed a random number generator for deterministic output
        np.random.seed(int(text_hash, 16) % (2**32))
        
        # Generate a random embedding vector of the appropriate dimension
        dimension = self.embedding_dimensions.get(self.model_id, self.default_dimension)
        embedding = np.random.normal(0, 0.1, dimension).tolist()
        
        # Normalize the embedding
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = [x / norm for x in embedding]
            
        return embedding

    def __call__(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts using Hugging Face API with caching and retries"""
        embeddings = []
        
        for text in texts:
            # Check cache first
            text_hash = self._get_text_hash(text)
            if text_hash in self.cache:
                embeddings.append(self.cache[text_hash])
                continue
                
            # Not in cache, try API with retries
            embedding = None
            for attempt in range(self.max_retries):
                try:
                    payload = {"inputs": text}
                    response = requests.post(self.api_url, headers=self.headers, json=payload)
                    response.raise_for_status()
                    
                    embedding = response.json()
                    
                    # Handle different response formats
                    if isinstance(embedding, list) and isinstance(embedding[0], list):
                        # Some models return a list of lists
                        embedding = embedding[0]
                    
                    # Cache the result
                    self.cache[text_hash] = embedding
                    embeddings.append(embedding)
                    break
                    
                except Exception as e:
                    import logging
                    logging.error(f"Error generating embedding (attempt {attempt+1}/{self.max_retries}): {str(e)}")
                    
                    # Exponential backoff before retry
                    if attempt < self.max_retries - 1:
                        sleep_time = self.base_delay * (2 ** attempt)
                        time.sleep(sleep_time)
            
            # If all retries failed, use fallback
            if embedding is None:
                print(f"All API attempts failed, using fallback embedding for: {text[:50]}...")
                embedding = self._fallback_embedding(text)
                self.cache[text_hash] = embedding  # Cache the fallback too
                embeddings.append(embedding)
        
        # Save updated cache
        self._save_cache()
        
        return embeddings

class QuestionVectorStore:
    def __init__(self, persist_directory: str = "data/vectorstore"):
        """Initialize the vector store for JLPT listening questions"""
        # Make persist_directory relative to the app directory
        self.persist_directory = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            persist_directory
        )
        os.makedirs(self.persist_directory, exist_ok=True)
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        
        # Use Hugging Face embedding model
        self.embedding_fn = HuggingFaceEmbeddingFunction()
        
        # Create or get collections for each section type
        self.collections = {
            "section2": self.client.get_or_create_collection(
                name="section2_questions",
                embedding_function=self.embedding_fn,
                metadata={"description": "JLPT listening comprehension questions - Section 2"}
            ),
            "section3": self.client.get_or_create_collection(
                name="section3_questions",
                embedding_function=self.embedding_fn,
                metadata={"description": "JLPT phrase matching questions - Section 3"}
            )
        }

    def add_questions(self, section_num: int, questions: List[Dict], video_id: str):
        """Add questions to the vector store"""
        if section_num not in [2, 3]:
            raise ValueError("Only sections 2 and 3 are currently supported")
            
        collection = self.collections[f"section{section_num}"]
        
        ids = []
        documents = []
        metadatas = []
        
        for idx, question in enumerate(questions):
            # Create a unique ID for each question
            question_id = f"{video_id}_{section_num}_{idx}"
            ids.append(question_id)
            
            # Store the full question structure as metadata
            metadatas.append({
                "video_id": video_id,
                "section": section_num,
                "question_index": idx,
                "full_structure": json.dumps(question)
            })
            
            # Create a searchable document from the question content
            if section_num == 2:
                document = f"""
                Situation: {question['Introduction']}
                Dialogue: {question['Conversation']}
                Question: {question['Question']}
                """
            else:  # section 3
                document = f"""
                Situation: {question['Situation']}
                Question: {question['Question']}
                """
            documents.append(document)
        
        # Add to collection
        collection.add(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

    def search_similar_questions(
        self, 
        section_num: int, 
        query: str, 
        n_results: int = 5
    ) -> List[Dict]:
        """Search for similar questions in the vector store"""
        if section_num not in [2, 3]:
            raise ValueError("Only sections 2 and 3 are currently supported")
            
        collection = self.collections[f"section{section_num}"]
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Convert results to more usable format
        questions = []
        for idx, metadata in enumerate(results['metadatas'][0]):
            question_data = json.loads(metadata['full_structure'])
            question_data['similarity_score'] = results['distances'][0][idx]
            questions.append(question_data)
            
        return questions

    def get_question_by_id(self, section_num: int, question_id: str) -> Optional[Dict]:
        """Retrieve a specific question by its ID"""
        if section_num not in [2, 3]:
            raise ValueError("Only sections 2 and 3 are currently supported")
            
        collection = self.collections[f"section{section_num}"]
        
        result = collection.get(
            ids=[question_id],
            include=['metadatas']
        )
        
        if result['metadatas']:
            return json.loads(result['metadatas'][0]['full_structure'])
        return None

    def parse_questions_from_file(self, filename: str) -> List[Dict]:
        """Parse questions from a structured text file"""
        questions = []
        current_question = {}
        
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                if line.startswith('<question>'):
                    current_question = {}
                elif line.startswith('Introduction:'):
                    i += 1
                    if i < len(lines):
                        current_question['Introduction'] = lines[i].strip()
                elif line.startswith('Conversation:'):
                    i += 1
                    if i < len(lines):
                        current_question['Conversation'] = lines[i].strip()
                elif line.startswith('Situation:'):
                    i += 1
                    if i < len(lines):
                        current_question['Situation'] = lines[i].strip()
                elif line.startswith('Question:'):
                    i += 1
                    if i < len(lines):
                        current_question['Question'] = lines[i].strip()
                elif line.startswith('Options:'):
                    options = []
                    for _ in range(4):
                        i += 1
                        if i < len(lines):
                            option = lines[i].strip()
                            if option.startswith('1.') or option.startswith('2.') or option.startswith('3.') or option.startswith('4.'):
                                options.append(option[2:].strip())
                    current_question['Options'] = options
                elif line.startswith('</question>'):
                    if current_question:
                        questions.append(current_question)
                        current_question = {}
                i += 1
            return questions
        except Exception as e:
            print(f"Error parsing questions from {filename}: {str(e)}")
            return []

    def index_questions_file(self, filename: str, section_num: int):
        """Index all questions from a file into the vector store"""
        # Extract video ID from filename
        video_id = os.path.basename(filename).split('_section')[0]
        
        # Parse questions from file
        questions = self.parse_questions_from_file(filename)
        
        if questions:
            # Add questions to vector store
            self.add_questions(section_num, questions, video_id)
            return len(questions)
        return 0
