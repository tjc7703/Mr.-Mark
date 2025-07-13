try:
    from googletrans import Translator
except ImportError:
    print('googletrans 패키지가 설치되어 있지 않습니다. pip install googletrans==4.0.0-rc1 로 설치하세요.')
    exit(1)
import sys

translator = Translator()
text = sys.argv[1] if len(sys.argv) > 1 else 'Hello, world!'
lang = sys.argv[2] if len(sys.argv) > 2 else 'ko'

translated = translator.translate(text, dest=lang)
print(translated.text) 