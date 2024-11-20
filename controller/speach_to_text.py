import threading
import time
from model.speach_to_text import SpeachToText
from common.path_manager import PathManager
from pydub.silence import split_on_silence
import wave
import pyaudiowpatch as pyaudio
import pydub
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import json
from pydub.playback import play

speach_to_text = SpeachToText()
r = sr.Recognizer()

input_wav  = None
output_wav = None


def input_callback(in_data, frame_count, time_info, status):
    input_wav.writeframes(in_data)
    return in_data, pyaudio.paContinue

def output_callback(in_data, frame_count, time_info, status):
    output_wav.writeframes(in_data)
    return in_data, pyaudio.paContinue

def start_streams():
    stop_streams()
    speach_to_text.output_stream = speach_to_text.p.open(
        format=pyaudio.paInt16,
        channels=speach_to_text.output_device["maxInputChannels"],
        rate=int(speach_to_text.output_device["defaultSampleRate"]),
        frames_per_buffer=speach_to_text.CHUNK_SIZE,
        input=True,
        input_device_index=speach_to_text.output_device["index"],
        stream_callback=output_callback
    )

    speach_to_text.input_stream = speach_to_text.p.open(
        format=pyaudio.paInt16,
        channels=speach_to_text.input_device["maxInputChannels"],
        rate=int(speach_to_text.input_device["defaultSampleRate"]),
        frames_per_buffer=speach_to_text.CHUNK_SIZE,
        input=True,
        input_device_index=speach_to_text.input_device["index"],
        stream_callback=input_callback
    )

def stop_streams():
    """stops open streams"""
    if speach_to_text.output_stream and speach_to_text.output_stream.is_active():
        speach_to_text.output_stream.stop_stream()
        speach_to_text.output_stream.close()

    if speach_to_text.input_stream and speach_to_text.input_stream.is_active():
        speach_to_text.input_stream.stop_stream()
        speach_to_text.input_stream.close()

def open_wav_files(report_id: str):
    global input_wav, output_wav
    input_wav = wave.open(str(PathManager().get_report_path(report_id) / 'input.wav'), 'wb')
    input_wav.setnchannels(2)
    input_wav.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
    input_wav.setframerate(int(speach_to_text.input_device["defaultSampleRate"]))

    output_wav = wave.open(str(PathManager().get_report_path(report_id) / 'output.wav'), 'wb')
    output_wav.setnchannels(2)
    output_wav.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
    output_wav.setframerate(int(speach_to_text.output_device["defaultSampleRate"]))

def close_wav_files():
    input_wav.close()
    output_wav.close()

def start_recording(report_id: str):
    open_wav_files(report_id)
    start_streams()

def play_zero():
    try:
        while speach_to_text.output_stream.is_active():
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

def process_recorded_tracks(report_id: str) -> list:
    aud1 = pydub.AudioSegment.from_file(str(PathManager().get_report_path(report_id) / 'output.wav'), format='wav')
    aud2 = pydub.AudioSegment.from_file(str(PathManager().get_report_path(report_id) / 'input.wav'), format='wav')

    aud1 = aud1.set_frame_rate(speach_to_text.SAMPLE_RATE)
    aud2 = aud2.set_frame_rate(speach_to_text.SAMPLE_RATE)

    aud1 = aud1.set_channels(1)
    aud2 = aud2.set_channels(1)

    aud1 = aud1.apply_gain(-aud1.max_dBFS) if aud1.max_dBFS > -35 else aud1
    aud2 = aud2.apply_gain(-aud2.max_dBFS) if aud2.max_dBFS > -35 else aud2

    aud_out = aud1.overlay(aud2)

    chunks = split_on_silence(aud2, min_silence_len=800, silence_thresh=aud_out.max_dBFS - 30, keep_silence=400)
    return chunks if len(chunks) > 1 else [aud_out]

def audio_to_test(audio_data: pydub.AudioSegment):
    try:
        text = r.recognize_google(sr.AudioData(audio_data.raw_data, speach_to_text.SAMPLE_RATE, audio_data.frame_width), language='pl-PL')
        #play(audio_data)
    except Exception as e:
        print('error')
        return ' '
    return text

def get_entire_recording_transcript(report_id: str):
    chunks = process_recorded_tracks(report_id)
    print(len(chunks))
    text = []
    for chunk in chunks:
        text.append(audio_to_test(chunk))

    print(' '.join(text))


if __name__ == "__main__":
    # start_recording('test')
    # threading.Thread(target=play_zero).start()
    # time.sleep(20)
    # stop_recording()
    get_entire_recording_transcript('test')
