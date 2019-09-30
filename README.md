# translatte
Easily translate texts in Python with the Google Translate API

### `class translatte.Translator`
#### `translate(input_text, target_language, source_language='auto')`
Translates a text to a target language. If the source language is not specified, it will be detected automatically by the Google Translate API.

```python
from translatte import Translator
# translation = Translator.translate("Este es el texto de entrada", "en", "es")
translation = Translator.translate("Este es el texto de entrada", "en")
```

Examples:
```python
>>> from translatte import Translator

>>> Translator.translate("Este es el texto de entrada", "en")
'This is the input text'

>>> Translator.translate("Este es el texto de entrada", "ja")
'これは入力テキストです'

>>> Translator.translate("Este es el texto de entrada", "pt")
'Este é o texto de entrada'
```
