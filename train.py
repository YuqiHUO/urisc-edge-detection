import sys
import argparse


def main():
    ##import libs
    
    #first, read the default.yaml or the user specific config file
    #then, modify the yaml with user-added options
    parser = argparse.ArgumentParser(description='Training phase for edge detection.', fromfile_prefix_chars='@')
    parser.add_argument('--config_file', '--config', nargs=1, default='configs/default.yaml', type=str, help='config .yaml file.')
    parser.add_argument('opt', nargs='*', type=str, help='user specific config.')
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()
    #if args.config_file is not None:
        #get_config_file(args.config)
    #if args.opt is not None:
        #get_config_from_list(args.opt)

if __name__ == '__main__':
    main()