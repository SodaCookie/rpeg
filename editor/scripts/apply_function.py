"""Script to apply a function to """
import sys
from os.path import relpath
import traceback

from engine.serialization.serialization import deserialize, serialize

if len(sys.argv) == 3:
    print("Reading data: %s" % relpath(sys.argv[1]))
    data = deserialize(sys.argv[1])
    with open(sys.argv[2], "r") as prog:
        print("Executing script: %s" % relpath(sys.argv[2]))
        try:
            exec(prog.read(), {"data": data})
            print("Script finished. Writing to file")
            serialize(data, sys.argv[1])
        except:
            print("Error occurred. Data was not written.")
            traceback.print_exc()
else:
    print("Usage: apply_function <pickle> <python script>")