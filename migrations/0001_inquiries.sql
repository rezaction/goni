-- Cloudflare D1 schema for the dashboard inquiry inbox.
CREATE TABLE IF NOT EXISTS inquiries (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at TEXT    NOT NULL,
  name       TEXT    NOT NULL,
  whatsapp   TEXT    NOT NULL,
  category   TEXT    NOT NULL DEFAULT '',
  volume     TEXT    NOT NULL DEFAULT '',
  message    TEXT    NOT NULL DEFAULT '',
  page       TEXT    NOT NULL DEFAULT '',
  lang       TEXT    NOT NULL DEFAULT 'en',
  referrer   TEXT    NOT NULL DEFAULT '',
  utm        TEXT    NOT NULL DEFAULT '{}',
  status     TEXT    NOT NULL DEFAULT 'new' CHECK (status IN ('new','contacted','quoted','won','lost','spam')),
  note       TEXT    NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_inquiries_created ON inquiries (created_at DESC);
CREATE INDEX IF NOT EXISTS idx_inquiries_status ON inquiries (status);
