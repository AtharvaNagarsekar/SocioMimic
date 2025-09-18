# simulation.py
import random
import google.generativeai as genai
from agent import AIAgent
from typing import List, Dict, Any

def run_simulation(topic: str, num_agents: int, api_key: str, model_name: str) -> List[Dict[str, Any]]:
    """
    Initializes and runs the social simulation using the Gemini API.
    """
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
    except Exception as e:
        # Return an error message if the API key or model name is invalid
        return [{"error": f"Failed to configure the Gemini API. Please check your API key and model name. Details: {e}"}]

    agents = [AIAgent(i, model) for i in range(num_agents)]

    # Simulate influence
    for influencer in agents:
        if influencer.job in ["News Reporter", "Celebrity", "Influencer"]:
            for target_agent in agents:
                if influencer.agent_id != target_agent.agent_id:
                    # A small chance to flip the opinion
                    if random.random() < 0.15: # 15% chance
                        target_agent.opinion = influencer.opinion

    # Generate responses after the influence stage
    simulation_results = []
    for agent in agents:
        response = agent.generate_response(topic)
        simulation_results.append({
            "id": agent.agent_id,
            "personality": agent.personality,
            "job": agent.job,
            "reach": agent.reach,
            "opinion": agent.opinion,
            "response": response,
        })

    return simulation_results