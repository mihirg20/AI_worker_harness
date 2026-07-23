from app.llm.delegate import ask


def main():
    prompt = "Explain in one sentence why abstraction is useful."

    response = ask(prompt)

    print("\nLLM Response:\n")
    print(response)


if __name__ == "__main__":
    main()