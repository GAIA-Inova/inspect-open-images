# Inspect Open Images

Esse repositório existe para armazenar e disponibilizar
códigos criados para a exploração de imagens de datasets
de computação visual. O projeto surgiu para gerar materiais
de trabalho e novas perspectivas dentro do [Grupo de Arte e
Inteligência Artificial – GAIA](https://sites.usp.br/gaia/).

## Dev setup

```
# Faça um fork do projeto
$ git clone git@github.com:SEU-USUARIO/inspect-open-images.git

# Crie um ambiente virtual python usando a ferramente que preferir
# Aqui vou demostrar como fazer utilizando o pyenv
$ pyenv virtualenv 3.8.6 inspect-open-images
$ pyenv activate inspect-open-images

$ pip install -r requirements.txt
$ python open_images/cli.py --help
```

Para importar os dados, siga as instruções na página de [descrição
dos dados](/open_images/data/).

## Comandos

```
$ ./cli.py bbox --help
Usage: cli.py bbox [OPTIONS]

Options:
  -i, --img-id TEXT
  -q, --quantity INTEGER
  --help                  Show this message and exit.

```


Baixa imagens de treinamento do dataset e, para cada uma nova delas,
gera novas images divididas por 3 tipos de categoria:

  - Conteúdo: uma única imagem composta apenas pelos conteúdos dos
    bouding boxes com as anotações sobre a imagem. O arquivo final chama-se
  `content.png`.
  - Borda: uma única imagem composta pelas áreas da imagem não compreendidas
    pelo conjunto de áreas delimitadas pelos bounding boxes com anotações da
    imagem. O arquivo final chama-se `border.png`.
  - Objetos: várias imagens, uma para cada objeto anotado na imagem original,
    sendo um recorte do objeto em si. Por exemplo, se uma das imagens possui uma
    anotação de uma pessoa em uma área de 64x220 pixels, isso resultará em um
    arquivo nomeado `01-person.png` coa mesma dimensão da área da anotação.

### Colaboradores

- Bernardo Fontes
