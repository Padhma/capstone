import time

class RateLimiter:
    def __init__(self, max_calls_per_minute=14, reset_interval=60):
        self.max_calls = max_calls_per_minute
        self.reset_interval = reset_interval
        self.call_count = 0
        self.last_reset = time.time()

    def wait_if_needed(self):
        current_time = time.time()
        if current_time - self.last_reset > self.reset_interval:
            self.call_count = 0
            self.last_reset = current_time

        if self.call_count >= self.max_calls:
            wait_time = self.reset_interval - (current_time - self.last_reset)
            if wait_time > 0:
                print(f"⏳ Rate limit reached. Sleeping for {int(wait_time)}s...")
                time.sleep(wait_time)
            self.call_count = 0
            self.last_reset = time.time()

    def record_call(self):
        self.call_count += 1