#!/usr/bin/env python
import json
import multiprocessing as mp

import requests
from flask import Flask, jsonify, render_template, request

import repository

app = Flask(__name__)


# FUNCTIONS #
def function_get_index_by_ein(ein):
    return repository.get_data_by_ein(ein)


def function_get_index_by_company_name(name):
    return repository.get_data_by_name(name)


def function_handle_search_argument(search_argument):
    return (
        function_get_index_by_ein(search_argument)
        if search_argument.isnumeric()
        else function_get_index_by_company_name(search_argument)
    )


def function_background_db_tasks():
    function_build_name_index()
    function_build_ein_index()


def function_build_name_index():
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
    repository.insert_bulk_with_name(sql_data)


def function_worker_load(json_uri):
    ein_response = requests.get(json_uri)
    ein_data = json.loads(ein_response.text)
    json_uri = ein_response.url
    for struct in ein_data["reporting_structure"]:
        for plan in struct["reporting_plans"]:
            ein = plan["plan_id"]
            repository.update_ein(json_uri, ein)


def function_build_ein_index():
    data = repository.get_rows_without_ein()
    with mp.Pool(processes=16) as pool:
        pool.map(function_worker_load, [item[0] for item in data])


# VIEWS #
@app.route("/")
def view_index():
    return render_template("index.html")


@app.route("/result")
def view_result_by_company_name():
    search_argument = request.args.get("search_argument")
    if not search_argument:
        return jsonify({})
    result_set = function_handle_search_argument(search_argument)

    return render_template(
        "result.html",
        result_set=result_set,
    )


# APIS #
@app.route("/api/fetch")
def endpoint_get_listings_by_index_file():
    index_file = request.args.get("index_file")
    if not index_file:
        return jsonify({})
    response = requests.get(index_file)
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


@app.route("/api/search/<search_argument>")
def endpoint_get_company_name_list(search_argument):
    return jsonify(function_handle_search_argument(search_argument))


# APP #
@app.before_first_request
def function_setup():
    mp.Process(target=function_background_db_tasks).start()


if __name__ == "__main__":
    repository.migrate()
    app.run(debug=True)
