#!/usr/bin/env python3
"""Troca as fotos do template pelas fotos do ateliê da Raquel.

Coloque as fotos (jpg, png ou webp) em fotos/ com estes nomes e rode,
a partir da raiz do repositório:

    python3 tools/trocar_fotos.py

    fotos/raquel.jpg     retrato da Raquel (bloco "Quem te recebe")
    fotos/casal.jpg      oficina de casal (card, painel e página de reservas)
    fotos/familia.jpg    oficina em família
    fotos/infantil.jpg   oficina infantil
    fotos/noturna.jpg    aula noturna
    fotos/atelie.jpg     o ateliê por dentro (foto grande do convite final)
    fotos/insta-1.jpg … fotos/insta-6.jpg   faixa "Siga no Instagram"

Cada foto é recortada no formato do arquivo original (sem distorcer) e salva
por cima dele, com o mesmo nome. Fotos que não existirem são puladas.
Os originais ficam em fotos/_originais/ na primeira vez que o script roda.
"""
import os
import shutil
import sys

from PIL import Image, ImageOps

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(RAIZ, 'assets', 'framerusercontent.com', 'images')
FOTOS = os.path.join(RAIZ, 'fotos')

SLOTS = {
    'raquel': ['A3SagsjNyizU4wknNZa1zXCFY', 'BN6PlTInKz6LKQYbj2KmWgZwZQ',
               'mo1KmRfXXVXtvFOARfp2ytGDpFM', 'TiqUFRPqbHDpY0gEHLm1g8CZ9s'],
    'casal': ['pBye4SLmcbj9cwwzjeSIbAiQeA', 'PGtB1eeiQhQM03pAOh4G4fUQvSo'],
    'familia': ['FkHT22wYhk5caanD7hTk2LIh0'],
    'infantil': ['nxI5dEc30UG9ZMDijEn1tELSqK4', 'qmgvvTEURvizwYOPuVheGzj3W8'],
    'noturna': ['ad2KA1o5R39dx0C60w5WHDgQR58'],
    'atelie': ['4hH1CCf6KQlCaH7hPsbvtDZwA5Y'],
    'insta-1': ['Xk1V4hjyowtT66nRBKhNKZUWBc'],
    'insta-2': ['nxI5dEc30UG9ZMDijEn1tELSqK4'],
    'insta-3': ['CoBInmgB2z1XtEZqO96gCHsrNmU'],
    'insta-4': ['YFvjbeGAtWhXcreN6gmPE1qsYYg'],
    'insta-5': ['DQ06a6U1YUIYUAQpkWzLeXfMkE'],
    'insta-6': ['dB5F7OhYcohZ8EU9S94O6lsjfto'],
}
EXT = ('.jpg', '.jpeg', '.png', '.webp', '.JPG', '.JPEG', '.PNG')


def achar(slot):
    for e in EXT:
        p = os.path.join(FOTOS, slot + e)
        if os.path.exists(p):
            return p
    return None


def main():
    if not os.path.isdir(FOTOS):
        sys.exit('Crie a pasta fotos/ com as imagens (veja o topo deste arquivo).')
    bak = os.path.join(FOTOS, '_originais')
    os.makedirs(bak, exist_ok=True)
    feitos = 0
    for slot, alvos in SLOTS.items():
        src = achar(slot)
        if not src:
            continue
        foto = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
        for nome in alvos:
            dst = os.path.join(IMG, nome + '.webp')
            if not os.path.exists(dst):
                print('  (não achei', nome, ')')
                continue
            if not os.path.exists(os.path.join(bak, nome + '.webp')):
                shutil.copy2(dst, bak)
            w, h = Image.open(dst).size
            ImageOps.fit(foto, (w, h), Image.LANCZOS, centering=(0.5, 0.45)).save(dst, 'WEBP', quality=84, method=6)
            feitos += 1
        print('ok', slot, '→', len(alvos), 'arquivo(s)')
    print(feitos, 'imagens trocadas.' if feitos else 'Nenhuma foto encontrada em fotos/.')


if __name__ == '__main__':
    main()
