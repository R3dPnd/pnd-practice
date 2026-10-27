# 08 — Bounded concurrency with cancellation (Python / asyncio)

Python version of the Go worker pool: [`../../../challenges/08_worker_pool/README.md`](../../../challenges/08_worker_pool/README.md).

```python
async def bounded_map(items, workers, fn) -> list:
    # fn is `async def fn(item) -> result`
```
- At most `workers` calls of `fn` in flight (`workers <= 0` → 1).
- Results in **input order**.
- On the first exception: cancel everything still running / not started, and re-raise it.

Approaches: `asyncio.Semaphore` + `asyncio.TaskGroup` (3.11+, cancels siblings on error for
free — but wraps the error in an `ExceptionGroup`, so unwrap it), or N worker tasks pulling
from an `asyncio.Queue`. Be ready to contrast with threads (`ThreadPoolExecutor`) and the GIL:
asyncio for I/O-bound (HTTP/DB calls), processes for CPU-bound.
