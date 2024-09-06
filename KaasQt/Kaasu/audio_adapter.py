import pyaudio
import wave
import os
from datetime import datetime
import logging
import traceback

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class AudioRecorder:
    def __init__(self):
        self.audio = None
        self.stream = None
        self.frames = []
        self.is_recording = False
        self.home_dir = os.path.expanduser("~")
        self.audio_dir = os.path.join(self.home_dir, "KaasAudio")
        
        if not os.path.exists(self.audio_dir):
            os.makedirs(self.audio_dir)
        
        try:
            self.audio = pyaudio.PyAudio()
            logging.info("PyAudio initialized successfully")
        except Exception as e:
            logging.error(f"Failed to initialize PyAudio: {e}")
            logging.debug(traceback.format_exc())

    def start_recording(self):
        try:
            self.stream = self.audio.open(format=pyaudio.paInt16,
                                          channels=1,
                                          rate=44100,
                                          input=True,
                                          frames_per_buffer=1024)
            self.frames = []
            self.is_recording = True
            logging.info("Recording started")
        except Exception as e:
            logging.error(f"Error starting recording: {e}")
            logging.debug(traceback.format_exc())
            self.is_recording = False

    def stop_recording(self):
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
                logging.info("Recording stopped")
            except Exception as e:
                logging.error(f"Error stopping stream: {e}")
                logging.debug(traceback.format_exc())
        self.is_recording = False
        self.save_audio()

    def record_audio(self):
        while self.is_recording:
            try:
                data = self.stream.read(1024)
                self.frames.append(data)
            except Exception as e:
                logging.error(f"Error recording audio: {e}")
                logging.debug(traceback.format_exc())
                self.is_recording = False
                break

    def save_audio(self):
        if not self.frames:
            logging.warning("No audio data to save")
            return

        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"audio_{timestamp}.wav"
            filepath = os.path.join(self.audio_dir, filename)

            wf = wave.open(filepath, 'wb')
            wf.setnchannels(1)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(44100)
            wf.writeframes(b''.join(self.frames))
            wf.close()

            logging.info(f"Audio saved to: {filepath}")
        except Exception as e:
            logging.error(f"Error saving audio: {e}")
            logging.debug(traceback.format_exc())

    def __del__(self):
        try:
            if self.audio:
                self.audio.terminate()
                logging.info("PyAudio terminated")
        except Exception as e:
            logging.error(f"Error terminating audio: {e}")
            logging.debug(traceback.format_exc())