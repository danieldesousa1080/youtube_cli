from distutils.util import convert_path
from time import sleep
from pytube import YouTube, Search, Playlist, Channel
import os
from moviepy.editor import *
from shutil import rmtree

def converter_pasta_mp4_para_mp3(caminho_origem:str,caminho_final:str) -> None:
    arquivos = os.listdir(caminho_origem)
    for i in arquivos:
        caminho_arquivo = os.path.join(caminho_origem,i)
        audio_mp4 = AudioFileClip(caminho_arquivo)
        audio_mp4.write_audiofile(os.path.join(caminho_final,i.replace('.mp4','.mp3')))
    rmtree(caminho_origem)




def ler_linhas(arquivo):  # Retorna as linhas do documento como lista
    lista = []
    for line in arquivo:
        line = line.replace('\n', '')
        lista.append(line)
    return (lista)


def detalhes_stream(mystream):  # Retorna o nome e a duração de uma stream como string
    stream = {
        "name": mystream.title
    }
    titulo = stream.get('name')
    

    return str(titulo)


def baixar_url(link,path,type): #Baixa o audio ou video através de uma url
    video = YouTube(link)
    descricao = detalhes_stream(video)

    convert_path = '.to_convert'

    if type == 'audio':
        print(f'Baixando audio {descricao}')
        stream = video.streams.get_audio_only()
        stream.download(convert_path)
        converter_pasta_mp4_para_mp3(convert_path,path)
    elif type == 'video':
        print(f'Baixando video {descricao}')
        stream = video.streams.get_highest_resolution()
        stream.download(path)


def baixar_nome(nome,path,type): # Baixa audio ou video através de um nome
    search = Search(nome)
    video = search.results[0]
    descricao = detalhes_stream(video)

    convert_path = '.to_convert'

    if type == 'audio':
        print(f'Baixando Audio {descricao}')
        stream = video.streams.get_audio_only()
        stream.download(convert_path,skip_existing=True)
        converter_pasta_mp4_para_mp3(convert_path,path)
    if type == 'video':
        print(f'Baixando Video {descricao}')
        stream = video.streams.get_highest_resolution()
        stream.download(path,skip_existing=True)


def baixar_lista_urls(caminho_urls, path, type):  # Baixa uma lista de urls

    caminho_lista_urls = open(caminho_urls)
    lista_links = ler_linhas(caminho_lista_urls)
    caminho_lista_urls.close()
    total_para_baixar = len(lista_links)
    
    total_baixado = 0

    convert_path = '.to_convert'

    for link in lista_links:
        total_baixado += 1
        video = YouTube(link)
        descricao = detalhes_stream(video)
        if type == 'audio':
            print('Baixando audio {} [{} de {}]'.format(descricao, total_baixado, total_para_baixar))
            stream = video.streams.get_audio_only()
            stream.download(convert_path,skip_existing=True)
            converter_pasta_mp4_para_mp3(convert_path,path)
        if type == 'video':
            print('Baixando video {} [{} de {}]'.format(descricao,total_baixado,total_para_baixar))
            stream = video.streams.get_highest_resolution()
            stream.download(path,skip_existing=True)
        


def baixar_lista_nomes(caminho_nomes, path, type): # Baixa uma lista de audios ou videos através de uma busca no Youtube
    
    caminho_lista_nomes = open(caminho_nomes)
    lista_nomes = ler_linhas(caminho_lista_nomes)
    caminho_lista_nomes.close()

    total_para_baixar = len(lista_nomes)
    total_baixado = 0

    convert_path = '.to_convert'

    for nome in lista_nomes:
        total_baixado += 1
        search = Search(nome)
        video = search.results[0] # Seleciona sempre o primeiro resultado da pesquisa
        descricao = detalhes_stream(video)
        if type == 'audio':
            print('Baixando audio {} [{} de {}]'.format(descricao,total_baixado,total_para_baixar))
            stream = video.streams.get_audio_only()
            stream.download(convert_path,skip_existing=True)
            converter_pasta_mp4_para_mp3(convert_path,path)
        if type == 'video':
            print('Baixando video {} [{} de {}]'.format(descricao,total_para_baixar,total_baixado))
            stream = video.streams.get_highest_resolution()
            stream.download(path,skip_existing=True)

def baixar_playlist(link,path,type):
    playlist = Playlist(link)
    
    print('-+'*10)
    print(f'Fazendo download da playlist {playlist.title}')
    print('-+'*10)

    convert_path = '.to_convert'

    if type == 'audio':
        try:
            os.mkdir(f'audio/{playlist.title}')
        except OSError as error:
            print(error)

        for video in playlist.videos:
            print(f'Baixando {detalhes_stream(video)}')
            stream = video.streams.get_audio_only()
            stream.download(f'{convert_path}/{playlist.title}',skip_existing=True)
        converter_pasta_mp4_para_mp3(f'{convert_path}/{playlist.title}',str(f'{path}/{playlist.title}'))
    if type == 'video':
        for video in playlist.videos:
            print(f'Baixando {detalhes_stream(video)}')
            stream = video.streams.get_highest_resolution()
            stream.download(f'{path}/{playlist.title}',skip_existing=True)
    
def baixar_canal(link,path,type):
    channel = Channel(link)
    count = 0
    print(f'Baixando videos do canal {channel.channel_name}')

    converter_pasta_mp4_para_mp3(convert_path,path)

    if type == 'audio':
        for link in channel:
            count += 1
            video = YouTube(link)
            stream = video.streams.get_audio_only()
            print(f'Baixando audio {detalhes_stream(video)} [{count} de {channel.length}]')
            stream.download(f'{path}/{channel.channel_name}')
    if type == 'video':
        for link in channel:
            count += 1
            video = YouTube(link)
            stream = video.streams.get_highest_resolution()
            print(f'Baixando video {detalhes_stream(video)} [{count} de {channel.length}]')
            stream.download(f'{path}/{channel.channel_name}')



def limpar():
    os.system('clear')

def saida():
    print('__Volte Sempre__')
    sys.exit()


'''
    Inicio do Programa

'''

def logo():
    limpar()
    print('-'*5,'Youtube Cli v0.0.3 Linux','-'*5)
    print('Desenvolvido por: W1R$0N')
    print('+='*20)
    sleep(3)

def start_screen():
    try:
        rmtree('.to_convert')
    except:
        ...
    print('\n','Escolha o que deseja baixar:')
    print('''
        [1] Audio
        [2] Video
        [0] Sair
    ''')
    op:str = input('Sua opção:  ')
    limpar()
    if op in '012':
        if op in '0':
            saida()
        if op in '1':

            tipo = 'audio'
            pasta = './audio'


            print('+='*30)
            print('-'*5,'O que deseja baixar?','-'*5)
            print('''
                [1] Link
                [2] Procurar no Youtube
                [3] Baixar lista de Links (arquivo de texto)
                [4] Baixar lista de Nomes (Arquivo de texto)
                [5] Baixar uma Playlist
                [6] Baixar um canal inteiro
            
            ''')
            op = input('Sua opção:  ')
            limpar()
            if op in '0':
                saida()
            if op in '1':
                link:str = input('Digite o link:    ')
                baixar_url(link,pasta,tipo)
            if op in '2':
                palavra:str = input('Digite o que deseja procurar:  ')
                baixar_nome(palavra,pasta,tipo)
            if op in '3':
                arquivo:str = input('Digite o caminho do arquivo:   ')
                baixar_lista_urls(arquivo,pasta,tipo)
            if op in '4':
                arquivo:str = input('Digite o caminho do arquivo:   ')
                baixar_lista_nomes(arquivo,pasta,tipo)
            if op in '5':
                link:str = input('Digite o link da Playlist:    ')
                baixar_playlist(link,pasta,tipo)
            if op in '6':
                link:str = input('Digite o link do canal:   ')
                baixar_canal(link,pasta,tipo)
            print('Tudo pronto!!')
            print ('Deseja continuar?')
            print ('''
                [0] Não
                [1] Sim
            ''')
            op = str(input('Digite sua opção:   '))
            if op in '1':
                limpar()
                start_screen()
            if op in '0':
                saida()
            else:
                print ('Opção inválida!')
                sleep(2)
                saida()

        if op in '2':

            tipo = 'video'
            pasta = './video'


            print('+='*30)
            print('-'*5,'O que deseja baixar?','-'*5)
            print('''
                [1] Link
                [2] Procurar no Youtube
                [3] Baixar lista de Links (arquivo de texto)
                [4] Baixar lista de Nomes (Arquivo de texto)
                [5] Baixar uma Playlist
                [6] Baixar um canal inteiro

                [0] Sair
            
            ''')
            op = input('Sua opção:  ')
            limpar()
            if op in '0':
                saida()

            if op in '1':
                link:str = input('Digite o link:    ')
                baixar_url(link,pasta,tipo)
            if op in '2':
                palavra:str = input('Digite o que deseja procurar:  ')
                baixar_nome(palavra,pasta,tipo)
            if op in '3':
                arquivo:str = input('Digite o caminho do arquivo:   ')
                baixar_lista_urls(arquivo,pasta,tipo)
            if op in '4':
                arquivo:str = input('Digite o caminho do arquivo:   ')
                baixar_lista_nomes(arquivo,pasta,tipo)
            if op in '5':
                link:str = input('Digite o link da Playlist:    ')
                baixar_playlist(link,pasta,tipo)
            if op in '6':
                link:str = input('Digite o link do canal:   ')
                baixar_canal(link,pasta,tipo)
            print('Tudo pronto!')
            saida()
    else: 
        print('Opção inválida!',end='\n'*2)
        sleep(2)
        start_screen()

if __name__ == '__main__':
    logo()
    start_screen()