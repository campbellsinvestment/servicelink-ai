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

## Interactive Documentation

FastAPI automatically generates OpenAPI documentation.

```
http://localhost:8000/docs
```