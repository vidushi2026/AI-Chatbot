import json
import os

def flatten_data(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    chunks = []
    
    # Process Mutual Funds
    for fund in data.get('mutual_funds', []):
        name = fund.get('name')
        url = fund.get('url')
        
        # Create individual chunks for each factual attribute to ensure precise retrieval
        attributes = [
            ("Expense Ratio", fund.get('expense_ratio')),
            ("Lock-in Period", fund.get('lock_in_period')),
            ("Minimum SIP", fund.get('min_sip')),
            ("Exit Load", fund.get('exit_load')),
            ("Riskometer", fund.get('riskometer')),
            ("Benchmark", fund.get('benchmark'))
        ]
        
        for attr_name, attr_value in attributes:
            if attr_value:
                content = f"The {attr_name} for {name} is {attr_value}."
                chunks.append({
                    "content": content,
                    "metadata": {
                        "source": url,
                        "fund_name": name,
                        "type": "fund_attribute",
                        "attribute": attr_name
                    }
                })

    # Process Guides
    for guide in data.get('guides', []):
        title = guide.get('title')
        steps = " ".join(guide.get('steps', []))
        content = f"Guide: {title}. Steps: {steps}"
        chunks.append({
            "content": content,
            "metadata": {
                "source": "https://groww.in/reports", # General guide link
                "type": "guide",
                "title": title
            }
        })
        
    return chunks

def save_chunks(chunks, output_file):
    with open(output_file, 'w') as f:
        json.dump(chunks, f, indent=4)
    print(f"Processed {len(chunks)} chunks and saved to {output_file}")

if __name__ == "__main__":
    input_path = os.path.join("..", "phase_1_ingestion", "ingested_data.json")
    output_path = "processed_chunks.json"
    
    if os.path.exists(input_path):
        processed_chunks = flatten_data(input_path)
        save_chunks(processed_chunks, output_path)
    else:
        print(f"Error: {input_path} not found.")
