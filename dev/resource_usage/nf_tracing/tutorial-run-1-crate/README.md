# Representing resource usage: Nextflow tracing example

The `tutorial.nf` workflow used for this example has been copied verbatim from the [Get started section of the Nextflow documentation](https://github.com/nextflow-io/nextflow/blob/f48a473c070f297bce6f97f6b076e4e92d25e00a/docs/getstarted.md), which is © Copyright 2023, Seqera Labs, S.L. and [distributed under](https://github.com/nextflow-io/nextflow/blob/f48a473c070f297bce6f97f6b076e4e92d25e00a/docs/README.md#license) the [CC BY-SA 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/).

The purpose of this exercise is to try a representation of [resource usage](https://github.com/ResearchObject/workflow-run-crate/issues/10) in a Workflow Run RO-Crate.

The tutorial has been run as follows:

```console
bash-4.2# date
Wed May 17 14:33:13 UTC 2023

bash-4.2# nextflow -v
nextflow version 23.05.0-edge.5861

bash-4.2# nextflow run tutorial.nf
N E X T F L O W  ~  version 23.05.0-edge
Launching `tutorial.nf` [lonely_dubinsky] DSL2 - revision: e61bd183fe
executor >  local (3)
[cd/ca5a2f] process > splitLetters       [100%] 1 of 1 ✔
[9f/7c259b] process > convertToUpper (1) [100%] 2 of 2 ✔
WORLD!
HELLO
```

With the following configuration:

```yaml
trace {
    enabled = true
    raw = true
}
```

Producing the `trace-20230517-52413675.txt` trace report.

To generate the RO-Crate:

```
pip install -r requirements.txt
python make_crate.py tutorial-run-1-crate
```
