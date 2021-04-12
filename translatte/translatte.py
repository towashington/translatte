#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.request import urlopen, Request
from urllib.parse import quote
import gzip, json, sys, os

sys.path.append('../..')
from src.aws_utils import connect_amazon_translate

from google.cloud import translate_v2


class Translator:
    @staticmethod
    def get_response_from_request(request):
        response = urlopen(request)
        return response.read()

    @staticmethod
    def get_translation_from_response(response):
        lists = json.loads(response)
        translation_sentences = []
        for list_ in lists[0]:
            translation_sentences.append(list_[0])
        translation = ''.join(translation_sentences)
        return translation

    @staticmethod
    def translate_google_free(input_text, target_lang, source_lang='auto'):
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={quote(input_text)}"
        response = Translator.get_response_from_request(Request(url=url))
        return Translator.get_translation_from_response(response)

    @staticmethod
    def translate_google(input_text, target_lang):
        translate_google_client = translate_v2.Client()
        response = translate_google_client.translate(input_text, target_language=target_lang)
        return response['translatedText']

    @staticmethod
    def translate_amazon(input_text, target_lang, source_lang='auto'):
        translate = connect_amazon_translate()
        try:
            result = translate.translate_text(Text=input_text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang).get('TranslatedText')
        except:
            result = input_text
        return result

    @staticmethod
    def translate(input_text, target_lang, engine, source_lang='auto'):
        assert engine in ['Amazon', 'Google', 'Google_free']

        if engine == 'Amazon':
            translate_client = connect_amazon_translate()
            try:
                response = translate_client.translate_text(Text=input_text, SourceLanguageCode=source_lang, TargetLanguageCode=target_lang)
                return response.get('SourceLanguageCode'), response.get('TranslatedText')
            except:
                return 'failed_to_translate', input_text
        
        if engine == 'Google':
            translate_client = translate_v2.Client()
            response = translate_client.translate(input_text, target_language=target_lang)
            return response['detectedSourceLanguage'], response['translatedText']
        
        if engine == 'Google_free':
            response = translate_google_free(input_text, target_lang, source_lang=source_lang)
            return 'no_detection', response
