from Picture import Picture

def main():
    file_path = input("Enter the image file path: ")
    m = float(input("Enter the value of m: "))
    n = float(input("Enter the value of n: "))

    picture = Picture(file_path)

    near_neighbour = picture.nearest_neighbour_interpolation(m, n)
    near_neighbour.save_picture('1_vizinho.ppm')

    four_neighbour = picture.four_neighbour_interpolation(m, n)
    four_neighbour.save_picture('4_vizinhos.ppm')


if __name__ == '__main__':
    main()