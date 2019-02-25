# k-terminal-cut

A Branch and Bound Algorithm based using Isolating Cuts for the k-terminal cut problem.

This is research code. It is a tool for studying properties of the branch-and-bound approach to the k-terminal cut problem. Its performance has not been optimized for large-scale projects (greater than 1,000,000 vertices).

If you use our algorithm in further research, please cite our paper: [Isolation Branching: A Branch and Bound Algorithm for the k-Terminal Cut Problem
](https://doi.org/10.1007/978-3-030-04651-4_42).

## Example Useage

```
def test_graph_tutte():
    from networkx.generators.small import tutte_graph
    from ktcut.isolation_branching import isolation_branching
    graph = tutte_graph()
    terminals = [1, 17, 34]
    partition, cut_value = isolation_branching(graph, terminals)
```

## Running the tests

```
pytest
```

## Built With

* [Python](https://www.python.org/)
* [NetworkX](https://networkx.github.io/)

## Authors

* **Mark Velednitsky**

## License

Apache 2.0