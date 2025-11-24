# apps/api/tests/test_rbac.py
def test_admin_access(client, admin_token):
    r = client.post("/governance/advisory/members", headers={"Authorization": f"Bearer {admin_token}"}, json={"name":"X", "role":"jurist","region":"europe"})
    assert r.status_code == 200

def test_public_denied(client):
    r = client.post("/governance/advisory/members", json={"name":"X"})
    assert r.status_code == 401 or r.status_code == 403
