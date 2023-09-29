import openai

openai.api_base = 'http://localhost:1234/v1'

openai.api_key = ''

# 'Llama2 Chat' prompt format:
prefix = "[INST]"
suffix = "[/INST]"

def get_completion(prompt, temperature=0.0):
    formatted_prompt = f"{prefix}{prompt}{suffix}"

    response = openai.ChatCompletion.create(
        model="local model",
        temperature=temperature,
        messages=[{"role": "user", "content": formatted_prompt}]
    )

    return response.choices[0].message["content"]
