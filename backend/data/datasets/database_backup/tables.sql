-- Table: public.students

-- DROP TABLE public.students;

CREATE TABLE public.students
(
    idx integer,
    anyo integer,
    institucion character varying COLLATE pg_catalog."default",
    per_id_anyo bigint,
    per_id integer,
    edad integer,
    genero character varying COLLATE pg_catalog."default",
    grado_cod numeric,
    jornada character varying COLLATE pg_catalog."default",
    estrato character varying COLLATE pg_catalog."default",
    pais_origen character varying COLLATE pg_catalog."default",
    discapacidad character varying COLLATE pg_catalog."default",
    srpa character varying COLLATE pg_catalog."default",
    institucion_sector character varying COLLATE pg_catalog."default",
    institucion_modelo character varying COLLATE pg_catalog."default",
    institucion_apoyo_academico_especial character varying COLLATE pg_catalog."default",
    institucion_zona character varying COLLATE pg_catalog."default",
    institucion_caracter character varying COLLATE pg_catalog."default",
    institucion_numero_de_sedes numeric,
    institucion_estado character varying COLLATE pg_catalog."default",
    institucion_latitude character varying COLLATE pg_catalog."default",
    institucion_longitud character varying COLLATE pg_catalog."default",
    institucion_prestador_de_servicio character varying COLLATE pg_catalog."default",
    institucion_tamanyo character varying COLLATE pg_catalog."default",
    institucion_nivel_basica_primaria integer,
    institucion_nivel_secundaria_primaria integer,
    institucion_nivel_media integer,
    institucion_nivel_preescolar integer,
    institucion_nivel_primera_infancia integer,
    institucion_especialidad_academica integer,
    institucion_especialidad_agropecuario integer,
    institucion_especialidad_comercial integer,
    institucion_especialidad_industrial integer,
    institucion_especialidad_no_aplica integer,
    institucion_especialidad_otro integer,
    edad_clasificacion character varying COLLATE pg_catalog."default",
    estado integer
)

TABLESPACE pg_default;

ALTER TABLE public.students
    OWNER to postgres;


-- Table: public.predicted_students

-- DROP TABLE public.predicted_students;

CREATE TABLE public.predicted_students
(
    idx integer,
    anyo integer,
    institucion character varying COLLATE pg_catalog."default",
    per_id_anyo bigint,
    per_id integer,
    edad integer,
    genero character varying COLLATE pg_catalog."default",
    grado_cod numeric,
    jornada character varying COLLATE pg_catalog."default",
    estrato character varying COLLATE pg_catalog."default",
    pais_origen character varying COLLATE pg_catalog."default",
    discapacidad character varying COLLATE pg_catalog."default",
    srpa character varying COLLATE pg_catalog."default",
    institucion_sector character varying COLLATE pg_catalog."default",
    institucion_modelo character varying COLLATE pg_catalog."default",
    institucion_apoyo_academico_especial character varying COLLATE pg_catalog."default",
    institucion_zona character varying COLLATE pg_catalog."default",
    institucion_caracter character varying COLLATE pg_catalog."default",
    institucion_numero_de_sedes numeric,
    institucion_estado character varying COLLATE pg_catalog."default",
    institucion_latitude character varying COLLATE pg_catalog."default",
    institucion_longitud character varying COLLATE pg_catalog."default",
    institucion_prestador_de_servicio character varying COLLATE pg_catalog."default",
    institucion_tamanyo character varying COLLATE pg_catalog."default",
    institucion_nivel_basica_primaria integer,
    institucion_nivel_secundaria_primaria integer,
    institucion_nivel_media integer,
    institucion_nivel_preescolar integer,
    institucion_nivel_primera_infancia integer,
    institucion_especialidad_academica integer,
    institucion_especialidad_agropecuario integer,
    institucion_especialidad_comercial integer,
    institucion_especialidad_industrial integer,
    institucion_especialidad_no_aplica integer,
    institucion_especialidad_otro integer,
    edad_clasificacion character varying COLLATE pg_catalog."default",
    estado integer
)

TABLESPACE pg_default;

ALTER TABLE public.predicted_students
    OWNER to postgres;