# Distributed experiment plan

Plan ID: `f4267c536222599d1155b43b755f0a5e2a0161b8ebd69d173e17883d42880b7a`
1 slices, 8 runs, 1 servers, 2 jobs/server.
10,000 warmup + 20,000 measured instructions; NEMU difftest enabled.
Estimated 0.01h nominal / 0.01h with runtime margin.
800 seconds/run is an input estimate; SMT, memory bandwidth and workload variation can change it.

Run exactly one distinct server-XX.sh per server. Paths default to this shared workspace.
See register_reuse_distributed/README.md for relocation, cancellation, import and reporting.
