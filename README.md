Output Diversity in Generative AI for Source Code
Dissertation Project – Mohammed Shajalal Sarwar
📌 Overview

This project investigates whether Large Language Models (LLMs)—specifically CodeLlama (via Ollama)—can generate context-specific cache replacement algorithms that perform optimally across different access patterns.

The study compares two prompting strategies:

Minimal Prompting – brief functional requirements

Detailed Prompting – explicit, structured instructions

The generated cache implementations (LRU, FIFO, LIFO) are evaluated against three controlled access sequences:

Cyclic

Random

Locality-based

The primary performance metric is cache hit ratio, enabling clear comparison between algorithm behaviour and prompting strategies.

This project also explores whether LLM-generated implementations could serve as an alternative to traditional Genetic Improvement (GI) techniques in software optimisation.

🧠 Research Questions

Can LLMs generate cache implementations that are not only functionally correct but also context-optimised?

How do minimal and detailed prompts influence implementation quality?

Do LLM-generated solutions exhibit behaviour comparable to optimisation methods like GI?

How do LRU, FIFO, and LIFO implementations perform under different access patterns?

🧪 Methodology
1. Prompting Approaches

Two prompting styles were used:

Minimal

Only essential functional requirements

LLM decides all implementation details

Produces creative but inconsistent results

Detailed

Explicit steps, data structures, and edge-case handling

More consistent and correct, less diverse

2. Generated Cache Algorithms

Each algorithm implements:

get(key)

put(key, value)

size()

Using different underlying structures:

Algorithm	Structure Used
LRU	OrderedDict
FIFO	deque + dictionary
LIFO	Python list

Examples sourced from LLM-generated python files, e.g. minLRU, detailedLRU, minFIFO, detailedLIFO, etc.

3. Test Sequence Generation

Defined in TYP.py:

Cyclic sequences

Random sequences

Locality-based sequences

Each evaluated using the provided test harness.

📊 Performance Metrics
Cache Hit Ratio

The hit ratio is defined as:

hits / (hits + misses)


This is computed using the get_hit_ratio() method in the shared BaseCache class.

Repeated Trials

Each configuration is run multiple times, and averaged, to smooth out:

LLM variability

Sequence randomness

🚀 How to Run
1. Install Dependencies
pip install matplotlib
pip install ollama   # if generating new implementations

2. Run Experiments
python main.py

3. Generate Charts
python charts.py


Charts include:

Hit ratios per sequence type

Prompting strategy comparisons

Algorithm performance comparisons

🔍 Key Findings

From the dissertation results :

Detailed prompts produce more reliable implementations.

Minimal prompts sometimes outperform detailed variants in specific contexts due to emergent behaviour.

LRU performs best under locality-based and cyclic sequences.

LIFO surprisingly performs strongly in locality-heavy sequences.

FIFO is stable but limited by simplistic eviction logic.

LLM-generated code can approach or exceed the performance of hand-coded implementations.

Demonstrated promise as an alternative to Genetic Improvement.

🧩 Future Work

Evaluate runtime and memory efficiency—not just hit ratio.

Extend beyond basic eviction policies (e.g., ARC, LFU).

Combine LLM generation with Genetic Improvement for hybrid optimisation.

Use adaptive prompting where the system refines prompts based on runtime performance.

Test in real systems or simulators with live workloads.
