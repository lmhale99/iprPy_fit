
We don't need lots of communication between processors!

Each processor loads only a fraction of the structures from the files. Then, the evaluation function runs only for those structures and passes the final error value out to be summed (reduce sum).

Example of how to do something similar:
https://stackoverflow.com/questions/37159923/parallelize-a-function-call-with-mpi4py

We probably need two "sends": a stopping flag like in the code and something to indicate that the next eval cycle is called, probably either PotentialLAMMPS JSON filename or contents.
