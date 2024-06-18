from RGB import RGB

class Picture:
    format : str = None
    height : int = 0
    width : int = 0
    max_color : int = 0

    pixels : list[list[RGB]]

    def __init__(self, file_path : str = None):
        if file_path is not None:
            try:
                with open(file_path, 'r') as file:
                    self.format = file.readline().strip()
                    self.width, self.height = map(int, file.readline().split())
                    self.max_color = int(file.readline())
                    self.pixels = [[None for _ in range(self.width)] for _ in range(self.height)]
                    pixel_values = list(map(int, file.read().split()))
                    for i in range(self.height):
                        for j in range(self.width):
                            index = 3 * (i * self.width + j)
                            self.pixels[i][j] = RGB(pixel_values[index], pixel_values[index+1], pixel_values[index+2])
                file.close()
            except (Exception) as e:
                print(f'Error: {e}')
        else:
            self.height = 0
            self.width = 0
            self.max_color = 0
            self.pixels = [[RGB() for _ in range(self.width)] for _ in range(self.height)]


    # overloading the - operator
    def __sub__(self, other):
        if self.width != other.width or self.height != other.height:
            raise ValueError('These pictures have different dimensions')

        new_pixels = [[RGB() for _ in range(self.width)] for _ in range(self.height)]

        for i in range(self.height):
            for j in range(self.width):
                new_pixels[i][j] = self.pixels[i][j] - other.pixels[i][j]

        new_picture = Picture()

        new_picture.format = self.format
        new_picture.width = self.width
        new_picture.height = self.height
        new_picture.max_color = self.max_color
        new_picture.pixels = new_pixels

        return new_picture

    def __str__(self) -> str:
        string = str(self.format) + '\n'
        string += str(self.width) + ' ' + str(self.height) + '\n'
        string += str(self.max_color) + '\n'

        for i in range(self.height):
            for j in range(self.width):
                string += str(self.pixels[i][j]) + '\n'

        return string

    def sampling(self, m : float, n : float):
        new_width = int(self.width * m)
        new_height = int(self.height * n)

        new_pixels = [[RGB() for _ in range(new_width)] for _ in range(new_height)]

        new_picture = Picture()

        new_picture.format = self.format
        new_picture.width = new_width
        new_picture.height = new_height
        new_picture.max_color = self.max_color
        new_picture.pixels = new_pixels

        return new_picture

    def nearest_neighbour_interpolation(self, m : float, n : float): #Interpolação por vizinho mais próximo
        new_picture = self.sampling(m,n)
        for i in range(new_picture.height):
            for j in range(new_picture.width):
                x = int(j/m)
                y = int(i/n)
                new_picture.pixels[i][j] = self.pixels[y][x]

        return new_picture

    def four_neighbour_interpolation(self, m : float, n : float):
        new_picture = self.sampling(m,n)
        for i in range (new_picture.height):
            for j in range (new_picture.width):
                x_ratio = (float(j)/new_picture.width) * (self.width - 1)
                y_ratio = (float(i)/new_picture.height) * (self.height - 1)
                x = int(x_ratio)
                y = int(y_ratio)
                diff_x = x_ratio - x
                diff_y = y_ratio - y

                if (x < self.width - 1) and (y < self.height - 1):
                    n1 = self.pixels[y][x]
                    n2 = self.pixels[y][x+1]
                    n3 = self.pixels[y+1][x]
                    n4 = self.pixels[y+1][x+1]

                    new_picture.pixels[i][j] = RGB(
                        int(n1.r * (1 - diff_x) * (1 - diff_y) + n2.r * (diff_x) * (1 - diff_y) + n3.r * (diff_y) * (
                                    1 - diff_x) + n4.r * (diff_x * diff_y)),
                        int(n1.g * (1 - diff_x) * (1 - diff_y) + n2.g * (diff_x) * (1 - diff_y) + n3.g * (diff_y) * (
                                    1 - diff_x) + n4.g * (diff_x * diff_y)),
                        int(n1.b * (1 - diff_x) * (1 - diff_y) + n2.b * (diff_x) * (1 - diff_y) + n3.b * (diff_y) * (
                                    1 - diff_x) + n4.b * (diff_x * diff_y))
                    )
                else:
                    new_picture.pixels[i][j] = self.pixels[y][x]

        return new_picture

    def save_picture(self, file_path : str) -> None:
        with open(file_path, 'w') as file:
            file.write(str(self))
            file.close()