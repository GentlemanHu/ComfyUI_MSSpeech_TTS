
import datetime

import numpy as np
import folder_paths
import os

from TikTok import TikTok


class Text2AudioTikTokTTS:
    def __init__(self):
        self.output_dir = os.path.join(folder_paths.get_output_directory(), 'audio')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        

    @classmethod
    def INPUT_TYPES(cls):
        VOICES=[
    "en_us_ghostface",  # Ghost Face
    "en_us_chewbacca",  # Chewbacca
    "en_us_c3po",  # C3PO
    "en_us_stitch",  # Stitch
    "en_us_stormtrooper",  # Stormtrooper
    "en_us_rocket",  # Rocket
    "en_female_madam_leota",  # Madame Leota
    "en_male_ghosthost",  # Ghost Host
    "en_male_pirate",  # pirate
    "en_au_001",  # English AU - Female
    "en_au_002",  # English AU - Male
    "en_uk_001",  # English UK - Male 1
    "en_uk_003",  # English UK - Male 2
    "en_us_001",  # English US - Female (Int. 1)
    "en_us_002",  # English US - Female (Int. 2)
    "en_us_006",  # English US - Male 1
    "en_us_007",  # English US - Male 2
    "en_us_009",  # English US - Male 3
    "en_us_010",  # English US - Male 4
    "en_male_narration",  # Narrator
    "en_male_funny",  # Funny
    "en_female_emotional",  # Peaceful
    "en_male_cody",  # Serious
    "en_female_f08_salut_damour",  # Alto
    "en_male_m03_lobby",  # Tenor
    "en_male_m03_sunshine_soon",  # Sunshine Soon
    "en_female_f08_warmy_breeze",  # Warmy Breeze
    "en_female_ht_f08_glorious",  # Glorious
    "en_male_sing_funny_it_goes_up",  # It Goes Up
    "en_male_m2_xhxs_m03_silly",  # Chipmunk
    "en_female_ht_f08_wonderful_world",  # Dramatic
 ]
        return {
            "required": {
                "voice": (VOICES, ),
                "session_id": ("STRING",),
                "filename_prefix": ("STRING", {"default": "comfyUI"}),
                "text": ("STRING", {"multiline": True}),
                "random_voice": ("BOOLEAN",{"default": False})
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("MP3 file: String",)
    FUNCTION = "t_2_audio"
    OUTPUT_NODE = True

    CATEGORY = "MicrosoftSpeech_TTS"

    def t_2_audio(self,voice,filename_prefix,text,session_id,random_voice):
        tiktok = TikTok(session_id=session_id)
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir)
        _datetime = datetime.datetime.now().strftime("%Y%m%d")
        _datetime = _datetime + datetime.datetime.now().strftime("%H%M%S%f")
        file = f"{filename}_{_datetime}_{voice}.mp3"
        audio_path=os.path.join(full_output_folder, file)
        
        print(f"MicrosoftSpeech TTS: Generating voice files, voice=‘{voice}’, audiofile_path='{audio_path}, 'text='{text}'")
        tiktok.run(text,audio_path,voice,random_voice=random_voice)


        return {"ui": {"text": "Audio file："+os.path.join(full_output_folder, file),
        'audios':[{'filename':file,'type':'output','subfolder':'audio'}]}, "result": (audio_path, )}


NODE_CLASS_MAPPINGS = {
    "TikTok_TTS": Text2AudioTikTokTTS
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TikTok_TTS": "MM_TikTok_TTS"
}
