import re
import csv
from datetime import datetime

# Filepath of the markdown file
input_file = r"c:\Users\DELL-7373\Desktop\internship\AI_engineer_intern_tasks\task1\scraper\ipl2024-stats\page.md"
output_file = "ipl_matches.csv"

# Dictionary to map full team names to their short forms
team_short_names = {
    "Royal Challengers Bengaluru": "RCB",
    "Chennai Super Kings": "CSK",
    "Mumbai Indians": "MI",
    "Kolkata Knight Riders": "KKR",
    "Sunrisers Hyderabad": "SRH",
    "Rajasthan Royals": "RR",
    "Punjab Kings": "PBKS",
    "Delhi Capitals": "DC",
    "Lucknow Super Giants": "LSG",
    "Gujarat Titans": "GT"
}

# Open the markdown file and read its content
with open(input_file, "r", encoding="utf-8") as file:
    content = file.read()

# Regex pattern to extract match details
pattern = r"(?P<date>\w{3} \d{1,2}, \w{3})\n\[(?P<teams>.+?)\]\(.*?\)\n(?P<venue>.+?)\n"

# Find all matches
matches = re.finditer(pattern, content)

# Open a CSV file to save the data
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header row
    csvwriter.writerow(["match", "date", "team1", "team2", "venue"])

    for match in matches:
        try:
            # Extract match details
            date_text = match.group("date")
            teams_text = match.group("teams")
            venue = match.group("venue").strip()

            # Parse date and set the correct year
            parsed_date = datetime.strptime(date_text, "%b %d, %a")
            match_date = parsed_date.replace(year=2025).strftime("%d-%m-%Y")

            # Extract teams and match number
            teams_match = re.match(r"(.+?) vs (.+?), (\d+)(?:th|st|nd|rd) Match", teams_text)
            if teams_match:
                team1 = teams_match.group(1).strip()
                team2 = teams_match.group(2).strip()
                match_number = teams_match.group(3).strip()

                # Convert team names to short forms
                team1 = team_short_names.get(team1, team1)
                team2 = team_short_names.get(team2, team2)
            else:
                team1, team2, match_number = "N/A", "N/A", "N/A"

            # Write the data to the CSV file
            csvwriter.writerow([match_number, match_date, team1, team2, venue])

        except Exception as e:
            print(f"Error processing match: {e}")

print(f"Data saved to {output_file}")