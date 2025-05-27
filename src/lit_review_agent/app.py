import sys
import os

# Get the path to the 'src' directory, which is the parent of 'lit_review_agent'
# os.path.dirname(__file__) gives the directory of app.py (src/lit_review_agent)
# os.path.join(..., '..') goes one level up to 'src'
SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH) # Insert at the beginning to ensure it's checked first

# Now that src is in sys.path, we can use absolute imports from lit_review_agent
import streamlit as st
import asyncio
from lit_review_agent.agent import LiteratureAgent # Assuming agent.py is in the same directory or a proper module
from lit_review_agent.utils.config import Config # Assuming Config is accessible

def main():
    st.set_page_config(page_title="AI Literature Review Assistant", layout="wide")

    st.title("AI Literature Review Assistant")

    st.sidebar.header("Controls")
    # Placeholder for future controls
    max_papers = st.sidebar.number_input("Max papers to retrieve:", min_value=1, max_value=100, value=10)
    retrieve_full_text = st.sidebar.checkbox("Retrieve full text (can be slow)", value=False)
    # Add more controls as needed, e.g., year range, sources

    query = st.text_input("Enter your research query or keywords:", "")

    if "review_results" not in st.session_state:
        st.session_state.review_results = None
    if "processing" not in st.session_state:
        st.session_state.processing = False

    if st.button("Start Review Process", disabled=st.session_state.processing):
        if query:
            st.session_state.processing = True
            st.session_state.review_results = None # Reset previous results
            st.info(f"Processing query: {query}...")
            
            # It's good practice to manage config loading properly.
            # For now, using default config.
            # In a real app, you might load from a file or environment variables.
            try:
                config = Config() 
                agent = LiteratureAgent(config=config)

                # Run the async function
                # This is a simplified way to run asyncio in Streamlit.
                # For more complex apps, consider a dedicated asyncio event loop management.
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                results = loop.run_until_complete(
                    agent.conduct_literature_review(
                        research_topic=query,
                        max_papers=max_papers,
                        retrieve_full_text=retrieve_full_text
                        # Pass other parameters like sources, year_start, year_end from sidebar controls
                    )
                )
                st.session_state.review_results = results
                st.success("Literature review process completed!")
            except Exception as e:
                st.error(f"An error occurred: {e}")
            finally:
                st.session_state.processing = False
                st.rerun() # Rerun to update button state and display results
        else:
            st.warning("Please enter a query.")

    if st.session_state.processing:
        st.progress(100) # Indeterminate progress bar while processing

    if st.session_state.review_results:
        st.subheader("Review Results")
        # Displaying a summary of results for now.
        # You can customize this to show more details.
        
        retrieved_count = len(st.session_state.review_results.get("retrieved_items", []))
        processed_count = len(st.session_state.review_results.get("processed_papers", []))
        
        st.write(f"Total items retrieved (after deduplication): {retrieved_count}")
        st.write(f"Total papers processed (with full text if enabled): {processed_count}")

        # Example: Display titles of retrieved papers
        if st.session_state.review_results.get("retrieved_items"):
            st.markdown("### Retrieved Papers:")
            for idx, item in enumerate(st.session_state.review_results["retrieved_items"]):
                title = item.get("title", "N/A")
                authors = ", ".join(item.get("authors", ["N/A"]))
                year = item.get("year", "N/A")
                source = item.get("source", "N/A")
                url = item.get("url", "#")
                markdown_string = f"""{idx+1}. **{title}**  
    *Authors: {authors} ({year}) - Source: {source}*  
    [Link]({url})"""
                st.markdown(markdown_string)
        
        # You might want to display other parts of the results dictionary:
        # st.json(st.session_state.review_results) # To see the full structure for debugging


if __name__ == "__main__":
    main() 