# How to run #

```
git clone https://github.com/wfzyx/special-octo-guide.git
cd special-octo-guide
pip3 install -r requirements.txt
python3 app.py
```

Obs: there is a .envrc file for convenience

# Acceptance Criteria #

- [X] Fetch transparency[dash]in[dash]coverage[dot]uhc[dot]com
- [X] Get the employer name list
- [X] Extract the json index files on demand
- Endponts to make:
	- [ ] Search for a company EIN
	- [X] Search for a company Name
	- [X] returns a list of "plan names" and their "in network pricing file locations" for the matching company.

Obs: EIN search was not implemented, because a reliable and fast way to fetch all the companies EINs wasn't found, the only approach would be to hit the target api thoushands of times, and that doesn't sound good :(

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
