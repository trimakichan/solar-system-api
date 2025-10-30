import pytest

def test_get_all_planets_with_no_records(client):
    response = client.get("/planets/")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_a_404_response(client):
    response = client.get("/planets/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Planet 1 is not found."}

def test_get_one_planet(client, add_one_planet):
    response = client.get("/planets/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
            "id": 1, 
            "name": "Mercury",
            "description": "Smallest planet, closest to the Sun", 
            "distance_from_sun": 57910000}

def test_get_second_planet(client, add_two_planet):
    response = client.get("/planets/2")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
            "id": 2, 
            "name": "Earth",
            "description": "Our beautiful home", 
            "distance_from_sun": 149600000}
    
def test_get_all_planets(client, add_two_planet):
    response = client.get("/planets/")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
        {
            "id": 1, 
            "name": "Mercury",
            "description": "Smallest planet, closest to the Sun", 
            "distance_from_sun": 57910000
        },
        {
            "id": 2, 
            "name": "Earth",
            "description": "Our beautiful home", 
            "distance_from_sun": 149600000
        }]


def test_create_one_planets(client):
    #Act
    response = client.post("/planets/", json={
        "name": "Mercury",
        "description": "Smallest planet, closest to the Sun",
        "distance_from_sun": 5791000
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "Mercury",
        "description": "Smallest planet, closest to the Sun",
        "distance_from_sun": 5791000
    }

def test_delete_one_planet(client, add_two_planet):
    response = client.delete("/planets/1")

    assert response.status_code == 204

def test_400_key_error_response(client):
    # Act            
    response = client.post("/planets/", json={
        "name": "Earth"
    })
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {
        "message": "Invalid request. Please include name, description, and distance_from_sun."
        }

    
# def test_400_type_error_response(client):
#     #Act
#     response = client.post("/planets/", json={
#         "name": "Mercury",
#         "description": "Smallest planet, closest to the Sun",
#         "distance_from_sun": "number"
#     })
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 400
#     assert response_body == {"message": "Name and Description must be strings. Distance from sun must be a number."}