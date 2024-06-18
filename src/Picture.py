from RGB import RGB

class Picture:
    format : str = None
    height : int = 0
    width : int = 0
    max_color : int = 0

    pixels : list[list[RGB]]

    def __init__(self, file_path : str = None, m : float = 1, n : float = 1):
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

        self.sampling(m,n)

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

    def sampling(self, m : float, n : float) -> None:
        self.height = int(self.height * n) #Multiplica a altura por m
        self.width = int(self.width * m) #Multiplica a largura por n
        new_pixels = [[None for _ in range(self.width)] for _ in range(self.height)]
        for i in range(self.height):
            for j in range(self.width):
                new_pixels[i][j] = self.pixels[int(i/m)][int(j/n)] # Atribui o valor do pixel da imagem original na nova imagem

        self.pixels = new_pixels

    def nearest_neighbour_interpolation(self): #Interpolação por vizinho mais próximo
        for i in range(self.height):
            for j in range(self.width):
                if self.pixels[i][j] is None: #Se o pixel for None
                    self.pixels[i][j] = self.pixels[i - 1][j] if i > 0 else self.pixels[i + 1][j] #Atribui o valor do pixel do vizinho de cima ou de baixo

    def four_neighbour_interpolation(self):
        for i in range(self.height):
            for j in range(self.width):
                if self.pixels[i][j] is None:
                    neighbours = [] #Cria uma lista de vizinhos
                    if i > 0:
                        neighbours.append(self.pixels[i - 1][j]) #Adiciona o vizinho de cima
                    if i < self.height - 1:
                        neighbours.append(self.pixels[i + 1][j]) #Adiciona o vizinho de baixo
                    if j > 0:
                        neighbours.append(self.pixels[i][j - 1]) #Adiciona o vizinho da esquerda
                    if j < self.width - 1:
                        neighbours.append(self.pixels[i][j + 1]) #Adiciona o vizinho da direita
                    self.pixels[i][j] = RGB(sum(pixel.r for pixel in neighbours) // len(neighbours),
                                            sum(pixel.g for pixel in neighbours) // len(neighbours),
                                            sum(pixel.b for pixel in neighbours) // len(neighbours)) #Atribui a média dos valores dos vizinhos

    def save_picture(self, file_path : str) -> None:
        with open(file_path, 'w') as file:
            file.write(str(self))
            file.close()