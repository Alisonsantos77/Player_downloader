# 🎵 Spotiplay

![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![Flet Version](https://img.shields.io/badge/Flet-0.2.2-blueviolet)

Spotiplay é uma aplicação que permite baixar músicas do Spotify e reproduzi-las diretamente em seu desktop. Desenvolvido utilizando a biblioteca Flet para Python, o Spotiplay combina funcionalidades de download e player de música em uma interface amigável e moderna.

## 🌟 Funcionalidades

- **Player de Música**:
  - 🎶 Reproduz músicas armazenadas localmente.
  - 🔊 Controle de volume ajustável.
  - ⏯️ Controle de reprodução: play, pause, próximo, anterior e shuffle.
  - 📜 Exibição do nome da música e duração atual.

- **Downloader de Música do Spotify**:
  - 🔗 Baixa músicas do Spotify através de links.
  - 📂 Seleção do diretório de download.
  - 📉 Barra de progresso do download.
  - 📜 Histórico de diretórios de download utilizados.

## 🛠️ Requisitos

- Python 3.7 ou superior.
- Bibliotecas: `flet`, `spotdl`.

## 🚀 Instalação

1. Clone este repositório:
   ```bash
   git clone https://github.com/Alisonsantos77/Player_downloader.git
   cd Player_downloader
   ```

2. Instale as dependências:
   ```bash
   pip install flet spotdl
   ```

2. Baixe o ffmpeg:
   ```bash
   spotdl --download-ffmpeg
   ```

## 🕹️ Como usar

1. Execute a aplicação:
   ```bash
   flet run main.py
   ```

2. A interface da aplicação será aberta. Utilize os botões de controle para reproduzir músicas ou baixar novas músicas do Spotify.

## 📂 Estrutura do Código

- `main(page: ft.Page)`: Função principal que inicializa a aplicação e configura a interface do usuário.
- Funções de controle do player:
  - `music_name(musica)`: Atualiza o nome da música em reprodução.
  - `music_seconds(e)`: Atualiza a exibição dos segundos atuais da música.
  - `music_time(musica)`: Atualiza a duração total da música.
  - `state_music()`: Controla o estado da música (play/pause).
  - `play_music(e)`: Controla a reprodução da música.
  - `slider_volume(e)`: Ajusta o volume da música.
  - `random_music(e)`: Reproduz uma música aleatória.
  - `prox_music(_)`: Reproduz a próxima música.
  - `voltar_musica(_)`: Reproduz a música anterior.
- Funções de download:
  - `download_spotify(e)`: Faz o download de músicas do Spotify.
  - `get_directory_result(e: FilePickerResultEvent)`: Seleciona o diretório de download.
  - `save_path_storage(new_path)`: Salva o caminho do diretório de download no armazenamento local.
- Funções de popup:
  - `open_popup(e)`: Abre o popup de informações.
  - `close_popup(e)`: Fecha o popup de informações.

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
