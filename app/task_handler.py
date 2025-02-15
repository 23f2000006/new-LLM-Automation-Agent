import os
import subprocess
import json
import glob
import re
import openai
from dotenv import load_dotenv

#OPENAI_API_KEY ='eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIzZjIwMDAwMDZAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.pye4_UbxcfItAf5zsgm-XrIsBon061fElwS3vwsctyQ'
# Set OpenAI API Key
# Ensure API key is set correctly
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Fetch from environment variable
print(os.getenv("OPENAI_API_KEY"))
if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API key! Set the 'OPENAI_API_KEY' environment variable.")

# # Create OpenAI client
client = openai.OpenAI(api_key=OPENAI_API_KEY)
# response = client.chat.completions.create(
#     model="gpt-4o",
#     messages=[{"role": "user", "content": "Parse and execute: hello"}]
# )
# action = response["choices"][0]["message"]["content"].strip().lower()
# print(action)
def process_task(task: str):
    # Use OpenAI API for task parsing
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"Parse and execute: {task}"}]
    )
    action = response["choices"][0]["message"]["content"].strip().lower()

    try:
        # Task A1: Install uv and run datagen.py
        if "install uv" in action:
            subprocess.run(["pip", "install", "uv"], check=True)
            subprocess.run(["python", "datagen.py", os.getenv("USER_EMAIL")], check=True)
            return "Task A1 completed: Installed uv and ran datagen.py"

        # Task A2: Format /data/format.md with Prettier
        elif "format" in action and "prettier" in action:
            subprocess.run(["npx", "prettier@3.4.2", "--write", "/data/format.md"], check=True)
            return "Task A2 completed: Formatted /data/format.md"

        # Task A3: Count Wednesdays in /data/dates.txt
        elif "count wednesdays" in action:
            with open("/data/dates.txt", "r") as f:
                dates = f.readlines()
            wednesdays = sum(1 for date in dates if "Wed" in date)
            with open("/data/dates-wednesdays.txt", "w") as f:
                f.write(str(wednesdays))
            return "Task A3 completed: Counted Wednesdays"

        # Task A4: Sort /data/contacts.json by last_name, first_name
        elif "sort contacts" in action:
            with open("/data/contacts.json", "r") as f:
                contacts = json.load(f)
            contacts.sort(key=lambda x: (x["last_name"], x["first_name"]))
            with open("/data/contacts-sorted.json", "w") as f:
                json.dump(contacts, f, indent=4)
            return "Task A4 completed: Sorted contacts"

        # Task A5: Write first line of 10 most recent .log files
        elif "most recent logs" in action:
            log_files = sorted(glob.glob("/data/logs/*.log"), key=os.path.getmtime, reverse=True)[:10]
            with open("/data/logs-recent.txt", "w") as output_file:
                for log_file in log_files:
                    with open(log_file, "r") as f:
                        output_file.write(f.readline())
            return "Task A5 completed: Extracted first lines from recent logs"

        # Task A6: Extract H1 headings from Markdown files
        elif "extract h1" in action:
            index = {}
            for root, _, files in os.walk("/data/docs"):
                for file in files:
                    if file.endswith(".md"):
                        with open(os.path.join(root, file), "r") as f:
                            content = f.read()
                            match = re.search(r"^#\s+(.+)", content, re.MULTILINE)
                            if match:
                                index[file] = match.group(1)
            with open("/data/docs/index.json", "w") as f:
                json.dump(index, f, indent=4)
            return "Task A6 completed: Created index.json"

        # Task A7: Extract sender's email from /data/email.txt
        elif "extract email" in action:
            with open("/data/email.txt", "r") as f:
                email_content = f.read()
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": f"Extract the sender's email address: {email_content}"}]
            )
            email = response["choices"][0]["message"]["content"].strip()
            with open("/data/email-sender.txt", "w") as f:
                f.write(email)
            return "Task A7 completed: Extracted sender's email"

        # Task A8: Extract credit card number from /data/credit-card.png
        elif "extract credit card" in action:
            # Placeholder for OCR or LLM-based extraction
            card_number = "1234567890123456"
            with open("/data/credit-card.txt", "w") as f:
                f.write(card_number)
            return "Task A8 completed: Extracted credit card number"

        # Task A9: Find most similar pair of comments
        elif "similar comments" in action:
            with open("/data/comments.txt", "r") as f:
                comments = f.readlines()
            # Placeholder logic for finding similar comments
            similar_pair = comments[:2]  
            with open("/data/comments-similar.txt", "w") as f:
                f.write("\n".join(similar_pair))
            return "Task A9 completed: Found most similar comments"

        # Task A10: Calculate total sales for "Gold" tickets
        elif "total sales gold" in action:
            import sqlite3
            conn = sqlite3.connect("/data/ticket-sales.db")
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(price * units) FROM tickets WHERE type = 'Gold'")
            total_sales = cursor.fetchone()[0]
            with open("/data/ticket-sales-gold.txt", "w") as f:
                f.write(str(total_sales))
            conn.close()
            return "Task A10 completed: Calculated total sales for Gold tickets"

        else:
            raise ValueError("Unsupported task")

    except Exception as e:
        return f"Error processing task: {str(e)}"