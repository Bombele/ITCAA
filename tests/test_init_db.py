import pytest
from apps.api.database import init_db, SessionLocal
from src import init_db as init_script
from apps.api.models.models_actors import Actor, Client, Partner

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Initialise la base avant les tests
    init_db()
    yield
    # Nettoyage éventuel après tests (rollback ou truncate si nécessaire)

def test_seed_data_inserts_records():
    success = init_script.seed_data()
    assert success is True

    db = SessionLocal()
    actors = db.query(Actor).all()
    clients = db.query(Client).all()
    partners = db.query(Partner).all()
    db.close()

    assert len(actors) >= 3
    assert len(clients) >= 3
    assert len(partners) >= 2

def test_seed_data_no_duplicates_on_rerun():
    # Relancer le seed
    success = init_script.seed_data()
    assert success is True

    db = SessionLocal()
    actors = db.query(Actor).filter_by(name="Alpha PMC").all()
    clients = db.query(Client).filter_by(name="ONU").all()
    partners = db.query(Partner).filter_by(name="Université de Bruxelles").all()
    db.close()

    # Vérifie qu'il n'y a qu'un seul enregistrement par entité
    assert len(actors) == 1
    assert len(clients) == 1
    assert len(partners) == 1

def test_seed_data_returns_false_on_error(monkeypatch):
    # Simule une erreur en forçant un rollback
    def fake_commit():
        raise Exception("Erreur simulée")

    db = SessionLocal()
    monkeypatch.setattr(db, "commit", fake_commit)

    result = init_script.seed_data()
    assert result is False