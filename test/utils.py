from asyncio import new_event_loop


def async_test(coroutine):
    def wrapper(*args, **kwargs):
        loop = new_event_loop()
        try:
            return loop.run_until_complete(coroutine(*args, **kwargs))
        finally:
            loop.close()
    return wrapper
