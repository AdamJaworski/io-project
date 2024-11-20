import pyaudiowpatch as pyaudio
import speech_recognition as sr


class SpeachToText:
    p: pyaudio.PyAudio
    r: sr.Recognizer
    CHUNK_SIZE: int
    SAMPLE_RATE: int
    output_stream: pyaudio.Stream
    input_stream: pyaudio.Stream

    def __init__(self) -> None:
        self.p = pyaudio.PyAudio()
        self.r = sr.Recognizer()

        self.CHUNK_SIZE:  int = int(8192)
        self.SAMPLE_RATE: int = int(44100)

        self.output_device = None
        self.input_device = None

        self.output_stream = None
        self.input_stream    = None

        self.select_devices()

    def select_devices(self):
        try:
            wasapi_info = self.p.get_host_api_info_by_type(pyaudio.paWASAPI)
        except OSError:
            raise RuntimeError("Looks like WASAPI is not available on the system. Exiting...")

        default_speakers = self.p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])

        if not default_speakers["isLoopbackDevice"]:
            for loopback in self.p.get_loopback_device_info_generator():
                if default_speakers["name"] in loopback["name"]:
                    default_speakers = loopback
                    break

        self.input_device  = self.p.get_default_input_device_info()
        self.output_device = default_speakers

        print(self.input_device, self.output_device)


if __name__ == "__main__":
    SpeachToText()