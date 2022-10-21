from central_application import log_parser 

def main():
    log_parser.grep("resources/test.txt","-c 1")
    res = log_parser.parse_with_re("resources/test2.txt","-sdfbasdf 123")
    for i in res:
        print(i)

if __name__ == "__main__":
    main()