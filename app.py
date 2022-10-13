#!/usr/bin/env python
import json
from multiprocessing import Process

import requests
from flask import Flask, jsonify, render_template, request

from repository import Repository

app = Flask(__name__)


def function_get_index_by_company_name(search_argument):
    return Repository().get_data_by_name(search_argument)


@app.route("/api/fetch")
def endpoint_get_listings_by_index_file():
    response = requests.get(request.args.get("index_file"))
    data = json.loads(response.text)
    plan_name_list = []
    network_file_list = []
    for reporting_structure in data["reporting_structure"]:
        for plan in reporting_structure["reporting_plans"]:
            plan_name_list.append(plan["plan_name"])
        for network_file in reporting_structure["in_network_files"]:
            network_file_list.append(network_file["location"])
    return jsonify(
        {"plan_name_list": plan_name_list, "network_file_list": network_file_list}
    )


@app.route("/api/search/byname/<search_argument>")
def endpoint_get_company_name_list(search_argument):
    return jsonify(function_get_index_by_company_name(search_argument))


@app.route("/result")
def view_result_by_company_name():
    result_set = function_get_index_by_company_name(request.args.get("search_argument"))
    return render_template(
        "result.html",
        result_set=result_set,
    )


@app.route("/")
def view_index():
    return render_template("index.html")


def background_db_tasks():
    build_name_index()
    build_ein_index()


def build_name_index():
    api_url = "https://transparency-in-coverage.uhc.com/api/v1/uhc/blobs/"
    response = requests.get(api_url)
    data = json.loads(response.text)
    sql_data = []
    for item in data["blobs"]:
        if item["name"].endswith("index.json"):
            download_url = item["downloadUrl"]
            clean_name = download_url.split("_")[-2].replace("-", " ").strip()
            sql_tuple = (download_url, clean_name)
            sql_data.append(sql_tuple)
    Repository().insert_bulk_with_name(sql_data)


def build_ein_index():
    data = Repository().get_rows_without_ein()
    for ein_response in [requests.get(item[0]) for item in data]:
        ein_data = json.loads(ein_response.text)
        json_uri = ein_response.url
        for struct in ein_data["reporting_structure"]:
            for plan in struct["reporting_plans"]:
                ein = plan["plan_id"]
                Repository().update_ein(json_uri, ein)


if __name__ == "__main__":
    Repository().migrate()
    Process(target=background_db_tasks).start()
    print("Missing still:", len(Repository().get_rows_without_ein()))
    app.run(debug=True)
