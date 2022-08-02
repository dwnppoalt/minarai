import requests

class OxfordDictionaries:
    def __init__(self) -> None:
        self.BASE_API = "https://od-api.oxforddictionaries.com/api/v2/"
        self.APP_ID = "c83e9d4f"
        self.API_KEY = "9ee7a221528ed8e31f0d6b3c1a902016"
    
    def get_word_definition(self, word: str) -> str:
        url = self.BASE_API + "entries/en/" + word
        headers = {
            "Accept": "application/json",
            "app_id": self.APP_ID,
            "app_key": self.API_KEY
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open("oxford.json", "w", encoding='utf-8') as f:
                f.write(response.text)
            return [
                {
                    'word' : i.get("id"),
                    "lexicalEntries" : [
                        {
                            "entries" : [
                                {
                                "origin" : entries.get("etymologies"),
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

ox = OxfordDictionaries()
print(ox.get_word_definition("apprentice"))
