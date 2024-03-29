from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "permissions" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "roles" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "users" (
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(200) NOT NULL,
    "phone" VARCHAR(12) NOT NULL,
    "password" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "organizations" (
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "legal_name" TEXT NOT NULL,
    "legal_name_prefix" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "department" (
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" TEXT NOT NULL,
    "organization_id" INT NOT NULL REFERENCES "organizations" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "employee" (
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "id" SERIAL NOT NULL PRIMARY KEY,
    "birth_date" DATE NOT NULL,
    "department_id" INT NOT NULL REFERENCES "department" ("id") ON DELETE CASCADE,
    "organization_id" INT NOT NULL REFERENCES "organizations" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL UNIQUE REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "roles_permissions" (
    "roles_id" INT NOT NULL REFERENCES "roles" ("id") ON DELETE CASCADE,
    "permission_id" INT NOT NULL REFERENCES "permissions" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "users_permissions" (
    "users_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "permission_id" INT NOT NULL REFERENCES "permissions" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "users_roles" (
    "users_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "role_id" INT NOT NULL REFERENCES "roles" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
