import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import yt_dlp
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

# Obtener el token desde el archivo .env
TOKEN = os.getenv("DISCORD_TOKEN")

# Ruta del ejecutable de ffmpeg
ffmpeg_executable = "C:/Users/SONIC/Desktop/Programación/ffmpeg-7.1.1-essentials_build/bin/ffmpeg.exe"  # Ruta correcta de ffmpeg

# Configurar los intents
intents = discord.Intents.default()
intents.message_content = True  # Esto habilita el acceso a los mensajes (si se necesita)

# Inicializar el bot con el prefijo "!" y los intents configurados
bot = commands.Bot(command_prefix='!', intents=intents)

# Lista para almacenar las canciones en la playlist
playlist = []

# Comando para unirse al canal de voz
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Conectado al canal de voz: {channel.name}")
    else:
        await ctx.send("¡Necesitas estar en un canal de voz primero!")

# Comando para salir del canal de voz
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Desconectado del canal de voz.")
    else:
        await ctx.send("No estoy en un canal de voz para desconectarme.")

# Comando para agregar canciones a la lista de reproducción
@bot.command()
async def add(ctx, *, url: str = None):
    if not url:
        await ctx.send("¡Debes proporcionar una URL de YouTube para agregar a la lista de reproducción!")
        return

    # Agregar la URL a la lista de reproducción
    playlist.append(url)
    await ctx.send(f"¡Canción agregada a la lista de reproducción! URL: {url}")

# Comando para reproducir la siguiente canción en la lista de reproducción
@bot.command()
async def play(ctx):
    if len(playlist) == 0:
        await ctx.send("¡La lista de reproducción está vacía!")
        return

    voice_client = ctx.voice_client

    if not voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            voice_client = await channel.connect()
        else:
            await ctx.send("¡Necesitas estar en un canal de voz para que el bot se conecte!")
            return

    # Tomar la primera canción de la lista de reproducción
    url = playlist.pop(0)

    # Opciones de configuración de yt-dlp para obtener el audio
    ydl_opts = {
        'format': 'bestaudio',  # Cambié 'bestaudio/best' por 'bestaudio'
        'extractaudio': True,  # Extraer solo el audio
        'audioquality': 1,  # Mejor calidad de audio
        'outtmpl': 'downloads/%(id)s.%(ext)s',  # Ruta temporal para guardar archivos descargados
        'restrictfilenames': True,
        'noplaylist': True,  # No permitir listas de reproducción
    }

    # Intentar descargar y reproducir el audio
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)  # No descargar el archivo, solo extraer la info
            print("Información extraída:", info)  # Verifica la información obtenida
            url2 = info['formats'][0]['url']  # Obtenemos la URL del archivo de audio
            
            # Reproducir el audio en el canal de voz con opciones de ffmpeg
            voice_client.play(FFmpegPCMAudio(url2, executable=ffmpeg_executable, options="-vn -ac 2 -ar 44100"))
            await ctx.send(f"Reproduciendo: {url}")
    except Exception as e:
        print(f"Error: {e}")
        await ctx.send(f"Ocurrió un error al intentar reproducir la canción: {e}")

# Evento cuando el bot está listo
@bot.event
async def on_ready():
    print(f'Conectado como {bot.user}')

# Ejecutar el bot
bot.run(TOKEN)


