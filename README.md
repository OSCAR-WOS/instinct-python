# instinct-python

Detects gif crashers along with removal, needs bare metal otherwise can run into memory issues. Requires ffmpeg binaries, making sure to correctly setup PATH. Does not work with Windows due to the inability to create a DEVNULL shell, being unable to prematurely exit, thenceforth fully occupying memory.

Uses TOKEN stored in the os

$ TOKEN={token}
