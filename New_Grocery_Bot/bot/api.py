import json

import requests


BASE_URL = 'http://127.0.0.1:8000/api'

class MessageAPI:

    keys = ('id', 'text', 'unix_time', 'is_bot', 'user_id')

    def create(self, data):
        base_url = BASE_URL + '/message/create/'
        dict_data = {}
        for key, data in data.items():
            dict_data[key] = data

        response = requests.post(base_url, data=dict_data)
        if response.status_code == 201:  # 201 means the item was created successfully
            print("Item created successfully!")
        else:
            print("Failed to create the item.")
            print("Response:", response.text)



class ProductAPI:

    keys = ('barcode', 'name')

    def get(self):
        base_url = BASE_URL + '/shop/get/'

        response = requests.get(base_url)
        if response.status_code == 201:  # 201 means the item was created successfully
            return "Got items successfully!"
        else:
            return "Response:", response.text

    def create(self, data: list[str]):
        base_url = BASE_URL + '/product/create/'
        dict_data = {}
        for key, data in zip(self.keys, data):
            dict_data[key] = data

        response = requests.post(base_url, data=dict_data)
        if response.status_code == 201:  # 201 means the item was created successfully
            print("Item created successfully!")
        else:
            print("Failed to create the item.")
            print("Response:", response.text)

    def delete(self, p_id):
        base_url = BASE_URL + f"/product/delete/{p_id}"

        response = requests.delete(base_url)
        # Check the response status
        if response.status_code == 204:  # 204 means the request was successful and the resource was deleted
            print("Item deleted successfully!")
        else:
            print("Failed to delete the item.")
            print("Response:", response.text)

    def update(self, product_data: list[str], p_id):
        base_url = BASE_URL + f"/product/update/{p_id}"

        dict_data = {}
        for key, data in zip(self.keys, product_data):
            dict_data[key] = data

        response = requests.put(base_url, product_data)
        # Check the response status
        if response.status_code == 200:  # 200 means the request was successful
            print("Item updated successfully!")
        else:
            print("Failed to update the item.")
            print("Response:", response.text)
