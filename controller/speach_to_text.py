import speech_recognition as sr
from common.path_manager import PathManager
import pydub
from pydub.silence import split_on_silence
from model.speach_to_text import r, SAMPLE_RATE
from common import variables

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

    chunks = split_on_silence(aud_out, min_silence_len=800, silence_thresh=aud_out.max_dBFS - 30, keep_silence=400)

    return chunks if len(chunks) > 1 else [aud_out]

def audio_to_text(audio_data: pydub.AudioSegment):
    try:
        text = r.recognize_google(sr.AudioData(audio_data.raw_data, SAMPLE_RATE, audio_data.frame_width), language='pl-PL')
    except:
        return ''
    # finally:
    #     print('playing chunk')
    #     play(audio_data)
    return text

def get_entire_recording_transcript(report_id: str):
    chunks = process_recorded_tracks(report_id)
    text = []
    for index, chunk in enumerate(chunks):
        variables.display.set(f'Tworzenie transkryptu {int(index/len(chunks))}%')
        text.append(audio_to_text(chunk))

    return ' '.join(text)
