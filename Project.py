import XMLParser as parser
import NetworkGraph as ng


def main ():
    conf = parser.ParseDBLP()
    network = ng.Network(conf)
    network.DrawGraph()


if __name__ == "__main__":
    main()
