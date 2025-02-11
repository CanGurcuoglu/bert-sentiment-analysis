from google import genai

class QueryAnalyzer:
    def __init__(self):
        self.client = genai.Client(api_key="AIzaSyCU6iFu1lgxDxOSnPJbphL4CK8m06di_UI")


    def analyze_query(self, text):
        print("analyze_query")
        """
        Uses Gemini to determine if the text requires:
        - Sentiment Analysis
        - Named Entity Recognition (NER)
        - Both
        Returns: 'sentiment', 'ner', or 'both'
        """
        prompt = f"""
        Analyze the following user input and decide the type of analysis required.
        Options:
        - 'sentiment': If the text expresses an opinion or emotion.
        - 'ner': If the text contains names, organizations, locations, dates, or numerical entities.
        - 'both': If both types of analysis are needed.

        Input: "{text}"
        Response (only one of 'sentiment', 'ner', or 'both'):
        """

        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )  # FIXED
        print("response alındı")
        decision = response.text.strip().lower()  # FIXED
        print("decision alındı")

        if decision not in {"sentiment", "ner", "both"}:
            print("bulamadım")
            return "sentiment"  # Default to sentiment analysis if Gemini output is invalid

        return decision
    