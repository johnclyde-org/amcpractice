import base64
import json
import os
import re
import subprocess
import time


def grep_png_files_from_last_10_days():
    """
    Use grep through subprocess to find files containing 'png' modified in the last 10 days.
    """
    days_ago = time.time() - (10 * 24 * 60 * 60)  # 10 days ago in seconds
    # Format for find command: %Y gives modification time in Unix time
    find_command = f"find . -maxdepth 1 -type f -mtime -10 -exec grep -l 'png' {{}} +"
    try:
        # Execute the find command followed by grep to filter files containing 'png'
        result = subprocess.run(
            find_command, shell=True, check=True, stdout=subprocess.PIPE, text=True
        )
        files = result.stdout.strip().split("\n")
        return files
    except subprocess.CalledProcessError as e:
        print(f"Error during grep operation: {e}")
        return []


# Get the list of matching files and print them
matching_files = grep_png_files_from_last_10_days()
for i, file in enumerate(matching_files, start=1):
    print(f"[{i}] {file}")

# Ask which file to parse (placeholder for user input)
choice = int(input("Which file would you like to parse? "))
filename = matching_files[choice - 1]

print(f"Parsing {filename} ...")
with open(filename, "r") as file:
    data = file.read()

# Find all PNG image URLs using regular expression
png_urls = re.findall(r'https?://[^\s<>"]+\.png', data)

print(f"Parsed {len(png_urls)} PNG URLs.")

test_type_input = (
    input("Are we building practice problem set for (A)MC, (M)ATHCOUNTS, or A(R)ML? ")
    .strip()
    .lower()
)
test_type = {"a": "AMC", "m": "Mathcounts", "r": "ARML"}.get(test_type_input, "Unknown")

year = input("Please label the problem set with a year [2024]: ").strip()

year = int(input("Please label the problem set with a year [2024]: ").strip())

labels = ["-"]
if test_type == "Mathcounts":
    level = (
        input("Is it for (N)ationals, (S)tate, (C)hapter, or sc(H)ool: ")
        .strip()
        .lower()
    )
    round_type = (
        input("Is it for (S)print, (T)arget, t(E)am, or (C)ountdown? ").strip().lower()
    )
    full_level = {"n": "National", "s": "State", "c": "Chapter", "h": "School"}.get(
        level, "???"
    )
    full_round = {"s": "Sprint", "t": "Target", "e": "Team", "c": "Countdown"}.get(
        round_type, "Unknown"
    )
    test_name = f"{year} {full_level} {full_round} Round"
    labels.extend(["A", "B", "C", "D", "E"])
    for problem in range(1, 31):
        labels.append(str(problem))

    # Wipe everything if it's Target and handle the special case.
    if full_round == "Target":
        last_problem = int(input("What's the last problem you want to print (e.g. 4 for problems 3-4): ").strip())
        first_label = str(last_problem - 1)
        last_label = str(last_problem)
        labels = ["-", "*", first_label, last_label]
        test_name = f"{year} {full_level} {full_round} Round {first_label}-{last_label}"
        png_urls = png_urls[2 * last_problem - 4:2 * last_problem]
elif test_type == "AMC":
    test_name = f"{year} {full_level} {full_round} Round {first_label}-{last_label}"
    amc_type = int(
        input(
            "1) AMC-8\n2) AMC-10\n3) AMC-12\n4) AIME\n5) USAJMO\n6) USAMO\n7) IMO\nWhich one: "
        ).strip()
    )
    test_name = f"{year} {amc_type_name} Practice"

print(f"Generating {test_name}")
if test_type == "Mathcounts":
    print(f"Level: {level}, Round type: {round_type}")
elif test_type == "AMC":
    print(f"AMC Type: {amc_type}")
elif test_type == "ARML":
    print(f"Level: {level}, Round type: {round_type}")
    year = int(input("Please label the problem set with a year [2024]: ").strip())

if len(labels) == len(png_urls):
    input(f"Confirm labels - {labels} (enter to accept):")

    # Example of proceeding based on the choices
    print(f"Generating {test_name}")
    if test_type == "mathcounts":
        print(f"Level: {level}, Round type: {round_type}")
    elif test_type == "amc":
        print(f"AMC Type: {amc_type}")

    problems = [
        {"label": label, "link": png_url} for label, png_url in zip(labels, png_urls)
    ]

data = {"set_label": test_name, "problems": problems}
print(json.dumps(data, indent=4))
print()
test_name_no_spaces = test_name.replace(" ", "")
b64data = base64.b64encode(
    json.dumps(data).replace(" ", "").replace(test_name_no_spaces, test_name).encode()
).decode()
print(f"Here is a save state you can share for the test:\n{b64data}")

for test in generate_tests():
    data = {"set_label": test.name, "problems": test.problems}
    labels = problem["label"] for problem in test.problems
    if len(labels) == len(png_urls):
        input(f"Confirm labels - {labels} (enter to accept):")

        print(json.dumps(data, indent=4))
        print()
        b64data = base64.b64encode(json.dumps(data).replace(" ", "").encode()).decode()
        print(f"Here is a save state you can share for the test:\n{b64data}")
