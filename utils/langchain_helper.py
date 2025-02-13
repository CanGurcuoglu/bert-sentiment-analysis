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
        - 'ner': If the text contains names, operator names, organizations, locations, dates, complaints about network, payment, service, infrastructure etc.
        - 'both': If both types of analysis are needed.
        - 'query': If the text requires sql query like "How many negative reviews are there about Vodafone?"
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
    
    def sql_analyzer(self,text):
        fallback_prompt = f"""
        You can use two function and they have required arguments:

        - ope_label which requires:
            -operator_name: must be in this list "ope_list = ["Turkcell","Vodafone","Turk Telekom","AT&T","T-mobile","ID-Mobile","O2"]"
            -label_type: must be in this list "labels = ['OPE', 'APP', 'PAY', 'DATE', 'SER', 'OTH', 'ORG', 'NUM', 'PER', 'LOC', 'PKG', 'NET', 'LIN', 'BANK']"
        - ope_sentiment which requires:
            -operator_name: must be in this list "ope_list = ["Turkcell","Vodafone","Turk Telekom","AT&T","T-mobile","ID-Mobile","O2"]"
            -sentiment_type: must be in this list "sentiment_labels = ["Negative", "Neutral", "Positive"]"
        The user input is: "{text}"

        args:
            replace this arguments with corresponding names from user input:
            "operator_name": one of these  ["Turkcell","Vodafone","Turk Telekom","AT&T","T-mobile","ID-Mobile","O2"]
            "label_type": one of these ['OPE', 'APP', 'PAY', 'DATE', 'SER', 'OTH', 'ORG', 'NUM', 'PER', 'LOC', 'PKG', 'NET', 'LIN', 'BANK']
            "sentiment_type": one of these ["Negative", "Neutral", "Positive"]

        Options:
            "ope_label", "operator_name", "label_type": If user input contains operator_name and label_type
            "ope_sentiment", "operator_name", "sentiment_type": If user input contains operator_name and sentiment_type
            "answer": If none of these.
        Response (only one of 'ope_label, operator_name, label_type', 'ope_sentiment, operator_name, sentiment_type', or 'answer')

        Example:
            "How many negative reviews are there about Vodafone?"--> 'ope_sentiment,Vodafone,Negative'
            "How many negative reviews are there?" --> "answer"
        """
        try:
            fallback_response = self.client.models.generate_content(
                model=self.model_name,
                contents=fallback_prompt
            )
        except:
            self.reload()
            return "an error occured. Please try again"

            # LLM'den gelen metni direkt dönüyoruz.
        return fallback_response.text.strip()
    