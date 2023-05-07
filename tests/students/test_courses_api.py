import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, make_m2m=True, *args, **kwargs)

    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)

    return factory


@pytest.mark.django_db
def test_one_course(client, course_factory):
    course = course_factory(_quantity=10)
    response = client.get('/api/v1/courses/')
    data = response.json()

    assert data[0]['id'] == 1
    assert response.status_code == 200


@pytest.mark.django_db
def test_one_course(client, course_factory):
    course = course_factory(_quantity=5)
    response = client.get('/api/v1/courses/')
    data = response.json()

    assert len(data) == 5
    assert response.status_code == 200


@pytest.mark.django_db
def test_filter_course_by_id(client, course_factory):
    courses = course_factory(_quantity=30)
    data_id = Course.objects.filter(id=courses[0].id).first().id
    response = client.get(f'/api/v1/courses/?id={data_id}')
    data = response.json()[0]
    assert data['id'] == data_id
    assert response.status_code == 200


@pytest.mark.django_db
def test_filter_course_by_name(client, course_factory):
    courses = course_factory(_quantity=10)
    data_name = Course.objects.filter(name=courses[0].name).first().name
    response = client.get(f'/api/v1/courses/?name={data_name}')
    data = response.json()[0]
    assert data['name'] == data_name
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_course(client):
    response = client.post('/api/v1/courses/', data={'name': 'test_name'}, format='json')


    assert Course.objects.filter(name='test_name').first().name == 'test_name'
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=10)
    data_id = Course.objects.filter(id=courses[0].id).first().id
    print(courses[0].id)
    response = client.patch(f'/api/v1/courses/{data_id}/', data={'name': 'test_name'}, format='json')
    assert response.status_code == 200

@pytest.mark.django_db
def test_delete_course(client, course_factory):
    courses = course_factory(_quantity=10)
    count = Course.objects.count()

    response = client.delete(f'/api/v1/courses/{courses[0].id}/')
    print(response.status_code)
    assert Course.objects.count() == count-1
    assert response.status_code == 204

