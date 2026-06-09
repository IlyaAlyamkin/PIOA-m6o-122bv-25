try:
    from .tui import run
except ImportError:  
    from tui import run


def main() -> None:
    run()


if __name__ == "__main__":  
    main()
