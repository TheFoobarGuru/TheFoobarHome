CREATE TABLE IF NOT EXISTS pv_generator (
   time TIMESTAMP WITHOUT TIME ZONE NOT NULL PRIMARY KEY,

   -- devices:local:pv1/U
   pv1_voltage DOUBLE PRECISION NOT NULL,
   -- devices:local:pv1/P
   pv1_power DOUBLE PRECISION NOT NULL,
   -- devices:local:pv1/I
   pv1_current DOUBLE PRECISION NOT NULL,

   -- devices:local:pv2/U
   pv2_voltage DOUBLE PRECISION NOT NULL,
   -- devices:local:pv2/P   
   pv2_power DOUBLE PRECISION NOT NULL,
   -- devices:local:pv2/I   
   pv2_current DOUBLE PRECISION NOT NULL,

   -- devices:local:pv3/U
   pv3_voltage DOUBLE PRECISION NOT NULL,
   -- devices:local:pv3/P
   pv3_power DOUBLE PRECISION NOT NULL,
   -- devices:local:pv3/I   
   pv3_current DOUBLE PRECISION NOT NULL,

   -- PV generator, all phases.
   pv_voltage DOUBLE PRECISION NOT NULL,
   pv_power DOUBLE PRECISION NOT NULL,
   pv_current DOUBLE PRECISION NOT NULL
);

-- Turn `pv_generator` into a hypertable.
SELECT create_hypertable('pv_generator', 'time');