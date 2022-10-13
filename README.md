# General Observations #

- sqlite3 doesn't love multithreading, but it is workable when doing small atomic operations - opening and closing the session on spot;
- The EIN index built by the background task is already hitting its throttling speed. To achieve better speeds a distributed approach using cloud would be needed;
- A copy of the fully built database is provided on this repo since building it from scratch takes a few minutes;

# How to run #

```
git clone https://github.com/wfzyx/special-octo-guide.git
cd special-octo-guide
pip3 install -r requirements.txt
python3 app.py
```

*Note: There is a .envrc file for convenience*

# Acceptance Criteria #

- [X] Fetch transparency[dash]in[dash]coverage[dot]uhc[dot]com
- [X] Get the employer name list
- [X] Extract the JSON index files on demand
- Endpoints to make:
	- [X] Search for a company EIN
	- [X] Search for a company Name
	- [X] returns a list of "plan names" and their "in network pricing file locations" for the matching company.

# Optional #

- [X] Create a simple UI with an input box where the user can type in their search term and see the results returned from the API.


# Evaluation Criteria #

- Work as intended
- Quality of code
- Speed
- Organization of the results

# Deliverables #

- Source code bundle
	- Data collection logic
	- API code
	- Instructions for running

(Original statement redacted to prevent future google-fu)
