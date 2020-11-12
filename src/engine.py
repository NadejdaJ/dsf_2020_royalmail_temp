import sys

def main(world):
	print("Hello", world)
	return


if __name__ == '__main__':
	main(sys.argv[1:][0])