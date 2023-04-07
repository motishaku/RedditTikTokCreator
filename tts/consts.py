from enum import Enum

TIKTOK_API_URL = "https://api16-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/"

TIKTOK_USER_AGENT = "com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; " \
                    "Build/NRD90M;tt-ok/3.12.13.1)"

BANNED_WORDS = {
    "AITA": "Am i the ahole"
}

class Voice(Enum):
    EN_AU_001 = "en_au_001"  # English AU - Female
    EN_AU_002 = "en_au_002"  # English AU - Male
    EN_UK_001 = "en_uk_001"  # English UK - Male 1
    EN_UK_003 = "en_uk_003"  # English UK - Male 2
    EN_US_001 = "en_us_001"  # English US - Female (Int. 1)
    EN_US_002 = "en_us_002"  # English US - Female (Int. 2)
    EN_US_006 = "en_us_006"  # English US - Male 1
    EN_US_007 = "en_us_007"  # English US - Male 2
    EN_US_009 = "en_us_009"  # English US - Male 3
    EN_US_010 = "en_us_010"  # English US - Male 4
    DISNEY_EN_US_GHOSTFACE = 'en_us_ghostface'  # Ghost Face
    DISNEY_EN_US_CHEWBACCA = 'en_us_chewbacca'  # Chewbacca
    DISNEY_EN_US_C3PO = 'en_us_c3po'  # C3PO
    DISNEY_EN_US_STITCH = 'en_us_stitch'  # Stitch
    DISNEY_EN_US_STORMTROOPER = 'en_us_stormtrooper'  # Stormtrooper
    DISNEY_EN_US_ROCKET = 'en_us_rocket'  # Rocket
    FR_001 = 'fr_001'  # French - Male 1
    FR_002 = 'fr_002'  # French - Male 2
    DE_001 = 'de_001'  # German - Female
    DE_002 = 'de_002'  # German - Male
    ES_002 = 'es_002'  # Spanish - Male
    ES_MX_002 = 'es_mx_002'  # Spanish MX - Male
    BR_001 = 'br_001'  # Portuguese BR - Female 1
    BR_003 = 'br_003'  # Portuguese BR - Female 2
    BR_004 = 'br_004'  # Portuguese BR - Female 3
    BR_005 = 'br_005'  # Portuguese BR - Male
    ID_001 = 'id_001'  # Indonesian - Female
    JP_001 = 'jp_001'  # Japanese - Female 1
    JP_003 = 'jp_003'  # Japanese - Female 2
    JP_005 = 'jp_005'  # Japanese - Female 3
    JP_006 = 'jp_006'  # Japanese - Male
    KR_002 = 'kr_002'  # Korean - Male 1
    KR_003 = 'kr_003'  # Korean - Female
    KR_004 = 'kr_004'  # Korean - Male 2
    EN_FEMALE_F08_SALUT_DAMOUR = 'en_female_f08_salut_damour'  # Alto
    EN_MALE_M03_LOBBY = 'en_male_m03_lobby'  # Tenor
    EN_FEMALE_F08_WARMY_BREEZE = 'en_female_f08_warmy_breeze'  # Warmy Breeze
    EN_MALE_M03_SUNSHINE_SOON = 'en_male_m03_sunshine_soon'  # Sunshine Soon
    EN_MALE_NARRATION = 'en_male_narration'  # narrator
    EN_MALE_FUNNY = 'en_male_funny'  # wacky
    EN_FEMALE_EMOTIONAL = 'en_female_emotional'  # peaceful


