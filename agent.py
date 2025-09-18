# agent.py
import random
import google.generativeai as genai

class AIAgent:
    """
    Represents an AI agent with a specific personality, job, and social reach, using the Gemini API.
    """
    def __init__(self, agent_id: int, model: genai.GenerativeModel):
        self.agent_id = agent_id
        self.personality = self._get_random_personality()
        self.job = self._get_random_job()
        self.reach = self._get_initial_reach()
        self.opinion = random.choice(["positive", "negative", "neutral"])
        self.model = model

    def _get_random_personality(self) -> str:
        """Assigns a random personality to the agent."""
        personalities = ["bossy", "egoistic", "selfish", "friendly", "analytical", "skeptical", "optimistic"]
        return random.choice(personalities)

    def _get_random_job(self) -> str:
        """Assigns a random job to the agent."""
        jobs = ["Business Analyst", "Customer Service Rep", "News Reporter", "Celebrity", "Influencer", "Teacher", "Engineer"]
        return random.choice(jobs)

    def _get_initial_reach(self) -> int:
        """Sets the initial social reach of the agent based on their job."""
        if self.job in ["News Reporter", "Celebrity", "Influencer"]:
            return random.randint(10000, 1000000)
        else:
            return random.randint(100, 5000)

    def generate_response(self, topic: str) -> str:
        """
        Generates a response to a topic based on the agent's personality and job using Gemini.
        """
        prompt = f"""
        You are an AI agent with the following characteristics:
        - Your personality is: {self.personality}
        - Your job is: {self.job}
        - Your current opinion on the topic is: {self.opinion}

        Based on these traits, write a short, compelling response to the following topic.
        Topic: "{topic}"
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            # It's helpful to see the specific error from the API
            return f"Error generating response: {e}"