"""Day 2: asyncio fundamentals.

Run it:  uv run python scripts/day2_parallel_models.py

Before running, predict: if three model calls take roughly 1.3s, 0.6s and 1.5s,
how long does the sequential version take, and how long the parallel one?
"""

import asyncio
import random
import time

MODELS = ["claude-sonnet", "gemini-flash", "qwen-plus"]


async def fake_model_call(model: str) -> str:
    """Stands in for a real LLM call: waits a random time, like network + inference."""
    latency = random.uniform(0.5, 2.0)
    await asyncio.sleep(latency)
    return f"{model:<14} answered in {latency:.2f}s"


async def run_sequential() -> float:
    start = time.perf_counter()
    for model in MODELS:
        print("  ", await fake_model_call(model))
    return time.perf_counter() - start


async def run_parallel() -> float:
    start = time.perf_counter()
    results = await asyncio.gather(*(fake_model_call(m) for m in MODELS))
    for line in results:
        print("  ", line)
    return time.perf_counter() - start


async def main() -> None:
    random.seed(7)
    print("Sequential:")
    print(f"   total {await run_sequential():.2f}s\n")

    random.seed(7)  # same latencies, so the comparison is fair
    print("Parallel with asyncio.gather:")
    print(f"   total {await run_parallel():.2f}s\n")

    # EXERCISE 1  Timeouts
    #   Wrap each call in asyncio.wait_for(fake_model_call(m), timeout=1.2).
    #   What happens to the whole gather when one model is slow?
    #   Then pass return_exceptions=True to gather. What changes, and why is that
    #   the behaviour you want in a gateway with fallback?
    #
    # EXERCISE 2  First answer wins
    #   Rewrite run_parallel with asyncio.as_completed so answers print in the
    #   order they finish, not the order they were started.
    #
    # EXERCISE 3  The real thing
    #   Replace fake_model_call with a call to your LiteLLM proxy:
    #     POST {LITELLM_BASE_URL}/v1/chat/completions
    #     headers: Authorization: Bearer {LITELLM_API_KEY}
    #     json:    {"model": model, "messages": [{"role": "user", "content": "Hola"}]}
    #   Use ONE httpx.AsyncClient shared by all calls (why one and not one per call?).


if __name__ == "__main__":
    asyncio.run(main())
