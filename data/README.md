# Data

This data directory contains several real SMPS files that are used to test the
implementation.

We include the following problems:
- `electric`, a two-stage, fully continuous electricity generation problem.
- `sslp`, a two-stage, fully binary stochastic server location problem.

TODO multi-stage problems

## The `test` directory

This does not contain any serious SMPS problems, but only various types of
small, partial files to test the implementation via unit tests. Do *not* use
these yourself to verify the whole implementation - that's what the problems
described above are for!
