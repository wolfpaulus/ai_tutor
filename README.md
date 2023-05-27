# AI - Tutor

The AI Tutor is a web application that allows students to ask questions about a programming task.
They can also ask to have their solution evaluated.

All answers are created by a chatbot currently based on OpenAI's _gpt-3.5-turbo_ model.
The AI Tutor is integrated into _Colab_ and can be used there without any installation required.

## Colab
Colaboratory, or “Colab” for short, is a product from Google Research. 
Colab allows anybody to write and execute arbitrary Python code through the browser.
While you need a Google account, and Chrome is of course the recommended browser, 
you don't need to have python nor an IDE installed on your computer.

In Colab, users can write Python code in their own Jupyter Notebooks, 
which they store in their Google Drives. Code is written into Jupyter cells and executed by pushing the execute button. 

Notebooks can be easily shared with other, by simply sharing the URL.

## Task
A task is a programming exercise that the student has to solve. E.g.
1. Find the first 100 prime numbers
2. Roll a dice until your have rolled a six twice in a row.
3. Ask a user for their name and output the number of vowels you found in the name.

## Solution
A solution is not provided to the student. However, line of actions (strategy) is included. 
This is necessary, since the AI Tutor is not able to provide a consistent approach for every task 
and often gets confused, e.g. in the case of the prime numbers task, the AI Tutor might provide a solution that is based 
on the Sieve of Eratosthenes, finding prime numbers inside a given range, instead of finding the first n prime numbers.

## Strategy
A strategy is a line of actions that the student can follow to solve the task.
E.g. for the prime numbers task, the strategy could be:
1. Initialize an empty list to store the prime numbers.
2. Start with a number, let’s say 2, and check if it is prime.
3. If the number is prime, add it to the list of primes.
4. Increment the number and repeat steps 3 and 4 until you have found 100 prime numbers.

At this point, the student may want to ask questions about the strategy, e.g. 
_What does it mean that a number is prime?_ or _How would I do step 3?_

![Alt text](images/q1.png?raw=true "What does it mean that a number is prime?")

The AI Tutor will answer these questions in the context of the given task and strategy. 
However, code snippets longer than `10` lines are removed from the answer:

![Alt text](images/q2.png?raw=true "How would I do step3?")


## Pseudo Code
Depending on the task, it might be helpful to include pseudo code.
E.g. for the prime numbers task, the pseudo code could be:
```
Initialize an empty list to store the prime numbers
Set num to 2, the first prime number
While the length of the list of prime numbers is less than 100:
    Set is_prime to True
    For each integer i from 2 to the square root of num (inclusive):
        If num is divisible by i:
            Set is_prime to False
            Break out of the loop
    If is_prime is True:
        Add num to the list of prime numbers
    Increment num by 1
```

## Coding Editor
The Colab notebook contains a coding editor that allows the student to write code and execute it.

## Asking questions
The student can ask the AI Tutor the evaluate their solution. E.g.
```python
"""
  This program finds the first 100 prime numbers
"""
from typing import List

def task() -> List[int]:
  primes = []
  primes.append(2)
  return primes

if __name__ == "__main__":
  result = task()
  print (result)
```

The AI Tutor will then evaluate the solution and provide feedback. E.g.
_The implementation is incomplete as it only appends the first prime number (2) to the list
and returns it. To find the first 100 prime numbers, you need to implement a loop that
checks for prime numbers and appends them to the list until the list has 100 prime
numbers. Additionally, the function `task()` should take an argument that specifies the
number of prime numbers to find. Finally, the function should be named more appropriately
to reflect its purpose._

# Proxy
The AI Tutor uses OpenAI's API to generate answers. However, the Colab notebook does not access the API directly, 
instead it uses a proxy server. This will leave the apikey unexposed, allows for the removal of longer code snippets, 
and backends can be switched easily.

## Build
The proxy is a simple python application. It can be build and run using docker:
```
docker build -t openai-proxy .
docker run --restart unless-stopped -d --name openai-proxy -p 8013:8080 -e OPENAI_API_KEY=sk... openai-proxy
```
