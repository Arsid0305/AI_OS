# connectors/ozon_connector.py
import os
import requests
from datetime import datetime

BASE_URL = "https://api-seller.ozon.ru"


def _headers():
    return {
        "Client-Id": os.getenv("OZON_CLIENT_ID", "").strip(),
        "Api-Key":   os.getenv("OZON_API_KEY", "").strip(),
        "Content-Type": "application/json",
    }


def _fmt_date(iso: str) -> str:
    if not iso:
        return ""
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.strftime("%d.%m.%Y")
    except Exception:
        return iso[:10]


def _get_product_info(skus: list) -> dict:
    """SKU → {name, offer_id} через /v3/product/info/list"""
    if not skus:
        return {}
    try:
        int_skus = [int(s) for s in skus if s.isdigit()]
        if not int_skus:
            return {}
        resp = requests.post(
            f"{BASE_URL}/v3/product/info/list",
            headers=_headers(),
            json={"sku": int_skus},
            timeout=15,
        )
        if not resp.ok:
            return {}

        items = resp.json().get("items", [])
        result = {}
        for item in items:
            name     = item.get("name", "")
            offer_id = item.get("offer_id", "—")
            for sku_field in ("sku", "fbo_sku", "fbs_sku", "id"):
                sku_val = str(item.get(sku_field, ""))
                if sku_val and sku_val in [str(s) for s in int_skus]:
                    result[sku_val] = {"name": name, "offer_id": offer_id}
                    break

        if not result:
            for item in items:
                for src in item.get("sources", []):
                    sku_val = str(src.get("sku", ""))
                    if sku_val in skus:
                        result[sku_val] = {
                            "name":     item.get("name", "Товар"),
                            "offer_id": item.get("offer_id", "—"),
                        }
        return result

    except Exception:
        return {}


def get_unanswered_feedbacks(take: int = 100, skip: int = 0) -> list[dict]:
    resp = requests.post(
        f"{BASE_URL}/v1/review/list",
        headers=_headers(),
        json={"status": "UNPROCESSED", "limit": min(max(take, 20), 100), "sort_dir": "DESC"},
        timeout=30,
    )
    resp.raise_for_status()
    reviews_raw = resp.json().get("reviews", [])

    if not reviews_raw:
        return []

    skus = list({str(r.get("sku", "")) for r in reviews_raw if r.get("sku")})
    info_map = _get_product_info(skus)

    result = []
    for r in reviews_raw:
        comment    = (r.get("text") or "").strip()
        photos_raw = r.get("photos") or []
        videos_raw = r.get("videos") or []

        if not comment and not photos_raw and not videos_raw:
            continue

        sku  = str(r.get("sku", "—"))
        info = info_map.get(sku, {})

        photos = []
        for p in photos_raw:
            url = p.get("url") or (p if isinstance(p, str) else "")
            if url:
                photos.append(url)

        video_url = ""
        for v in videos_raw:
            url = v.get("url") or (v if isinstance(v, str) else "")
            if url:
                video_url = url
                break

        result.append({
            "id":              r.get("id", ""),
            "productName":     info.get("name", f"Товар (SKU {sku})"),
            "article":         sku,
            "supplierArticle": info.get("offer_id", "—"),
            "color":           "",
            "author":          "",
            "stars":           r.get("rating", 0),
            "pros":            "",
            "cons":            "",
            "comment":         comment,
            "date":            _fmt_date(r.get("published_at", "")),
            "orderDate":       "",
            "photos":          photos,
            "videoUrl":        video_url,
            "status":          "pending",
            "platform":        "ozon",
        })

    return result


def _change_status(review_ids: list, status: str = "PROCESSED") -> bool:
    try:
        resp = requests.post(
            f"{BASE_URL}/v1/review/change-status",
            headers=_headers(),
            json={"review_ids": review_ids, "status": status},
            timeout=15,
        )
        return resp.ok
    except Exception:
        return False


def send_reply(feedback_id: str, text: str) -> bool:
    for payload in [
        {"review_id": feedback_id, "text": text},
        {"review_uuid": feedback_id, "text": text},
    ]:
        resp = requests.post(
            f"{BASE_URL}/v1/review/comment/create",
            headers=_headers(),
            json=payload,
            timeout=30,
        )
        if resp.ok:
            _change_status([feedback_id])
            return True
    resp.raise_for_status()
    return False


def check_token() -> dict:
    try:
        resp = requests.post(
            f"{BASE_URL}/v1/review/list",
            headers=_headers(),
            json={"status": "UNPROCESSED", "limit": 20},
            timeout=10,
        )
        if resp.status_code == 401:
            return {"ok": False, "error": "Ozon токен недействителен (401)"}
        if resp.status_code == 403:
            return {"ok": False, "error": "Нет доступа к Ozon API (403). Роль: Review."}
        resp.raise_for_status()
        return {"ok": True}
    except requests.RequestException as e:
        return {"ok": False, "error": str(e)}
