CREATE TABLE "admingo_ventas" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "cantidad" integer NOT NULL, "precio" decimal NOT NULL, "nombre_cliente" varchar(100) NOT NULL, "telefono_cliente" varchar(100) NOT NULL, "descripcion_venta" text NOT NULL, "fecha_venta" datetime NOT NULL, "id_usuario_id" integer NOT NULL REFERENCES "admingo_usuarios" ("id") DEFERRABLE INITIALLY DEFERRED, "id_producto_id" integer NOT NULL REFERENCES "admingo_productos" ("id") DEFERRABLE INITIALLY DEFERRED,"media_id" varchar(1000) NOT NULL, "varias" integer NOT NULL);

ALTER TABLE "admingo_ventas" ADD "varias" integer NOT NULL;

CREATE INDEX "admingo_ventas_id_usuario_id_646f1470" ON "admingo_ventas" ("id_usuario_id");

CREATE INDEX "admingo_ventas_id_producto_id_646f1470" ON "admingo_ventas" ("id_productos_id");

ALTER TABLE "admingo_ventas" ADD "id_producto_id" integer NOT NULL REFERENCES "admingo_productos" ("id") DEFERRABLE INITIALLY DEFERRED;

CREATE TABLE "admingo_imagenes" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "media_id" varchar(1000) NOT NULL, "imagen" text NOT NULL, "id_usuario_id" integer NOT NULL REFERENCES "admingo_usuarios" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "admingo_ventas_id_usuario_id_646f1471" ON "admingo_ventas" ("id_usuario_id");


CREATE TABLE "admingo_info" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "seguidores" integer NOT NULL, "seguidos" integer NOT NULL, "fotos" integer NOT NULL, "hastags" integer NOT NULL, "fecha_creacion" datetime NOT NULL, "id_usuario_id" integer NOT NULL REFERENCES "admingo_usuarios" ("id") DEFERRABLE INITIALLY DEFERRED);

CREATE INDEX "admingo_info_cuenta_usuario_id_id_0b521d3b" ON "admingo_info" ("id_usuario_id");


ALTER TABLE "admingo_ventas" ADD "img_varias" integer NOT NULL;

ALTER TABLE "admingo_concursos" ADD "condiciones" text NOT NULL;

CREATE TABLE "admingo_concursos" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "ruta_img" varchar(1000) NOT NULL, "seguirnos" integer NOT NULL, "like" integer NOT NULL, "hastags" varchar(1000) NOT NULL, "seguir_otros" varchar(1000) NOT NULL, "cant_etiqueta" integer NOT NULL, "like_amigo_otros" integer NOT NULL, "seguirme_amigos" integer NOT NULL,"condiciones" text NOT NULL, "fecha_creacion" datetime NOT NULL, "id_usuario_id" integer NOT NULL REFERENCES "admingo_usuarios" ("id") DEFERRABLE INITIALLY DEFERRED, "seguir_amigos_otras" integer NOT NULL);
CREATE INDEX "admingo_concursos_id_usuario_id_e6d0b763" ON "admingo_concursos" ("id_usuario_id");

ALTER TABLE "admingo_concursos" ADD "img_url" text NOT NULL;