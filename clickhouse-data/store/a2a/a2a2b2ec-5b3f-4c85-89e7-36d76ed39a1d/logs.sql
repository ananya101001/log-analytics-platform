ATTACH TABLE _ UUID 'ce6da4ec-654f-4bc9-8a56-a0856f86d948'
(
    `timestamp` DateTime64(3, 'UTC'),
    `log_level` LowCardinality(String),
    `service` LowCardinality(String),
    `message` String,
    `trace_id` UUID,
    `user_id` String
)
ENGINE = MergeTree
PARTITION BY toYYYYMM(timestamp)
ORDER BY (service, log_level, timestamp)
SETTINGS index_granularity = 8192
