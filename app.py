# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from simulation import run_simulation

st.set_page_config(layout="wide")

st.title("Socio-Mimic ")
st.markdown("This application simulates a social network of AI agents with diverse personalities and roles. Enter a topic and see how they react and influence one another.")

# --- Sidebar Inputs (No Changes Here) ---
st.sidebar.header("Simulation Settings")
user_topic = st.sidebar.text_area("Enter a topic or post for the agents to discuss:", "The impact of generative AI on the job market.")
num_agents = st.sidebar.slider("Number of AI Agents:", min_value=5, max_value=100, value=25)

st.sidebar.subheader("API Credentials")
api_key = st.sidebar.text_input("Google AI API Key", type="password", value="Enter your API key here")
model_name = st.sidebar.text_input("Gemini Model Name", value="gemini-1.5-flash")


if st.sidebar.button("Run Simulation"):
    if not all([user_topic, api_key, model_name]):
        st.warning("Please provide a topic, your API key, and a model name.")
    else:
        with st.spinner("The AI agents are gathering their thoughts..."):
            results = run_simulation(user_topic, num_agents, api_key, model_name)

        # --- NEW: Check for API errors before proceeding ---
        if results and "error" in results[0]:
            st.error(results[0]["error"])
        else:
            # --- NEW: Convert results to a DataFrame for analysis ---
            df = pd.DataFrame(results)

            st.header("Simulation Dashboard")
            st.markdown("---")

            # --- NEW: Data Analysis and Visualization Section ---
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Opinion Distribution")
                # Count agents per opinion
                opinion_counts = df['opinion'].value_counts().reset_index()
                opinion_counts.columns = ['Opinion', 'Number of Agents']
                
                # Bar chart for agent counts
                fig_counts = px.bar(opinion_counts, x='Opinion', y='Number of Agents', color='Opinion',
                                    color_discrete_map={'positive': '#2ECC71', 'negative': '#E74C3C', 'neutral': '#95A5A6'},
                                    labels={'Number of Agents': 'Number of Agents', 'Opinion': 'Sentiment'})
                st.plotly_chart(fig_counts, use_container_width=True)

            with col2:
                st.subheader("Potential Reach by Opinion")
                # Sum reach for each opinion group
                reach_by_opinion = df.groupby('opinion')['reach'].sum().reset_index()
                
                # Pie chart for total reach
                fig_reach = px.pie(reach_by_opinion, names='opinion', values='reach',
                                   title='Share of Voice by Potential Reach', color='opinion',
                                   color_discrete_map={'positive': '#2ECC71', 'negative': '#E74C3C', 'neutral': '#95A5A6'})
                st.plotly_chart(fig_reach, use_container_width=True)

            st.markdown("---")

            # --- NEW: Summarized View and Scalability Section ---
            st.header("Analysis & Scalability Outlook")

            # Calculate metrics for the summary
            total_reach = df['reach'].sum()
            reach_by_opinion_dict = reach_by_opinion.set_index('opinion')['reach'].to_dict()
            opinion_counts_dict = opinion_counts.set_index('Opinion')['Number of Agents'].to_dict()

            dominant_opinion_by_count = max(opinion_counts_dict, key=opinion_counts_dict.get)
            dominant_opinion_by_reach = max(reach_by_opinion_dict, key=reach_by_opinion_dict.get)

            st.markdown(f"""
            #### Summarized View
            - **Dominant Opinion (by Agent Count):** The most common stance is **{dominant_opinion_by_count}**, held by **{opinion_counts_dict.get(dominant_opinion_by_count, 0)}** agents.
            - **Dominant Opinion (by Potential Reach):** The **{dominant_opinion_by_reach}** viewpoint commands the largest audience, with a potential reach of **{reach_by_opinion_dict.get(dominant_opinion_by_reach, 0):,}** people. This represents **{reach_by_opinion_dict.get(dominant_opinion_by_reach, 0)/total_reach:.1%}** of the total possible reach.
            """)

            # Identify the top influencer
            top_influencer = df.loc[df['reach'].idxmax()]
            st.markdown(f"""
            - **Key Influencer:** The most influential agent is **Agent #{top_influencer['id']}** ({top_influencer['job']}), whose **{top_influencer['opinion']}** opinion alone can reach **{top_influencer['reach']:,}** individuals.
            """)
            
            st.markdown("""
            #### How This Might Scale to a Larger Audience
            When a simulation scales from a small group to millions, the dynamics of reach and influence become far more critical. Here's what we could expect:

            1.  **Viral Cascades:** The opinion of the key influencer(s) (like Celebrities or News Reporters) would likely spread exponentially. If their message is compelling, it could trigger an "information cascade," where other agents adopt the opinion simply because a trusted, high-reach source did.

            2.  **Echo Chambers:** Agents are more likely to interact with and be influenced by opinions they already lean towards. On a large scale, this can create "echo chambers" or "filter bubbles," where the **{dominant_opinion_by_reach}** view is amplified within a large segment of the population, while opposing views are suppressed or ignored.

            3.  **The Tipping Point:** In a large network, a small but highly influential group can create a "tipping point." If the **{dominant_opinion_by_reach}** camp manages to convince a critical mass of moderately connected individuals, their opinion could rapidly become the dominant public consensus, even if it started as a minority view.
            """)

            st.markdown("---")

            # --- OLD: Detailed agent results are now in an expander ---
            with st.expander("View Detailed Agent-by-Agent Responses"):
                for res in results:
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.info(f"**Agent #{res['id']}**")
                        st.write(f"**Personality:** {res['personality']}")
                        st.write(f"**Job:** {res['job']}")
                        st.write(f"**Reach:** {res['reach']:,}")
                        st.write(f"**Opinion:** {res['opinion'].capitalize()}")
                    with col2:
                        st.markdown(f"> {res['response']}")
            
            st.success("Simulation and analysis complete.")

else:
    st.info("Adjust the settings in the sidebar and click 'Run Simulation' to begin.")