import threading
import time


def cooldown(duration):
    def decorator(function):
        function.on_cooldown = False

        def sleeper():
            function.on_cooldown = True
            time.sleep(duration)
            function.on_cooldown = False

        async def wrapper(*args, **kwargs):
            if function.on_cooldown:
                print(f"Function {function.__name__} on cooldown")
            else:
                timer = threading.Thread(target=sleeper)
                await function(*args, **kwargs)
                timer.start()
        return wrapper
    return decorator
