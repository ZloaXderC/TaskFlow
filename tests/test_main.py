import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app


@pytest.mark.asyncio
async def test_root(client):
    response = await client.get("/")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_register(client):
    response = await client.post(
        "/auth/register",
        json = {
            "email":"test@example.com",
            "password": "123456"
        }
    )
    print([getattr(route,"path", None) for route in app.routes])
    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_existing_email(client):
    user_data = {
        "email": "test@example.com",
        "password":"123456"
    }

    response = await client.post(
        "/auth/register",
        json = user_data
    )
    response1 =  await client.post(
        "/auth/register",
        json = user_data)
    assert response.status_code == 201
    assert response1.status_code ==409

@pytest.mark.asyncio
async def test_current_login(client):
    await client.post(
        "/auth/register",
        json ={
            "email": "test@example.com",
            "password": "123456"
        }
    )
    response = await client.post(
        "/auth/login",
        data = {
            "username": "test@example.com",
            "password": "123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

@pytest.mark.asyncio
async def test_incorrect_password(client):
    await client.post(
        "/auth/register",
        json = {
            "email": "test@example.com",
            "password": "123456"
        }
    )
    response = await client.post(
        "auth/login",
        data = {
            "username": "test@example.com",
            "password": "123"
        }
    )

    assert response.status_code == 401

@pytest.mark.asyncio
async def test_JWT(client):
    await client.post(
        "/auth/register",
        json = {
            "email": "test@example.com",
            "password": "12345"
        }
    )
    login_response = await client.post(
        "/auth/login",
        data = {
            "username": "test@example.com",
            "password": "12345"
        }
    )

    token = login_response.json()["access_token"]

    response = await client.get(
        "/auth/me",
        headers = {
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_not_JWT(client):
    response = await client.get("/auth/me")

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_task(client):
    await client.post(
        "/auth/register",
        json = {
            "email": "test@example.com",
            "password": "12345"
        }
    )
    login = await client.post(
        "/auth/login",
        data = {
            "username": "test@example.com",
            "password": "12345"
        }
    )

    token = login.json()["access_token"]

    response = await client.post(
        "/task",
        headers = {
            "Authorization": f"Bearer {token}"
        },
        json = {
            "title":"Test task"
        }
    )

    assert response.status_code ==201

    data = response.json()
    assert data["title"] == "Test task"
    assert "id" in data

@pytest.mark.asyncio
async def test_create_task_without_token(client):
    response = await client.post(
        "/task",
        json = {
            "title": "test"
        }
    )
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_tasks(client):
    await client.post(
        "/auth/register",
        json = {
            "email":"test@example.com",
            "password":"12345"
        }
    )

    login = await client.post(
        "/auth/login",
        data = {
            "username":"test@example.com",
            "password":"12345"
        }
    )

    token = login.json()["access_token"]

    await client.post(
        "/task",
        headers = {
            "Authorization":f"Bearer {token}"
        },
        json = {
            "title":"task1"
        }
    )

    await client.post(
        "/task",
        headers = {
                    "Authorization":f"Bearer {token}"
        },
        json = {
            "title":"task2"
        }
    )

    

    response = await client.get(
        "/task",
        headers = {
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data,list)
    assert len(data)>=1


@pytest.mark.asyncio
async def research_task(client):
    await client.post(
        "/auth/register",
        json = {
            "email":"test@example.com",
            "password":"12345"
        }
    )
    
    login = await client.post(
        "/auth/login",
        data = {
            "username":"test@example.com",
            "password":"12345"
        }
    )
    
    token = login.json()["access_token"]

    create_task = await client.post(
        "task",
        headers = {
            "Authorization": f"Bearer {token}"
        },
        json = {
            "title": "task"
        }
    )

    task_id = create_task.json()["id"]

    response = await client.get(
        f"/task/{task_id}",
        headers = {
            "Authorization":f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "task"
    assert "id" in data



@pytest.mark.asyncio
async def test_patch(client):
    await client.post(
            "/auth/register",
            json = {
                "email":"test@example.com",
                "password":"12345"
            }
        )
        
    login = await client.post(
        "/auth/login",
        data = {
            "username":"test@example.com",
            "password":"12345"
        }
    )
    
    token = login.json()["access_token"]

    create_task = await client.post(
        "/task",
        headers = {
            "Authorization": f"Bearer {token}"
        },
        json = {
            "title": "task"
        }
    )

    task_id = create_task.json()["id"]

    response = await client.patch(
        f"/task/{task_id}",
        headers = {
            "Authorization":f"Bearer {token}"
        },
        json = {
            "title":"Update",
            "complited": True
        }
    )

    assert response.status_code ==200

    data = response.json()
    assert data["title"] == "Update"
    assert data["complited"] is True


@pytest.mark.asyncio
async def test_delete_task(client):
    await client.post(
        "/auth/register",
        json = {
            "email":"test@example.com",
            "password":"12345"
        }
    )
    
    login = await client.post(
        "/auth/login",
        data = {
            "username":"test@example.com",
            "password":"12345"
        }
    )
    
    token = login.json()["access_token"]

    create_task = await client.post(
        "task",
        headers = {
            "Authorization": f"Bearer {token}"
        },
        json = {
            "title": "task"
        }
    )

    task_id = create_task.json()["id"]

    response = await client.delete(
        f"/task/{task_id}",
        headers = {
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code ==200

    response = await client.get(
        f"/task/{task_id}",
        headers ={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 404

@pytest.mark.asyncio
async def test_user_cannot_get_another_users_task(client):
    await client.post(
        "/auth/register",
        json = {
            "email":"test@example.com",
            "password":"12345"
        }
    )
    
    login = await client.post(
        "/auth/login",
        data = {
            "username":"test@example.com",
            "password":"12345"
        }
    )
    
    token = login.json()["access_token"]

    create_task = await client.post(
        "task",
        headers = {
            "Authorization": f"Bearer {token}"
        },
        json = {
            "title": "task"
        }
    )

    task_id = create_task.json()["id"]

    await client.post(
            "/auth/register",
            json = {
                "email":"test2@example.com",
                "password":"12345"
            }
        )
        
    login2 = await client.post(
            "/auth/login",
            data = {
                "username":"test2@example.com",
                "password":"12345"
            }
        )
    token2 = login2.json()["access_token"]

    response = await client.get(
        f"/task/{task_id}",
        headers = {
            "Authorization":f"Bearer {token2}"
        }
    )

    assert response.status_code ==404

@pytest.mark.asyncio
async def null_task(client):
    await client.post(
            "/auth/register",
            json = {
                "email":"test@example.com",
                "password":"12345"
            }
        )
        
    login = await client.post(
            "/auth/login",
            data = {
                "username":"test@example.com",
                "password":"12345"
            }
        )
    token = login.json()["access_token"]

    response = await client.post(
        "/task",
        headers = {
            "Authorization":f"Bearer {token}"
        },
        json = {
            "title": ""
        }
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def task_filter_complited(client):
    await client.post(
            "/auth/register",
            json = {
                "email":"test@example.com",
                "password":"12345"
            }
        )
        
    login = await client.post(
            "/auth/login",
            data = {
                "username":"test@example.com",
                "password":"12345"
            }
        )
    token = login.json()["acess_token"]

    create_task_1 = await client.post(
            "task",
            headers = {
                "Authorization": f"Bearer {token}"
            },
            json = {
                "title": "task1",
                "complited": True
            }
        )

    create_task2 = await client.post(
            "task",
            headers = {
                "Authorization": f"Bearer {token}"
            },
            json = {
                "title": "task2",
                "complited": False
            }
        )

    response = await client.get(
        "task",
        headers = {
            "Authorization":f"Bearer {token}"
        },
        params = {
            "comlited": True
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) ==1
    assert data[0]["complited"] is True

@pytest.mark.asyncio
async def test_search(client):
    await client.post(
                "/auth/register",
                json = {
                    "email":"test@example.com",
                    "password":"12345"
                }
            )
            
    login = await client.post(
            "/auth/login",
            data = {
                "username":"test@example.com",
                "password":"12345"
            }
        )
    token = login.json()["access_token"]

    await client.post(
            "task",
            headers = {
                "Authorization": f"Bearer {token}"
            },
            json = {
                "title": "Buy milk",
                "complited": True
            }
        )
    
    await client.post(
            "task",
            headers = {
                "Authorization": f"Bearer {token}"
            },
            json = {
                "title": "Buy book",
                "complited": True
            }
        )

    response = await client.get(
        "task",
        headers = {
            "Authorization": f"Bearer {token}"
        },
        params= {
            "search":"milk"
        }
    )

    assert response.status_code ==200

    data = response.json()

    assert len(data) ==1
    assert data[0]["title"] =="Buy milk"