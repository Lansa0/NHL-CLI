import ArgumentsHandler
import RequestsHandler
import OutputHandler


def main() -> None:

    Arguments = ArgumentsHandler.run()

    Response : dict = RequestsHandler.getData(Arguments)

    OutputHandler.renderOutput(Arguments, Response)

if __name__ == "__main__":
    main()