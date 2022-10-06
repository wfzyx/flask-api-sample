#!/usr/bin/env python

import json

import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
ein_index = {}
name_index = {}


def get_index_by_company_name(search_argument):
    return {
        company_name: url
        for company_name, url in name_index.items()
        if search_argument.lower() in company_name.lower()
    }


@app.route("/api/search/byname/<search_argument>")
def api_get_company_name_list(search_argument):
    return jsonify(get_index_by_company_name(search_argument))


@app.route("/result")
def view_result_by_company_name():
    result_set = get_index_by_company_name(request.args.get("search_argument"))
    return render_template(
        "result.html",
        result_set=result_set,
    )


@app.route("/")
def index():
    return render_template("index.html")


def build_name_index():
    api_url = "https://transparency-in-coverage.uhc.com/api/v1/uhc/blobs/"
    response = requests.get(api_url)
    data = json.loads(response.text)
    for item in data["blobs"]:
        if item["name"].endswith("index.json"):
            formatted_name = (
                item["downloadUrl"].split("_")[-2].replace("-", " ").strip()
            )
            name_index[formatted_name] = item["downloadUrl"]


# This is very slow right now, don't use it
# def build_ein_index():
#     api_url = "https://transparency-in-coverage.uhc.com/api/v1/uhc/blobs/"
#     response = requests.get(api_url)
#     data = json.loads(response.text)
#     async_requests = [
#         grequests.get(item["downloadUrl"])
#         for item in data["blobs"]
#         if item["name"].endswith("index.json")
#     ]
#     for ein_response in grequests.imap(async_requests, size=100):
#         ein_data = json.loads(ein_response.text)
#         clean_name = ein_response.url.split("_")[-2].replace("-", " ").strip()
#         ein_index[
#             ein_data["reporting_structure"][0]["reporting_plans"][0]["plan_id"]
#         ] = clean_name


if __name__ == "__main__":
    build_name_index()
    app.run(debug=True)
