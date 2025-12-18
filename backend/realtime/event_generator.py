import random
import asyncio

LOCATIONS = ["paint", "left wing", "right wing", "top of key"]

def generate_event():
    return {
        "time_remaining": random.randint(1, 24),
        "score_diff": random.randint(-5, 5),
        "defender_distance": round(random.uniform(0.5, 4.0), 2),
        "location": random.choice(LOCATIONS)
    }

async def event_stream(delay=2):
    while True:
        yield generate_event()
        await asyncio.sleep(delay)