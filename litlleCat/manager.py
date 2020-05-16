# run here
from application import manager
import www


def main():
    manager.run()


if __name__ == "__main__":
    try:
        import sys
        sys.exit( main() )
    except Exception as e:
        import traceback
        traceback.print_exc()





