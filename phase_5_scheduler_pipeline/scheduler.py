import time
import os
import sys
import hashlib
import shutil
import json
import logging

# Add project root to path
ROOT_DIR = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(ROOT_DIR)

# Paths
PHASE_1_DIR = os.path.join(ROOT_DIR, 'phase_1_ingestion')
PHASE_2_DIR = os.path.join(ROOT_DIR, 'phase_2_processing_indexing')
PHASE_3_DIR = os.path.join(ROOT_DIR, 'phase_3_retrieval_generation')
PHASE_4_DIR = os.path.join(ROOT_DIR, 'phase_4_frontend_backend')
PHASE_5_DIR = os.path.join(ROOT_DIR, 'phase_5_scheduler_pipeline')

INGESTED_DATA = os.path.join(PHASE_1_DIR, 'ingested_data.json')
DATA_HASH_FILE = os.path.join(PHASE_5_DIR, 'data_hash.txt')
SCHEDULER_LOG = os.path.join(PHASE_5_DIR, 'scheduler.log')
LAST_UPDATED_FILE = os.path.join(PHASE_4_DIR, 'static', 'last_updated.txt')
PROCESSED_DATA_FILE = os.path.join(PHASE_2_DIR, 'processed_data.json')
VECTOR_INDEX_FILE = os.path.join(PHASE_2_DIR, 'vector_index.json')

# Configure Logging
logging.basicConfig(
    filename=SCHEDULER_LOG,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_file_hash(path):
    if not os.path.exists(path): return None
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def update_metadata():
    """Update the frontend last_updated timestamp."""
    with open(LAST_UPDATED_FILE, 'w') as f:
        f.write(time.strftime('%Y-%m-%d %H:%M:%S'))
    logging.info("Frontend metadata updated (last_updated.txt).")

def run_pipeline(simulate=False):
    logging.info("--- Starting Scheduler Pipeline Run ---")
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting Pipeline Run...")
    
    try:
        # 1. Data Ingestion
        logging.info("STEP 1: Running Scraper...")
        from phase_1_ingestion.scraper import run_scraper
        run_scraper(simulate_change=simulate)
        
        if not os.path.exists(INGESTED_DATA):
            logging.error("Ingested data file missing. Skipping run.")
            return

        # 2. Change Detection
        current_hash = get_file_hash(INGESTED_DATA)
        previous_hash = None
        if os.path.exists(DATA_HASH_FILE):
            with open(DATA_HASH_FILE, 'r') as f:
                previous_hash = f.read().strip()
        
        if current_hash == previous_hash:
            logging.info("STEP 2: No changes detected (hash matched). Finishing run.")
            print("No changes detected. Knowledge base is already up to date.")
        else:
            logging.info(f"STEP 2: CHANGES DETECTED. Re-processing knowledge base...")
            print("Changes detected. Refreshing system...")

            # 3. Processing
            from phase_2_processing_indexing.processor import flatten_data, save_chunks
            processed_chunks = flatten_data(INGESTED_DATA)
            save_chunks(processed_chunks, PROCESSED_DATA_FILE)
            logging.info(f"STEP 3: Data processed and saved to {PROCESSED_DATA_FILE}.")
            
            # 4. Embedding Update & Index Refresh
            # In our zero-dependency RAG, the "vector index" is the processed JSON file
            shutil.copy2(PROCESSED_DATA_FILE, VECTOR_INDEX_FILE)
            logging.info(f"STEP 4: Search index (vector_index.json) updated.")

            # Update Metadata for Frontend
            update_metadata()

            # Store new hash
            with open(DATA_HASH_FILE, 'w') as f:
                f.write(current_hash)

            # 5. Validation (Health Check)
            from phase_5_scheduler_pipeline.health_check import run_health_check
            if run_health_check():
                logging.info("STEP 5: Post-update health check PASSED.")
                print("Pipeline run successful! Health Check PASSED.")
            else:
                logging.warning("STEP 5: Post-update health check FAILED.")
                print("Pipeline run failed health check. Inspect health_check.py output.")

    except Exception as e:
        logging.error(f"Pipeline crashed: {str(e)}")
        print(f"Pipeline Error: {str(e)}")

def start_scheduler(interval_hours=24, simulate_test=False):
    """Starts the scheduler at a configurable interval."""
    interval_seconds = interval_hours * 3600
    logging.info(f"Scheduler started. Interval: {interval_hours} hours.")
    print(f"Scheduler running every {interval_hours}h...")
    while True:
        run_pipeline(simulate=simulate_test)
        time.sleep(interval_seconds)

if __name__ == "__main__":
    # For verification, run one simulation cycle if --test is passed
    import sys
    if "--test" in sys.argv:
        run_pipeline(simulate=True)
    elif "--run" in sys.argv:
        run_pipeline(simulate=False)
    else:
        print("Usage: python3 scheduler.py [--test | --run | --start-24h]")
        if "--start-24h" in sys.argv:
            start_scheduler(interval_hours=24)
