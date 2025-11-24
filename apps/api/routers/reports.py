# apps/api/routers/reports.py
@router.get("/certification/{actor_id}/public-report")
def public_report(actor_id: int, request: Request):
    lang = get_lang(request); t = load_locale(lang)
    capsule = get_capsule_data(actor_id)  # scores + version + proofs count
    return {
        "title": f"{t['app.title']} – {t['capsule.score']}",
        "actor_id": actor_id,
        "scores": capsule["scores"],
        "version": capsule["version"],
        "proofs_count": capsule["proofs_count"],
        "lang": lang
    }
