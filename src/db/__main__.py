try:
    from .tui import run
except ImportError:  # pragma: no cover
    from tui import run


def main() -> None:
    run()


if __name__ == "__main__":  # pragma: no cover
    main()
