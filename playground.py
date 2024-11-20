import pydub
import pyaudiowpatch as pyaudio
from common.path_manager import PathManager
import speech_recognition as sr
from pydub.silence import split_on_silence

# aai.settings.api_key = "04fc49a6ac514d9c9ba261ce5ecd4b80"
# transcriber = aai.Transcriber()
#
r = sr.Recognizer()
input_seg = pydub.AudioSegment.from_file(str(PathManager().get_report_path('test') / 'input.wav'), format='wav')

input_seg = input_seg.set_frame_rate(16000)
input_seg = input_seg.set_channels(1)
input_seg = input_seg.apply_gain(-input_seg.max_dBFS)

chunks = split_on_silence(input_seg, min_silence_len=800, silence_thresh=input_seg.max_dBFS - 30, keep_silence=400)
print(len(chunks))
for chunk in chunks:
    try:
        text = r.recognize_google(sr.AudioData(chunk.raw_data, 16000, chunk.frame_width), language='pl-PL')
        print(text)
    except:
        print('error')
# #play(input_seg)
# config = aai.TranscriptionConfig(speaker_labels=True, language_code='pl')
# transcript = transcriber.transcribe(str(PathManager().get_report_path('test') / 'input.wav'))
# if transcript.error:
#    print(transcript.error)
#
# print(transcript.text)
# print(transcript.words)
# try:
#     for utterance in transcript.utterances:
#        print(f"Speaker {utterance.speaker}: {utterance.text}")
# except:
