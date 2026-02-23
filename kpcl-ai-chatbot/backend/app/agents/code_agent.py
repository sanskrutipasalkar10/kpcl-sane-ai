import logging
import langchain
from app.core.config import settings
from app.agents.prompts import SYSTEM_PLANNER_PROMPT
from app.services.data_parser import execute_agent_code
from app.models.response import ChatResponse
from langchain_community.llms import Ollama

# 🔦 Turn on LangChain's internal "glass-box" logging
langchain.debug = True

logger = logging.getLogger(__name__)
llm = Ollama(model=settings.MODEL_NAME, base_url=settings.OLLAMA_BASE_URL)

async def run_data_agent(user_message: str, user_id: str) -> ChatResponse:
    
    # 🚀 FAST GREETING BYPASS
    # If the user just says a basic greeting, answer instantly without writing Python code.
    clean_msg = user_message.lower().strip()
    greetings = ["hi", "hello", "hey", "hi there", "hello kbot", "hi kbot", "good morning", "good afternoon"]
    
    if clean_msg in greetings:
        logger.info("👋 Instant Greeting triggered. Bypassing LLM.")
        return ChatResponse(
            answer="Hello! I am KBot, your KPCL Data Assistant. I can help you analyze compressor data, calculate metrics, or plot graphs. What would you like to know?",
            confidence="High",
            reasoning_path="Direct Greeting Bypass"
        )

    # ... Normal LLM Data Agent Execution ...
    current_prompt = f"{SYSTEM_PLANNER_PROMPT}\n\nUser Question: {user_message}\n\nPython Code:"
    max_retries = 3
    last_error = ""

    for attempt in range(max_retries):
        logger.info(f"\n" + "="*50)
        logger.info(f"🧠 Attempt {attempt + 1}: Asking Qwen to generate code...")
        logger.info(f"="*50 + "\n")
        
        try:
            # This will trigger the [llm/start] and [llm/end] logs
            generated_code = llm.invoke(current_prompt)
            
            logger.info(f"\n📜 RAW CODE FROM AI:\n{generated_code}\n")
            
            # Clean Markdown formatting out of the LLM's response
            if "```python" in generated_code:
                generated_code = generated_code.split("```python")[1].split("```")[0].strip()
            elif "```" in generated_code:
                generated_code = generated_code.split("```")[1].split("```")[0].strip()

            logger.info("⚙️ Sending cleaned code to execution sandbox...")

            # Execute code in our secure sandbox
            result = execute_agent_code(generated_code)

            # If it succeeded, return the answer to the user!
            if not result.get("error"):
                logger.info("✅ Code executed successfully!")
                return ChatResponse(
                    answer=result["answer"],
                    confidence="High" if attempt == 0 else "Medium (Self-Corrected)",
                    graph_json=result.get("graph_json"), # <-- CHANGED FROM BASE64 TO JSON
                    reasoning_path=f"Successful on attempt {attempt + 1}"
                )
            
            # If it failed, update the prompt with the error for the next loop
            last_error = result["error"]
            logger.warning(f"⚠️ Attempt {attempt + 1} failed: {last_error}. Retrying...")
            current_prompt += f"\n\nPrevious Code: {generated_code}\nError: {last_error}\nPlease correct the code and try again. Python Code:"

        except Exception as e:
            logger.error(f"❌ Critical Agent Failure: {e}")
            break

    # If it failed all 3 attempts, tell the user gracefully
    logger.error("🚨 All attempts failed. Returning error to user.")
    return ChatResponse(
        answer="I tried several times but encountered a persistent error with the data logic.",
        confidence="Low",
        reasoning_path=f"Failed after {max_retries} attempts.",
        error=last_error
    )