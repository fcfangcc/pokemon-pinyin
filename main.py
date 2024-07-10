from draw import draw_a4
from pokemon import get_pokemon

if __name__ == "__main__":
    # todo: iterable
    pokemons = [get_pokemon(i, download_img=True) for i in range(1, 16)]
    ttf_path = "./simhei/SimHei.ttf"
    draw_a4(pokemons, output="test.png", font_path=ttf_path)
