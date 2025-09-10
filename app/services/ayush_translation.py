"""
AYUSH/NAMASTE to English Translation Service

This module provides translation mappings for traditional medicine condition names
from AYUSH/NAMASTE systems to standardized English medical terminology.
"""

from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class AYUSHTranslator:
    """
    Translator for AYUSH/NAMASTE condition names to English equivalents.
    """

    def __init__(self):
        # Comprehensive mapping dictionary for AYUSH/NAMASTE condition names
        self.condition_mapping = {
            # Common Ayurvedic conditions (Sanskrit/Hindi)
            "शिरःशूल": "Headache",
            "शीर्षवेदना": "Head Pain",
            "अजीर्ण": "Indigestion",
            "अग्निमांद्य": "Digestive Weakness",
            "ज्वर": "Fever",
            "सन्धिवात": "Arthritis",
            "अस्थिसंधि वेदना": "Bone and Joint Pain",
            "संधिशूल": "Joint Pain",
            "कटिशूल": "Back Pain",
            "कटिवेदना": "Lower Back Pain",
            "अर्श": "Hemorrhoids",
            "पाइल्स": "Piles",
            "कास": "Cough",
            "श्वास": "Asthma",
            "श्वसन रोग": "Respiratory Disorder",
            "नासावेग": "Allergic Rhinitis",
            "नाक बहना": "Runny Nose",
            "अतिसार": "Diarrhea",
            "गुदव्रण": "Anal Fissure",
            "मुंहासे": "Acne",
            "त्वचा रोग": "Skin Disease",
            "खाज": "Itching",
            "दाद": "Ringworm",
            "एक्जिमा": "Eczema",
            "बवासीर": "Hemorrhoids",
            "अनिद्रा": "Insomnia",
            "निद्रानाश": "Sleep Disorder",
            "मानसिक तनाव": "Mental Stress",
            "चिंता": "Anxiety",
            "अवसाद": "Depression",
            "स्मृति हानि": "Memory Loss",
            "मधुमेह": "Diabetes",
            "प्रमेह": "Diabetes Mellitus",
            "रक्तचाप": "Hypertension",
            "उच्च रक्तचाप": "High Blood Pressure",
            "हृदय रोग": "Heart Disease",
            "हृदयाघात": "Heart Attack",
            "स्त्री रोग": "Gynecological Disorder",
            "मासिक धर्म विकार": "Menstrual Disorder",
            "बांझपन": "Infertility",
            "गर्भधारण समस्या": "Pregnancy Complications",
            "बाल रोग": "Pediatric Disorder",
            "बच्चों की बीमारी": "Childhood Illness",
            "वृद्धावस्था रोग": "Geriatric Disorder",
            "बुढ़ापे की बीमारी": "Age-related Disease",

            # Siddha medicine conditions
            "வலி": "Pain",
            "காய்ச்சல்": "Fever",
            "இருமல்": "Cough",
            "மூச்சுத்திணறல்": "Breathing Difficulty",
            "வயிற்றுப்போக்கு": "Diarrhea",
            "கல்லீரல் நோய்": "Liver Disease",
            "சிறுநீர்ப்பை நோய்": "Bladder Disease",
            "நீரிழிவு நோய்": "Diabetes",

            # Unani medicine conditions
            "سرد و بلغم": "Cold and Phlegm",
            "حرارت": "Heat/Fever",
            "سعال": "Cough",
            "زکام": "Cold",
            "اسہال": "Diarrhea",
            "قئ": "Nausea",
            "دموی": "Bloody",
            "سفید": "White Discharge",

            # Homeopathy conditions
            "सिर दर्द": "Headache",
            "पेट दर्द": "Abdominal Pain",
            "बुखार": "Fever",
            "खांसी": "Cough",
            "दस्त": "Diarrhea",
            "एलर्जी": "Allergy",
            "त्वचा रोग": "Skin Disease",
            "अनिद्रा": "Insomnia",

            # Additional common conditions
            "माइग्रेन": "Migraine",
            "टी बी": "Tuberculosis",
            "कैंसर": "Cancer",
            "एड्स": "AIDS",
            "मलेरिया": "Malaria",
            "डेंगू": "Dengue",
            "चिकनगुनिया": "Chikungunya",
            "कोविड": "COVID-19",
            "कोरोना": "Coronavirus",

            # English to English (for completeness)
            "headache": "Headache",
            "fever": "Fever",
            "cough": "Cough",
            "cold": "Common Cold",
            "diarrhea": "Diarrhea",
            "indigestion": "Indigestion",
            "arthritis": "Arthritis",
            "asthma": "Asthma",
            "diabetes": "Diabetes",
            "hypertension": "Hypertension",
            "anxiety": "Anxiety",
            "depression": "Depression",
            "insomnia": "Insomnia",
            "acne": "Acne",
            "eczema": "Eczema",
            "migraine": "Migraine"
        }

        # System type mappings
        self.system_type_mapping = {
            "आयुर्वेद": "Ayurveda",
            "सिद्ध": "Siddha",
            "यूनानी": "Unani",
            "होम्योपैथी": "Homeopathy",
            "ஆயுர்வேதம்": "Ayurveda",
            "சித்த மருத்துவம்": "Siddha",
            "யூனானி மருத்துவம்": "Unani",
            "ஹோமியோபதி": "Homeopathy"
        }

        # Severity level mappings
        self.severity_mapping = {
            "मृदु": "Mild",
            "मध्यम": "Moderate",
            "तीव्र": "Severe",
            "गंभीर": "Critical",
            "हल्का": "Mild",
            "भारी": "Severe",
            "कुपोषण": "Malnutrition",
            "जटिल": "Complicated"
        }

    def translate_condition(self, condition_name: str) -> str:
        """
        Translate AYUSH/NAMASTE condition name to English equivalent.

        Args:
            condition_name: Original condition name in native language

        Returns:
            Translated condition name in English
        """
        if not condition_name:
            return ""

        # Clean the input
        cleaned_name = condition_name.strip()

        # Try exact match first
        if cleaned_name in self.condition_mapping:
            return self.condition_mapping[cleaned_name]

        # Try case-insensitive match
        for key, value in self.condition_mapping.items():
            if key.lower() == cleaned_name.lower():
                return value

        # Try partial match (contains)
        for key, value in self.condition_mapping.items():
            if key.lower() in cleaned_name.lower() or cleaned_name.lower() in key.lower():
                logger.info(
                    "Partial match found for condition translation",
                    original=condition_name,
                    matched=key,
                    translated=value
                )
                return value

        # If no match found, return original with note
        logger.info(
            "No translation found for condition",
            original=condition_name,
            action="keeping_original"
        )
        return condition_name

    def translate_system_type(self, system_type: str) -> str:
        """
        Translate system type to English equivalent.

        Args:
            system_type: Original system type in native language

        Returns:
            Translated system type in English
        """
        if not system_type:
            return ""

        cleaned_type = system_type.strip()

        # Try exact match
        if cleaned_type in self.system_type_mapping:
            return self.system_type_mapping[cleaned_type]

        # Try case-insensitive match
        for key, value in self.system_type_mapping.items():
            if key.lower() == cleaned_type.lower():
                return value

        return system_type

    def translate_severity(self, severity: str) -> str:
        """
        Translate severity level to English equivalent.

        Args:
            severity: Original severity in native language

        Returns:
            Translated severity in English
        """
        if not severity:
            return ""

        cleaned_severity = severity.strip()

        # Try exact match
        if cleaned_severity in self.severity_mapping:
            return self.severity_mapping[cleaned_severity]

        # Try case-insensitive match
        for key, value in self.severity_mapping.items():
            if key.lower() == cleaned_severity.lower():
                return value

        return severity

    def get_translation_stats(self) -> Dict[str, int]:
        """
        Get statistics about available translations.

        Returns:
            Dictionary with translation counts by category
        """
        return {
            "condition_mappings": len(self.condition_mapping),
            "system_type_mappings": len(self.system_type_mapping),
            "severity_mappings": len(self.severity_mapping),
            "total_mappings": len(self.condition_mapping) + len(self.system_type_mapping) + len(self.severity_mapping)
        }

    def add_condition_mapping(self, native_term: str, english_term: str) -> None:
        """
        Add a new condition mapping to the dictionary.

        Args:
            native_term: Term in native language
            english_term: Equivalent term in English
        """
        self.condition_mapping[native_term] = english_term
        logger.info(
            "Added new condition mapping",
            native=native_term,
            english=english_term
        )

    def add_system_type_mapping(self, native_term: str, english_term: str) -> None:
        """
        Add a new system type mapping to the dictionary.

        Args:
            native_term: Term in native language
            english_term: Equivalent term in English
        """
        self.system_type_mapping[native_term] = english_term
        logger.info(
            "Added new system type mapping",
            native=native_term,
            english=english_term
        )

    def add_severity_mapping(self, native_term: str, english_term: str) -> None:
        """
        Add a new severity mapping to the dictionary.

        Args:
            native_term: Term in native language
            english_term: Equivalent term in English
        """
        self.severity_mapping[native_term] = english_term
        logger.info(
            "Added new severity mapping",
            native=native_term,
            english=english_term
        )


# Global translator instance
translator = AYUSHTranslator()


def translate_condition_name(condition_name: str) -> str:
    """
    Convenience function to translate condition names.

    Args:
        condition_name: Original condition name

    Returns:
        Translated condition name
    """
    return translator.translate_condition(condition_name)


def translate_system_type(system_type: str) -> str:
    """
    Convenience function to translate system types.

    Args:
        system_type: Original system type

    Returns:
        Translated system type
    """
    return translator.translate_system_type(system_type)


def translate_severity(severity: str) -> str:
    """
    Convenience function to translate severity levels.

    Args:
        severity: Original severity

    Returns:
        Translated severity
    """
    return translator.translate_severity(severity)
