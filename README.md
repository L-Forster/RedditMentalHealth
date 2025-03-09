# Reddit Mental Health Analyzer

## Overview
This application analyzes Reddit user activity to estimate the probability of various mental health conditions based on language patterns and posting behaviors. It uses machine learning models trained on data from mental health-related subreddits to identify linguistic and behavioral patterns associated with different conditions.

## Features
- Analyze any Reddit username to generate mental health probability scores
- Visual representation of results through an interactive bar chart
- Support for multiple mental health conditions including depression, anxiety, bipolar disorder, PTSD, NPD, and BPD
- Model updating capability to keep analysis current

## Project Structure
```
RedditMentalDisorders/
└── RedditEmotions/
    ├── backend/
    │   ├── scripts/
    │   │   ├── app.py                  # Flask backend
    │   │   ├── classify_facade.py      # Interface for classification
    │   │   ├── scraper_facade.py       # Interface for Reddit scraping
    │   │   ├── training_facade.py      # Interface for model training
    │   │   ├── scraper.py              # Reddit data extraction
    │   │   └── ... (other scripts)
    │   ├── models/                     # Trained ML models 
    │   ├── positive_samples/           # Training data from subreddits
    │   └── user/                       # Stored user data
    └── frontend/
        ├── public/
        ├── src/
        │   ├── App.js                  # Main React component
        │   ├── App.css                 # Styling
        │   ├── index.js                # React entry point
        │   └── ... (other React files)
        ├── package.json
        └── ...
```

## Requirements
### Backend
- Python 3.6+
- Flask
- Flask-CORS
- PRAW (Python Reddit API Wrapper)
- Scikit-learn
- Pandas
- NumPy

### Frontend
- Node.js and npm
- React
- Recharts

## Installation and Setup

### Backend
1. Navigate to the backend directory:
   ```
   cd RedditMentalDisorders/RedditEmotions/backend/scripts
   ```

2. Install required packages:
   ```
   pip install flask flask-cors praw scikit-learn pandas numpy
   ```

3. Ensure you have a Reddit API key. Create a Reddit Developer Application at https://www.reddit.com/prefs/apps and note your client ID and secret.

4. Update the `clientID` and `secretID` variables in your scraper_facade.py file with your Reddit API credentials.

5. Run the Flask server:
   ```
   python app.py
   ```

### Frontend
1. Navigate to the frontend directory:
   ```
   cd RedditMentalDisorders/RedditEmotions/frontend
   ```

2. Install dependencies:
   ```
   npm install
   npm install recharts
   ```

3. Run the development server:
   ```
   npm start
   ```

4. Access the application at http://localhost:3000

## Usage
1. Enter a Reddit username in the input field
2. Click "Analyze User"
3. The application will process the user's Reddit history through various mental health models
4. View the results in the bar chart, showing probability scores for each condition

## Notes on Ethics and Privacy
- This tool is for educational and research purposes only
- The predictions should not be considered medical diagnoses
- User data is temporarily stored for analysis but not shared
- Always respect Reddit's API terms of service
- Consider the privacy implications before analyzing usernames without consent

## Contributing
Contributions are welcome. Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.