# Conversation Notes

## Async Function in Python

An `async` function in Python is a function defined using the `async def` syntax. It allows the function to be run asynchronously, meaning it can perform non-blocking operations and can be paused and resumed, which is useful for I/O-bound and high-level structured network code. These functions return a coroutine object, which can be awaited using the `await` keyword.

### Overview

1. **Defining an async function**: Use `async def` to define an asynchronous function.
2. **Awaiting**: Use the `await` keyword to pause the execution of the coroutine until the awaited coroutine completes.
3. **Running async functions**: Use an event loop to run async functions. In a script, you can use `asyncio.run()` to run the main coroutine.

### Example

```python
import asyncio

async def fetch_data():
    print("Start fetching data...")
    await asyncio.sleep(2)  # Simulate an I/O operation using sleep
    print("Data fetched!")
    return "Data"

async def main():
    result = await fetch_data()
    print(result)

# Run the main coroutine
asyncio.run(main())
```

### Without `await`

If you don't use `await` in the result assignment of an `async` function, the function will return a coroutine object instead of the actual result. This coroutine object represents the asynchronous operation but does not execute it immediately. You need to `await` the coroutine to get the result and execute the asynchronous operation.

#### Example

```python
import asyncio

async def fetch_data():
    print("Start fetching data...")
    await asyncio.sleep(2)  # Simulate an I/O operation using sleep
    print("Data fetched!")
    return "Data"

async def main():
    result = fetch_data()  # Not using await here
    print(result)  # This will print a coroutine object, not the actual result

# Run the main coroutine
asyncio.run(main())
```

Output:
```
Start fetching data...
<coroutine object fetch_data at 0x...>
```

To get the actual result, you need to use `await`:

```python
async def main():
    result = await fetch_data()  # Using await here
    print(result)  # This will print the actual result

# Run the main coroutine
asyncio.run(main())
```

Output:
```
Start fetching data...
Data fetched!
Data
```
