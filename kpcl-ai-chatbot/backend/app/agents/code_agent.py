import logging
import langchain
import os
from app.core.config import settings
from app.agents.prompts import SYSTEM_PLANNER_PROMPT
# 🚀 Import both the execution sandbox and the new Search-First node
from app.services.data_parser import execute_agent_code, find_relevant_context
from app.models.response import ChatResponse

# 🚀 Initializing Google Gemini Flash 2.5/3
from langchain_google_genai import ChatGoogleGenerativeAI

# 🔦 Debug mode shows exactly what is sent to Gemini in your terminal
langchain.debug = True

logger = logging.getLogger(__name__)

# 🚀 SAFETY CHECK: Ensure the key is loaded
api_key = settings.GEMINI_API_KEY
if not api_key:
    raise ValueError("🚨 CRITICAL ERROR: The API key is blank! Check your .env file.")

# 🚀 Initialize Gemini with a specific timeout to handle complex queries
llm = ChatGoogleGenerativeAI(
    model=settings.MODEL_NAME, 
    google_api_key=api_key, 
    temperature=0, 
    max_retries=0,      # 🚀 SET TO 0: Stops Langchain's massive exponential backoffs
    timeout=30          # 🚀 SET TO 30: Forces it to fail fast so our custom loop handles it
)

async def run_data_agent(user_message: str, user_id: str) -> ChatResponse:
    
    # 🚀 1. FAST GREETING BYPASS
    # Responds instantly to greetings without using API tokens or processing data
    clean_msg = user_message.lower().strip()
    greetings = ["hi", "hello", "hey", "hi there", "hello kbot", "hi kbot", "good morning", "good afternoon"]
    
    if clean_msg in greetings:
        logger.info("👋 Greeting triggered. Bypassing LLM for speed.")
        return ChatResponse(
            answer="Hello! I am KBot, your KPCL Data and Diagnostic Assistant. I can help you analyze compressor data, calculate metrics, or troubleshoot problems. What can I do for you today?",
            confidence="High",
            reasoning_path="Direct Greeting Bypass"
        )

    # 🚀 2. SEARCH-FIRST NODE (The Accuracy & Speed Engine)
    # Instead of sending 3,300 rows, we find only the 5-10 rows relevant to the user's query.
    # This handles "oil-leak", "oilleakage", and "Oil Leak" automatically via Python.
    logger.info(f"🔍 Search-First Node: Filtering data for query: {user_message}")
    search_results = find_relevant_context(user_message)

    # 🚀 3. CONTEXT INJECTION (Fixes 500 Error and Column Guesses)
    # Safely retrieving the text-based cost string and exact dataframe columns
    context_str = f"""
    EXACT COLUMNS IN WARRANTY DATABASE (Use these for your Pandas code):
    {search_results.get('df_columns', [])}

    SEARCH RESULTS (Pre-filtered from Database):
    - Relevant Diagnostic Knowledge: {search_results.get('filtered_kb', [])}
    - Recent Related Warranty Claims: {search_results.get('filtered_warranty', [])}
    
    COMPLETE SPARE PART COST LIST (Text Format):
    {search_results.get('cost_table_str', 'No cost data available.')}
    """

    # Combine the System Instructions, the Filtered Data, and the User Question
    current_prompt = f"{SYSTEM_PLANNER_PROMPT}\n\n{context_str}\n\nUser Question: {user_message}\n\nPython Code:"
    
    max_retries = 3
    last_error = ""

    # 🚀 4. AGENT EXECUTION LOOP (with Self-Correction)
    for attempt in range(max_retries):
        logger.info(f"\n" + "="*50)
        logger.info(f"🧠 Attempt {attempt + 1}: Asking Gemini to process filtered data...")
        logger.info(f"="*50 + "\n")
        
        try:
            # Generate the Python code using Gemini
            response = llm.invoke(current_prompt)
            generated_code = response.content
            
            logger.info(f"\n📜 RAW CODE FROM AI:\n{generated_code}\n")
            
            # Clean Markdown formatting (e.g., ```python ... ```)
            if "```python" in generated_code:
                generated_code = generated_code.split("```python")[1].split("```")[0].strip()
            elif "```" in generated_code:
                generated_code = generated_code.split("```")[1].split("```")[0].strip()

            logger.info("⚙️ Executing code in Python Sandbox...")

            # Run the code against the dataframes in RAM
            result = execute_agent_code(generated_code)

            # If successful, return the formatted answer!
            if not result.get("error"):
                logger.info("✅ Success!")
                return ChatResponse(
                    answer=result["answer"],
                    confidence="High" if attempt == 0 else "Medium (Self-Corrected)",
                    graph_json=result.get("graph_json"),
                    reasoning_path=f"Successful search-led execution on attempt {attempt + 1}"
                )
            
            # If code execution failed, provide the error back to Gemini to fix it
            last_error = result["error"]
            logger.warning(f"⚠️ Attempt {attempt + 1} failed: {last_error}. Retrying...")
            current_prompt += f"\n\nPrevious Code: {generated_code}\nError: {last_error}\nPlease fix the logic and try again. Python Code:"

        except Exception as e:
            logger.error(f"❌ Critical Agent Failure: {e}")
            break

    # 🚀 5. FAIL-SAFE
    logger.error("🚨 All attempts failed.")
    return ChatResponse(
        answer="I successfully identified the records but had trouble calculating the final summary. Please try rephrasing your question.",
        confidence="Low",
        reasoning_path=f"Failed after {max_retries} attempts.",
        error=last_error
    )