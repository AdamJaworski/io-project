import speech_recognition as sr
from common.path_manager import PathManager
import pydub
from pydub.silence import split_on_silence
from model.speach_to_text import r, SAMPLE_RATE
from common import variables
from scipy.fft import fft
import numpy as np


known_speakers = {}
new_append     = 1

def process_recorded_tracks(report_id: str) -> list:
    path_manager = PathManager(report_id)
    aud1 = pydub.AudioSegment.from_file(str(path_manager.get_report_path() / 'output.wav'), format='wav')
    aud2 = pydub.AudioSegment.from_file(str(path_manager.get_report_path() / 'input.wav'), format='wav')

    aud1 = aud1.set_frame_rate(SAMPLE_RATE)
    aud2 = aud2.set_frame_rate(SAMPLE_RATE)

    aud1 = aud1.set_channels(1)
    aud2 = aud2.set_channels(1)

    aud1 = aud1.apply_gain(-aud1.max_dBFS) if aud1.max_dBFS > -35 else aud1
    aud2 = aud2.apply_gain(-aud2.max_dBFS) if aud2.max_dBFS > -35 else aud2

    aud_out = aud2.overlay(aud1) if aud2.max_dBFS > aud1.max_dBFS else aud1.overlay(aud2)

    chunks = split_on_silence(aud_out, min_silence_len=800, silence_thresh=aud_out.max_dBFS - 30, keep_silence=400) #800/400

    return chunks if len(chunks) > 1 else [aud_out]

def get_speaker_id(voice_freq):
    global new_append

    distance = 100
    closest_key = None
    for key, value in known_speakers.items():
        if value - 20 < voice_freq < value + 20:
            distance_now = abs(voice_freq - value)

            if distance_now < distance:
                closest_key = key

    if not closest_key:
        closest_key = f'Mówca {new_append}'
        known_speakers[closest_key] = voice_freq
        new_append += 1

    return closest_key

def get_freq(signal):
    magnitudes = np.abs(fft(signal))
    max_index = np.argmax(magnitudes)
    frequency = max_index * SAMPLE_RATE / len(signal)

    return frequency

def audio_to_text(audio_data: pydub.AudioSegment):
    frequency = get_freq(audio_data.get_array_of_samples())

    try:
        text = r.recognize_google(sr.AudioData(audio_data.raw_data, SAMPLE_RATE, audio_data.frame_width), language='pl-PL')
    except:
        return False, False
    # finally:
    #     print('playing chunk')
    #     play(audio_data)
    return text, get_speaker_id(frequency)

def get_entire_recording_transcript(report_id: str, detect_speaker=True):
    chunks = process_recorded_tracks(report_id)
    print(f'[STT] {len(chunks)} chunk/s')
    text = []
    speakers = []
    for index, chunk in enumerate(chunks):
        variables.display.set(f'Tworzenie transkryptu {int(index/len(chunks) * 100)}%')
        text_chunk, speaker = audio_to_text(chunk)
        if not text_chunk:
            continue
        text.append(text_chunk)
        speakers.append(speaker)

    entire_transcript = ''
    previous_speaker = None
    speakers.append(None)
    for index, text in enumerate(text):
        if speakers[index] != previous_speaker and speakers[index] == speakers[index + 1]:
            previous_speaker = speakers[index]
            entire_transcript += f'\n({previous_speaker}):\n'

        entire_transcript += ' ' + text

    return entire_transcript if detect_speaker else ' '.join(text)
