from http.client import responses

import requests
import allure
import pytest


class MainAPI:

    def __init__(self):
        self.url = "http://51.250.26.13:8083/"
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiYWRtaW4iLCJpYXQiOjE3NTY3NDI0NzcsImV4cCI6MTc1Njc0MzM3N30.JzCp5Qr3afeQZV6zMOlDQkoSt9Rpk8oIOJJJ1R-PXaM"

    def get_token(self, username="leyla", password="water-fairy"):
        body = {
            "username": username,
            "password": password
        }
        response = requests.post(self.url + "auth/login", json=body)
        token = response.json()['userToken']
        return response.status_code, token

    def get_company(self, active: bool = None):
        param = {"active": active}
        response = requests.get(self.url + "company", params=param)
        company_list = response.json()
        return response.status_code, company_list

    def create_company(self, name: str, desc: str, token: str):
        body = {
            "name": name,
            "description": desc
        }
        response = requests.post(self.url + "company", headers={"x-client-token" : token}, json=body)
        resp = response.json()
        return response.status_code, resp['id']

    def get_company_by_id(self, id_company: int):
        response = requests.get(self.url + f"company/{id_company}")
        resp = response.json()
        return response.status_code, resp["id"]

    def delete_company(self, id_company, token):
        response = requests.get(self.url + f"company/delete/{id_company}", headers={"x-client-token" : token})
        return response.status_code

    def change_status(self, id_company: int, token, active: bool):
        body = {
            "isActive": active
        }
        response = requests.patch(self.url + f"company/status/{id_company}", headers={"x-client-token" : token}, json=body)
        resp = response.json()
        status_active = resp["isActive"]
        return response.status_code, status_active