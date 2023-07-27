from settings import ADDRESS, SIGNATURE
from parsers.soquest import SoQuest


def main():
    soquest = SoQuest(ADDRESS, SIGNATURE)
    soquest.parse_data()


if __name__ == '__main__':
    main()
