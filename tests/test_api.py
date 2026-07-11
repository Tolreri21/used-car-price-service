def test_predict(client, sample_df):
    response = client.post("/predict" , json= sample_df)
    body = response.json()
    assert response.status_code == 200
    assert "predicted_price" in body
    assert body["predicted_price"] > 0


