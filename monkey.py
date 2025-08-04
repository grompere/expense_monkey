from settings import get_settings
from pydantic import ValidationError
import google.generativeai as genai
import csv
import random
import argparse
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)

def main(input_filename, output_filename="processed_results.csv", sample_size=None):
    try:
        # Load application settings
        settings = get_settings()
        
        if settings.debug:
            print(f"🔧 Running in {settings.environment} environment")
        
        genai.configure(api_key=settings.google.api_key)
        
    except ValidationError as e:
        print(f"❌ Configuration error: {e}")
        print("Please check your .env file and ensure all required settings are configured.")
        return

    generation_config = {
    "temperature": 0,
    "top_p": 0.5,
    "top_k": 1,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        generation_config=generation_config,
        system_instruction="""
        Your job is to categorize credit card charges from my statement. For each
        charge, I will give you the following information: date, description, amount.\n
        You will then need respond with the name of the category you think the expense
        matches best. Use all three fields, your knowledge about vendors, and typical
        price ranges to infer the category. \n

        Here is the list of categories you can choose from, with a brief description:
        - Auto & Transport: Includes fuel, ridesharing services, vehicle maintenance, and public transportation.
        - Bills & Utilities: Includes recurring service bills such as subscriptions, phone, internet, and utility payments.
        - Education: Includes tuition, school supplies, books, and training programs.
        - Entertainment: Includes spending on movies, music, recreational activities, and concerts.
        - Food & Dining: Includes groceries, restaurants, bars, cafes, and food delivery services.
        - Gifts & Donations: Includes charitable contributions and gifts to others, and Patreon subscriptions.
        - Health & Wellness: Includes spending on medical, dental, fitness, personal training, and personal wellness.
        - Misc: Use for Venmo transactions and other very small expenses that don't fit these categories.
        - Rent: Includes rent or mortgage payments.
        - Shopping: Includes purchases of goods such as clothing, electronics, and household items.
        - Travel: Includes hotels, airfare, car rentals, expenses incurred abroad, and other travel-related expenses.
        - Uncategorized: If it's unclear or doesn't fit any of these categories.

        Respond only with the category name and nothing else.

        Here are a few examples:
        1. Input: '10/22/2019; Amount: -1.25; Description: Ext Credit Card Debit AMAZON GO
                    AMZN.COM/BILLWA' -> Output: 'Food & Dining'\n
        2. Input: '12/7/2021; Amount: -68.99; Description: Ext Credit Card Debit QUINN'S PUB
                    SEATTLE      WA' -> Output: 'Food & Dining'\n
        3. Input: '12/29/2020; Amount: -236.62; Description: Ext Credit Card Debit EVO -
                    SEATTLE            SEATTLE      WA' -> Output: Shopping\n
        4. Input: '6/23/2022; Amount: -16.98; Description: Ext Credit Card Debit UBER
                    TRIP' -> Output: 'Auto & Transport'\n
        5. Input: 'Date: 5/18/2021; Amount: -163.24; Description: Ext Credit Card
                    Debit DOWNTOWN SPIRITS         SEATTLE      WA' -> Output: 'Food & Dining'\n
    """
    )

    # Implement exponential backoff & retry for the Gemini API call
    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def generation_with_backoff(*args, **kwargs):
        return model.generate_content(*args, **kwargs)

    data_list = []

    with open(input_filename, 'r') as file:
        reader = csv.reader(file)
        next(reader) # skip header
        for row in reader:
            input_value = row[0]
            output_value = row[1]
            data_list.append((input_value,output_value))
    
    # Sample data if sample_size is specified
    total_records = len(data_list)
    if sample_size and sample_size < total_records:
        data_to_process = random.sample(data_list, sample_size)
        print(f"🎲 Randomly selected {sample_size} records out of {total_records} total records")
    else:
        data_to_process = data_list
        if sample_size and sample_size >= total_records:
            print(f"📋 Processing all {total_records} records (requested {sample_size}, but file only has {total_records})")
        else:
            print(f"📋 Processing all {total_records} records")
    
    processed_data_list = []
    for index, (input_value, output_value) in enumerate(data_to_process):
        model_label = generation_with_backoff(input_value).text
        agreement = output_value.strip() == model_label.strip()
        processed_data_list.append((input_value, output_value, model_label, agreement))
    
    # Output processed data to CSV file
    print(f"📁 Processing input file: {input_filename}")
    with open(output_filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['Input', 'Expected_Output', 'Model_Label', 'Agreement'])
        # Write data
        writer.writerows(processed_data_list)
    
    print(f"✅ Processed data saved to {output_filename}")
    print(f"📊 Records processed: {len(processed_data_list)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process expense categorization data using Gemini API")
    parser.add_argument("input_filename", help="Path to the input CSV file to process")
    parser.add_argument("-o", "--output", default="processed_results.csv", 
                       help="Output CSV filename (default: processed_results.csv)")
    parser.add_argument("-s", "--sample", type=int, default=None,
                       help="Number of random records to process (default: process all records)")
    
    args = parser.parse_args()
    
    # Check if input file exists
    import os
    if not os.path.exists(args.input_filename):
        print(f"❌ Error: Input file '{args.input_filename}' not found.")
        exit(1)
    
    main(args.input_filename, args.output, args.sample)