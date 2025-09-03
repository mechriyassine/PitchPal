from modules.rag import generate_answer

test_questions = [
    "Who is the latest Liverpool transfer?",
    "What did Hamann say about Liverpool?",
    "Who is Marc Guehi?",
    "Which Arsenal player is in the news?",
    "Who won the Ballon d’Or?",
]

def test_answers():
    for question in test_questions:
        print(f"Question: {question}")
        answer = generate_answer(question)
        print(f"Answer: {answer}\n{'-'*40}")

if __name__ == "__main__":
    test_answers()