from Picture import Picture

def main():
    file_path = input("Enter the image file path: ")
    m = float(input("Enter the value of m: "))
    n = float(input("Enter the value of n: "))

    picture = Picture(file_path, m, n)
    picture.nearest_neighbour_interpolation()
    picture.four_neighbour_interpolation()

    picture.save_picture('output.ppm')

if __name__ == '__main__':
    main()