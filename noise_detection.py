import pyaudio
import wave
import datetime
import soundfile as sf
from pydub import AudioSegment
from pydub.playback import play
import pyloudnorm as pyln
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# recording params
form_1 = pyaudio.paInt16 # 16-bit resolution
chans = 1 # 1 channel
samp_rate = 44100 # 44.1kHz sampling rate
chunk = 4096 # 2^12 samples for buffer
record_secs = 5 # seconds to record
dev_index = 0 # device index found by p.get_device_info_by_index(ii)
wav_output_filename = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")+".wav" # name of .wav file

# loop forever, unless manually stopped
while 1 == 1:

    audio = pyaudio.PyAudio() # create pyaudio instantiation

    # create pyaudio stream
    stream = audio.open(format = form_1,rate = samp_rate,channels = chans, \
                        input_device_index = dev_index,input = True, \
                        frames_per_buffer=chunk)

    print("*** RECORDING NOW ***")
    frames = []

    # loop through stream and append audio chunks to frame array
    for ii in range(0,int((samp_rate/chunk)*record_secs)):
        data = stream.read(chunk)
        frames.append(data)

    print("*** FINISHED RECORDING ***")

    # stop the stream, close it, and terminate the pyaudio instantiationpip 
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # save the audio frames as .wav file
    wavefile = wave.open(wav_output_filename,'wb')
    wavefile.setnchannels(chans)
    wavefile.setsampwidth(audio.get_sample_size(form_1))
    wavefile.setframerate(samp_rate)
    wavefile.writeframes(b''.join(frames))
    wavefile.close()


    # playback
    sound = AudioSegment.from_wav(wav_output_filename)
    #play(sound) # play the sound that was recorded


    #loudness check
    data, rate = sf.read(wav_output_filename) # load audio (with shape (samples, channels))
    meter = pyln.Meter(rate) # create BS.1770 meter
    loudness = meter.integrated_loudness(data) # measure loudness

    print("Loudness: ", -100/loudness*5)

    if -100/loudness*5 > 20: # if it's loud enough, then send the recording via email

        # for email sending
        fromaddr = "" # Emaail origin address
        toaddr = "" # Email address where notification goes

        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "Noise Detected: " + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") 

        body = "A noise was detected at " + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ". The loudness of this noise was " + str(-100/loudness*5) + "."
        msg.attach(MIMEText(body, 'plain'))

        filename = wav_output_filename
        attachment = open(wav_output_filename, "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587) # change this if you're not using GMail
        server.starttls()
        server.login(fromaddr, "") # password to the origin email account
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        
    # delete recording
    
    os.remove(wav_output_filename)
