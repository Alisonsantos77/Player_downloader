import os
import random
import subprocess
import sys
from time import sleep
import flet as ft
from flet import (
    FilePicker,
    FilePickerResultEvent,
    Text,
)


def main(page: ft.Page):
    page.bgcolor = '#080C1C'
    page.scroll = ft.ScrollMode.AUTO
    page.window_height = 900
    page.window_width = 900
    pb = ft.ProgressBar(width=400, value=0, bgcolor=ft.colors.BLUE, color=ft.colors.WHITE)

    # Refs
    animacao_componente = ft.Ref[ft.Lottie]()
    troca_componente = ft.Ref[ft.IconButton]()
    titulo_musica = ft.Ref[ft.Text]()
    segundos_text = ft.Ref[ft.TextSpan]()
    minutos_text = ft.Ref[ft.TextSpan]()
    barra_time = ft.Ref[ft.TextSpan]()
    icone_destino = ft.Ref[ft.IconButton]()

    musicas = os.listdir("assets/audios")

    def music_name(musica):
        audio1.data = musica
        audio1.update()
        titulo_musica.current.value = f"{musica}"
        titulo_musica.current.update()
        titulo_musica.current.visible = True
        titulo_musica.current.update()

    def music_seconds(e):
        try:
            ms_real = audio1.get_current_position()
            if ms_real != 'null':
                segundos_real = ms_real / 1000
                calcula_segundos = int(segundos_real % 60)

                segundos_text.current.text = f"{calcula_segundos}"
                segundos_text.current.update()

                if ms_real > 1000:
                    segundos_text.current.visible = True

            else:
                print("Erro: Posição atual não disponível.")
        except Exception as e:
            print(f"Um erro ocorreu: {e}")

    def music_time(musica):
        tempo_total = audio1.get_duration()
        # Converte para segundos
        tempo_total_segundos = tempo_total / 1000

        # Calcula minutos e segundos do tempo total
        total_minutos = int(tempo_total_segundos // 60)
        total_segundos = int(tempo_total_segundos % 60)

        # Mostrar barra entre segundos e minutos
        barra_time.current.visible = True
        barra_time.current.update()

        # Atualizando o título da música com a posição atual e a duração total
        minutos_text.current.text = f"{total_minutos}:{total_segundos}"
        minutos_text.current.update()

    def state_music():
        tempo_atual = audio1.get_current_position()
        if audio1.on_loaded:
            troca_componente.current.icon = ft.icons.PLAY_CIRCLE_SHARP
            troca_componente.current.update()
        if audio1.release and tempo_atual < 1000:
            troca_componente.current.icon = ft.icons.PLAY_CIRCLE_SHARP
            troca_componente.current.update()
            animacao_componente.current.animate = False
            animacao_componente.current.update()
        if audio1.release and tempo_atual > 1000:
            audio1.update()
            audio1.play()
            troca_componente.current.icon = ft.icons.PLAY_CIRCLE_SHARP
            troca_componente.current.update()
            animacao_componente.current.animate = True
            animacao_componente.current.update()
            if audio1.play:
                troca_componente.current.icon = ft.icons.STOP_CIRCLE_SHARP
                troca_componente.current.update()
        else:
            print("Música finalizada")

    def play_music(e):
        posicao = audio1.get_current_position()
        if audio1.play and posicao < 1000:
            troca_componente.current.icon = ft.icons.STOP_CIRCLE_SHARP
            troca_componente.current.update()
            animacao_componente.current.animate = True
            animacao_componente.current.update()
            audio1.play()
            audio1.update()
            music_time(audio1.src)
            music_name(audio1.src)
        elif audio1.play and posicao > 500:
            audio1.release()
            state_music()

    def slider_volume(e):
        if e.control.on_change_end:
            audio1.volume = e.control.value / 100
            audio1.update()

    def random_music(e):
        if len(musicas) > 1:
            index = random.randint(0, len(musicas) - 1)
            audio1.src = musicas[index]
            audio1.update()
        else:
            print("Não há mais músicas para reproduzir.")

    def prox_music(_):
        if len(musicas) > 1:
            index = (musicas.index(audio1.src) + 1) % len(musicas)
            audio1.src = musicas[index]
            audio1.update()
        else:
            print("Não há mais músicas para reproduzir.")

    def voltar_musica(_):
        if len(musicas) > 1:
            index = (musicas.index(audio1.src) - 1) % len(musicas)
            audio1.src = musicas[index]
            audio1.update()

        else:
            print("Não há mais músicas para reproduzir.")

    audio1 = ft.Audio(
        src=musicas[0],
        autoplay=False,
        volume=1,
        on_loaded=lambda _: print("Loaded"),
        on_position_changed=music_seconds

    )
    page.overlay.append(audio1)

    # Caixa de dialogo para selecionar o diretorio do download
    def get_directory_result(e: FilePickerResultEvent):
        directory_path.value = e.path if e.path else "Cancelled!"
        directory_path.update()

    get_directory_dialog = FilePicker(on_result=get_directory_result)
    directory_path = Text('', visible=False)
    page.overlay.extend([get_directory_dialog, directory_path])

    # Função para baixar o música do Spotify
    def download_spotify(e):
        link = input_link.value
        paths = page.client_storage.get('path.downloader')
        if paths is None:
            paths = []

        destino = directory_path.value if directory_path.value else paths[-1]['path'] if paths else None

        if not link.strip() or destino is None:
            label_download.value = 'Preencha todos os campos'
            label_download.update()
            return
        try:

            label_download.value = 'Baixando...'
            label_download.update()
            pb.value = 0.4
            pb.update()
            subprocess.run([sys.executable, '-m', 'spotdl', '--output', destino, link])
            label_download.value = 'Download concluído!'
            label_download.update()
            pb.value = 1
            pb.update()
            sleep(0.3)
            save_path_storage(new_path=destino)
            input_link.value = ""
            input_link.update()

        except Exception as e:
            label_download.value = f'Erro: {e}'
            label_download.update()

    def save_path_storage(new_path):
        # Verifica se existe um caminho anterior
        current_paths = page.client_storage.get('path.downloader')

        # Se não houver caminhos anteriores, inicializa como uma lista vazia
        if not current_paths:
            current_paths = []

        # Adiciona o novo caminho à lista
        current_paths.append({'path': new_path})

        # Armazena a lista atualizada de caminhos
        page.client_storage.set('path.downloader', current_paths)

    def open_popup(e):
        page.dialog = popup
        popup.open = True
        page.update()

    def close_popup(e):
        page.dialog = popup
        popup.open = False
        page.update()

    popup = ft.AlertDialog(
        title=ft.Text(value='Bem vindo ao Spotiplay'),
        content=ft.Text(value='Projeto desenolvido por Alison santos'),
        content_padding=ft.padding.all(30),
        inset_padding=ft.padding.all(10),
        adaptive=True,
        actions=[
            ft.TextButton(
                text='Fechar', style=ft.ButtonStyle(
                    color=ft.colors.RED,
                    shape=ft.RoundedRectangleBorder(radius=5),

                ),
                on_click=close_popup,
            ),
        ]

    )

    downloader_side = ft.Container(
        col={'xs': 12, 'md': 6},
        bgcolor=ft.colors.BLUE,
        padding=ft.padding.all(30),
        aspect_ratio=9 / 16,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            controls=[
                ft.Container(
                    col={'xs': 12, 'md': 6},
                    shadow=ft.BoxShadow(
                        blur_radius=500,
                        color=ft.colors.BLUE_100),
                    content=ft.Image(
                        src='assets/images/monkey_banner.png',
                        col={'xs': 6, 'md': 3},
                    ),
                ),

                ft.ResponsiveRow(
                    col={'xs': 6, 'sm': 3},
                    vertical_alignment=ft.alignment.center,
                    controls=[
                        ft.Column([
                            label_download := ft.Text(value='Aguardando link',
                                                      weight=ft.FontWeight.BOLD,
                                                      color=ft.colors.WHITE54),
                            pb]),
                    ]

                ),
                ft.ResponsiveRow(
                    spacing=10,
                    vertical_alignment=ft.alignment.center,
                    col={'xs': 12, 'sm': 6},
                    controls=[
                        input_link := ft.TextField(
                            col=12,
                            label="Link",
                            hint_text="Insira seu link",
                            border_color=ft.colors.BLUE_200,
                            width=400),
                    ]
                ),
                ft.ResponsiveRow(
                    col={'xs': 12, 'sm': 6},
                    controls=[
                        ft.ElevatedButton(
                            col={'xs': 10, 'sm': 6},
                            text='Download',
                            on_click=download_spotify,
                            style=ft.ButtonStyle(
                                padding=ft.padding.all(20),
                                side={
                                    ft.MaterialState.DEFAULT: ft.BorderSide(width=2, color=ft.colors.BLUE_200)
                                },
                                bgcolor={
                                    ft.MaterialState.DEFAULT: ft.colors.BLUE_300,
                                },
                                color={
                                    ft.MaterialState.DEFAULT: ft.colors.WHITE,
                                    ft.MaterialState.HOVERED: ft.colors.BLUE_600,

                                }
                            )

                        ),

                        ft.IconButton(
                            col={'xs': 2, 'sm': 6},
                            ref=icone_destino,
                            icon=ft.icons.FOLDER_COPY_SHARP,
                            disabled=page.web,
                            on_click=lambda _: get_directory_dialog.get_directory_path(),
                            tooltip=f'{directory_path.value}' if f'{directory_path.value}' else 'Selecione um destino'
                        ),

                    ]
                )
            ],
        ),
    )

    player_side = ft.Container(
        col={'xs': 12, 'md': 6},
        padding=ft.padding.all(30),
        bgcolor='#0b0916',
        aspect_ratio=9 / 16,
        content=ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            spacing=50,
            controls=[
                ft.Row(
                    col=12,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.INFO_SHARP,
                            on_click=open_popup,
                        ),
                        ft.Text(
                            value='Home Music',
                            size=20,
                            color=ft.colors.WHITE,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.IconButton(icon=ft.icons.SETTINGS_SHARP,
                                      ),
                    ]
                ),
                ft.ResponsiveRow(
                    columns=12,
                    col={'xs': 12, 'sm': 8},
                    controls=[
                        ft.Card(
                            content=ft.Row(
                                scroll=ft.ScrollMode.HIDDEN,
                                alignment=ft.MainAxisAlignment.CENTER,
                                width=300,
                                controls=[
                                    ft.Lottie(
                                        ref=animacao_componente,
                                        src='https://lottie.host/4ad37fa5-52d9-44b5-a12d-033c338b6b3d/aw9QCDGF8E.json',
                                        width=350,
                                        repeat=True,
                                        reverse=False,
                                        animate=False,
                                        background_loading=True,
                                        visible=True,
                                    )

                                ]
                            ),
                            color='#33452'
                        ),
                    ]
                ),
                ft.Column(
                    controls=[
                        ft.Column(
                            alignment=ft.MainAxisAlignment.CENTER,
                            col=12,
                            controls=[
                                ft.Text(
                                    ref=titulo_musica,
                                    col=6,
                                    text_align=ft.TextAlign.JUSTIFY,
                                    value='',
                                    color=ft.colors.WHITE,
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,

                                ),
                                ft.Row(
                                    controls=[
                                        ft.Text(
                                            spans=[
                                                ft.TextSpan(
                                                    ref=segundos_text,
                                                    text='',
                                                    visible=False,

                                                ),
                                                ft.TextSpan(
                                                    ref=barra_time,
                                                    text='/',
                                                    visible=False,
                                                ),

                                                ft.TextSpan(
                                                    ref=minutos_text,
                                                    text=''
                                                )
                                            ]
                                        ),
                                    ]
                                )

                            ]
                        ),
                    ]
                ),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Slider(
                            value=50,
                            min=0,
                            max=100,
                            divisions=10,
                            label='Volume: {value}%',
                            on_change_end=slider_volume,
                        ),
                    ]
                ),
                ft.Row(
                    col=12,
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY,

                    controls=[
                        ft.Container(content=ft.IconButton(
                            icon=ft.icons.SHUFFLE_SHARP, col={"sm": 6, "md": 4, "xl": 2},
                            on_click=random_music
                        )),
                        ft.Container(content=ft.IconButton(
                            icon=ft.icons.FAST_REWIND_SHARP, col={"sm": 6, "md": 4, "xl": 2},
                            on_click=voltar_musica
                        )),
                        ft.Container(content=ft.IconButton(
                            ref=troca_componente,
                            icon=ft.icons.PLAY_CIRCLE_SHARP, col={"sm": 6, "md": 4, "xl": 2},
                            icon_size=50, on_click=play_music),
                        ),
                        ft.Container(content=ft.IconButton(
                            icon=ft.icons.FAST_FORWARD_SHARP, col={"sm": 6, "md": 4, "xl": 2},
                            on_click=prox_music
                        )),
                        ft.Container(content=ft.IconButton(
                            icon=ft.icons.FOLDER_COPY_SHARP, col={"sm": 6, "md": 4, "xl": 2},
                            tooltip='Em breve'
                        )),

                    ]
                )
            ]
        )
    )

    layout = ft.Container(
        width=900,
        margin=ft.margin.all(30),
        shadow=ft.BoxShadow(blur_radius=300, color=ft.colors.BLUE),
        content=ft.ResponsiveRow(
            columns=12,
            spacing=0,
            run_spacing=0,
            controls=[
                downloader_side,
                player_side,
            ]
        )

    )

    page.add(layout)


if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets/audios', )
