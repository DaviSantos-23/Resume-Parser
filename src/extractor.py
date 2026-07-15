import re
from src.skills import HARD_SKILLS


class ResumeExtractor:
    @staticmethod
    def extract_skills(text):

        encontradas = []

        texto = text.lower()

        for skill in HARD_SKILLS:

            pattern = r"\b" + re.escape(skill.lower()) + r"\b"

            if re.search(pattern, texto):

                encontradas.append(skill)

        return sorted(encontradas)

    @staticmethod
    def extract_email(text):

        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

        result = re.search(pattern, text)

        return result.group() if result else ""

    @staticmethod
    def extract_phone(text):

        pattern = r"(?:\+55\s?)?(?:\(?\d{2}\)?\s?)?(?:9?\d{4})[-\s]?\d{4}"

        result = re.search(pattern, text)

        return result.group() if result else ""

    @staticmethod
    def extract_linkedin(text):

        pattern = r"(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[A-Za-z0-9_-]+"

        result = re.search(pattern, text, re.IGNORECASE)

        return result.group() if result else ""

    @staticmethod
    def extract_github(text):

        pattern = r"(?:https?:\/\/)?(?:www\.)?github\.com\/[A-Za-z0-9_-]+"

        result = re.search(pattern, text, re.IGNORECASE)

        return result.group() if result else ""

    @staticmethod
    def extract_name(text):

        linhas = text.split("\n")

        for linha in linhas[:10]:

            linha = linha.strip()

            if len(linha) < 5:
                continue

            if "@" in linha:
                continue

            if "linkedin" in linha.lower():
                continue

            if "github" in linha.lower():
                continue

            if any(char.isdigit() for char in linha):
                continue

            palavras = linha.split()

            if len(palavras) >= 2:
                return linha

        return ""


    @classmethod
    def extract_all(cls, text):

        data = {

        "name": cls.extract_name(text),

        "email": cls.extract_email(text),

        "phone": cls.extract_phone(text),

        "linkedin": cls.extract_linkedin(text),

        "github": cls.extract_github(text),

        "skills": ", ".join(
            cls.extract_skills(text)
        )

        }

        data["status"] = cls.get_status(data)

        return data

    @staticmethod
    def get_status(data):

            campos = [
                data["name"],
                data["email"],
                data["phone"]
            ]

            preenchidos = sum(
                1 for campo in campos if campo
            )

            if preenchidos == 3:
                return "🟢 Completo"

            elif preenchidos == 2:
                return "🟡 Parcial"

            return "🔴 Insuficiente"

                