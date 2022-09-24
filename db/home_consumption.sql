CREATE TABLE IF NOT EXISTS home_consumption (
   time TIMESTAMP WITHOUT TIME ZONE NOT NULL PRIMARY KEY,

   -- devices:local/HomeBat_P
   from_battery DOUBLE PRECISION NOT NULL,
   -- devices:local/HomePv_P
   from_pv DOUBLE PRECISION NOT NULL,
   -- devices:local/HomeGrid_P
   from_grid DOUBLE PRECISION NOT NULL,
   -- total 
   total DOUBLE PRECISION NOT NULL,

   -- devices:local/Home_P
   home_p DOUBLE PRECISION NOT NULL,
   -- devices:local/HomeOwn_P
   home_own_p DOUBLE PRECISION NOT NULL
);

-- Turn `pv_generator` into a hypertable.
SELECT create_hypertable('home_consumption', 'time');