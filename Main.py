import argparse
from Solution import Queens_game

def main():
    parser = argparse.ArgumentParser(description="Queens Game Solver")
    parser.add_argument("size", nargs="?", type=int, help="Enter the board size (e.g., 4, 8, 10)")

    args = parser.parse_args()

    if args.size is None:
        while True:
            try:
                args.size = int(input("Enter the board size (e.g., 4, 8, 10): "))
                if args.size > 0:
                    break
                else:
                    print("Please enter a positive integer.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    game = Queens_game(args.size)
    game.main()

if __name__ == "__main__":
    main()
