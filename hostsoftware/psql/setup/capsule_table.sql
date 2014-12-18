CREATE TABLE capsules
(
  id bigserial PRIMARY KEY NOT NULL,
  event character varying(64) NOT NULL,
  origin character varying(64) NOT NULL,
  destination character varying(64) NOT NULL,
  "time" timestamp without time zone NOT NULL,
  velocity real NOT NULL
);
