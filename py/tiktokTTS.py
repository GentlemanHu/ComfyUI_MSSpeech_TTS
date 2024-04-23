
import datetime

import numpy as np
import folder_paths
import os

# documentation for tiktok api: https://github.com/oscie57/tiktok-voice/wiki
import base64
import random
import time
from typing import Optional, Final

import requests


# __all__ = ["TikTok", "TikTokTTSException"]

disney_voices: Final[tuple] = (
    "en_us_ghostface",  # Ghost Face
    "en_us_chewbacca",  # Chewbacca
    "en_us_c3po",  # C3PO
    "en_us_stitch",  # Stitch
    "en_us_stormtrooper",  # Stormtrooper
    "en_us_rocket",  # Rocket
    "en_female_madam_leota",  # Madame Leota
    "en_male_ghosthost",  # Ghost Host
    "en_male_pirate",  # pirate
)

eng_voices: Final[tuple] = (
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
)

non_eng_voices: Final[tuple] = (
    # Western European voices
    "fr_001",  # French - Male 1
    "fr_002",  # French - Male 2
    "de_001",  # German - Female
    "de_002",  # German - Male
    "es_002",  # Spanish - Male
    "it_male_m18",  # Italian - Male
    # South american voices
    "es_mx_002",  # Spanish MX - Male
    "br_001",  # Portuguese BR - Female 1
    "br_003",  # Portuguese BR - Female 2
    "br_004",  # Portuguese BR - Female 3
    "br_005",  # Portuguese BR - Male
    # asian voices
    "id_001",  # Indonesian - Female
    "jp_001",  # Japanese - Female 1
    "jp_003",  # Japanese - Female 2
    "jp_005",  # Japanese - Female 3
    "jp_006",  # Japanese - Male
    "kr_002",  # Korean - Male 1
    "kr_003",  # Korean - Female
    "kr_004",  # Korean - Male 2
)

vocals: Final[tuple] = (
    "en_female_f08_salut_damour",  # Alto
    "en_male_m03_lobby",  # Tenor
    "en_male_m03_sunshine_soon",  # Sunshine Soon
    "en_female_f08_warmy_breeze",  # Warmy Breeze
    "en_female_ht_f08_glorious",  # Glorious
    "en_male_sing_funny_it_goes_up",  # It Goes Up
    "en_male_m2_xhxs_m03_silly",  # Chipmunk
    "en_female_ht_f08_wonderful_world",  # Dramatic
)


class TikTok:
    """TikTok Text-to-Speech Wrapper"""

    def __init__(self,session_id):
        headers = {
            "User-Agent": "com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; "
            "Build/NRD90M;tt-ok/3.12.13.1)",
            "Cookie": f"sessionid={session_id}",
        }

        self.URI_BASE = "https://api16-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/"
        self.max_chars = 300

        self._session = requests.Session()
        # set the headers to the session, so we don't have to do it for every request
        self._session.headers = headers

    def run(self, text: str, filepath: str,m_voice, random_voice: bool = False):
        if random_voice:
            voice = self.random_voice()
        else:
            voice = m_voice

        # get the audio from the TikTok API
        data = self.get_voices(voice=voice, text=text)

        # check if there was an error in the request
        status_code = data["status_code"]
        if status_code != 0:
            raise TikTokTTSException(status_code, data["message"])

        # decode data from base64 to binary
        try:
            raw_voices = data["data"]["v_str"]
        except:
            print(
                "The TikTok TTS returned an invalid response. Please try again later, and report this bug."
            )
            raise TikTokTTSException(0, "Invalid response")
        decoded_voices = base64.b64decode(raw_voices)

        # write voices to specified filepath
        with open(filepath, "wb") as out:
            out.write(decoded_voices)

    def get_voices(self, text: str, voice: Optional[str] = None) -> dict:
        """If voice is not passed, the API will try to use the most fitting voice"""
        # sanitize text
        text = text.replace("+", "plus").replace("&", "and").replace("r/", "")

        # prepare url request
        params = {"req_text": text, "speaker_map_type": 0, "aid": 1233}

        if voice is not None:
            params["text_speaker"] = voice

        # send request
        try:
            response = self._session.post(self.URI_BASE, params=params)
        except ConnectionError:
            time.sleep(random.randrange(1, 7))
            response = self._session.post(self.URI_BASE, params=params)

        return response.json()

    @staticmethod
    def random_voice() -> str:
        return random.choice(eng_voices)


class TikTokTTSException(Exception):
    def __init__(self, code: int, message: str):
        self._code = code
        self._message = message

    def __str__(self) -> str:
        if self._code == 1:
            return f"Code: {self._code}, reason: probably the aid value isn't correct, message: {self._message}"

        if self._code == 2:
            return f"Code: {self._code}, reason: the text is too long, message: {self._message}"

        if self._code == 4:
            return f"Code: {self._code}, reason: the speaker doesn't exist, message: {self._message}"

        return f"Code: {self._message}, reason: unknown, message: {self._message}"






class TikTok_VOICE_CHOOSER:

    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(self):
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
            },
        }

    RETURN_TYPES = ('STRING',)
    RETURN_NAMES = ('tk_voice',)
    FUNCTION = 'tk_voice'
    CATEGORY = "MicrosoftSpeech_TTS"

    def tk_voice(self, voice):
        return {"ui":{"tk_voice":voice},"result": (voice,)}  # Return the absolute path to the output video





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
                "tk_session_id": ("STRING",{"default": ""}),
                "filename_prefix": ("STRING", {"default": "comfyUI"}),
                "text": ("STRING", {"multiline": True}),
                "random_voice": ("BOOLEAN",{"default": False}),
                "use_voice_from_input": ("BOOLEAN", {"default": False}),
            },
            "optional": {
                "voice_input": ("STRING", {"default": "en_us_stormtrooper"}),
            },
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("MP3 file: String",)
    FUNCTION = "t_2_audio"
    OUTPUT_NODE = True

    CATEGORY = "MicrosoftSpeech_TTS"

    def t_2_audio(self,voice,filename_prefix,text,tk_session_id,random_voice,voice_input,use_voice_from_input):
        tiktok = TikTok(session_id=tk_session_id)
        if use_voice_from_input:
            voice = voice_input
        
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
    "TikTok_TTS": Text2AudioTikTokTTS,
    "TikTok_Voice_Chooser": TikTok_VOICE_CHOOSER
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TikTok_TTS": "MM_TikTok_TTS",
    "TikTok_Voice_Chooser": "MM_TK_Voice_Chooser"
}
