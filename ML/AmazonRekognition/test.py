import requests
import os
import time

# --- CONFIGURATION ---
URL = 'http://localhost:5000/predict-image'
FOLDER_PATH = 'test_set'  # Name of your folder

def run_batch_test():
    # 1. Check if the folder exists
    if not os.path.exists(FOLDER_PATH):
        print(f"Error: Folder '{FOLDER_PATH}' not found!")
        return

    # 2. Get list of all image files in the folder
    # This filters for .jpg, .jpeg, and .png files
    valid_extensions = ('.jpg', '.jpeg', '.png')
    image_files = [f for f in os.listdir(FOLDER_PATH) if f.lower().endswith(valid_extensions)]

    if not image_files:
        print(f"No images found in '{FOLDER_PATH}'.")
        return

    print(f"--- Starting Batch Test: {len(image_files)} images found ---")
    
    # Counters for the summary
    stats = {"emergency": 0, "non-emergency": 0, "errors": 0}

    # 3. Loop through each image
    for filename in image_files:
        file_path = os.path.join(FOLDER_PATH, filename)
        print(f"\nProcessing: {filename}...", end=" ", flush=True)

        try:
            with open(file_path, 'rb') as img:
                files = {'file': img}
                response = requests.post(URL, files=files)

            if response.status_code == 200:
                result = response.json()
                status = result['status']
                stats[status] += 1
                
                # Print result in a nice format
                icon = "🚨" if status == "emergency" else "✅"
                print(f"{icon} [{status.upper()}]")
                
                # Optional: Show what labels were detected
                # print(f"   Labels: {', '.join(result['detected_labels'][:3])}...") 

            else:
                print(f"❌ Error (Code {response.status_code})")
                stats["errors"] += 1

        except Exception as e:
            print(f"❌ Connection Failed: {e}")
            stats["errors"] += 1
        
        # Small pause to avoid hitting AWS rate limits too fast
        time.sleep(0.2)

    # 4. Final Summary Report
    print("\n" + "="*30)
    print("      FINAL SUMMARY")
    print("="*30)
    print(f"Total Images processed: {len(image_files)}")
    print(f"🚨 Emergencies Found : {stats['emergency']}")
    print(f"✅ Safe / Normal     : {stats['non-emergency']}")
    print(f"❌ Failed Requests   : {stats['errors']}")
    print("="*30)

if __name__ == "__main__":
    run_batch_test()