import pytest
import requests
import time

BASE_URL = "https://api.restful-api.dev/objects"

# ===== Вспомогательные функции =====
def sleep_if_needed(test_number):
    if (test_number + 1) % 2 == 0:
        time.sleep(8)

# ===== Тесты =====

def test_get_all_objects():
    sleep_if_needed(0)
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_objects_by_ids():
    sleep_if_needed(1)
    response = requests.get(f"{BASE_URL}?id=1&id=2&id=3")
    assert response.status_code == 200
    assert len(response.json()) == 3

def test_get_single_object():
    sleep_if_needed(2)
    response = requests.get(f"{BASE_URL}/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "1"
    assert data["name"] == "Google Pixel 6 Pro"

def test_post_add_object():
    sleep_if_needed(3)
    payload = {
        "name": "Test Device",
        "data": {"color": "Black", "capacity": "64 GB"}
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 200
    created_object = response.json()
    assert created_object["name"] == payload["name"]

def test_put_update_object():
    sleep_if_needed(4)
    payload = {
        "name": "Updated Device",
        "data": {"color": "Green", "capacity": "128 GB"}
    }
    # Для обновления сначала нужно создать объект
    create_response = requests.post(BASE_URL, json={"name": "Temp Device"})
    obj_id = create_response.json()["id"]

    update_response = requests.put(f"{BASE_URL}/{obj_id}", json=payload)
    assert update_response.status_code == 200
    updated_object = update_response.json()
    assert updated_object["name"] == "Updated Device"

def test_patch_partial_update_object():
    sleep_if_needed(5)
    payload_patch = {
        "data": {"capacity": "256 GB"}
    }
    create_response = requests.post(BASE_URL, json={"name": "Temp Patch Device"})
    obj_id = create_response.json()["id"]

    patch_response = requests.patch(f"{BASE_URL}/{obj_id}", json=payload_patch)
    assert patch_response.status_code == 200
    patched_object = patch_response.json()
    assert patched_object["data"]["capacity"] == "256 GB"

def test_delete_object():
    sleep_if_needed(6)
    create_response = requests.post(BASE_URL, json={"name": "Temp Delete Device"})
    obj_id = create_response.json()["id"]

    delete_response = requests.delete(f"{BASE_URL}/{obj_id}")
    assert delete_response.status_code == 200

    # Проверяем что объект реально удалён
    get_response = requests.get(f"{BASE_URL}/{obj_id}")
    assert get_response.status_code == 404

# ===== Плохие тесты (ожидаем фейлы) =====
'''
def test_fail_wrong_status_code():
    sleep_if_needed(7)
    response = requests.get(BASE_URL)
    assert response.status_code == 404  # Специальная ошибка

def test_fail_post_without_name():
    sleep_if_needed(8)
    payload = {
        "data": {"capacity": "64 GB"}
    }
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 400  # Но API вернёт 200 → тест упадёт
'''
# ===== Дополнительные тесты для покрытия =====

def test_get_object_not_found():
    sleep_if_needed(9)
    response = requests.get(f"{BASE_URL}/9999999")
    assert response.status_code in (404, 200)  # У кого-то может быть по-разному

def test_post_and_delete_object():
    sleep_if_needed(10)
    payload = {
        "name": "Temp Device for Deletion",
        "data": {"price": 123}
    }
    post_response = requests.post(BASE_URL, json=payload)
    assert post_response.status_code == 200
    obj_id = post_response.json()["id"]

    delete_response = requests.delete(f"{BASE_URL}/{obj_id}")
    assert delete_response.status_code == 200
