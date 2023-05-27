"""
Minimal test for the ai_tutor module.
"""
from ai_tutor import create_context, ask

task = "Create the first 100 prime numbers"
steps = """1. Initialize an empty list to store the prime numbers.
2. Start with a number, let's say 2, and check if it is prime.
3. If the number is prime, add it to the list of primes.
4. Increment the number and repeat steps 3 and 4 until you have found n prime numbers."""

code = '''
"""
  This program finds the first 100 prime numbers
"""
from typing import List

def task() -> List[int]:
  primes = [2]
  k = 3
  while len(primes) < 100:
    for i in range(3, int(3**0.5)+1, 2):
        if k % i == 0:
            break
    else:
        primes.append(k)
    k += 2
  return primes       

if __name__ == "__main__":
  result = task()
  print (result)

'''


def test_ask():
    context = create_context(task, steps)
    question = "How would I approach step 3?"
    answer = ask(context, question)
    assert answer is not None


def test_validate():
    context = create_context(task, "Provide feedback on the python implementation below.")
    answer = ask(context, code, code=True)
    print(answer)
    assert answer is not None
