Slide 1 notes“These

“These are not Python-specific rules — they are backend engineering rules, applied to Python.”
“Controllers should handle requests, services should contain business logic, repositories talk to databases or external systems.”
“Errors should be intentional and meaningful — not generic stack traces or exceptions
Logging over print - 

“Print works for scripts.
Logs work for distributed systems.”.”
“Once multiple requests run in parallel, logs are the only source of truth.”

Externalized configuration

“The same codebase should run everywhere — only configuration changes.”

“This avoids environment-specific bugs.”

Transition line

“With this foundation in place, let’s move into how Python actually executes multiple tasks — concurrency vs parallelism.”


Slide 2 : 

“Async is about handling many tasks efficiently, not doing work faster.”

“While one task waits for I/O, another task runs.”

Slide line: Asynchronous Python = Concurrency

Speaker note:

“Async is about handling many tasks at the same time, but not necessarily running them in parallel.”

Slide line: Single process, single thread

Speaker note:

“Everything runs inside one Python process and usually one thread.
There is no parallel CPU execution happening here.”

Slide line: Uses event loop for task scheduling

Speaker note:

“The event loop decides which task should run next.
It keeps switching between tasks whenever one is waiting.”

Slide line: Tasks run by cooperatively yielding

Speaker note:

“Tasks voluntarily give up control when they are waiting for something like I/O.
That’s why async code must be written in a specific way.”

Slide line: Best suited for I/O-bound workloads

Speaker note:

“Async shines when the code spends most of its time waiting — network calls, DB calls, APIs.”

Slide line: Common use cases

Speaker note:

“Most web servers and backend APIs today use async for better throughput without using more CPU.”

Slide 3

Multiprocessing (Parallelism)
Slide line: Multiprocessing = Parallelism

Speaker note:

“Multiprocessing means real parallel execution — multiple things running at the same time.”

Slide line: Multiple processes

Speaker note:

“Python creates separate OS processes, not just threads.”

Slide line: Each process has its own Python interpreter

Speaker note:

“Every process has its own memory and its own interpreter instance.”

Slide line: Bypasses the GIL

Speaker note:

“Because each process has its own interpreter, the Global Interpreter Lock is no longer a limitation.”

Slide line: True CPU parallel execution

Speaker note:

“This allows Python to fully utilize multiple CPU cores.”

Speaker note:

“Multiprocessing is ideal for heavy computation, data processing

Concurrency vs parallelism


Rule of thumb
“If your code waits — use async.
 If your code computes — use multiprocessing.”

