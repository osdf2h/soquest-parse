from settings import ADDRESS
from parse_soquest import SoQuest


def main():
    soquest = SoQuest(ADDRESS)
    soquest.parse_data()


if __name__ == '__main__':
    main()
