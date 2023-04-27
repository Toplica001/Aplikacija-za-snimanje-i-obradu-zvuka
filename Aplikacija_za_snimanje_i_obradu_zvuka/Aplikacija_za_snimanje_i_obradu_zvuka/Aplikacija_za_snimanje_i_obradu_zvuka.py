import sounddevice as sd
import matplotlib.pyplot as plt
import soundfile as sf
import numpy as np
from skimage.restoration import wiener


def SnimiZvuk(trajanje):

    print("Snimanje zapocinje....")
    audio = sd.rec(int(trajanje * 44100), samplerate = 44100, channels = 1)
    sd.wait()
    print("Snimanje je zavrseno!")
    return audio.flatten()

def PustiZvuk(audio, sr):

    sd.play(audio, samplerate = sr)
    sd.wait()
    
def CrtajSpektrogram(audio, sr):

    plt.specgram(audio, Fs = sr)
    plt.xlabel("Vreme [s]")
    plt.ylabel("Frekvencija [Hz]")
    plt.show()

def ExportWAV(naziv_fajla, audio, sr):

    sf.write(naziv_fajla, audio, sr, format='WAV', subtype='PCM_16')
    print(f"Snimljeni zvuk je uspesno sacuvan kao {naziv_fajla}")

def ImportWAV(naziv_fajla):

    audio, sr = sf.read(naziv_fajla)
    print(f"Ucitan zvuk {naziv_fajla} sa samplerate-om {sr}")
    return audio, sr

def DodajSum(audio, snr):

    rms_audio = np.sqrt(np.mean(np.square(audio)))
    std_noise = rms_audio / (10 ** (snr / 20))
    noise = np.random.normal(scale=std_noise, size=len(audio))
    audio_noise = audio + noise
    return audio_noise

def Denoise(audio, sr):
    psf = np.ones(3) / 3
    denoised_audio = wiener(audio, psf=psf, balance=0.3, clip=True)
    return denoised_audio


print("Odaberite opciju:")
print("1. Snimi zvuk")
print("2. Import-ujte audio fajl")
opcija = input("Unesite opciju (1 ili 2): ")

if opcija == "1":
    trajanjeSnimanja = int(input("Unesite trajanje snimanja u sekundama: "))
    audio = SnimiZvuk(trajanjeSnimanja)
    PustiZvuk(audio, 44100)
    CrtajSpektrogram(audio, 44100)

    export = input("Da li zelite da export-ujete zvuk? (da/ne): ")
    if export.lower() == "da":
        naziv_fajla = input("Unesite naziv fajla: ")
        ExportWAV(naziv_fajla, audio, 44100)
        
    shum = input("Da li zelite da dodate sum u snimljeni zvuk? (da/ne): ")
    if shum.lower() == "da":
        snimljeni_zvuk = DodajSum(audio, 0.005)
        PustiZvuk(snimljeni_zvuk, 44100)
        CrtajSpektrogram(snimljeni_zvuk, 44100)

        denoise = input("Da li zelite da primenite denoise? (da/ne): ")
        if denoise.lower() == "da":
            snimljeni_zvuk = Denoise(snimljeni_zvuk, 44100)
            PustiZvuk(snimljeni_zvuk, 44100)
            CrtajSpektrogram(snimljeni_zvuk, 44100)

elif opcija == "2":
    naziv_fajla = input("Unesite naziv fajla: ")
    audio, sr = ImportWAV(naziv_fajla)
    PustiZvuk(audio, sr)
    CrtajSpektrogram(audio, sr)

    shum = input("Da li zelite da dodate sum u snimljeni zvuk? (da/ne): ")
    if shum.lower() == "da":
        audio = DodajSum(audio, 0.005)
        PustiZvuk(audio, sr)
        CrtajSpektrogram(audio, sr)

        denoise = input("Da li zelite da primenite denoise? (da/ne): ")
        if denoise.lower() == "da":
            audio = Denoise(audio, 44100)
            PustiZvuk(audio, sr)
            CrtajSpektrogram(audio, sr)
else:
    print("Pogresna opcija, pokrenite program ponovo i pokusajte ponovo.")
