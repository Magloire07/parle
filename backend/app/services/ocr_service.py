"""
Service OCR pour l'extraction de texte à partir d'images
"""
import pytesseract
from PIL import Image
import io
import logging
from typing import Dict, List
import re

logger = logging.getLogger(__name__)

class OCRService:
    """Service de traitement OCR"""
    
    def __init__(self):
        self.tesseract_config = '--oem 3 --psm 6'
        self.languages = 'fra+eng'
    
    async def extract_text(self, image_content: bytes) -> Dict:
        """
        Extrait le texte d'une image
        """
        try:
            # Ouverture de l'image
            image = Image.open(io.BytesIO(image_content))
            
            # Vérification de la taille de l'image
            if image.size[0] < 100 or image.size[1] < 100:
                raise ValueError("Image trop petite pour l'OCR")
            
            # Conversion en RGB si nécessaire
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Amélioration de l'image pour l'OCR
            image = self._enhance_image(image)
            
            # Extraction du texte avec Tesseract
            text = pytesseract.image_to_string(
                image, 
                lang=self.languages,
                config=self.tesseract_config
            )
            
            # Nettoyage du texte
            cleaned_text = self._clean_text(text)
            
            # Vérification que du texte a été extrait
            if not cleaned_text.strip():
                raise ValueError("Aucun texte détecté dans l'image")
            
            # Segmentation en paragraphes
            paragraphs = self._segment_paragraphs(cleaned_text)
            
            # Calcul de la confiance
            confidence = self._calculate_confidence(image)
            
            return {
                "text": cleaned_text,
                "paragraphs": paragraphs,
                "confidence": confidence,
                "language": self._detect_language(cleaned_text)
            }
            
        except Exception as e:
            logger.error(f"Erreur extraction OCR: {str(e)}")
            raise
    
    async def analyze_text(self, text: str) -> Dict:
        """
        Analyse un texte déjà extrait pour le structurer
        """
        try:
            # Nettoyage du texte
            cleaned_text = self._clean_text(text)
            
            # Segmentation en paragraphes
            paragraphs = self._segment_paragraphs(cleaned_text)
            
            return {
                "text": cleaned_text,
                "paragraphs": paragraphs,
                "confidence": 1.0,  # Texte déjà extrait
                "language": self._detect_language(cleaned_text)
            }
            
        except Exception as e:
            logger.error(f"Erreur analyse texte: {str(e)}")
            raise
    
    def _clean_text(self, text: str) -> str:
        """Nettoie le texte extrait"""
        # Suppression des caractères de contrôle
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        # Normalisation des espaces
        text = re.sub(r'\s+', ' ', text)
        
        # Suppression des espaces en début et fin
        text = text.strip()
        
        return text
    
    def _segment_paragraphs(self, text: str) -> List[str]:
        """Segmente le texte en paragraphes"""
        # Division par double saut de ligne
        paragraphs = re.split(r'\n\s*\n', text)
        
        # Nettoyage des paragraphes vides
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        return paragraphs
    
    def _calculate_confidence(self, image: Image.Image) -> float:
        """Calcule la confiance de l'extraction OCR"""
        try:
            # Utilisation de l'API de confiance de Tesseract
            data = pytesseract.image_to_data(
                image, 
                lang=self.languages,
                config=self.tesseract_config,
                output_type=pytesseract.Output.DICT
            )
            
            # Calcul de la confiance moyenne
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            if confidences:
                return sum(confidences) / len(confidences) / 100.0
            else:
                return 0.0
                
        except Exception:
            return 0.5  # Confiance par défaut
    
    def _enhance_image(self, image: Image.Image) -> Image.Image:
        """Améliore l'image pour l'OCR"""
        try:
            from PIL import ImageEnhance, ImageFilter
            
            # Augmentation du contraste
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)
            
            # Augmentation de la netteté
            image = image.filter(ImageFilter.SHARPEN)
            
            # Amélioration de la luminosité
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(1.1)
            
            return image
        except Exception as e:
            logger.warning(f"Erreur amélioration image: {str(e)}")
            return image
    
    def _detect_language(self, text: str) -> str:
        """Détecte la langue du texte"""
        # Analyse simple basée sur les caractères
        french_chars = len(re.findall(r'[àâäéèêëïîôöùûüÿç]', text.lower()))
        english_chars = len(re.findall(r'[a-z]', text.lower()))
        
        if french_chars > english_chars * 0.1:
            return "fr"
        else:
            return "en"
