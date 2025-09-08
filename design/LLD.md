log-analytics-platform/design/LLD.md
# Low-Level Design (LLD)

## Database Schema

The ClickHouse table for storing logs:

```sql
-- This table will store our incoming log events.
CREATE TABLE logs (
    -- Core log fields
    timestamp   DateTime64(3, 'UTC'), -- Millisecond precision, UTC timezone
    log_level   LowCardinality(String), -- Optimized for strings with few unique values (INFO, ERROR, etc.)
    service     LowCardinality(String), -- The name of the application that generated the log
    message     String,                 -- The log message itself

    -- Optional structured metadata for better querying
    trace_id    UUID,
    user_id     String
)
ENGINE = MergeTree()
PARTITION BY toYYYYMM(timestamp) -- Partitions data by month for efficient deletion and maintenance
ORDER BY (service, log_level, timestamp); -- The primary key, determines how data is sorted on disk for fast queries
