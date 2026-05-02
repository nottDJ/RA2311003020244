# Notification System Design

## Stage 1
**APIs to Fetch and Read Notifications**
1. **Get Notifications:** `GET /api/notifications`
   - Headers: `Authorization: Bearer <token>`
   - Response: A JSON array of notification objects (id, type, message, is_read, timestamp).

2. **Mark as Read:** `PUT /api/notifications/{id}/read`
   - Updates the database so the notification doesn't show up as unread anymore.

**Real-Time Design:** 
To get notifications instantly, we should use WebSockets. When a student logs in, the frontend opens a WebSocket connection. Whenever the backend creates a new notification, it pushes the data through that socket directly to the user's screen.

---

## Stage 2
**Database Choice**
I suggest using a SQL database like **PostgreSQL** or **MySQL**. Notifications have a very fixed structure, so a relational database works perfectly.

**Basic Schema:**
- `id` (Primary Key)
- `student_id` (Number)
- `type` (String/Enum: Placement, Result, Event)
- `message` (Text)
- `is_read` (Boolean, default is false)
- `created_at` (Timestamp)

**Scaling Issues:**
When we hit millions of rows, searching through them will get slow. To fix this, we can add indexes to the columns we search the most (like `student_id`). 

**Query Example:**
```sql
SELECT * FROM notifications WHERE student_id = 12345 AND is_read = false ORDER BY created_at DESC;

---

## Stage 3
**Fixing the Slow Query**
The query is slow because the database has to scan all 5,000,000 rows. 

**Solution:**
We need to add an index on `studentID` and `isRead`. Adding an index to *every* column is a bad idea because it takes up extra storage space and slows down the database every time we insert new data.

**Placement Query:**
```sql
SELECT DISTINCT studentID FROM notifications 
WHERE notificationType = 'Placement' 
AND createdAt >= DATE_SUB(NOW(), INTERVAL 7 DAY);

---

## Stage 5
**Fixing the "Notify All" Loop**
**Shortcomings:**
The loop runs everything synchronously. It waits to send the email, then waits to save to the DB. If the email server is slow, the loop freezes. Saving to the DB and sending the email should **not** happen at the exact same time.

**Redesign:**
We should push tasks into a background queue (like RabbitMQ) and return a success message immediately. Then, background workers can read those tasks and send the emails safely.

**Revised Pseudocode:**
```python
function notify_all(student_ids, message):
    for id in student_ids:
        queue.add_task("send_email", id, message)
        queue.add_task("save_db", id, message)
        queue.add_task("send_push", id, message)
    
    return "Started processing in the background"

function background_email_worker():
    while task = queue.get_task("send_email"):
        try:
            send_email(task.id, task.message)
        except Error:
            queue.retry_later(task)