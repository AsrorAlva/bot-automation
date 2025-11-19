# bagian import (tambahkan ini)
import sys

# Cross-platform masked password input (tampilkan '*' saat ketik)
def get_password_masked(prompt="Password: "):
    """Baca password dari terminal dan tampilkan '*' untuk tiap karakter.
    Works on Windows (msvcrt) and Unix (termios + tty).
    """
    if sys.platform.startswith("win"):
        import msvcrt
        sys.stdout.write(prompt)
        sys.stdout.flush()
        buf = []
        while True:
            ch = msvcrt.getch()
            if ch in (b'\r', b'\n'):  # Enter
                sys.stdout.write("\n")
                return b"".join(buf).decode()
            if ch == b'\x03':  # Ctrl-C
                raise KeyboardInterrupt
            if ch == b'\x08':  # Backspace
                if buf:
                    buf.pop()
                    # move cursor back, overwrite with space, move back again
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue
            # normal char
            buf.append(ch)
            sys.stdout.write("*")
            sys.stdout.flush()
    else:
        # Unix-like
        import tty
        import termios
        sys.stdout.write(prompt)
        sys.stdout.flush()
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            buf = []
            while True:
                ch = sys.stdin.read(1)
                if ch in ("\r", "\n"):
                    sys.stdout.write("\n")
                    return "".join(buf)
                if ch == "\x03":  # Ctrl-C
                    raise KeyboardInterrupt
                if ch in ("\x7f", "\b"):  # Backspace (DEL or BS)
                    if buf:
                        buf.pop()
                        sys.stdout.write("\b \b")
                        sys.stdout.flush()
                    continue
                buf.append(ch)
                sys.stdout.write("*")
                sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
