# Testing Documentation

## Testing Strategy
This project was tested using manual, functional, and integration-style testing
to ensure that all major workflows operate correctly from user input to final output.

Testing focused on correctness, error handling, data persistence, and usability.
Due to the GUI-based nature of the application, testing emphasized end-to-end
system behavior rather than isolated automated unit tests.

---

## Scope of Testing

### Stock Analysis (Option 1)
- Valid ticker symbols
- Invalid ticker handling
- Date format validation
- Minimum date range enforcement (1 month)
- Handling of weekends and future dates
- Indicator calculation accuracy (SMA, RSI)
- Integration between StockDataManager, StockAnalyzer, and SystemController

---

### News Sentiment Analysis (Option 2)
- RSS feed retrieval
- Sentiment classification
- Keyword extraction
- Handling of empty or limited news results
- Display of article metadata
- Integration between NewsAnalyzer and GUI display components

---

### Portfolio Dashboard (Option 3)
- Loading default portfolio CSV
- Updating portfolio after importing new CSV
- Portfolio value calculations
- Error handling for missing or invalid files
- Integration between CSV import, PortfolioManager, and dashboard display

---

### Stock Chart Visualization (Option 4)
- Rendering charts after analysis
- Tooltip behavior on hover
- Zoom and pan functionality
- X-axis formatting for different date ranges
- Anomaly marker display
- Integration between analysis output and visualization layer

---

### CSV Import (Option 5)
- Importing valid CSV files
- Handling invalid or unreadable CSV files
- Previewing imported data
- Updating active portfolio file for use in the dashboard

---

### Export Functionality (Option 6)
- Exporting analysis to JSON
- Handling export cancellation
- Verifying saved file contents
- Automatically opening exported files

---

### Persistence Testing
- Saving application state on exit
- Reloading previous state on restart
- Handling missing or corrupted state files

---

## How to Run Tests
1. Run the application using `python api/app.py`
2. Navigate through each option in the main menu
3. Provide both valid and invalid inputs
4. Verify outputs, error messages, and saved files
5. Restart the application to confirm persistence behavior

---

## Test Results Summary
All core workflows executed successfully during testing.
Errors were handled gracefully with informative user messages.
The application remained stable across repeated runs, file imports,
and data changes.

