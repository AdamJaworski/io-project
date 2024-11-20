# import pydub
# import pyaudiowpatch as pyaudio
# from common.path_manager import PathManager
# from pydub.playback import play
# import speech_recognition as sr
# import assemblyai as aai
from huggingsound import SpeechRecognitionModel

# aai.settings.api_key = "04fc49a6ac514d9c9ba261ce5ecd4b80"
# transcriber = aai.Transcriber()
#
# r = sr.Recognizer()
# input_seg = pydub.AudioSegment.from_file(str(PathManager().get_report_path('test') / 'input.wav'), format='wav')
#
# input_seg = input_seg.set_frame_rate(44100)
# input_seg = input_seg.set_channels(2)
# #input_seg = input_seg.apply_gain(-input_seg.max_dBFS)
#
# #text = r.recognize_google(input_seg, language='pl-PL')
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
#     pass

model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-polish")
transc = model.transcribe([str(PathManager().get_report_path('test') / 'input.wav')])
print(transc)