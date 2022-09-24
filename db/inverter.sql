CREATE TABLE IF NOT EXISTS inverter (
   time TIMESTAMP WITHOUT TIME ZONE NOT NULL PRIMARY KEY,

   -- devices:local:ac/InvOut_P
   output_power DOUBLE PRECISION NOT NULL,
   -- devices:local:ac/Frequency
   grid_frequency DOUBLE PRECISION NOT NULL,
   -- devices:local:ac/CosPhi
   cos_phi DOUBLE PRECISION NOT NULL,

   -- devices:local:ac/L1_U
   l1_voltage DOUBLE PRECISION NOT NULL,
   -- devices:local:ac/L1_P
   l1_power DOUBLE PRECISION NOT NULL,
   -- devices:local:ac/L1_I
   l1_current DOUBLE PRECISION NOT NULL,

   -- devices:local:ac/L2_U
   l2_voltage DOUBLE PRECISION NOT NULL,
   -- devices:local:ac/L2_P
   l2_power DOUBLE PRECISION NOT NULL,
   -- devices:local:ac/L2_I
   l2_current DOUBLE PRECISION NOT NULL,

   -- devices:local:ac/L3_U
   l3_voltage DOUBLE PRECISION NOT NULL,
   -- devices:local:ac/L3_P
   l3_power DOUBLE PRECISION NOT NULL,
   -- devices:local:ac/L3_I
   l3_current DOUBLE PRECISION NOT NULL
);

-- Turn `pv_generator` into a hypertable.
SELECT create_hypertable('inverter', 'time');