import os.path
import sys

from mkfilename import make_filename


def main():
    if len(sys.argv) == 2:
        print(make_filename(sys.argv[1]))
        return
    import pyperclip

    if len(sys.argv) == 1 and (clipboard := pyperclip.paste().strip()):
        print(f"clipboard had: {clipboard}")
        print(f"clipboard contains: {(content := make_filename(clipboard))}")
        pyperclip.copy(content)
    else:
        prg = os.path.basename(sys.argv[0])
        print(f"{prg} <string> | (without arg, clipboard is used)")


if __name__ == "__main__":
    main()
