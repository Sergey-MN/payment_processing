import asyncio

import httpx

MAX_RETRIES = 3

async def send_webhook(url: str, payload: dict):
    delay = 1

    async with httpx.AsyncClient(verify=False) as client:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = await client.post(url, json=payload, timeout=5)

                if response.status_code < 300:
                    return

                raise Exception(f"Bad status: {response.status_code}")

            except Exception:
                if attempt == MAX_RETRIES:
                    raise
                await asyncio.sleep(delay)
                delay *= 2
