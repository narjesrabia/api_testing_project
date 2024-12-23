import requests
import pytest
import csv


def log_to_csv(request_type, endpoint, status_code, result):
    with open('results.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([request_type, endpoint, status_code, result])

@pytest.fixture
def base_url():
    return "https://jsonplaceholder.typicode.com"


def test_status_code(base_url):
    response = requests.get(f"{base_url}/posts")
    result = 'success' if response.status_code == 200 else 'failure'
    log_to_csv('GET', '/posts', response.status_code, result)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


def test_value_in_response(base_url):
    response = requests.get(f"{base_url}/posts")
    json_data = response.json()
    result = 'success' if json_data[0]['id'] == 1 else 'failure'
    log_to_csv('GET', '/posts', response.status_code, result)
    assert json_data[0]['id'] == 1, f"Expected value 1, got {json_data[0]['id']}"


def test_with_variables(base_url):
    variable_key = "some_value"
    response = requests.get(f"{base_url}/posts")
    json_data = response.json()
    result = 'success' if json_data[0]['id'] == 1 else 'failure'
    log_to_csv('GET', '/posts', response.status_code, result)
    assert json_data[0]['id'] == 1, f"Expected value 1, got {json_data[0]['id']}"


def test_set_variables(base_url):
    variable_key = "variable_value"
    response = requests.get(f"{base_url}/posts")
    json_data = response.json()
    result = 'success' if json_data[0]['id'] == 1 else 'failure'
    log_to_csv('GET', '/posts', response.status_code, result)
    assert json_data[0]['id'] == 1, f"Expected value 1, got {json_data[0]['id']}"


def test_put_post_success(base_url):
    post_data = {
        "title": "Updated Post",
        "body": "This is the updated content of the post.",
        "userId": 1
    }
    post_id = 1  
    response = requests.put(f"{base_url}/posts/{post_id}", json=post_data)
    json_data = response.json()
    result = 'success' if response.status_code == 200 else 'failure'
    log_to_csv('PUT', f'/posts/{post_id}', response.status_code, result)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert json_data['title'] == "Updated Post", f"Expected title to be 'Updated Post', got {json_data['title']}"


def test_put_post_id_remains_the_same(base_url):
    post_data = {
        "title": "Updated Post",
        "body": "This is the updated content of the post.",
        "userId": 1
    }
    post_id = 1
    response = requests.put(f"{base_url}/posts/{post_id}", json=post_data)
    json_data = response.json()
    result = 'success' if response.status_code == 200 else 'failure'
    log_to_csv('PUT', f'/posts/{post_id}', response.status_code, result)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert json_data['id'] == 1, f"Expected id to be 1, got {json_data['id']}"


def test_put_post_body_updated(base_url):
    post_data = {
        "title": "Updated Post",
        "body": "This is the updated content of the post.",
        "userId": 1
    }
    post_id = 1
    response = requests.put(f"{base_url}/posts/{post_id}", json=post_data)
    json_data = response.json()
    result = 'success' if response.status_code == 200 else 'failure'
    log_to_csv('PUT', f'/posts/{post_id}', response.status_code, result)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert json_data['body'] == "This is the updated content of the post.", f"Expected body to be 'This is the updated content of the post.', got {json_data['body']}"


def test_put_post_id_unchanged(base_url):
    post_data = {
        "title": "Updated Post",
        "body": "This is the updated content of the post.",
        "userId": 1
    }
    post_id = 1
    response = requests.put(f"{base_url}/posts/{post_id}", json=post_data)
    json_data = response.json()
    result = 'success' if response.status_code == 200 else 'failure'
    log_to_csv('PUT', f'/posts/{post_id}', response.status_code, result)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    assert json_data['id'] == 1, f"Expected id to be 1, got {json_data['id']}"


def test_delete_post_not_found(base_url):
    post_id = 1
    response = requests.delete(f"{base_url}/posts/{post_id}")
    result = 'success' if response.status_code == 200 else 'failure'
    log_to_csv('DELETE', f'/posts/{post_id}', response.status_code, result)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"


def test_delete_response_empty(base_url):
    post_id = 1
    response = requests.delete(f"{base_url}/posts/{post_id}")
    json_data = response.json()
    result = 'success' if response.status_code == 200 else 'failure'
    log_to_csv('DELETE', f'/posts/{post_id}', response.status_code, result)
    assert json_data == {}, f"Expected empty response body, got {json_data}"


def test_response_contains_content_type_header(base_url):
    post_id = 1
    response = requests.get(f"{base_url}/posts/{post_id}")
    result = 'success' if "Content-Type" in response.headers else 'failure'
    log_to_csv('GET', f'/posts/{post_id}', response.status_code, result)
    assert "Content-Type" in response.headers, "Expected 'Content-Type' header not found"


def test_post_create_valid_data(base_url):
    post_data = {"title": "foo", "body": "bar", "userId": 1}
    response = requests.post(f"{base_url}/posts", json=post_data)
    result = 'success' if response.status_code == 201 else 'failure'
    log_to_csv('POST', '/posts', response.status_code, result)
    assert response.status_code == 201


def test_post_create_missing_body(base_url):
    post_data = {"title": "foo", "userId": 1}  
    response = requests.post(f"{base_url}/posts", json=post_data)
    result = 'success' if response.status_code == 201 else 'failure'
    log_to_csv('POST', '/posts', response.status_code, result)
    assert response.status_code == 201


def test_post_create_invalid_userId(base_url):
    post_data = {"title": "foo", "body": "bar", "userId": "invalid"}  
    response = requests.post(f"{base_url}/posts", json=post_data)
    result = 'success' if response.status_code == 201 else 'failure'
    log_to_csv('POST', '/posts', response.status_code, result)
    assert response.status_code == 201


def test_post_create_empty_title(base_url):
    post_data = {"title": "", "body": "bar", "userId": 1}  
    response = requests.post(f"{base_url}/posts", json=post_data)
    result = 'success' if response.status_code == 201 else 'failure'
    log_to_csv('POST', '/posts', response.status_code, result)
    assert response.status_code == 201


def test_post_create_with_extra_fields(base_url):
    post_data = {"title": "foo", "body": "bar", "userId": 1, "extraField": "notAllowed"}
    response = requests.post(f"{base_url}/posts", json=post_data)
    result = 'success' if response.status_code == 201 else 'failure'
    log_to_csv('POST', '/posts', response.status_code, result)
    assert response.status_code == 201


def test_get_non_existent_post(base_url):
    post_id = 9999 
    response = requests.get(f"{base_url}/posts/{post_id}")
    result = 'success' if response.status_code == 404 else 'failure'
    log_to_csv('GET', f'/posts/{post_id}', response.status_code, result)
    assert response.status_code == 404


def test_delete_non_existent_post(base_url):
    post_id = 9999 
    response = requests.delete(f"{base_url}/posts/{post_id}")
    result = 'success' if response.status_code in [200, 404] else 'failure'
    log_to_csv('DELETE', f'/posts/{post_id}', response.status_code, result)
    assert response.status_code in [200, 404]


def test_patch_post(base_url):
    post_id = 1 
    patch_data = {"title": "Partially Updated Title"}
    response = requests.patch(f"{base_url}/posts/{post_id}", json=patch_data)
    json_data = response.json()
    result = 'success' if response.status_code == 200 else 'failure'
    log_to_csv('PATCH', f'/posts/{post_id}', response.status_code, result)
    assert response.status_code == 200


def test_get_posts_list(base_url):
    response = requests.get(f"{base_url}/posts")
    json_data = response.json()
    result = 'success' if response.status_code == 200 else 'failure'
    log_to_csv('GET', '/posts', response.status_code, result)
    assert response.status_code == 200
