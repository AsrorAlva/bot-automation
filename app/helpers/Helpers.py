import pandas as pd
import time
import random

def random_wait(min_seconds=1, max_seconds=5):
    """Pause execution for a random duration between min_seconds and max_seconds."""
    wait_time = random.uniform(min_seconds, max_seconds)
    time.sleep(wait_time)
    print(f"Waited for {wait_time:.2f}s antara {min_seconds}-{max_seconds} detik.")
    
def human_type(page, selector, text, min_delay=0.05, max_delay=0.2):
    """Simulate human-like typing into a web page element."""
    page.wait_for_selector(selector, timeout=5000)
    page.click(selector, force=True)
    
    try:
        page.fill(selector, '')
    except Exception as e:
        pass
    
    for ch in text:
        delay_ms = int(random.uniform(min_delay, max_delay) * 1000)
        page.keyboard.type(ch, delay=delay_ms)
        time.sleep (random.uniform(0.005, 0.02))
        
    print(f"Finished human typing into {selector}")
    
def read_excel_data(file_path, sheet_name="pengajuan"):
    """Baca data dari Excel dan kembalikan dict {selector: value}"""
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    data = dict(zip(df["selector"], df["value"]))
    return data
    
# def safe_click(page, selector, description="", timeout=5000):
#     try:
#         page.click(selector, timeout=timeout)
#         print(f"[CLICK] {description or selector}")
#         random_wait(0.5, 1.2)
#         return True
#     except Exception as e:
#         print(f"[ERROR] Gagal klik {description or selector}: {e}")
#         return False
    
# def wait_for_selector_safe(page, selector, description="", timeout=8000):
#     try:
#         page.wait_for_selector(selector, timeout=timeout)
#         print(f"[FOUND] {description or selector}")
#         return True
#     except Exception as e:
#         print(f"[TIMEOUT] {description or selector} tidak muncul: {e}")
#         return False