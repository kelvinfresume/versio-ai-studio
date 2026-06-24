# Database Documentation

## PostgreSQL

Database Name:

```text
versio_dev
```

---

## Tables

### projects

Stores uploaded audio projects.

| Column | Type |
|----------|----------|
| project_id | varchar |
| project_name | varchar |
| story_prompt | text |
| bucket | varchar |
| object_key | varchar |
| filename | varchar |
| content_type | varchar |
| status | varchar |
| created_at | timestamp |

---

### storyboards

Stores generated storyboard scenes.

| Column | Type |
|----------|----------|
| storyboard_id | varchar |
| project_id | varchar |
| scene_number | integer |
| title | varchar |
| visual | text |
| camera | text |
| emotion | text |
| created_at | timestamp |

---

### scene_images

Stores generated scene image metadata.

| Column | Type |
|----------|----------|
| image_id | varchar |
| project_id | varchar |
| scene_number | integer |
| bucket | varchar |
| object_key | varchar |
| prompt | text |
| status | varchar |
| created_at | timestamp |

---

## Useful Queries

### Projects

```sql
SELECT *
FROM projects
ORDER BY created_at DESC;
```

### Storyboards

```sql
SELECT *
FROM storyboards
ORDER BY created_at DESC;
```

### Scene Images

```sql
SELECT *
FROM scene_images
ORDER BY created_at DESC;
```

### Storyboard Join

```sql
SELECT
    p.project_name,
    s.scene_number,
    s.title,
    s.emotion
FROM storyboards s
JOIN projects p
    ON p.project_id = s.project_id
ORDER BY p.project_name, s.scene_number;
```
