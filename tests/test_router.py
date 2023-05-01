
from fastapi import status


def test_poi_list(api_client, poi_factory):
    poi_factory.create_batch(5)
    response = api_client.get("/api/poi/")
    assert response.status_code == status.HTTP_200_OK
    breakpoint()
    # assert response.json() ==
