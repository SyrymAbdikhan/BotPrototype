
import os
import aiohttp
import json


class GPT:
    def __init__(self):
        self.url = os.getenv('MODEL_URL')
        self.headers = {"Authorization": f"Bearer {os.getenv('HUGGINFACE_INFERENCE_TOKEN')}"}

    async def query(self, input: str) -> list:
        payload = {'inputs': input}
        data = json.dumps(payload)

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, headers=self.headers, data=data) as response:
                data = await response.text()

        data = json.loads(data)
        return data['generated_text']

