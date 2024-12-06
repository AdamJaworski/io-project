import wave
import pyaudiowpatch as pyaudio
import sounddevice as sd
import numpy as np
from model.audio_capture import AudioCapture
from common.path_manager import PathManager


input_wav  = None
output_wav = None

audio_capture = AudioCapture()

def input_callback(in_data, *args):
    input_wav.writeframes(in_data)
    return in_data, pyaudio.paContinue

def output_callback(in_data, *args):
    output_wav.writeframes(in_data)
    return in_data, pyaudio.paContinue

def start_streams():
    audio_capture.output_stream = audio_capture.p.open(
        format=pyaudio.paInt16,
        channels=audio_capture.output_device["maxInputChannels"],
        rate=int(audio_capture.output_device["defaultSampleRate"]),
        frames_per_buffer=audio_capture.CHUNK_SIZE,
        input=True,
        input_device_index=audio_capture.output_device["index"],
        stream_callback=output_callback
    )

    audio_capture.input_stream = audio_capture.p.open(
        format=pyaudio.paInt16,
        channels=audio_capture.input_device["maxInputChannels"],
        rate=int(audio_capture.input_device["defaultSampleRate"]),
        frames_per_buffer=audio_capture.CHUNK_SIZE,
        input=True,
        input_device_index=audio_capture.input_device["index"],
        stream_callback=input_callback
    )

def stop_streams():
    """stops open streams"""
    if audio_capture.output_stream and audio_capture.output_stream.is_active():
        audio_capture.output_stream.stop_stream()
        audio_capture.output_stream.close()

    if audio_capture.input_stream and audio_capture.input_stream.is_active():
        audio_capture.input_stream.stop_stream()
        audio_capture.input_stream.close()

def open_wav_files(report_id: str):
    global input_wav, output_wav
    input_wav = wave.open(str(PathManager().get_report_path(report_id) / 'input.wav'), 'wb')
    input_wav.setnchannels(2)
    input_wav.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
    input_wav.setframerate(int(audio_capture.input_device["defaultSampleRate"]))

    output_wav = wave.open(str(PathManager().get_report_path(report_id) / 'output.wav'), 'wb')
    output_wav.setnchannels(2)
    output_wav.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
    output_wav.setframerate(int(audio_capture.output_device["defaultSampleRate"]))

def close_wav_files():
    input_wav.close()
    output_wav.close()

def start_recording(report_id: str):
    open_wav_files(report_id)
    start_streams()

def play_zero():
    try:
        while audio_capture.output_stream.is_active():
            t = np.linspace(0, 0.1, int(44100 * 0.1), endpoint=False)
            sine_wave = (0.5 * np.sin(2 * np.pi * 440 * t) * 32767 * 0.0001).astype(np.int16)
            sd.play(sine_wave)
            sd.wait()
    except OSError:
        print("Closing play_zero func")
        return


def stop_recording():
     stop_streams()
     close_wav_files()