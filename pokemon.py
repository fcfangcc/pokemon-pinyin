import json
import sys
from pathlib import Path

import requests
from lxml import html

BASE_URL = "https://www.pokemon.cn"


def get_pokemon_name(tree):
    PATH = '//*[contains(@class, "pokemon-slider__main-name")]'
    elements = tree.xpath(PATH)
    if len(elements) != 1:
        raise ValueError("获取名字失败")
    return elements[0].text_content().strip()


def list_pokemon_attribute(tree):
    PATH = '//*[contains(@class, "pokemon-type__type")]'
    elements = tree.xpath(PATH)
    return [i.text_content().strip() for i in elements]


def list_pokemon_weakness(tree):
    PATH = '//*[contains(@class, "pokemon-weakness__btn")]'
    elements = tree.xpath(PATH)
    return [i.text_content().strip() for i in elements]


def get_pokemon_img_url(tree):
    PATH = '//*[contains(@class, "pokemon-img__front")]'
    elements = tree.xpath(PATH)
    if len(elements) != 1:
        raise ValueError("获取img失败")
    return BASE_URL + elements[0].attrib["src"].strip()


def download_pokemon_img(pokedex: int, url: str, to_dir: str) -> str | None:
    dir_path = Path(to_dir)
    if not dir_path.exists():
        dir_path.mkdir(parents=True)
        print(f"文件夹`{to_dir}`不存在，自动创建")

    local_path = dir_path.joinpath(f"{pokedex:04}.png")
    if Path(local_path).exists():
        return local_path.absolute().as_posix()

    response = requests.get(url)
    if response.status_code == 200:
        with open(local_path, "wb") as file:
            file.write(response.content)
        return local_path.absolute().as_posix()
    else:
        print("无法下载图片，状态码：", response.status_code)
    return None


def get_pokemon(pokedex: int, download_img: bool = False):
    cache_dir = Path("./.cache")
    if not cache_dir.exists():
        cache_dir.mkdir(parents=True)

    cache_path = cache_dir.joinpath(f"{pokedex}.json")
    if cache_path.exists():
        with open(cache_path, "rb") as f:
            pokemon = json.load(f)
    else:
        url = BASE_URL + f"/play/pokedex/{pokedex:04}"
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            raise ValueError("get response error")

        html_tree = html.fromstring(response.content)
        with open(cache_path, "w") as f:
            pokemon = {}
            pokemon["name"] = get_pokemon_name(html_tree)
            pokemon["attributes"] = list_pokemon_attribute(html_tree)
            pokemon["weakness"] = list_pokemon_weakness(html_tree)
            pokemon["img_url"] = get_pokemon_img_url(html_tree)
            if download_img:
                img_local_path = download_pokemon_img(
                    pokedex, pokemon["img_url"], "./imgs"
                )
                pokemon["img_local_path"] = img_local_path
            json.dump(pokemon, f, indent=4)
    return pokemon


if __name__ == "__main__":
    args = sys.argv[1:]
    pokedexs = [int(i) for i in args]
    for pokedex in pokedexs:
        pokemon = get_pokemon(pokedex, download_img=True)
        print(f"pokemon:{pokedex:04}, data: {pokemon}")
