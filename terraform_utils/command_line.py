from argparse import ArgumentParser


def build_parser():
    parser = ArgumentParser()
    parser.add_argument('-t', '--target',  type=str, help='tfvars search target')
    parser.add_argument('-k', '--key',   type=str, help='variable to read')
    parser.add_argument('-c', '--component', choices=['bucket', 'object', 'table', 'env'])
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    print(args)
