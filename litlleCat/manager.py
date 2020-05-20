# run here

# You must import the app_fk or uwsgi cans't not find the app_fk
from application import manager, app_fk
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





