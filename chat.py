import openai

# Put your URI end point:port here for your local inference server (in LM Studio)
openai.api_base = 'http://localhost:1234/v1'

# Put in an empty API Key
openai.api_key = ''

# Adjust the following based on the model type
# Alpaca style prompt format:
# prefix = "### Instruction:\n"
# suffix = "\n### Response:"

# 'Llama2 Chat' prompt format:
prefix = "[INST]"
suffix = "[/INST]"

# This is a simple wrapper function to allow you to simplify your prompts
def get_completion(prompt, temperature=0.0):
    formatted_prompt = f"{prefix}{prompt}{suffix}"

    response = openai.ChatCompletion.create(
        model="local model",
        temperature=temperature,
        messages=[{"role": "user", "content": formatted_prompt}]
    )

    return response.choices[0].message["content"]
