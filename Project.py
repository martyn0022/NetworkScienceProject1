import XMLParser as parser
import NetworkGraph as ng


def main ():
    conf = parser.ParseDBLP()
    ng.initialize(conf)


if __name__ == "__main__":
    main()
