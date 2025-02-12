from google import genai

class QueryAnalyzer:
    def __init__(self):
        self.client = genai.Client(api_key="AIzaSyCU6iFu1lgxDxOSnPJbphL4CK8m06di_UI")
        self.model_name = "gemini-2.0-flash"

    def reload(self):
        self.client = genai.Client(api_key="AIzaSyCU6iFu1lgxDxOSnPJbphL4CK8m06di_UI")
        self.model_name = "gemini-2.0-flash"


    
    def analyze_query(self, text):
        """
        Uses a Gemini-based model to determine if the text requires:
        - Sentiment Analysis
        - Named Entity Recognition (NER)
        - Both
        
        Returns: 
            str: 'sentiment', 'ner', 'both', 
                 veya sınıflandırılamazsa kendi dilinde fallback metni.
        """
        classification_prompt = f"""
        Analyze the following user input and decide the type of analysis required.
        Options:
        - 'sentiment': If the text expresses an opinion or emotion.
        - 'ner': If the text contains names, organizations, locations, dates, or numerical entities.
        - 'both': If both types of analysis are needed.
        - 'else': If none of these.

        Input: "{text}"
        Response (only one of 'sentiment', 'ner', 'both', or 'else'):
        """

        # 1) Önce metnimizi modele sınıflandırma prompt'u göndererek sorguluyoruz
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=classification_prompt
            )
        except:
            self.reload()
            return "else"



  
        decision =  response.text.strip().lower()

        return decision
    

    def chat_response(self,text):
        fallback_prompt = f"""
        The user input is: "{text}"

        It was classified as something outside of 'sentiment', 'ner', or 'both'.
        Please generate a short reply in own language to the user,
        and at the end of the reply, mention that you are a model that performs NER and sentiment analysis and request a suitable prompt.
            
        The reply should be natural.

        """
        try:
            fallback_response = self.client.models.generate_content(
                model=self.model_name,
                contents=fallback_prompt
            )
        except:
            self.reload()
            return "an error occured. Please, try again"

            # LLM'den gelen metni direkt dönüyoruz.
        return fallback_response.text.strip()
    