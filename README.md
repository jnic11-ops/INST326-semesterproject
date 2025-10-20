INST326 Semester Project 

Project 01: Function Library

Dedicated access Alpha Vantage API Key: DY8T5FSL5F1QV5N7





# Stock Market Data \& News Analysis System

#### **Project Description**

Our project will be an information retrieval and analysis tool focused on collecting current stock information, such as prices and trends, as well as current news regarding those stocks. This project is a comprehensive stock market information platform that integrates financial APIs (Alpha Vantage, IEX Cloud) and news APIs (NewsAPI, Bing News, RSS feeds) to collect, process, analyze, and visualize stock data and related news sentiment. 



The system provides:

* Real-time \& historical stock market data
* Financial news sentiment and topic analysis
* Portfolio tracking with user-uploaded data 
* Trend detection \& anomaly analysis
* Interactive dashboards for stock/news insights
* Exportable reports (PDF, CSV, JSON)



#### **Team Members \& Roles**

* Matthew Daniel -- Data Base Researcher/Graphical Output Designer 
* Jacob Nicholson -- Project Coordinator
* Ray Dickscheid -- Documentation Manager
* Dorian Mkam -- User Interface Designer





#### **Domain Focus \& Problem Statement**

**Domain**: Information Retrieval and Analysis Tool



**Problem**: Many new investors who lack experience or financial literacy struggle with decision-making due to information overload from fragmented data sources(news sites, market analysis, social media, financial statements). This information is scattered, overwhelming, and often unclear. We aim to develop a system that centralizes financial data, news sentiment, and trend detection into a single program, providing beginner investors with relevant knowledge to make efficient and informed data-driven investment choices and prevent losses due to uninformed or hasty decisions.  


####**Installation & Setup** 

1. Clone the repository: https://github.com/jnic11-ops/INST326-semesterproject
2. Create a virtual environment (Visual Studio Code)
3. Install dependencies
4. Run example scripts to test functionality



#### **Usage Examples For Key Functions**

###### **validate\_ticker(ticker: str)**

from src.utils.validate\_ticker import validate\_ticker

print(validate\_ticker("AAPL"))  # True

print(validate\_ticker("goog"))  # False





###### **clean\_text(text: str)**

from src.utils.clean\_text import clean\_text

print(clean\_text("<p>The market is rising!</p>"))

\# Output: "market rising"



###### **format\_currency(value: float)**

from src.utils.format\_currency import format\_currency

print(format\_currency(1234.56))  # $1,234.56







###### **parse\_portfolio\_csv(file\_path: str)**

from src.data\_collection.parse\_portfolio\_csv import parse\_portfolio\_csv

portfolio = parse\_portfolio\_csv("portfolio.csv")

print(portfolio)





#### **Function Library Overview**

###### **utils**

* \_\_init\_\_
* validate\_ticker()
* normalize\_date()
* clean\_text()
* format\_currency()
* log\_metadata()



###### **data collection**

* \_\_init\_\_
* fetch\_stock\_data()
* fetch\_news()
* parse\_portfolio()



###### **analysis**

* \_\_init\_\_
* sentiment\_analysis()
* topic\_modeling()
* detect\_price\_anomalies()
* calculate\_technical\_indicators()
* generate\_wordcloud\_data



###### **reporting**

* \_\_init\_\_
* export\_report



###### **interface**

* \_\_init\_\_





#### **Contribution Guidelines for Team Members** 



1. **Branching Strategy:** 

* Always work on a separate branch, never directly on main. 

* Creating different branches for each project feature based on the level of complexity of each function. For example, Matthew worked on creating the simple utility functions of our program, so we would create a separate branch for the utility functions if any updates were going to be made.
* Branch naming convention, such as feature/ utils and feature/data collection



**2. Commit Guidelines:**

* Commit frequently with clear, descriptive messages.
* Example:

&nbsp;  git commit -m "Add clean\_text utility function"



**3. Code Style:**

* Follow PEP8 Python standards.
* Include docstrings for all functions (parameters, return values, description).
* Keep functions modular and reusable.



**4. Pull Requests (PRs):**

* Open a PR when your feature or bugfix is ready.
* Include a description of changes, relevant issues, and example usage if applicable.
* Assign at least one team member to review your PR.
* After approval, merge into main using GitHub’s merge tool or git merge.



**5. Testing:**

* Always test new functions locally before pushing.
* Include example scripts in the examples/ folder.
* For data processing or analysis functions, provide sample input/output.



**6. Documentation:**

* Update the function\_reference.md when you add or modify functions.
* Update usage\_examples.md with sample scripts demonstrating function usage.
* Ensure README reflects any new features or dependencies.



**7. Issues \& Bug Tracking:**

* Use GitHub Issues to track bugs, tasks, or enhancements.
* Reference issues in commits and PRs using #issue-number.



**8. Communication:** 

* Discuss major design decisions before implementation.
* Notify the team of changes affecting folder structure, APIs, or data schema.









