# Distributed experiment plan

Plan ID: `e37c5c85366b7d9e4020ae4941520605fb134aa2a5ca162995363e30b5bb59b6`
584 slices, 14016 runs, 6 servers, 64 jobs/server.
20,000,000 warmup + 20,000,000 measured instructions; NEMU difftest enabled.
Estimated 8.22h nominal / 10.28h with runtime margin.
800 seconds/run is an input estimate; SMT, memory bandwidth and workload variation can change it.

Run exactly one distinct server-XX.sh per server. Paths default to this shared workspace.
See register_reuse_distributed/README.md for relocation, cancellation, import and reporting.
