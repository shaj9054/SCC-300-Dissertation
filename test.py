from TYP import create_cyclic_sequence, create_random_sequence, create_locality_sequence, multiple_run_test
from wrapper import MinimalLRUWrapper, MinimalFifoWrapper, MinimalLifoWrapper, DetailedLifoWrapper, DetailedFifoWrapper, DetailedLRUWrapper
from charts import plot_results 

CACHE_CLASSES = {
    "Minimal LRU": MinimalLRUWrapper,
    "Minimal FIFO": MinimalFifoWrapper,
    "Minimal LIFO": MinimalLifoWrapper,
    "Detailed LIFO": DetailedLifoWrapper,
    "Detailed FIFO": DetailedFifoWrapper,
    "Detailed LRU": DetailedLRUWrapper,
}

SEQUENCES = {
    "Cyclic": create_cyclic_sequence,
    "Random": create_random_sequence,
    "Locality": create_locality_sequence
}

def test_wrappers():
    results = {
        "Minimal LRU": [],
        "Minimal FIFO": [],
        "Minimal LIFO": [],
        "Detailed LIFO": [],
        "Detailed FIFO": [],
        "Detailed LRU": []
    }
    # The sequence labels (in the order we run them)
    sequence_labels = list(SEQUENCES.keys())  # e.g. ["Cyclic", "Random", "Locality"]

    for seq_name, seq_func in SEQUENCES.items():
        print(f"\n=== Testing {seq_name} Sequence ===")

        for cache_name, cache_class in CACHE_CLASSES.items():
            avg_ratio = multiple_run_test(
                cache_class,
                seq_func,
                n_items=6,
                sequence_length=20,
                runs=10,
                cache_size=5
            )
            print(f"{cache_name} Hit Ratio (avg over 10 runs): {avg_ratio:.2%}")
            results[cache_name].append(avg_ratio * 100)


    # Step 2: After finishing all sequences, we plot
    plot_results(results)

if __name__ == "__main__":
    test_wrappers()
