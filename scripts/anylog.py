import sys
import anylog_node.cmd.user_cmd as user_cmd

def main():
    argv = sys.argv
    argc = len(argv)

    user_input = user_cmd.UserInput()
    user_input.process_input(arguments=argc, arguments_list=argv)


if __name__ == '__main__':
    main()
