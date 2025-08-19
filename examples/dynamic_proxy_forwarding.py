"""
Example: forwarding OpenAI requests through an intermediary proxy.

Machine A sends requests to Machine B, and Machine B forwards to the OpenAI service
while preserving streaming responses.

For demonstration, set PROXY_BASE_URL environment variable to your proxy, e.g., "http://my.proxy.host:8080/v1".
"""

import os
import httpx
from openai import OpenAI, AsyncOpenAI

# Use environment variable or default proxy base URL
proxy_base_url = os.getenv("PROXY_BASE_URL", "http://my.proxy.host:8080/v1")


def run_sync_example() -> None:
    """Run a synchronous example that streams the response through the proxy."""
    client = OpenAI(
        base_url=proxy_base_url,
        http_client=httpx.Client(proxies=proxy_base_url),
    )
    # Streaming example
    with client.chat.completions.stream(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello!"}],
    ) as stream:
        for event in stream:
            # event.choices[0].delta.content may be None for some event types
            print(event.choices[0].delta.content or "", end="", flush=True)
    print()


async def run_async_example() -> None:
    """Run an asynchronous example that streams the response through the proxy."""
    async_client = AsyncOpenAI(
        base_url=proxy_base_url,
        http_client=httpx.AsyncClient(proxies=proxy_base_url),
    )
    async with async_client.chat.completions.stream(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hi!"}],
    ) as stream:
        async for event in stream:
            content = (event.choices[0].delta.content or "")
            print(content, end="", flush=True)
    print()


if __name__ == "__main__":
    run_sync_example()
    # To run the async example, import asyncio and use:
    # asyncio.run(run_async_example())
