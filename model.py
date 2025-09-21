import torch
import soundfile as sf
import librosa
import noisereduce as nr
import numpy as np
import os
from transformers import AutoModelForCTC, Wav2Vec2BertProcessor
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import json
from pydub import AudioSegment
def get_set():
    f = open("setting.json")
    set = json.load(f)
    return set

def openWhisper():
    set=get_set()
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = set["model"]["model_id"]
    folder=set["audio"]["WAVE_OUTPUT_FOLDER"] 
    file=set["audio"]["WAVE_OUTPUT_FILENAME"]+".wav"    
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        torch_dtype=torch_dtype,
        device=device,
        generate_kwargs={"task": "transcribe","language": set["model"]["language"]},
    )
    sample=audios(folder,file)
    predictions=pipe(sample,return_timestamps=True)
    res=[]
    for i in predictions["chunks"]:
         res.append(i["text"])

    print("End of prediction")    
    return " ".join(str(x) for x in res)    

def w2v_bert():
    # Config
    model_name = 'Yehor/w2v-bert-2.0-uk-v2.1'
    device = 'cpu' # or cpu
    sampling_rate = 16_000
    time=15
    predictions=[]

    # Load the model
    asr_model = AutoModelForCTC.from_pretrained(model_name).to(device)
    processor = Wav2Vec2BertProcessor.from_pretrained(model_name)

    
    chunks=[]
    y=audios()
    streams=librosa.effects.split(y=y,top_db=40,frame_length=1024 , hop_length=100)
    for st in streams:
        l=y[st[0]:st[1]]
        #l, _ = librosa.effects.trim(l, top_db=20) 
        chunks.append(l)
    for audio in chunks:
            # Transcribe the audio
            input_features = processor(audio, sampling_rate=sampling_rate).input_features
            features = torch.tensor(input_features).to(device)

            with torch.inference_mode():
                logits = asr_model(features).logits

            predicted_ids = torch.argmax(logits, dim=-1)
            predictions+=processor.batch_decode(predicted_ids)+[" "]

        # Log results
    return " ".join(str(x) for x in predictions)

def audios(folder,file,sr=16_000):
    path=os.path.join(folder, file )
    y,sr= librosa.load(path=path, sr=sr)
    y = librosa.to_mono(y)
    y = librosa.util.normalize(y)
    noise_profile = y[:sr]
    y = nr.reduce_noise(y=y, sr=sr,y_noise=noise_profile)

        
    return y
        
def toWav():
    set=get_set()
    input_path=os.path.join(set["audio"]["WAVE_OUTPUT_FOLDER"], set["audio"]["WAVE_OUTPUT_FILENAME"] + ".webm")
    out_path=os.path.join(set["audio"]["WAVE_OUTPUT_FOLDER"], set["audio"]["WAVE_OUTPUT_FILENAME"] + ".wav")
    audio = AudioSegment.from_file(input_path, format="webm")
    audio.export(out_path,format="wav")
     