
CREATE TABLE override_table (
    id INT IDENTITY PRIMARY KEY,          -- Unique identifier for each row
    segment_json NVARCHAR(MAX) NOT NULL,  -- JSON data for active segments
    segment_hash_id VARCHAR(255) UNIQUE,  -- Unique hash ID for grouping
    exit_strategy_new VARCHAR(50),        -- Updated exit strategy (override)
    exit_phase_new VARCHAR(50),           -- Updated exit phase (override)
    exit_period_new INT,                  -- Updated exit period (override)
    last_updated_by VARCHAR(50),          -- User who performed the override
    last_updated_on DATETIME DEFAULT GETDATE() -- Timestamp of the override
);
