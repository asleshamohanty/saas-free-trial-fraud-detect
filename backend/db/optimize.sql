-- -------------------------------------------------------------------
-- Database Optimization Script (optimize.sql)
--
-- This script improves query performance and enforces data integrity
-- for the fraud detection system.
--
-- It focuses on optimizing the most frequent operations used in the
-- risk engine, including:
--   - Counting signups per device (fingerprint_id)
--   - Tracking activity per IP address
--   - Linking events to users efficiently
--
-- Key optimizations:
--   1. Adds indexes on high-frequency query columns to reduce
--      full table scans and improve lookup speed.
--   2. Enforces uniqueness on device fingerprints to maintain
--      consistent identity mapping.
--   3. Improves scalability as event data grows over time.
--
-- This ensures that fraud detection queries remain fast,
-- reliable, and production-ready.
-- -------------------------------------------------------------------

-- 1. Index for fast IP lookups
CREATE INDEX IF NOT EXISTS idx_signup_ip
ON signup_events(ip_address);

-- 2. Index for fingerprint queries
CREATE INDEX IF NOT EXISTS idx_signup_fingerprint
ON signup_events(fingerprint_id);

-- 3. Index for user queries
CREATE INDEX IF NOT EXISTS idx_signup_user
ON signup_events(user_id);

-- 4. Safe unique constraint for fingerprint hash
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint WHERE conname = 'unique_fingerprint_hash'
    ) THEN
        ALTER TABLE fingerprints
        ADD CONSTRAINT unique_fingerprint_hash UNIQUE (hash);
    END IF;
END
$$;

-- 5. Index for email lookup
CREATE INDEX IF NOT EXISTS idx_users_email
ON users(email);