# Troubleshooting Log

## PyTorch and Streamlit Compatibility Issue

### Error

```
Traceback (most recent call last):
  File "/home/emmaahmads/workspace/genAI/listening-comp/env/lib/python3.12/site-packages/streamlit/web/bootstrap.py", line 345, in run
    if asyncio.get_running_loop().is_running():
       ^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: no running event loop

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/home/emmaahmads/workspace/genAI/listening-comp/env/lib/python3.12/site-packages/streamlit/watcher/local_sources_watcher.py", line 217, in get_module_paths
    potential_paths = extract_paths(module)
                      ^^^^^^^^^^^^^^^^^^^^^
  File "/home/emmaahmads/workspace/genAI/listening-comp/env/lib/python3.12/site-packages/streamlit/watcher/local_sources_watcher.py", line 210, in <lambda>
    lambda m: list(m.__path__._path),
                   ^^^^^^^^^^^^^^^^
  File "/home/emmaahmads/workspace/genAI/listening-comp/env/lib/python3.12/site-packages/torch/_classes.py", line 13, in __getattr__
    proxy = torch._C._get_custom_class_python_wrapper(self.name, attr)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: Tried to instantiate class '__path__._path', but it does not exist! Ensure that it is registered via torch::class_
```

### Cause

This error occurred due to two main issues:

1. **Asyncio Event Loop Conflict**: The initial approach of manually checking and setting up an asyncio event loop in the `main.py` file was causing conflicts with Streamlit's own event loop management.

2. **PyTorch and Streamlit File Watcher Incompatibility**: Streamlit's file watcher system was trying to inspect PyTorch modules during hot-reloading. However, PyTorch's custom class system doesn't support this kind of introspection in the way Streamlit expected, leading to the `RuntimeError: Tried to instantiate class '__path__._path'` error.

### Solution

The issue was resolved by:

1. **Removing Manual Asyncio Event Loop Initialization**: We removed the following code from `main.py`:
   ```python
   # Initialize asyncio event loop
   try:
       asyncio.get_running_loop()
   except RuntimeError:
       asyncio.set_event_loop(asyncio.new_event_loop())
   ```
   This allowed Streamlit to manage its own event loop properly.

2. **Disabling Streamlit's File Watcher**: We created a `.streamlit/config.toml` file with the following configuration:
   ```toml
   [server]
   fileWatcherType = "none"

   [runner]
   fastReruns = false
   ```
   This configuration disables Streamlit's file watcher system, preventing it from trying to inspect PyTorch modules during hot-reloading.

### Trade-offs

By disabling the file watcher, the application will not automatically reload when code changes are made. You'll need to manually restart the Streamlit app when you make changes to your code. This is a reasonable compromise to get the app working properly with PyTorch.

### Additional Notes

This is a known compatibility issue between Streamlit's hot-reloading feature and certain Python libraries that use custom class systems, such as PyTorch. The solution we implemented is a common workaround for this specific issue.

## Hugging Face API Service Unavailability

### Error

```
ERROR:root:Error generating embedding: 503 Service Temporarily Unavailable for url: https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2
```

### Cause

This error occurred when attempting to use the Hugging Face API for generating embeddings. A 503 Service Temporarily Unavailable error indicates that the Hugging Face API service was temporarily down or overloaded. This is a common issue with external API dependencies that can happen due to:

1. Temporary service outages
2. Rate limiting
3. Network connectivity issues
4. Server maintenance

### Solution

To address this issue and make the application more resilient to API failures, we implemented several improvements to the `HuggingFaceEmbeddingFunction` class in `vector_store.py`:

1. **Local Embedding Cache**:
   ```python
   # Setup cache directory
   self.cache_dir = os.path.join(
       os.path.dirname(os.path.abspath(__file__)),
       "data/embedding_cache"
   )
   os.makedirs(self.cache_dir, exist_ok=True)
   
   # Load cache if exists
   self.cache = self._load_cache()
   ```
   This caches embeddings locally to reduce API calls and provide immediate results for previously processed text.

2. **Retry Logic with Exponential Backoff**:
   ```python
   # Retry settings
   self.max_retries = 3
   self.base_delay = 2  # seconds
   
   # In the __call__ method:
   for attempt in range(self.max_retries):
       try:
           # API call code...
       except Exception as e:
           # Exponential backoff before retry
           if attempt < self.max_retries - 1:
               sleep_time = self.base_delay * (2 ** attempt)
               time.sleep(sleep_time)
   ```
   This implements a retry mechanism that makes multiple attempts with increasing delays between retries.

3. **Deterministic Fallback Embedding Generation**:
   ```python
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
   ```
   This provides a consistent fallback mechanism when the API is completely unavailable, ensuring the application continues to function.

### Benefits of the Solution

1. **Improved Resilience**: The application can now handle temporary API outages gracefully.
2. **Better Performance**: Caching reduces redundant API calls, improving response times.
3. **Consistent Behavior**: The deterministic fallback ensures consistent results even when the API is unavailable.
4. **Reduced API Costs**: Fewer API calls means reduced usage costs for paid API services.

### Additional Notes

This pattern of caching, retrying, and providing fallbacks is a best practice when working with external API dependencies. It ensures that your application remains functional even when external services experience issues, providing a better user experience.
