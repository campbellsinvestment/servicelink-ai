# REST API

## Base URL

```
http://localhost:8000
```

---

## Health

GET

```
/health
```

Example

```json
{
    "status":"healthy"
}
```

---

## Services

GET

```
/services
```

Returns normalized community services.

---

## Reddit Posts

GET

```
/social-posts/reddit
```

Returns normalized Reddit posts.

---

## Reddit Summary

GET

```
/social-posts/reddit/summary
```

Returns summary statistics.

---

## Job Postings

GET

```
/job-postings
```

Returns normalized Indeed and ZipRecruiter jobs.

---

## Job Summary

GET

```
/job-postings/summary
```

Returns aggregated job statistics.

---

## Entity Links

GET

```
/entity-links
```

Returns explainable links between enriched Reddit posts and normalized
community services.

Example

```json
[
  {
    "post_id": "reddit-r001",
    "service_id": "community-A101",
    "score": 15,
    "match_reasons": [
      "category:transportation",
      "city:Edmonton"
    ]
  }
]
```

---

## Reddit Post Service Links

GET

```
/social-posts/reddit/{post_id}/service-links
```

Returns service links for a single Reddit post.

Example

```
/social-posts/reddit/reddit-r001/service-links
```

---

## Interactive Documentation

FastAPI automatically generates OpenAPI documentation.

```
http://localhost:8000/docs
```