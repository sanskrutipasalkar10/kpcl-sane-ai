import pandas as pd
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

# 🚀 GLOBAL CACHE: Load the dataset once into RAM so we don't read the hard drive every time
global_df = None

def get_dataframe():
    global global_df
    if global_df is None:
        logger.info(f"📂 Loading Excel data into memory cache for the first time...")
        df = pd.read_excel(settings.ACTIVE_DATA_PATH)
        
        # 🛡️ THE BULLETPROOF SHIELD: Force these columns to be numeric.
        # errors='coerce' turns any text into safe NaN values that Pandas will ignore during math.
        numeric_cols = ['RunHrs.', 'RPM', 'Period DD to DC in months', 'FSR No']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                
        global_df = df
    return global_df

def execute_agent_code(python_code: str) -> dict:
    try:
        # ⚡ Instant load from RAM instead of reading the .xlsx file again
        df = get_dataframe() 
    except Exception as e:
        return {"error": f"Failed to load Excel: {str(e)}"}

    local_env = {
        "df": df, 
        "pd": pd,
        "final_answer": "No answer generated.",
        "graph_json": None 
    }
    
    # Auto-import Plotly
    if "px" in python_code or "plotly" in python_code:
        import plotly.express as px
        local_env["px"] = px

    # Execute the code
    try:
        exec(python_code, {}, local_env)
    except Exception as e:
        return {"error": str(e), "failed_code": python_code}

    # Extract results
    ans = str(local_env.get("final_answer"))
    g_json = local_env.get("graph_json")

    # 🛡️ THE SAFETY NET: If the AI accidentally puts the JSON into the text answer, fix it automatically!
    if ans.startswith('{"data":') or ans.startswith('{"layout":'):
        g_json = ans
        ans = "Here is the requested graph."
        logger.info("🛡️ Intercepted raw JSON in final_answer and rerouted it to Plotly.")

    return {
        "answer": ans,
        "graph_json": g_json,
        "error": None
    }