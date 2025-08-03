# 🐒 Expense Monkey

An AI-powered expense categorization tool that automatically categorizes credit card transactions using Google's Gemini AI.

## 🎯 Purpose

Expense Monkey helps you automatically categorize your credit card expenses by analyzing transaction data (date, description, amount) and assigning them to predefined categories. This saves time on manual expense tracking and provides consistent categorization for financial analysis.

## 🚀 Features

- **AI-Powered Categorization**: Uses Google's Gemini 2.5 Flash model for intelligent expense categorization
- **Comprehensive Categories**: Supports 11 different expense categories with clear definitions
- **Batch Processing**: Process multiple transactions from CSV files
- **Accuracy Evaluation**: Compare AI predictions with ground truth data to measure performance
- **Flexible Configuration**: Environment-based settings with validation

## 📁 Categories

The system categorizes expenses into the following categories:

- **Auto & Transport**: Fuel, ridesharing, vehicle maintenance, public transportation
- **Bills & Utilities**: Subscriptions, phone, internet, utility payments
- **Education**: Tuition, school supplies, books, training programs
- **Entertainment**: Movies, music, recreational activities, concerts
- **Food & Dining**: Groceries, restaurants, bars, cafes, food delivery
- **Gifts & Donations**: Charitable contributions, gifts, Patreon subscriptions
- **Health & Wellness**: Medical, dental, fitness, personal training
- **Misc**: Venmo transactions and small expenses that don't fit other categories
- **Rent**: Rent or mortgage payments
- **Shopping**: Clothing, electronics, household items
- **Travel**: Hotels, airfare, car rentals, international expenses
- **Uncategorized**: Unclear or unmatched expenses

## 🛠️ Setup

### Prerequisites

- Python 3.9+
- Google API key for Gemini AI

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd expense-monkey
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create environment configuration**
   
   Create a `.env` file in the project root:
   ```env
   # Google API Configuration
   GOOGLE_API_KEY=your_actual_api_key_here
   
   # Application Settings (optional)
   ENVIRONMENT=development
   DEBUG=true
   ```

4. **Get Google API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

## 📊 Usage

### Basic Usage

The main script processes a CSV file containing expense data and evaluates categorization accuracy:

```bash
python monkey.py
```

### Input Data Format

Your CSV file should contain expense data in the following format:
```
Date: MM/DD/YYYY; Amount: -XX.XX; Description: VENDOR NAME LOCATION
```

Example:
```
Date: 10/22/2019; Amount: -1.25; Description: Ext Credit Card Debit AMAZON GO AMZN.COM/BILLWA
```

### Output

The system will categorize each expense

## 🔧 Configuration

### Settings Structure

The project uses a layered settings approach:

- **AppSettings**: Main application configuration
- **GoogleSettings**: Google API specific settings

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | Required |
| `ENVIRONMENT` | Application environment | `development` |
| `DEBUG` | Enable debug mode | `false` |

## 📝 Files Structure

```
expense-monkey/
├── monkey.py              # Main application script
├── settings.py            # Configuration management
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── .gitignore            # Git ignore patterns
└── README.md             # This file
```

## 🔍 Example Categorizations

Here are some example categorizations the AI model makes:

- `STARBUCKS` → **Food & Dining**
- `UBER TRIP` → **Auto & Transport**
- `SPOTIFY USA` → **Bills & Utilities**
- `AMAZON.COM` → **Shopping**
- `NETFLIX` → **Entertainment**

## ⚙️ Technical Details

- **AI Model**: Google Gemini 2.5 Flash
- **Configuration**: Pydantic-based settings with validation
- **Data Processing**: CSV file handling with random sampling
- **Evaluation**: Accuracy measurement against ground truth data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT license

## 🐛 Troubleshooting

### Common Issues

1. **Import Error for google.generativeai**
   - Ensure you've installed all requirements: `pip install -r requirements.txt`

2. **API Key Not Found Error**
   - Verify your `.env` file exists and contains `GOOGLE_API_KEY`
   - Check that your API key is valid

3. **CSV File Not Found**
   - Ensure your CSV file is in the correct location
   - Update the filename in `monkey.py` if needed
