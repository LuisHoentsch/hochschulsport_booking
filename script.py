from typing import Tuple
import sys
import datetime
import business_logic


def load_config(path: str) -> Tuple[str]:
    return tuple(open(path, "r").read().split("\n")[:3])


print(datetime.datetime.now())
if __name__ == "__main__":
    if len(sys.argv) == 2:
        print(business_logic.book(*load_config(sys.argv[1])))
    elif len(sys.argv) == 4:
        print(business_logic.book(*sys.argv[1:]))
    else:
        print("Usage:\n\tscript.py <email> <password> <course>\n\tscript.py <path/to/config.txt>")
print(str(datetime.datetime.now()) + "\n\n")
