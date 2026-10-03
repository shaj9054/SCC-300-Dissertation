# Output Diversity in Generative AI for Source Code

BSc Computer Science dissertation by Mohammed Shajalal Sarwar, Lancaster University.

This project investigates whether CodeLlama, accessed through Ollama, can generate cache replacement implementations suited to different access patterns. It compares minimal and detailed prompting for LRU, FIFO and LIFO caches, using cache hit ratio as the performance metric. The wider research considers generated implementations as a possible alternative to Genetic Improvement approaches.

## Research questions

- How does prompt detail affect the behaviour of generated cache code?
- How do generated LRU, FIFO and LIFO implementations perform under cyclic, random and locality-based workloads?
- Can generated implementations offer useful, workload-specific alternatives to conventional implementations?

## Methodology

Minimal prompts give essential functional requirements; detailed prompts add more explicit implementation guidance. Generated cache classes are adapted through wrappers that standardise their interface and count hits and misses.

The primary metric is:

```text
cache hit ratio = hits / (hits + misses)
```

Repeated runs explore variation across generated access sequences. The submitted dissertation contains the methodology, results and interpretation; it should be used for reported findings rather than assuming that every script snapshot reproduces the final experiment configuration.

## Repository structure

| Path | Purpose |
| --- | --- |
| [Dissertation PDF](Output_Diversity_in_Generative_AI_for_Source_Code.pdf) | Full research report. |
| `main.py` | Interactive CodeLlama application with prompt history and error logging. |
| `TYP.py` | Baseline caches, sequence generators and repeated-run evaluation. |
| `minLRU.py`, `minFIFO.py`, `minLIFO.py` | Minimal-prompt generated implementations. |
| `detailedLRU.py`, `detailedFIFO.py`, `detailedLIFO.py` | Detailed-prompt generated implementations. |
| `wrapper.py` | Common wrappers for the generated implementations. |
| `test.py` | Generated-cache comparison script snapshot. |
| `charts.py` | Grouped bar chart using stored result arrays. |
| `conversation_history.txt` | Saved prompting history. |
| `Dissertation.zip` | Included project archive. |

## Running the baseline experiment

Use Python 3 in a fresh environment. The baseline harness uses the standard library:

```bash
git clone https://github.com/shaj9054/SCC-300-Dissertation.git\ncd SCC-300-Dissertation\npython3 -m venv .venv\nsource .venv/bin/activate\npython TYP.py
```

On Windows, activate with `.venv\\Scripts\\activate`. Do not rely on the committed `bin/` and `lib/` directories as a portable environment.

The current baseline entry point uses six items, sequence length 20, ten runs and cache capacity three. It prints mean hit ratios for each cache/workload combination. Random sequences are not seeded in this script, so runs can differ.

## Viewing the stored chart

```bash
python -m pip install numpy matplotlib\npython charts.py
```

This plots hard-coded arrays; it does not load fresh experimental output or calculate uncertainty.

## Interactive code generation

`main.py` requires a running Ollama service with the `codellama` model and compatible LangChain packages. Install the Python dependencies in the fresh environment:

```bash
python -m pip install langchain langchain-ollama
```

With Ollama installed and running:

```bash
ollama pull codellama\npython main.py
```

The script uses the legacy `langchain.prompts` import path; newer package releases may need a compatible environment or an import update. There is no pinned dependency lockfile. The application loads saved conversation history and writes it when you exit, so use a local copy if you want to preserve the included prompt log.

## Reproduction notes

The checked-in `test.py` imports a `plot_results` function that `charts.py` does not define, and passes the locality generator without its required locality-window argument. It also sets capacity to five, unlike the baseline entry point. These issues must be reconciled before treating that script as a runnable reproduction of the generated-cache comparison.

Cache hit ratio does not measure runtime, memory consumption or overall software correctness. Conclusions are workload-dependent; the project does not establish that generated code is universally better than hand-written code or perform a direct, general benchmark against Genetic Improvement.

## Future work

Evaluate runtime and memory efficiency, add correctness and reproducibility checks, compare more cache policies, and investigate hybrid generation/optimisation or adaptive prompting. A unified experiment entry point with explicit parameters and uncertainty reporting would make reproduction easier.
