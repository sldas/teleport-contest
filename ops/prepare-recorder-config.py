#!/usr/bin/env python3
"""Complete Linux recorder installation using upstream sample configuration.
Only adjusts optional crash-debugger settings when that executable is absent.
Never modifies the source sample, canonical fixtures, or an existing config.
"""
from pathlib import Path
root=Path(__file__).resolve().parent.parent
src=root/'nethack-c/recorder/sys/unix/sysconf'
dst=root/'nethack-c/recorder/install/games/lib/nethackdir/sysconf'
if not dst.exists():
 text=src.read_text()
 if not Path('/usr/bin/gdb').exists():
  text=text.replace('GDBPATH=/usr/bin/gdb','# GDBPATH omitted: debugger unavailable in this hosted runtime')
  text=text.replace('PANICTRACE_GDB=1','PANICTRACE_GDB=0')
 dst.write_text(text)
 print('Installed upstream sysconf with available crash-debugging settings.')
else:
 print('Preserved existing recorder sysconf.')
