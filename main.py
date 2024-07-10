import fire

from draw import draw_pdf
from pokemon import Pokemon


class Main(object):
    def range(
        self,
        start: int,
        end: int,
        ttf_path: str = "./simhei/SimHei.ttf",
        output: str = "output_a4.pdf",
    ):
        """python main.py range 1 10"""
        if start >= end or start < 1 or end > 1100:
            raise ValueError("开始和结束必须在1-1100以内")
        pokemons = [Pokemon.from_pokemon_cn(i) for i in range(start, end + 1)]
        draw_pdf(iter(pokemons), output, font_path=ttf_path)

    def choice(
        self,
        *args,
        ttf_path: str = "./simhei/SimHei.ttf",
        output: str = "output_a4.pdf",
    ):
        """python main.py choice 1 2 3"""
        pokemons = (Pokemon.from_pokemon_cn(int(i)) for i in args)
        draw_pdf(pokemons, output, font_path=ttf_path)


if __name__ == "__main__":
    fire.Fire(Main)
