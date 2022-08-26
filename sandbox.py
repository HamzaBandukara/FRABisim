import subprocess

import py4j.java_gateway
from py4j.java_gateway import JavaGateway
from py4j.java_collections import JavaSet, JavaMap


def func():
    print("Executed!")


if __name__ == '__main__':
    x = subprocess.Popen("java -jar japfra/japfra.jar", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    try:
        gateway = JavaGateway(auto_field=True)
        FRA = gateway.entry_point.getJ()
        print(py4j.java_gateway.get_field(FRA, "transitions"))
        FRA.Run("tmp.pi", "q")
        print(py4j.java_gateway.get_field(FRA, "transitions"))
    except:
        print("JAPFRA ERROR!")
    for line in x.stdout: print(line)
    x.kill()