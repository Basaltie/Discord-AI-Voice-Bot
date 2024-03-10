from email import message
from pyexpat import model
from urllib import response
import discord
import os
from discord.ext import commands
from discord import FFmpegPCMAudio
import openai
import elevenlabs
from elevenlabs import generate, set_api_key, save
import pyaudio
import wave
import keyboard
# Replace keys with whatever file holds your api keys
import keys

promptfile = open("prompt.txt", "rt")
prompt = promptfile.read()
promptfile.close()


messages = []
# Is the "systemrole" variable redundant?
# Yes, and no. I like having it as it creates a logical link for me between the prompt and the Chat GPT API.
# So I am keeping it in for now although it may be changed later.
systemrole = prompt
messages.append({"role": "system", "content": systemrole})
p = pyaudio.PyAudio()
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
stream = p.open(format =FORMAT, channels= CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
elevenlabs.set_api_key(keys.api_elevenlabs)
openai.api_key = keys.api_openai
intents = discord.Intents.default()
intents.members = True
#FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@client.event
async def on_ready():
    print("Arthur is on call!")
    try:
        synced = await client.tree.sync()
        print("Commands Synced:",synced)
    except Exception as e:
        print(e)
    #print(completion.choices[0].message)

@client.command()
async def hello(ctx):
    await ctx.send("Hi")

@client.command(pass_context = True)
async def join(ctx):
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        source = FFmpegPCMAudio('FIFTY POUNDS.wav') ## Add audio source here
        #voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
        player = voice.play(source)
    else:
        await ctx.send("I'm sorry my boy, but it appears something has gone wrong. Maybe try again.")

@client.command(pass_context = True)
async def leave(ctx):
    if(ctx.voice_client):
        await ctx.guild.voice_client.disconnect()
        await ctx.send("Goodbye my friend. I am needed elsewhere.")
        
    else:
        await ctx.send("I'm sorry my boy, but it appears something has gone wrong. Maybe try again.")

async def play(ctx):
    audio_stream = generate(
        text="This is a... streaming voice!!",
        
    )
    save(audio_stream, "Ai file.wav")
    if(ctx.author.voice):
        channel = ctx.message.author.voice.channel
        voice = await channel.connect()
        voice.play(FFmpegPCMAudio("Ai file.wav"), after=lambda e: print('done', e)) #**FFMPEG_OPTS
    else:
        await ctx.send("I'm sorry my boy, but it appears something has gone wrong. Maybe try again.")

@client.tree.command(name ="requesting", description= "request stuff")
async def r(interaction: discord.Interaction, arg: str):
        
       await interaction.response.defer(ephemeral = False)
       voice = discord.utils.get(client.voice_clients, guild=interaction.guild)
       print("Generating response")
       messages.append({"role": "user", "content": arg})
       print(messages)
       response = openai.ChatCompletion.create(
           model="gpt-3.5-turbo",
           messages=messages
           )
       print("Response Generated")
       reply = response["choices"][0]["message"]["content"]
       messages.append({"role": "assistant", "content": reply})
       print(messages)
       print("Generating Audio")
       audio_stream = generate(
        text=reply,
        voice= keys.voice_elevenlabs
        )
       print("Audio Generated")
       save(audio_stream, "Ai file.wav")
       if voice:
           print("Attempting to play audio") 
           voice.play(FFmpegPCMAudio("Ai file.wav"), after=lambda e: print('done', e)) #**FFMPEG_OPTS

       else:
            if(interaction.user.voice):
                channel = interaction.user.voice.channel
                voice = await channel.connect()
                print("Attempting to play audio") 
                voice.play(FFmpegPCMAudio("Ai file.wav"), after=lambda e: print('done', e)) #**FFMPEG_OPTS
                
       await interaction.followup.send("{} said to Arthur, \"{}\"".format(interaction.user, arg))        




recordon = False
frames =[]

async def record():
    while recordon == True:
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    p.terminate
    wf = wave.open("hspeech.wav", 'wb'"w")
    wf.setnchannels(CHANNELS)
    wf.setframerate(RATE)
    wf.setsamplewidth(p.get_sample_size(FORMAT))
    wf.writeframes(b''.join(frames))
    wf.close()

async def on_press():
    
  if recordon != True:
    recordon = True
    print("record is on")
    record()
  else:
    recordon = False


#keyboard.add_hotkey('h', on_press)
#keyboard.wait()
    
    
        
        
#@client.command()
#async def test(ctx):
   # completion = openai.ChatCompletion.create(
   # model="gpt-3.5-turbo",
   # messages=[{"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},{"role": "user", "content": "Compose a poem about a boy called jeremiah."}])
   # await ctx.send(completion.choices[0].message)

   

client.run(keys.token_discord)
