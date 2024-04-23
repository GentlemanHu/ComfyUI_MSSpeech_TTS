import asyncio
import datetime

import edge_tts
import numpy as np
import folder_paths
import os

async def gen_tts(_text,_voice,_rate,filename):
    tts = edge_tts.Communicate(text = _text, voice = _voice, rate = _rate)
    await tts.save(filename)



class MSTTS_VOICE_CHOOSER:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
        VOICES=[
'zh-CN-XiaoxiaoNeural','zh-CN-XiaoyiNeural','zh-CN-YunjianNeural','zh-CN-YunxiNeural','zh-CN-YunxiaNeural',
'zh-CN-YunyangNeural','zh-CN-liaoning-XiaobeiNeural','zh-CN-shaanxi-XiaoniNeural','zh-HK-HiuGaaiNeural',
'zh-HK-HiuMaanNeural','zh-HK-WanLungNeural','zh-TW-HsiaoChenNeural','zh-TW-HsiaoYuNeural','zh-TW-YunJheNeural',
'en-US-AnaNeural','en-US-AriaNeural','en-US-ChristopherNeural','en-US-EricNeural','en-US-GuyNeural',
'en-US-JennyNeural','en-US-MichelleNeural','en-US-RogerNeural','en-US-SteffanNeural',
'en-GB-LibbyNeural','en-GB-MaisieNeural','en-GB-RyanNeural','en-GB-SoniaNeural','en-GB-ThomasNeural'
                ]
        return {
            "required": {
                "voice": (VOICES, ),
            },
        }

    RETURN_TYPES = ('STRING',)
    RETURN_NAMES = ('ms_voice',)
    FUNCTION = 'ms_voice'
    CATEGORY = "MicrosoftSpeech_TTS"

    def ms_voice(self, voice):
        return {"ui":{"ms_voice":voice},"result": (voice,)}  # Return the absolute path to the output video



class Text2AudioEdgeTts:
    def __init__(self):
        self.output_dir = os.path.join(folder_paths.get_output_directory(), 'audio')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    @classmethod
    def INPUT_TYPES(cls):
        VOICES=[
'zh-CN-XiaoxiaoNeural','zh-CN-XiaoyiNeural','zh-CN-YunjianNeural','zh-CN-YunxiNeural','zh-CN-YunxiaNeural',
'zh-CN-YunyangNeural','zh-CN-liaoning-XiaobeiNeural','zh-CN-shaanxi-XiaoniNeural','zh-HK-HiuGaaiNeural',
'zh-HK-HiuMaanNeural','zh-HK-WanLungNeural','zh-TW-HsiaoChenNeural','zh-TW-HsiaoYuNeural','zh-TW-YunJheNeural',
'en-US-AnaNeural','en-US-AriaNeural','en-US-ChristopherNeural','en-US-EricNeural','en-US-GuyNeural',
'en-US-JennyNeural','en-US-MichelleNeural','en-US-RogerNeural','en-US-SteffanNeural',
'en-GB-LibbyNeural','en-GB-MaisieNeural','en-GB-RyanNeural','en-GB-SoniaNeural','en-GB-ThomasNeural'
                ]
        return {
            "required": {
                "voice": (VOICES, ),
                "rate": ("INT", {"default": 0, "min": -200, "max": 200}),
                "filename_prefix": ("STRING", {"default": "comfyUI"}),
                "text": ("STRING", {"multiline": True}),
                "use_voice_from_input": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "voice_input": ("STRING", {"default": "zh-CN-XiaoxiaoNeural"}),
            },
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("MP3 file: String",)
    FUNCTION = "text_2_audio"
    OUTPUT_NODE = True

    CATEGORY = "MicrosoftSpeech_TTS"

    def text_2_audio(self,voice,filename_prefix,text,rate,voice_input,use_voice_from_input):
        if use_voice_from_input:
            voice = voice_input
        
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        _datetime = datetime.datetime.now().strftime("%Y%m%d")
        _datetime = _datetime + datetime.datetime.now().strftime("%H%M%S%f")
        file = f"{filename}_{_datetime}_{voice}.mp3"
        audio_path=os.path.join(full_output_folder, file)
        _rate = str(rate) + "%" if rate < 0 else "+" + str(rate) + "%"
        print(f"MicrosoftSpeech TTS: Generating voice files, voice=‘{voice}’, rate={rate}, audiofile_path='{audio_path}, 'text='{text}'")

        asyncio.run(gen_tts(text,voice,_rate,audio_path))

        return {"ui": {"text": "Audio file："+os.path.join(full_output_folder, file),
        'audios':[{'filename':file,'type':'output','subfolder':'audio'}]}, "result": (audio_path, )}


async def edge_tts_text_2_audion(VOICE,TEXT,OUTPUT_FILE) -> None:
    communicate = edge_tts.Communicate(TEXT, VOICE)
    await communicate.save(OUTPUT_FILE)

NODE_CLASS_MAPPINGS = {
    "MicrosoftSpeech_TTS": Text2AudioEdgeTts,
    "MicrosoftSpeech_Voice_Chooser": MSTTS_VOICE_CHOOSER
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MicrosoftSpeech_TTS": "MicrosoftSpeech_TTS",
    "MicrosoftSpeech_Voice_Chooser": "MicrosoftSpeech_Voice_Chooser"
}
