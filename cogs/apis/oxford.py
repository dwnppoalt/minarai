import requests
import os
class OxfordDictionaries:
    def __init__(self) -> None:
        self.BASE_API = "https://od-api.oxforddictionaries.com/api/v2/"
        self.APP_ID = os.getenv("OXFORD_APP_ID")
        self.API_KEY = os.getenv("OXFORD_API_KEY")
    
    def dictionary(self, word):
        url = self.BASE_API + "entries/en/" + word
        headers = {
            "Accept": "application/json",
            "app_id": self.APP_ID,
            "app_key": self.API_KEY
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return [
                {
                    "lexicalEntries" : [
                        {
                            'word' : x.get("id"),
                            "entries" : [
                                {
                                "origin" : None if not entries.get("etymologies") else entries.get("etymologies"),
                                "pronunciations" : [
                                    {
                                        "phoneticSpelling" : pronounciations.get("phoneticSpelling"),
                                        "audioFile" : pronounciations.get("audioFile"),
                                        "dialects" : pronounciations.get("dialects"),
                                    } for pronounciations in entries.get("pronunciations")
                                ],
                                'senses' : [
                                    {
                                        'definitions' : senses.get("definitions"),
                                        'examples' : None if not senses.get("examples") else [ex.get("text") for ex in senses.get("examples")],
                                        'synonyms' : None if not senses.get("synonyms") else [syn.get("text") for syn in senses.get("synonyms")], 
                                    } for senses in entries.get("senses")
                                ],
                                "lexicalCategory" : x.get("lexicalCategory").get("text"),
                                } for entries in x.get("entries")
                            ]
                        } for x in i.get("lexicalEntries")
                    ]
                } for i in response.json().get('results')
            ]
        else:
            return "Word not found"

    def thesaurus(self, word):
        url = self.BASE_API + "thesaurus/en/" + word
        headers = {
            "Accept": "application/json",
            "app_id": self.APP_ID,
            "app_key": self.API_KEY
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return [
                {
                    "lexicalEntries" : [
                        {
                            "word" : x.get("text"),
                            "entries" : [
                                {
                                    "senses" : [
                                        {
                                            "antonyms" : None if not senses.get("antonyms") else [ant.get("text") for ant in senses.get("antonyms")],
                                            "synonyms" : None if not senses.get("synonyms") else [syn.get("text") for syn in senses.get("synonyms")]
                                        } for senses in entries.get("senses")
                                    ],
                                    "lexicalCategory" : x.get("lexicalCategory").get("text"),
                                } for entries in x.get("entries")
                            ]
                        } for x in i.get("lexicalEntries")
                    ]
                } for i in response.json().get('results')
            ]

