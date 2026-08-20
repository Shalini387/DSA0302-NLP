import os
from openai import OpenAI

def generate_text(prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text


def main():
    print("====================================")
    print("      GPT TEXT GENERATION SYSTEM")
    print("====================================")

    print("\nEnter a prompt for text generation.")
    prompt = input("Prompt: ").strip()

    if not prompt:
        print("\nError: Prompt cannot be empty.")
        return

    if not os.getenv("OPENAI_API_KEY"):
        print("\nError: OPENAI_API_KEY is not set.")
        print("Please set your OpenAI API key before running.")
        return

    try:
        generated_text = generate_text(prompt)

        print("\n====================================")
        print("          GENERATED TEXT")
        print("====================================")
        print(generated_text)
        print("====================================")

    except Exception as error:
        print("\nAn error occurred:")
        print(error)


if __name__ == "__main__":
    main()