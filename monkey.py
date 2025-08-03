from settings import get_settings
from pydantic import ValidationError
import google.generativeai as genai
import csv
import random

def main():
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

    input_filename = "categorized_expenses_ground_truth_v4.csv"

    data_list = []

    with open(input_filename, 'r') as file:
        reader = csv.reader(file)
        next(reader) # skip header
        for row in reader:
            input_value = row[0]
            output_value = row[1]
            data_list.append((input_value,output_value))

    data_list_sample = random.sample(data_list,5)
    print(data_list_sample)

    processed_data_list = []
    for index, (input_value, output_value) in enumerate(data_list_sample):
        model_label = model.generate_content(input_value).text
        agreement = output_value.strip() == model_label.strip()
        processed_data_list.append((input_value, output_value, model_label, agreement))

    disagreement_count = 0
    for input_value, output_value, model_label, agreement in processed_data_list:
        if agreement == False:
            disagreement_count += 1
            print(f"Input: '{input_value}'; \n My output: '{output_value}'; \n Model label: '{model_label}'\n")

    print(f"Disagreements: '{disagreement_count}'; Disagreement rate: {disagreement_count/len(processed_data_list)}")

if __name__ == "__main__":
    main()