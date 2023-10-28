import openai

openai.api_base = 'http://localhost:1234/v1'
openai.api_key = ''

def get_completion(prompt, temperature=0.1, model_max_tokens=-1, prefix="[INST]", suffix="[/INST]"):
    formatted_prompt = f"{prefix}{prompt}{suffix}"

    response = openai.ChatCompletion.create(
        model="local model",
        temperature=temperature,
        max_tokens=model_max_tokens,
        messages=[{"role": "user", "content": formatted_prompt}]
    )

    return response.choices[0].message["content"]
