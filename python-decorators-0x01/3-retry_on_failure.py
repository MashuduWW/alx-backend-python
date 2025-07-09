import time
import random
import functools

def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    print(f"[WARNING] Attempt {attempt} failed with error: {e}")
                    if attempt < retries:
                        print(f"[INFO] Retrying in {delay} seconds...")
                        time.sleep(delay)
                    else:
                        print("[ERROR] All retries failed.")
                        raise
        return wrapper
    return decorator

# Example usage
@retry_on_failure(retries=3, delay=2)
def flaky_operation():
    if random.random() < 0.7:  # Simulates a 70% failure chance
        raise RuntimeError("Temporary failure occurred.")
    print("Operation succeeded!")

# Run the flaky operation with retry logic
flaky_operation()
