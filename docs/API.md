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

## Job Links

GET

```
/job-links
```

Returns explainable links between enriched job postings and normalized
community services.

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

## Job Posting Service Links

GET

```
/job-postings/{posting_id}/service-links
```

Returns service links for a single job posting.

Example

```
/job-postings/ziprecruiter-z003/service-links
```

---

## Conversational Search

GET

```
/search?q={query}
```

Interprets a natural-language question, extracts service categories and
locations, and returns ranked community-service matches with an
explainable answer.

Optional query parameter:

```
limit=5
```

Example

```
/search?q=meal%20delivery%20in%20Stony%20Plain
```

---

## Recommendations

GET

```
/recommendations
```

Returns globally ranked, explainable service recommendations with post
and service context.

Example

```json
[
  {
    "rank": 1,
    "post_id": "reddit-r004",
    "post_title": "Home care services",
    "service_id": "informalberta-3",
    "service_name": "Home Care Assistance",
    "organization": "Alberta Wellness Network",
    "city": "Spruce Grove",
    "category": "home_care",
    "score": 29,
    "match_reasons": [
      "category:home_care",
      "city:Spruce Grove",
      "keywords:care,home,seniors",
      "source:InformAlberta",
      "organization:Alberta Wellness Network"
    ]
  }
]
```

---

## Reddit Post Recommendations

GET

```
/social-posts/reddit/{post_id}/recommendations
```

Returns ranked recommendations for a single Reddit post.

Optional query parameter:

```
limit=5
```

---

## Interactive Documentation

FastAPI automatically generates OpenAPI documentation.

```
http://localhost:8000/docs
```