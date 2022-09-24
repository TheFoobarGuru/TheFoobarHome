CREATE TABLE IF NOT EXISTS minute_stats (
   time TIMESTAMP WITHOUT TIME ZONE NOT NULL PRIMARY KEY,

   from_battery DOUBLE PRECISION NOT NULL,
   from_pv DOUBLE PRECISION NOT NULL,
   from_grid DOUBLE PRECISION NOT NULL,
   from_total DOUBLE PRECISION NOT NULL,

   to_battery DOUBLE PRECISION NOT NULL,
   to_pv DOUBLE PRECISION NOT NULL,
   to_grid DOUBLE PRECISION NOT NULL,
   to_total DOUBLE PRECISION NOT NULL
);

CREATE TABLE IF NOT EXISTS hour_stats (LIKE minute_stats);

CREATE TABLE IF NOT EXISTS day_stats (LIKE minute_stats); 

CREATE TABLE IF NOT EXISTS month_stats (LIKE minute_stats); 

CREATE TABLE IF NOT EXISTS year_stats (LIKE minute_stats); 

CREATE TABLE IF NOT EXISTS total_stats (LIKE minute_stats);